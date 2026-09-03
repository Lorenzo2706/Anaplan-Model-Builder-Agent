# Anaplan Model Builder Agent

A **Claude Code-powered knowledge vault** for Anaplan model builders. Drop in Anapedia docs, articles, and model CSV exports; Claude ingests them into a structured, interlinked Obsidian-style wiki that becomes durable context for future model-building work (formulas, debugging, design reviews, deltas across re-uploads).

The wiki is the agent's **external memory** — not the product. The point is that every subsequent question Claude answers ("write me a formula for X", "what changed in this re-upload", "is this Polaris-safe?") is grounded in your actual model context, accumulated over time.

---

## What you get

- **Claude Code as an Anaplan model-builder agent** with a project-specific system prompt (`CLAUDE.md`) that defines a multi-customer vault schema, the **Client Resolution** procedure for routing every model-touching request to the right domain, ingest/query/lint workflows, and Anaplan-aware conventions (DISCO, PLANS, engine-aware reasoning).
- **A vault layout split into three domains**: `anaplan/` (generic, customer-agnostic Anaplan tool knowledge — tracked in git, ships in the public template), `customers/<Name>/` (per-customer content — CSV exports, customer-specific docs, model wikis, analyses — gitignored, local only), and `other-topics/` (unrelated, non-Anaplan content — gitignored). A `customers/registry.md` file (gitignored) maps model names to their customer and engine (Classic/Polaris), so any question that names a model resolves to the right folder automatically.
- **Eight skills** that auto-activate from context, all shipped as project skills in `.claude/skills/`: `project-setup` (bootstraps a freshly cloned vault into a working vault, and onboards additional customers into an already-set-up vault — the same idempotent flow, auto-detected by current state), `anaplan-formula-agent` (formula writing/debugging, Step-0 context-loading + Classic-vs-Polaris reasoning), `anaplan-module-mapping` (cross-module wiring — delivers dual financial-logic + Anaplan-mechanics explanations for every formula), `anaplan-model-optimizer` (runs the NUX/UX scraper for a model and cross-references usage against the raw CSV export to flag genuinely dead modules, never the ones invisible-by-design), `anaplan-model-documentation` (fans out parallel research agents to assemble a full Word documentation deliverable for a model), `circular-reference-prevention` (audits a model for circular-reference/DISCO-break risk and modules mislabeled as Calculation that actually behave as Output, with independent verification of every candidate), `wiki-lint` (generic wiki sanity-check — orphans, broken links, stale stats, contradictions, auto-fix pass, now walking all domain trees), and `wiki-data-ingestion` (structured ingest of docs and model CSVs — Client Resolution, path acquisition, grouping, delta detection, index/log updates, post-ingest summary; can drive the optional `scrape_model_data.py` exporter directly for model CSV refreshes, with manual drops as a fallback).
- **Obsidian compatibility** — open the vault in Obsidian to browse `[[wiki links]]` visually while Claude maintains it.

