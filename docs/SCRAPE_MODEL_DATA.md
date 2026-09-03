# `scrape_model_data.py` — model-settings CSV exporter

Retrieves the model-settings export **mostly through Anaplan HTTP APIs** (no Dojo
UI navigation), with **two grids exported via the Selenium UI** because the API
can't deliver them reliably. The REST calls need no browser at all; the browser
exists only to hold a session for those two UI exports and for the classic
core-webapp calls behind `--full`.

`tools/scrape_model_data.py` is the single merged exporter. It contains both the
fast API-driven path and the original pure-Selenium model-settings fallback (see
[Pure-UI fallback](#pure-ui-fallback---ui-only) below).

Four modes:

- **default (7 fast files)** → 5 files from Anaplan's REST API v2
  (`/2/0/models/{id}/...`) as JSON over plain `requests`, **plus** `Modules.csv`
  and `General Lists.csv` via the Selenium model-settings UI export.
- **`--full` (all 15 files)** → the 7 default files **plus** the 8 legacy-engine
  grids over the **classic core-webapp API** (not the UI). One browser login.
- **`--rest-only` (5 files, no browser)** → just the Integration-API files.
  Nothing Selenium, nothing Dojo — the fastest formula/structure refresh, and
  the isolated path to test when the REST pull misbehaves.
- **`--ui-only` (13 UI files)** → the original pure-Selenium model-settings
  export path, useful for debugging or as a fallback if the API path changes.

```powershell
# For a model already registered in models.py, omit --out entirely — the
# output folder is derived from that entry's own folder + raw_dir.
python tools/scrape_model_data.py modela              # 7 fast files
python tools/scrape_model_data.py modela --full       # all 15 files
python tools/scrape_model_data.py modela --rest-only  # 5 files, no browser
python tools/scrape_model_data.py modela --ui-only    # pure UI fallback

# --out is for a scratch export only (e.g. a temp dir to diff before
# promoting into the vault) — it is created if missing.
python tools/scrape_model_data.py modela --out "C:/temp/probe"
```

> [!important] Omitting `--out` is the safe default for a registered model.
> The output folder is `customers/<Customer>/raw/models/<Model>/`, derived
> from the registry entry's own `folder` + `raw_dir` fields — never from the
> shortcut's display name. That folder must **already exist**: `resolve_out_dir`
> raises, naming the path, rather than creating it — so a typo'd `raw_dir` in
> `models.py` cannot silently manufacture a plausible-looking empty folder
> instead of writing into the real one.
>
> An explicit `--out` is different: it **is** created with `exist_ok=True` if
> missing, because it's routinely a scratch export destination. Reach for
> `--out` only for that scratch case, or before a model has a registry entry
> at all — not as the everyday invocation.
>
> `--name` sets the **display name** used in console output only. It does not
> affect the output folder at all — a shortcut's display name and its export
> folder legitimately differ (a shortcut named `modela` can export into a
> folder called `ModelA 2.0`).

## Authentication

The REST calls are **head-less** — no browser. They use the documented
Integration-API flow:

```
POST https://auth.anaplan.com/token/authenticate   (Authorization: Basic <b64 user:pass>)
  -> tokenInfo.tokenValue
GET  https://api.anaplan.com/2/0/...               (Authorization: AnaplanAuthToken <token>)
```

Credentials come from `.env` (`ANAPLAN_USERNAME` / `ANAPLAN_PASSWORD`). The token
lasts ~30 minutes, which covers a full export run.

The browser is still required for the **Selenium UI export** (`Modules.csv`,
`General Lists.csv`) and for the **classic core-webapp API** calls behind
`--full`, both of which need a real authenticated session.

> [!important] Use `https://api.anaplan.com`, never the regional app shard.
> The app shard (`eu2a.app.anaplan.com/2/0/...`) redirects `/2/0/` to the global
> `us1a` endpoint, which accepts **only** Integration-API auth and rejects web
> session cookies with `401 {"status":{"code":401,"message":"Not Authenticated."}}`.

### Incident: the 2026-08-13 empty-CSV export

An earlier version authenticated the REST calls by lifting the logged-in
browser's **session cookies** into a `requests.Session` and calling the app
shard. That worked until ~2026-08-07, then started returning 401 on every
endpoint, and the 2026-08-13 refresh wrote five empty CSVs over good exports.

Two independent bugs, both fixed:

1. **Wrong auth model.** Diagnosed live 2026-08-14: cookie auth against `/2/0/`
   is dead from *every* transport — same-origin in-page `fetch`, `requests` +
   lifted cookies, `api.anaplan.com` + cookies, and plain browser navigation all
   returned the identical 401. The Anaplan web client never calls `/2/0/` itself,
   so there was no client header to replay either. Fixed by switching to the
   token flow above. A previous note claiming Basic auth was disabled for the
   Integration API on this tenant (`FAILURE_BAD_CREDENTIAL`, 2026-07-15) is
   **stale** — the token exchange succeeds and every endpoint returns 200.
2. **Silent failure.** `_get()` swallowed any non-200/non-JSON response into
   `{}`, so a 401 was indistinguishable from "this model has no data": every
   builder produced 0 rows, those empty CSVs overwrote good exports, and the run
   still printed `ok`. `_get()` now **raises** with the status and body snippet,
   a failed pull leaves the existing file untouched, and a 0-row pull refuses to
   overwrite a non-empty file. `--rest-only` also exits non-zero unless all 5
   files are produced.

Regression tests for the failure handling run offline — no tenant, no browser:

```bash
pytest tools/test_scrape_model_data.py
```

## How the three paths work

**REST API v2 (5 files).** Standard `GET /2/0/models/{id}/{lineItems|versions|
actions|imports|views}` against `https://api.anaplan.com`, token-authenticated
over plain `requests` (see [Authentication](#authentication)). `Line Items.csv`
is the rich one (formula, format,
applies-to, summary, time scale/range, versions, style, cell count, is-summary,
formula scope, use switchover, breakback, start of section, referenced-by,
module name). A few columns the REST API doesn't expose are left blank
(Populated Cell Count, Memory Used, Calculation Complexity/Effort, Read/Write
Access Driver, Users List, Parent, Code, Data Tags).

**Selenium UI export (Modules.csv + General Lists.csv — default and `--full`).** These two
blueprint grids are exported by navigating the classic model-settings shell and
running the grid's own Export (via the local `_export_one_target` helper),
because neither API path delivers them correctly:

- **REST is too sparse.** `GET /modules` returns id+name only, so every module
  stat/metadata column (Functional Area, Applies To, Time Scale, Cell Count,
  Referenced By, Used in Dashboards, …) came out blank. `GET /lists` lacks Top
  Level, Parent Hierarchy, and the dependency-graph columns (Referenced in
  Applies To / as Format / in Formula), which only the classic engine computes.
- **The classic core-webapp API can't drive them reliably.** Unlike the 8 legacy
  grids, there is no dependable `viewDefinition` template for Modules/General
  Lists: the classic client references already-open grids **by view index**
  (so its jsonrpc traffic carries no reusable definition), and the UI export is
  a **form-submit download** that isn't interceptable via `fetch`/XHR (0 servlet
  requests captured). A *guessed* template is dangerous — a wrong `viewDefinition`
  silently exports the **wrong grid**. For these core files, "silently wrong" is
  unacceptable.

The Selenium export is **byte-for-byte identical** to Anaplan's own export
(SHA-256-verified against a reference export). It runs with a 3-attempt retry that
re-opens the shell each try.

**Classic core-webapp API (8 legacy files, `--full`).** The legacy blueprint
grids (Line Item Subsets, Time Ranges, Source Models, Roles + Roles Modules/
Versions/Lists/Actions) live in the classic core engine and have no REST
endpoint — but the engine's own HTTP protocol is driven directly, no UI clicking:

1. `POST .../anaplan/jsonrpc` `{requestType:"VIEW_REQUEST_SET", viewRequests:[{viewIndex:-1, viewGuid:<new>, viewDefinition:<grid template>}], activeViewIndices:[], modelDefinitionSerialNumber, clientSessionId}` → returns the opened view's `viewIndex`.
2. `POST .../anaplan/jsonrpc` `{requestType:"PROGRESS", activeViewIndices:[viewIndex]}` → returns a `taskId`.
3. `POST .../anaplan/servlet?taskType=export` (multipart: `taskId`, `entityId`=grid name, `viewDefinition`, `fileType=CSV`) → streams the grid CSV.

A **minimal** `VIEW_REQUEST_SET` (empty carried view-state, single new view) is
sufficient — proven live against all 8 grids, byte-for-byte equal to the
reference exports. `entityId` (= the grid name, i.e. the filename minus `.csv`)
is the primary driver; the `viewDefinition` is a **model-independent template**
(system identifiers `_SYSTEM_AXIS_IDENTIFIER.*` / `_2000000xxx_` / `_4000xxxxx_`
only) baked into `_LEGACY_TEMPLATES`. Only `modelDefinitionSerialNumber` and
`clientSessionId` are per-session, and they're scraped from the client's own
first jsonrpc call at run time. Any legacy grid that fails the classic-API path
falls back to this script's UI export path for that one grid, so
coverage never regresses.

## Output

All CSVs reuse the **exact blueprint column layout** (first header cell blank,
first data column = entity name), so `wiki-data-ingestion` parses them
identically to the pure-Selenium exports. `Modules.csv`, `General Lists.csv`, and
the 8 legacy files are byte-for-byte the same grids the UI produces. `Line
Items.csv` omits the module-separator pseudo-rows the UI export interleaves (~1
fewer row per module) but is otherwise cleaner — every line item still carries
its `Module Name`.

> **Note:** the tool overwrites each output CSV in place. If an output file is
> open in Excel, Windows locks it and that one file fails with
> `[Errno 13] Permission denied` (the others still succeed). Close the file(s)
> and re-run.

## Finding a model that isn't registered yet

The script will not scrape a raw model_id GUID directly — it needs a
`models.py` shortcut with `customer_id`/`workspace_id`/`model_id`. If you don't
have those for a model yet, fetch the live list instead of hunting through the
Anaplan UI:

```powershell
python tools/scrape_model_data.py --list-models --shard eu3
```

`--shard` is required here: every other mode reads its shard from the model's
own `models.py` registry entry, but `--list-models` runs *before* that entry
exists — there is nothing to read a shard from, so it must be told explicitly
which shard to log into (e.g. `eu2a`, `eu3`, `eu4`, `eu9`). Omitting it exits
non-zero rather than guessing a default shard.

Logs in, calls the same `springboard-platform-gateway-service/models` API the
interactive `scraper_ux.py` wizard uses for "Browse all models…", and prints
every model visible to this account as JSON (`model_name`, `model_id`,
`workspace_name`, `workspace_id`, `customer_id`) — no `models.py` shortcut
required. Confirm the right entry with the user, then add it to `.env`/
`models.py` (mirror the example entry in `tools/models.py.example`) before
scraping. `tools/models.py` itself is gitignored — like `.env`, it holds your
real shortcuts locally and never reaches git; `tools/models.py.example` is
the tracked template to copy from on a fresh clone.

## When to use which mode

- **Quick formula/structure refresh** → `--rest-only` (5 files, no browser,
  seconds) if you don't need module/list stats; otherwise default mode (7 files).
- **Complete model export** → `--full` (all 15, one login). Recommended default
  for onboarding/refresh.
- **Pure UI export / debugging a single grid in isolation** →
  `python tools/scrape_model_data.py <shortcut> --ui-only` (see below). Still
  useful as the fallback path `--full` invokes automatically.

Prerequisites: `.env` filled in, a `models.py` shortcut, Edge installed, and
`pip install requests selenium openpyxl webdriver-manager python-dotenv`.

---

## Pure-UI fallback: `--ui-only`

`python tools/scrape_model_data.py <shortcut> --ui-only` runs the original,
fully UI-driven exporter from the merged script. It automates the manual
"export the 13 blueprint CSVs from the Anaplan UI" step by navigating the
model-settings Dojo app grid-by-grid. Use it to debug one grid in isolation, or
as a full pure-UI fallback if the API-driven approach ever breaks against a
future Anaplan release.

### What it produces

All 13 files land in the output folder, matching the naming used under
`customers/<Customer>/raw/models/<Model>/`:

```
Modules.csv          Line Items.csv       Line Item Subsets.csv
General Lists.csv     Versions.csv         Time Ranges.csv
Actions.csv          Source Models.csv    Roles.csv
Roles Modules.csv    Roles Versions.csv   Roles Lists.csv
Roles Actions.csv
```

> **Not every model's raw folder will have this exact set.** A model's
> `customers/<Customer>/raw/models/<Model>/` folder may have fewer than these 13 files (e.g. it
> predates the scraper, or the export includes files the scraper doesn't
> produce at all, like `Imports.csv`/`Import Data Sources.csv`). Re-running
> the scraper only ever touches these 13 filenames — anything else already in
> the folder is left alone, and any of the 13 that fail to export leave the
> prior file for that name untouched rather than deleting it.

### Usage

```powershell
# Registered model: omit --out, the folder is derived from the registry entry
python tools/scrape_model_data.py modela --ui-only

# Export into a scratch dir (e.g. to diff before promoting into the vault)
python tools/scrape_model_data.py modela --out "C:/temp/probe" --ui-only
```

As a library:

```python
from scrape_model_data import download_model_exports
results = download_model_exports("modela")   # default: registry-derived out_dir
# results: {filename: {"ok": bool, "saved_path": str|None, "error": str|None}}
```

`model` is a `models.MODELS` shortcut key (e.g. `modela`). It opens a real
(non-headless) Edge window and logs in automatically via basic auth; no manual
step is needed unless SSO is enabled. It prints a per-grid ✅/✗ summary and an
`N/13 exported` line, and exits 0 only when all 13 succeed.

### Adding a new model

1. Add `<PREFIX>_MODEL_ID=<guid>` to `.env`. A workspace variable and a
   `customer_id` can be reused **only** by models in the same customer's
   tenant and workspace — a second customer has its own tenant GUID, its own
   workspaces, and possibly its own Anaplan shard, so nothing here is global.
2. Mirror the example entry in `models.py` with `folder`, `raw_dir`, `shard`,
   `customer_id`, `workspace_id`, `model_id`, then call
   `python tools/scrape_model_data.py <prefix> --ui-only` — the output folder
   is derived from the entry's `folder` + `raw_dir`, so no `--out` is needed
   once the entry exists (and that folder must already exist in the vault; see
   the callout above).

(Raw model-id GUIDs are rejected on purpose — a bare id has no reliable way to infer
its workspace, so register a shortcut instead.)

### How it works (for future maintainers)

The model-settings UI is a legacy **Dojo** app inside **nested iframes**: an outer
shell iframe (`data-testid="shell-content"`) holds the left-nav; its first nested
iframe holds the grid, sub-tabs, toolbar and export dialog. Per grid the script:
navigates the left-nav (shell frame) → switches into the inner grid frame → clicks
the sub-tab if any → clicks the toolbar `Export...` (`<span class="dijitButtonText">`,
not a `<button>`) → presses **Run Export** in the dialog (File Type defaults to CSV) →
saves the download under the target filename.

Two non-obvious gotchas it handles:
- The modeling URL **must not** contain a double slash (`.../` + `/a/...`), or Anaplan
  serves a "We can't find this page" 404 — the script `rstrip("/")`s the base URL.
- Dojo keeps **hidden duplicate widgets** in the DOM, so every click is filtered to
  `is_displayed()`; sub-tabs are matched on alphanumeric-only text because the
  "Roles → Modules" arrow is a CSS icon (real text is `RolesModules`).
