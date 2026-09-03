---
name: wiki-data-ingestion
description: >
  Ingest one or more new sources into the Anaplan LLM wiki — including raw docs, articles,
  PDFs, web clippings, and model CSV exports. Trigger whenever the user mentions ingesting a
  file, dropping something into raw/, adding a new source to the wiki, refreshing or
  re-scraping a model's data, or updating the wiki with new content. Also trigger when the
  user says things like "I added a new doc", "process this CSV", "refresh the <Model> data",
  "update the wiki with this file", "I dropped something in raw/", or any variant of "ingest".
  Handles both general sources and model CSV ingestion — first-time, incremental delta, and
  scraper-automated refresh. Always use this skill instead of doing ad-hoc ingest work — it
  ensures indexes, log, and cross-references are consistently updated.
---

# Wiki Data Ingestion

This skill drives a consistent, structured ingest of new sources into the wiki. It handles
two source families — general docs (articles, PDFs, web clippings) and model CSVs — and
branches automatically based on what it finds. The goal is to make every ingest predictable:
you always know what got created, what got updated, and what the wiki state is afterward.

---

## Phase 0 — Which path: document, or model data?

Two source families need different acquisition steps. Decide which path applies before
doing anything else:

- **Path A — Document ingestion**: general docs, articles, PDFs, web clippings, logs, or any
  file(s) the user already has in hand and wants placed into the wiki as-is.
- **Path B — Model data ingestion**: the user wants a model's blueprint data (Modules, Line
  Items, Lists, Actions, Roles, etc.) refreshed or ingested for the first time — e.g. "refresh
  the ModelA data", "pull the latest ModelB export", "ingest model X". This path is scraper-driven
  (`tools/scrape_model_data.py`) — the user does not need to have any file in hand.

If the user's message doesn't make the path obvious, ask: *"Is this a document/source to
ingest, or a model data refresh?"*

---

## Phase 0.5 — Resolve the domain

Before reading or writing any path below, resolve which domain this ingest
belongs to, per `CLAUDE.md` § Client Resolution:

1. **Model CSV export** (Modules.csv, Line Items.csv, General Lists.csv,
   Actions.csv, Model Calendar.csv, or any file inside a per-model
   subfolder) → always customer-specific. Resolve `<CUSTOMER_ROOT>` via
   `customers/registry.md` by model name; if the model isn't in the
   registry yet, ask which customer it belongs to and add a row.
2. **Diagnostic/error log** (from an import, action, or process) → always
   customer-specific, same as a CSV export — lands in
   `<CUSTOMER_ROOT>/logs/<Model>/`, a peer of `raw/`, never under
   `raw/logs/`. Resolve `<CUSTOMER_ROOT>` the same way as step 1.
3. **General source** (article, PDF, web clipping, plain-text doc) → ask
   yourself: is this generic Anaplan tool knowledge (Anapedia,
   best-practice, platform release notes)? → `<SHARED_ROOT>`. Is it tied
   to one customer (their standards doc, a meeting note, a model-build
   narrative)? → that customer's `<CUSTOMER_ROOT>`. Is it unrelated to
   Anaplan? → `other-topics/`. If genuinely ambiguous, ask the user —
   never guess when the wrong guess would publish customer data into the
   tracked `anaplan/` tree.

Every `raw/docs/`, `raw/models/`, `wiki/sources/`, `wiki/models/`,
`wiki/concepts/`, `wiki/functions/`, `wiki/patterns/`, `analyses/`,
`index.md`, and `log.md` reference elsewhere in this skill is relative to
the domain root resolved here — `<SHARED_ROOT>` or the resolved
`<CUSTOMER_ROOT>`, never the vault root directly. The one exception is
`logs/`, which is always `<CUSTOMER_ROOT>/logs/` (never `<SHARED_ROOT>/logs/`
— see step 2 above) and is never nested under `raw/`.

---

## Phase 0A — Acquire file paths (Path A only)

Before any reading or writing, you need to know exactly which files to ingest.

### If the user already provided file path(s)

Trust the input completely. Do not scan `raw/` or look for other new files. Proceed directly
to Phase 1 with the provided paths.

### If no paths were provided

**Stop immediately** and ask:

> "Which file(s) should I ingest? You can paste the path(s) or drag them in. If you'd prefer
> I discover them automatically, just say so."

- If the user provides path(s) → proceed to Phase 1 with those paths only.
- If the user explicitly declines to provide paths ("discover them", "check yourself", etc.):
  1. Read `wiki/sources/` index to build a set of already-ingested source slugs/filenames.
  2. Scan `raw/docs/`, `raw/models/`, and `raw/logs/` for files whose basenames do NOT
     appear in any existing `wiki/sources/` page (match on filename stem, case-insensitive).
  3. Present the candidate list to the user:
     > "I found these files that don't appear to be ingested yet: [list]. Should I proceed
     > with all of them, or only some?"
  4. Wait for confirmation before proceeding.