---

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed (CLI or IDE extension).
- A local folder you'll use as the vault root (this becomes Claude Code's working directory).
- [Obsidian](https://obsidian.md/) pointed at the same folder for browsing the wiki.

No databases, no servers, no API keys beyond what Claude Code itself needs. Everything is flat markdown + CSVs on disk.

---

## Setup

### Quick start (recommended)

1. Clone the repo and start Claude Code inside it:
   ```powershell
   git clone <repo-url> <vault-root>
   cd <vault-root>
   claude
   ```
2. Tell Claude: **"Run project setup."** The `project-setup` skill (ships in `.claude/skills/`, so it's available immediately) takes it from there. It detects current state and auto-selects the right mode:
   - **On a fresh clone** (no `customers/registry.md` yet), it builds the empty shared `anaplan/` subfolders that aren't already present (`anaplan/` itself ships tracked and pre-populated with the generic knowledge base — this step just fills any gaps), then asks how many customers you want the vault set up for and, for each one, builds the `customers/<Name>/raw/`, `wiki/`, `logs/`, `analyses/` skeleton, an `index.md` + `log.md`, and adds a row per model + engine (Classic/Polaris) you already know to `customers/registry.md` (creating the file if needed),
   - **On an already-set-up vault**, it skips straight to onboarding exactly the one new customer you asked for (no "how many" question — that's only asked on first run) and never touches an existing `customers/<Name>/` tree,
   - it reports which of the eight project skills are present under `.claude/skills/` (all eight ship with the repo, so normally all are).

That's it. Claude will create wiki pages, indexes, and logs under the right domain as you start ingesting content. The skill is idempotent — re-running "run project setup" later (e.g. to onboard another customer, or because something didn't finish) is always a safe no-op or additive extension; it never overwrites an existing `customers/<Name>/` tree.

### Manual setup

Prefer to do it by hand, or want to see exactly what the skill automates? Here's the same process step by step.

#### 1. Create the vault

```
<vault-root>/
├── CLAUDE.md                       # project system prompt — generic and customer-agnostic, ships already tracked
├── README.md                       # this file
├── index.md                        # root router (Claude maintains) — thin pointer to each domain's own index
├── log.md                          # root router (Claude maintains)
├── anaplan/                        # generic Anaplan knowledge — tracked in git, ships in the public template
│   ├── raw/
│   │   ├── docs/                   # Anapedia clippings, generic best-practice articles, release notes
│   │   └── assets/                 # images referenced from anaplan/ sources
│   ├── wiki/
│   │   ├── concepts/               # Anaplan concepts (line items, dimensions, …)
│   │   ├── functions/              # categorized function index + category pages
│   │   ├── patterns/               # DISCO, PLANS, Planual, Anaplan Way, naming, …
│   │   └── sources/                # one summary page per ingested generic source
│   ├── index.md                    # domain index (Claude maintains)
│   └── log.md                      # domain log (Claude maintains)
├── customers/                      # gitignored — per-customer content, never leaves this machine
│   ├── registry.md                 # Customer | Model | Folder | Engine | Notes
│   └── <Customer Name>/
│       ├── raw/
│       │   ├── models/<Model Name>/   # CSV exports per model
│       │   ├── docs/                   # standards docs, meeting notes, model-build narratives
│       │   └── assets/
│       ├── wiki/
│       │   ├── models/<Model Name>/    # per-model dossiers (mirrors raw/models/)
│       │   └── sources/                 # one summary page per ingested customer-specific source
│       ├── logs/<Model Name>/           # error/diagnostic logs — a peer of raw/, not nested in it
│       ├── analyses/                    # HTML/docx deliverables for this customer's models
│       ├── index.md
│       └── log.md
├── other-topics/                   # gitignored — unrelated, non-Anaplan content
│   └── <topic>/
├── Clippings/                      # Obsidian Web Clipper landing folder for new raw docs
└── .claude/
    ├── settings.local.json
    └── skills/
        ├── project-setup/
        │   └── SKILL.md
        ├── anaplan-formula-agent/
        │   └── SKILL.md
        │       └── references/
        │           └── classic-vs-polaris.md
        │           └── polaris-function-compatibility.md    
        ├── anaplan-module-mapping/
        │   └── SKILL.md
        ├── anaplan-model-optimizer/
        │   ├── SKILL.md
        │   └── scripts/
        │       └── analyze_module_usage.py
        ├── anaplan-model-documentation/
        │   └── SKILL.md
        ├── circular-reference-prevention/
        │   └── SKILL.md
        ├── wiki-lint/
        │   └── SKILL.md
        └── wiki-data-ingestion/
            └── SKILL.md
```

Optional: a `tools/` folder holding `scraper_ux.py`, `scrape_model_data.py`, and `models.py`, plus `docs/SCRAPE_MODEL_DATA.md`, a gitignored `.env`, and a `UI/` output folder — the toolchain `anaplan-model-optimizer` drives to pull live NUX usage data, and `wiki-data-ingestion` drives to refresh a model's blueprint CSVs. `models.py` is gitignored like `.env` — copy it from `models.py.example`. See [Scraper toolchain](#scraper-toolchain-optional) below.

`CLAUDE.md`, all eight `.claude/skills/` folders, `tools/scraper_ux.py`/`tools/models.py.example`/`tools/scrape_model_data.py`/`docs/SCRAPE_MODEL_DATA.md`, and `anaplan/` (fully populated with the generic knowledge base) ship with the repo. `customers/` and `other-topics/` don't exist yet on a fresh clone — they're gitignored and built up per customer, either by `project-setup` or by hand:

```powershell
New-Item -ItemType Directory -Force -Path "customers/<Name>/raw/models", "customers/<Name>/raw/docs", `
  "customers/<Name>/raw/assets", "customers/<Name>/wiki/models", "customers/<Name>/wiki/sources", `
  "customers/<Name>/logs", "customers/<Name>/analyses", other-topics, Clippings | Out-Null
```

Claude will create the wiki pages, each domain's `index.md`/`log.md`, and `customers/registry.md` as you ingest content and onboard customers — don't pre-create those.

#### 2. Install the project skills

Copy all eight `.claude/skills/` subfolders into your vault:

**`project-setup`** — auto-activates on "run first-time setup", "set up this vault", "bootstrap this repo", "onboard this repo", "add a customer", "add a new client", "I'm starting work for `<name>`", or whenever `customers/registry.md` doesn't exist yet. Detects whether this is a fresh clone or an already-set-up vault and either builds the shared `anaplan/` skeleton, onboards one or more customers into `customers/<Name>/` + `customers/registry.md`, or both — always checking current state first so re-running is a safe no-op.

**`anaplan-formula-agent`** — auto-activates when you ask Claude to write, fix, refactor, or explain a formula; mention a module/line item/list by name; ask about Classic vs Polaris differences; or have model CSVs ingested. Includes a Step-0 context-loading protocol, Planual checklist, and `references/classic-vs-polaris.md`.

**`anaplan-module-mapping`** — auto-activates whenever you wire one module into another: cross-module formulas (`SUM:`, `LOOKUP:`, `SELECT:`, dot-notation), data-flow questions, or "why is this formula written this way?" questions. Always delivers two separate explanations per formula — financial/functional logic first, then Anaplan mechanics — plus a dimension-alignment checklist and sign-convention reference.

**`anaplan-model-optimizer`** — auto-activates on "optimize this model", "which modules can I delete", "unused/orphaned/dead modules", or any mention of the NUX/UX scraper. Runs `scraper_ux.py` for the chosen model, then cross-references the resulting Excel against `customers/<Customer>/raw/models/<Model>/Modules.csv` and `Imports.csv` (customer resolved via Client Resolution) via the bundled `scripts/analyze_module_usage.py`, so it never flags Data/Load/Calculation modules that are intentionally invisible in the UX but still feed other modules by formula. Recommendation only — never deletes anything itself; saves the full report under that customer's `analyses/`. Needs the optional [scraper toolchain](#scraper-toolchain-optional) set up first.

**`anaplan-model-documentation`** — auto-activates on "document this model", "draft documentation for X", "write up the model", or a request to redraft an existing model doc to match a reference style. Dispatches six parallel background research agents against the model's wiki + raw CSVs (one per outline domain: Introduction, Data Flows, Technical Set-up, Appendices), then assembles a validated `.docx` with `[PLACEHOLDER: ...]` markers for anything the sources don't confirm. Saves to `customers/<Customer>/analyses/<Model>-Model-Documentation.docx`.

**`circular-reference-prevention`** — auto-activates on "circular reference", "DISCO break", "engine failure risk", "loop risk", "mislabeled module", or a whole-model integrity pass over `Line Items.csv`/`Modules.csv`. Distinguishes same-period edges (real risk) from `PREVIOUS()`/`OFFSET()`/`NEXT()`-shifted edges (safe, sequential), and a module's behavioral Output role (nothing reads it back for calculation) from its raw DISCO tag. Every candidate cycle or mislabel gets independently verified by a separate agent rather than self-reviewed, with `Workflow`-based orchestration once the model is bigger than a handful of modules. Saves to `customers/<Customer>/analyses/<Model>-circular-reference-audit-<date>.html`.

**`wiki-lint`** — auto-activates on "lint the wiki", "health check", "check for orphan pages", "wiki cleanup", and similar phrasing. Walks all domain trees (`anaplan/`, each `customers/<Name>/`, `other-topics/`) and runs five standard checks: orphan pages, broken internal links, stale counts/stats, contradictions across pages, undocumented companion files. Fixes what's safe automatically (registers orphans in indexes, corrects stale counts, notes undocumented files) and flags anything requiring judgment. Appends a dated entry to each touched domain's `log.md`. Generic — works on any markdown wiki, not specific to Anaplan.

**`wiki-data-ingestion`** — auto-activates whenever you say "ingest", "process this CSV", "refresh the `<Model>` data", "I dropped something in raw/", or any variant. Performs Client Resolution first — determining which domain (`anaplan/`, a specific `customers/<Name>/`, or `other-topics/`) the source belongs to — then handles the full ingest pipeline: for general docs, asks for file paths if not provided (or auto-discovers by diffing each domain's `raw/` against its own `wiki/sources/`); for model data, asks which model (or resolves it via `customers/registry.md` if already known) and can drive the optional `scrape_model_data.py` exporter directly, with manually-dropped CSVs as a fallback. Groups multiple files into batches by topic, classifies each batch, auto-detects first-time vs incremental delta for CSVs, applies only deltas on re-uploads (preserving your annotations, always overwriting the raw CSV in place — no dated archive copies), updates the resolved domain's indexes and `log.md`, and ends with a structured post-ingest summary in chat.

#### 3. Start Claude Code in the vault root

```powershell
cd <vault-root>
claude
```

Claude will read `CLAUDE.md` automatically.

---

## Daily workflow

### Ingest a new source

Drop a file into the right domain's `raw/docs/` — `anaplan/raw/docs/` for generic Anapedia/best-practice content, `customers/<Customer>/raw/docs/` for anything customer-specific — then tell Claude:

> "Ingest `<new-clipping>.md`."

The `wiki-data-ingestion` skill activates automatically and resolves the domain (Client Resolution) before anything else. If you don't provide a path, it will ask; if you'd rather not specify one, it discovers new files by comparing each domain's `raw/` against its own `wiki/sources/`. It then creates a `wiki/sources/YYYY-MM-DD-<slug>.md` summary page under the resolved domain, touches every relevant concept/function/pattern page, updates that domain's `index.md`, and appends to its `log.md`. A structured summary is printed in chat when done.

### Refresh or ingest a model's CSVs

> "Refresh the `<Model>` data." (or "pull the latest `<Model>` export", "ingest the new `<Model>` CSVs")

The model name resolves to its customer via `customers/registry.md` (Client Resolution) before anything else. The `wiki-data-ingestion` skill is scraper-driven by default: if the optional `tools/scrape_model_data.py` toolchain is set up, it asks which model, resolves (or helps you register) a `models.py` shortcut, snapshots the current `customers/<Customer>/raw/models/<Model>/` files for diffing, then runs the scraper to pull the model's blueprint CSVs straight from Anaplan into `customers/<Customer>/raw/models/<Model>/` (7 files by default, 15 with `--full`). Prefer dropping CSVs manually into that same folder instead? That still works — just say "ingest the new `<Model>` CSVs."

Either way, the skill detects automatically whether this is a first-time ingest or a re-upload by checking that customer's `wiki/sources/` and `wiki/models/`. On a re-upload it diffs against the prior state (an ephemeral pre-scrape snapshot for scraper refreshes, or the existing wiki pages as a proxy for manual drops), applies only added/removed/renamed/modified items, preserves your annotations, and writes a new dated delta source page. **Raw CSVs are always overwritten in place** — this vault keeps no dated archive copies, whether the refresh came from the scraper or a manual re-upload.

### Ask model-building questions

> "Write a formula on `<Module Name>.<Line Item>` that …"
> "Why is `<Module Name>.<Line Item>` returning blank?"
> "What changed in `<Model Name>` between this upload and the last?"

Claude resolves the domain first (Client Resolution — a named model resolves to its customer via `customers/registry.md`; generic questions resolve to `anaplan/`), reads that domain's `index.md`, descends into sub-indexes, follows `[[wiki links]]`, and answers with citations to wiki pages and raw sources.

### Health-check the vault

> "Run a vault health check" (or "lint the vault" / "wiki sanity check")

Triggers the **`wiki-lint`** skill, which walks all domain trees (`anaplan/`, each `customers/<Name>/`, `other-topics/`) and scans for orphan pages, broken `[[wiki links]]`, stale counts in index files, contradictions across pages, and undocumented companion files. It auto-fixes safe issues and reports anything requiring manual attention.

### Find dead modules in a live model

> "Which modules in `<Model>` are safe to delete?" (or "optimize this model" / "model housekeeping")

Triggers the **`anaplan-model-optimizer`** skill. It runs `tools/scraper_ux.py` against the live tenant to pull fresh NUX usage data for the model, then cross-references it against that model's customer folder — `customers/<Customer>/raw/models/<Model>/Modules.csv` and `Imports.csv` (resolved via Client Resolution) — so Data/Load/Calculation modules that are invisible-by-design in the UX aren't flagged as dead. Reports candidates in chat and saves the full report under that customer's `analyses/`. Requires the [scraper toolchain](#scraper-toolchain-optional).

### Generate a Word doc for a model

> "Document the `<Model>` model" (or "write up onboarding material for X")

Triggers the **`anaplan-model-documentation`** skill. Fans out six background research agents over the model's wiki pages and raw CSVs, then assembles a styled `.docx` under `customers/<Customer>/analyses/<Model>-Model-Documentation.docx` with explicit placeholders for anything unconfirmed.

### Audit a model for circular-reference risk

> "Check `<Model>` for circular reference risk" (or "any DISCO breaks?" / "which modules are mislabeled as Calculation?")

Triggers the **`circular-reference-prevention`** skill. Distinguishes genuine same-period feedback loops from safe `PREVIOUS()`/`OFFSET()`/`NEXT()`-shifted edges, and flags modules tagged Calculation that behave as Output because nothing reads them back for calculation. Every candidate is independently verified by a separate agent before being reported. Saves the HTML deliverable under `customers/<Customer>/analyses/<Model>-circular-reference-audit-<date>.html`.

---

## Customizing for your team

- **Different engine per model?** Edit that model's row in `customers/registry.md` — engines are resolved per-model via the registry (Client Resolution), never hardcoded in `CLAUDE.md`.
- **Different naming convention?** Ingest your own naming doc into `anaplan/raw/docs/` (or `customers/<Name>/raw/docs/` if it's customer-specific) and Claude will create an `anaplan/wiki/patterns/naming-convention-<yourteam>.md` page from it.
- **More models?** Create `customers/<Name>/raw/models/<NewModel>/` and `customers/<Name>/wiki/models/<NewModel>/`, then add a row to `customers/registry.md` (`Customer | Model | Folder | Engine | Notes`). The per-model-subfolder convention means filenames can repeat across models — the directory name disambiguates.
- **More customers?** Tell Claude "add a new client" or "onboard `<Customer>`" — the `project-setup` skill builds the `customers/<Name>/` skeleton and registry rows without touching any existing customer.
- **More skills?** Add `.claude/skills/<skill-name>/SKILL.md`. Frontmatter `description:` controls when it auto-activates.
- **More models for the scraper?** Add a `<PREFIX>_MODEL_ID` to `.env` and mirror the example entry in `tools/models.py`, filling in its own `folder`, `raw_dir`, `shard`, `customer_id`, `workspace_id`, and `model_id` — a `customer_id`/workspace ID can be reused only by other models in that same tenant's workspace, never assumed across customers.

---

## Scraper toolchain (optional)

Two independent tools share this toolchain: **`anaplan-model-optimizer`**'s dead-module analysis (needs live NUX usage data that never appears in a CSV export) and **`wiki-data-ingestion`**'s scraper-driven model refresh (needs a live pull of the blueprint CSVs). Both are optional — manual CSV drops and skipping the optimizer skill both still work without this section set up.

- **`tools/scraper_ux.py`** — interactive wizard that logs into Anaplan via Selenium/Edge, lets you pick a model, and exports a 5-sheet Excel report (`All Views`, `Actions Usage Report`, `Views Usage Report`, `Modules Usage Count`, `Actions <model>`). Every default (username, environment, SSO, output folder) is sourced from `.env` — no hardcoded credentials. Drives `anaplan-model-optimizer`.
- **`tools/scrape_model_data.py`** — the merged model-settings exporter (reuses `scraper_ux.py`'s login as a black box, pulls most files over Anaplan's HTTP APIs, and keeps the Selenium UI path in the same script). Default mode gets 7 files (5 REST + `Modules.csv`/`General Lists.csv` via a Selenium UI export the API can't deliver usably); `--full` adds the 8 legacy-engine grids for 15 total; `--ui-only` runs the original 13-grid pure-Selenium fallback. Each `models.py` entry carries its own `folder`/`raw_dir`/`shard`, so the output folder is derived automatically — run `python tools/scrape_model_data.py <shortcut>` and omit `--out` (it's for scratch exports only; `--name` only relabels console output, it never selects a folder). When no `models.py` shortcut exists yet, `python tools/scrape_model_data.py --list-models --shard <shard>` fetches every model visible to the account via the live API (`--shard` is required there — there's no registry entry yet to read one from). Drives `wiki-data-ingestion`'s model-refresh path.
- **`tools/models.py`** (gitignored, like `.env`) — a `MODELS` dict of quick-select shortcuts so the wizard's "pick from a live list" step can be scripted instead of browsed. An entry only counts as usable once its `folder`, `raw_dir`, `shard`, `customer_id`, `workspace_id`, and `model_id` are all present — each model declares these itself, none of them are shared globally. Copy `tools/models.py.example` (tracked, ships empty with one commented-out example entry) to `tools/models.py` and fill in your own shortcuts — they never reach git.
- **`.env`** (gitignored, create it yourself) — `ANAPLAN_USERNAME`, `ANAPLAN_PASSWORD`, `ANAPLAN_ENVIRONMENT`, `ANAPLAN_USE_SSO`, `ANAPLAN_OUTPUT_FOLDER`, and per-model `<PREFIX>_MODEL_ID` entries. A workspace ID and `customer_id` are shared only among models in the same customer's tenant and workspace — a second customer has its own tenant GUID, its own workspaces, and possibly its own shard, all declared per-entry in `models.py`, not here.
- **`UI/`** (gitignored) — default output folder for scraped Excel reports and per-run logs. May contain real model data — never commit it.

See `docs/SCRAPE_MODEL_DATA.md` for the full field list, partial-export handling, and implementation notes on both exporters.

Install and run:

```powershell
pip install selenium openpyxl webdriver-manager python-dotenv
python tools/scraper_ux.py
```

It opens a real (non-headless) Edge window — the driver is auto-downloaded via Selenium Manager. Every wizard prompt defaults from `.env`; only the model-selection number and the final "scrape another model?" question need real input.

The scraper itself has no automated test suite — verification is by actually running it against a live tenant and inspecting the resulting Excel. `analyze_module_usage.py`'s manual-marker detection does have unit tests:

```bash
pytest .claude/skills/anaplan-model-optimizer/scripts/test_analyze_module_usage.py
```

---

## Tips

- **Confirm angle before big ingests.** A two-line "I'll emphasize X, Y, Z — OK?" exchange beats redoing 20 wiki pages.
- **Never edit `raw/`.** It's the source of truth and the diff baseline for every domain — edit `wiki/` instead.
- **File non-wiki outputs under `customers/<Customer>/analyses/<Model>/`.** Anything that isn't a wiki page (HTML audits, Word docs, other one-off deliverables) goes into that customer's model-specific subfolder — create one if it doesn't exist yet. `anaplan/` and `other-topics/` don't accumulate per-model analyses this way; a non-Anaplan output goes to `other-topics/analyses/` instead.
- **Keep page scope tight** — one concept, one function, one module per page. Split at ~400 lines.
- **Update domain sub-indexes, not the root.** The root `index.md` is a thin router and only changes when a new customer or top-level domain appears.
- **Use the log.** Each domain's `log.md` is the chronological audit trail; Claude appends to it on every ingest. `grep '^## \[' <domain>/log.md` for a quick history.

---

## Repo layout in this reference vault

What's checked in here as a working example:

- `CLAUDE.md` — the generic, customer-agnostic system prompt (ships already tracked — no `.example` copy step needed)
- `.claude/skills/project-setup/` — bootstrap + customer-onboarding skill: builds the shared `anaplan/` skeleton on a fresh clone, and onboards additional customers into `customers/<Name>/` + `customers/registry.md` on this and every later run (project skill)
- `.claude/skills/anaplan-formula-agent/` — formula-writing skill (project skill)
- `.claude/skills/anaplan-module-mapping/` — cross-module wiring skill (project skill)
- `.claude/skills/anaplan-model-optimizer/` — dead-module analysis skill, cross-references a scraped NUX report against `Modules.csv`/`Imports.csv` (project skill)
- `.claude/skills/anaplan-model-documentation/` — generates a full Word documentation deliverable for a model via parallel research agents (project skill)
- `.claude/skills/circular-reference-prevention/` — audits a model for circular-reference/DISCO-break risk and mislabeled Calculation modules, with independent per-finding verification (project skill)
- `.claude/skills/wiki-lint/` — generic wiki sanity-check skill, walks all domain trees (project skill)
- `.claude/skills/wiki-data-ingestion/` — structured ingest pipeline for docs and model CSVs, Client-Resolution-aware (project skill)
- `tools/scraper_ux.py`, `tools/scrape_model_data.py`, `tools/models.py.example`, `docs/SCRAPE_MODEL_DATA.md` — optional scraper toolchain: NUX usage-data export (drives `anaplan-model-optimizer`) and model blueprint CSV export (drives `wiki-data-ingestion`'s model-refresh path); see [Scraper toolchain](#scraper-toolchain-optional) above. `tools/models.py` itself is gitignored — copy it from `models.py.example` locally.
- `anaplan/` — the generic, customer-agnostic Anaplan knowledge base (concepts, functions, patterns, generic sources) — fully tracked and public, ships pre-populated with this maintainer's accumulated generic content.
- `customers/`, `other-topics/`, and every domain's `index.md`/`log.md` are local-only and not checked in — `project-setup` creates the `customers/<Name>/` skeleton and `customers/registry.md` as you onboard each customer, and Claude generates the wiki pages inside as you ingest content.