---

## Phase 0B — Resolve the model and its scraper shortcut (Path B only)

1. **Ask which model** if not already stated: *"Which model?"* Don't assume any particular
   model — this vault may have any number of models ingested, or none yet.

2. **Check whether it's already ingested** — does `<CUSTOMER_ROOT>/wiki/models/<Model>/`
   and/or `<CUSTOMER_ROOT>/raw/models/<Model>/` exist? Do this check yourself; don't ask
   the user. It decides
   first-time (Phase 3B) vs incremental-delta (Phase 3C) later. If the folder name doesn't
   already exist, confirm the exact display name with the user before creating it — match
   whatever short-code convention this customer's existing model folders already use (check
   `<CUSTOMER_ROOT>/raw/models/` and `<CUSTOMER_ROOT>/wiki/models/`), not a full
   descriptive name.

3. **Resolve a scraper shortcut.** Check `tools/models.py`'s `MODELS` dict for a key whose
   entry has `customer_id`, `workspace_id`, and `model_id` all present for this model.
   Verify the entry's `customer_id` is the tenant of the customer resolved in Phase 0.5 —
   shortcut keys are a flat namespace across every customer, so a similarly-named entry
   can belong to a different tenant, and scraping the wrong one writes another customer's
   model into this customer's folder.
   - **Shortcut exists** → note the key and the model's exact folder name, go to Phase 1B.
   - **No shortcut yet** (expected for any model not already registered — `tools/models.py`
     ships with an empty `MODELS` dict plus one commented-out example) → run:
     ```powershell
     python tools/scrape_model_data.py --list-models --shard eu3
     ```
     `--shard` is required here — every other mode reads its shard from the model's own
     `models.py` registry entry, but `--list-models` runs before that entry exists, so it has
     no entry to infer a shard from and must be told explicitly (e.g. `eu2a`, `eu3`, `eu4`,
     `eu9`). This logs in and calls the live Anaplan model-list API directly — no `models.py`
     shortcut needed for this step. It prints JSON: `model_name`, `model_id`,
     `workspace_name`, `workspace_id`, `customer_id` for every model visible to this account.
     Filter to candidates matching the requested name and **show them to the user for
     explicit confirmation** — the same model name can exist in more than one workspace.
   - Once confirmed, add `<PREFIX>_MODEL_ID=<model_id>` to `.env` (reuse a shared workspace
     var if one already exists for this tenant/workspace; otherwise ask the user what to call
     the new one) and mirror the example entry in `tools/models.py` with `customer_id`,
     `workspace_id`, `model_id`. Show the user what you're about to add before writing it —
     this is the first time this model becomes scriptable, worth a quick confirmation.
   - Proceed to Phase 1B with the new shortcut key.

---

## Phase 1B — Snapshot before scraping (Path B only)

The scraper overwrites each of its target files in place — this vault does not keep dated
archive copies of raw CSVs ([[feedback_no_dated_raw_copies]]; this applies to the scraper path
too). That means the "before" state must be captured before the scraper runs, or it's gone by
the time you want to diff.

1. If `<CUSTOMER_ROOT>/raw/models/<Model Name>/` already exists, copy only the files whose names are in the
   scraper's fixed target set for the mode you're about to run — 7 files by default, 15 with
   `--full` (see `docs/SCRAPE_MODEL_DATA.md` → "How the three paths work" for exact names) —
   into a temp folder under the session's scratchpad directory. This is ephemeral diff input
   only — never write it into `raw/`, and delete it once Phase 3C has applied the delta.
2. If the folder doesn't exist yet (true first-time ingest), skip this — there's nothing to
   diff against.
3. Leave any file in that folder whose name is *not* in the target set untouched and out of
   scope (e.g. `Import Data Sources.csv` — the scraper doesn't produce this and never will).

## Phase 2B — Run the scraper

```powershell
python tools/scrape_model_data.py <shortcut>
```

Omit `--out` for a registered model — that is now the safe default. The output folder is
derived from the shortcut's own `models.py` entry (`folder` + `raw_dir`), which must already
match `<CUSTOMER_ROOT>/raw/models/<exact existing folder name>`; if it doesn't,
`resolve_out_dir` raises rather than silently creating a wrong-named sibling folder, so a
`raw_dir`/`folder` typo in `models.py` surfaces immediately instead of manufacturing a
plausible-looking empty folder. Only pass `--out` for a scratch export (e.g. a temp dir to
diff before promoting into the vault) — an explicit `--out` **is** created if missing
(`exist_ok=True`), which is exactly why it must not be used as the everyday invocation for a
registered model: it bypasses the pre-exist guard that `raw_dir`/`folder` typos rely on.

`--name` is a display name for the script's console output only — it does not affect the
output folder at all. A shortcut's display name in `models.py` can differ from the vault's
folder name (e.g. a shortcut named `"modela"` might correspond to a folder called
`"ModelA 2.0"`); pass `--name` only if you want the log to read a particular way.

Read the script's own summary output — a ✅/✗ (or `ok`/`--`) line per target file plus a
produced-file count (7 or 15 depending on mode):
- **All targets succeeded** → every file in that mode's target set under
  `<CUSTOMER_ROOT>/raw/models/<Model Name>/` is now current.
- **Some failed** → the failed targets' prior files (if any) are left untouched, not deleted.
  Treat those specific files as still reflecting their pre-scrape state, ingest the deltas for
  whatever did succeed, and say explicitly in the Phase 4 summary which targets didn't refresh
  this run — don't silently treat a failed export as "no change."

Once the run completes, go to Phase 2 to classify (it will resolve to a model-CSV batch) and
then Phase 3B (first-time) or Phase 3C (delta, diffing against the Phase 1B snapshot instead
of a prior raw file).

---

## Phase 1 — Grouping (multiple files only)

When more than one file is in scope, ask before diving in:

> "Are these files related to the same topic, or are they independent sources?"

Use the answer to build **batches** — groups that will be processed together in a single
ingest pass. Rules:
- Related files → one batch (they share a source page and cross-reference each other).
- Unrelated files → separate batches processed sequentially.
- Mixed answer (e.g., "A and B are related, C is separate") → two batches: {A, B} then {C}.

If there is only one file, skip this phase.

---

## Phase 2 — Classify each batch

For each batch, classify the source type and (for CSVs) determine first-time vs re-upload.

### Classification rules

**Model CSV batch** — all files match the pattern of Anaplan model exports: filenames like
`Modules.csv`, `Line Items.csv`, `General Lists.csv`, `Actions.csv`, `Model Calendar.csv`,
or any file inside a `raw/models/<Model>/` subfolder.

**General source batch** — anything else: articles, PDFs, web clippings, plain text docs,
diagnostic logs under `<CUSTOMER_ROOT>/logs/` (never nested under `raw/` — see Phase 0.5 above).

### Delta detection for model CSVs

Check `wiki/sources/` for any prior ingest of the same model (match on model name in the
source page title or frontmatter slug). Also check `wiki/models/<Model>/` for existing pages.

- If prior pages exist → **incremental delta** mode (see Phase 3C).
- If no prior pages exist → **first-time ingest** mode (see Phase 3B).

When unsure (e.g., model name is ambiguous), ask the user: "Is this a re-upload of an
existing model, or a first-time ingest?"

---

## Phase 3A — Ingest: general source

For each batch of general sources:

1. **Read the source(s).** For CSVs outside the model export pattern, read structure first
   (headers, sample rows) before reading all content. For PDFs and long docs, read in
   sections.

2. **Create `wiki/sources/YYYY-MM-DD-<slug>.md`** with YAML frontmatter:
   ```yaml
   ---
   title: <Descriptive title>
   type: source
   tags: [anaplan, ...]
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   sources: [raw/docs/<filename>]
   ---
   ```
   Include: a summary of the source, key takeaways, and links to every wiki page created
   or updated as a result of this ingest.

3. **Touch relevant wiki pages:**
   - Create new pages for concepts, functions, or patterns introduced by the source (follow
     the function pages policy: only create individual function pages when the function is
     non-obvious, is used in a model being built, or the user asks).
   - Update existing pages with new facts, corrections, or examples. Preserve any
     user-added commentary.
   - Add cross-references both directions (new page → source, source → new page).

4. **Update indexes:**
   - Update the sub-index for every section touched (`wiki/concepts/index.md`,
     `wiki/functions/index.md`, `wiki/patterns/index.md`, `wiki/sources/index.md`).
   - Update the master `index.md` only if a new top-level section or sub-index was created.

5. **Append to `log.md`:**
   ```markdown
   ## [YYYY-MM-DD] ingest | <source title>
   Created: [list of new pages]
   Updated: [list of updated pages]
   ```

---

## Phase 3B — Ingest: model CSV (first-time)

1. **Sample the CSV structure** — read headers and a few rows to infer schema before
   loading the full file. Understand what each CSV covers (modules, line items, lists,
   dimensions, formulas, etc.).

2. **Seed `wiki/models/<Model Name>/`** — create structured pages for each entity type
   present in the exports:
   - One overview page listing all modules with their DISCO category (Data, Input, System,
     Calculation, Output) if inferable.
   - Subpages or sections per module, capturing: name, dimensions, line items, formulas
     (verbatim), and any flags (summary method, format).
   - Note the model's engine (Classic or Polaris) if determinable from context; otherwise
     flag as unknown.

3. **Create `wiki/sources/YYYY-MM-DD-<model>-initial.md`** summarizing the export scope
   (N modules, N line items, N lists, etc.) and linking to the model overview page.

4. **Update indexes** — `wiki/models/index.md`, `wiki/sources/index.md`, master `index.md`.

5. **Append to `log.md`:**
   ```markdown
   ## [YYYY-MM-DD] ingest | <Model Name> — initial CSV export
   Seeded wiki/models/<Model Name>/. Pages: [list]. Modules: N, Line items: N.
   ```

---

## Phase 3C — Ingest: model CSV (incremental delta)

The export is mostly the same as a prior version (~80% unchanged). Don't re-ingest from
scratch — apply only what changed.

1. **Diff against prior state.** This vault does not keep dated archive copies of raw CSVs
   ([[feedback_no_dated_raw_copies]]) — the prior raw file is gone by the time you're doing
   this diff, so pick the right "before" source:
   - **Scraper path (Phase 1B ran)** → diff against the ephemeral snapshot taken before the
     scraper overwrote the file. This is the accurate, file-level diff.
   - **Manually-dropped CSV (Path A/no Phase 1B snapshot)** → the user has typically already
     overwritten the raw file in place before handing it to you, so there is no prior raw
     version left on disk. Diff against the wiki model pages as a proxy instead.

   Identify: **added**, **removed**, **renamed**, and **modified** items (modules, line items,
   formulas, dimensions, lists).

2. **Do not create a dated archive copy of the new raw file.** It simply replaces what's on
   disk at `raw/models/<Model>/<filename>.csv` — matching how the scraper itself overwrites,
   and how the user already handles manual re-uploads. If you took a Phase 1B snapshot for
   diffing, delete it once this delta has been applied.

3. **Apply only the deltas to the wiki:**
   - Added items → create new pages or add sections.
   - Modified items → update the relevant page/section with the new value; note the change
     inline if significant.
   - Removed items → do not silently delete. Add a note: `> [!note] Removed YYYY-MM-DD —
     this item no longer appears in the export.` This guards against accidental deletions.
   - Renamed items → update the page title and all inbound `[[links]]`; add an alias note.
   - Preserve all user-added commentary and cross-references on existing pages.

4. **Create a new `wiki/sources/YYYY-MM-DD-<model>-delta.md`** summarizing what changed
   since the previous version. Link back to the prior source page. Do NOT overwrite the
   prior source page.

5. **Update indexes** as needed.

6. **Append to `log.md`:**
   ```markdown
   ## [YYYY-MM-DD] ingest-delta | <Model Name>
   +N modules, +N line items, N formula changes, N renames, N removals.
   Source: wiki/sources/YYYY-MM-DD-<model>-delta.md
   ```

---

## Phase 4 — Post-ingest summary

After every ingest (regardless of type), end with a structured summary in chat. This is
**always required** — do not skip it even for small ingests.

```
## Ingest complete — <source title or model name>

**Mode:** [General source | First-time model CSV | Incremental delta]
**Batch:** [file(s) processed]
**Scraper run** (Path B only): [N/7 or N/15 exported, depending on mode; list any targets
  that failed and were left at their pre-scrape state]

**Created:**
- wiki/sources/... (source page)
- wiki/concepts/... (if any)
- wiki/models/... (if any)

**Updated:**
- wiki/.../... — [what changed]
- index.md — [what was added]
- log.md — appended

**Delta summary** (model CSVs only):
- Added: N modules, N line items
- Modified: N formulas
- Removed: N items (flagged, not deleted)
- Renamed: N items

**Notes / flags for review:**
- [Anything ambiguous, contradictory, or requiring manual judgment]
```

If nothing was flagged, say so explicitly: "No issues flagged — wiki is consistent."

---

## Constraints and guardrails

- **Never hand-edit files under `raw/`** — they are immutable source documents. The scraper
  (Phase 2B) and manual re-uploads are the only sanctioned ways a raw model CSV changes; both
  replace the file wholesale with a fresh authoritative export, not an edit.
- **Always include a `sources:` frontmatter field** in every wiki page pointing back to the
  originating raw file.
- **Never create a dated archive copy of a raw CSV** — overwrite it in place, whether the
  refresh came from the scraper or a manual re-upload ([[feedback_no_dated_raw_copies]]).
  Diff against a Phase 1B ephemeral snapshot (scraper path) or the wiki pages (manual path)
  instead of a versioned raw file.
- **One source page per ingest event**, not per file. If a batch of 3 related CSVs is
  ingested together, one source page covers all three.
- **Prefer updating an existing wiki page over creating a near-duplicate.** Search
  `wiki/` before creating a new page.
- **Use Obsidian-compatible syntax** throughout: `[[wiki links]]`, YAML frontmatter,
  callouts (`> [!note]`), relative paths.
