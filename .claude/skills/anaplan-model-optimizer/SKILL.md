---
name: anaplan-model-optimizer
description: >
  Analyze a production Anaplan model end-to-end to find modules AND line
  items that are safe to delete. Runs scraper_ux.py to pull a fresh new-UX
  (NUX) usage export for the chosen model - including the widget- and
  filter-level line item exposure sheets - then cross-references it against
  the model's raw CSV export (cross-module formula references, import/export
  targets, classic dashboard usage) so it never flags Data/Load/Calculation
  modules that are intentionally invisible in the UX but still feed other
  modules, and never flags a line item that's still referenced, imported, or
  shown/filtered on anywhere in the front end. Also surfaces a model owner's
  own deletion intent (Notes text, Functional Area=DELETE) as an annotation,
  including cases where something was marked for deletion but never actually
  cleaned up. Reports module candidates first, then line-item candidates
  within the surviving modules. Use this skill whenever the user asks to
  optimize, clean up, shrink, or reduce the size/complexity of an Anaplan
  model, asks which modules or line items are unused/orphaned/dead/safe to
  delete, mentions running the NUX/UX scraper or scraper_ux.py, or wants a
  "model health check" or "model housekeeping" pass. Always prefer this
  skill over eyeballing the Excel output manually - the cross-referencing
  against Modules.csv, Line Items.csv, and Imports.csv is what prevents
  false positives on load-bearing backend modules and line items.
---

# Anaplan Model Optimizer

**Before anything else:** resolve `<CUSTOMER_ROOT>` for the model in question via `customers/registry.md`, per `CLAUDE.md` § Client Resolution. All paths below are relative to that resolved root.

Finds modules in a production Anaplan model that can likely be deleted, by
combining two signals that neither one alone can safely provide:

1. **New-UX (NUX) exposure** - is the module shown on any app page/board? Comes
   from `scraper_ux.py`, which is the only source for this (it isn't in the
   static CSV export).
2. **Internal load-bearing-ness** - does the module feed other modules via
   formula, get written to by an import, or appear on a classic dashboard?
   Comes from the model's raw CSV export (`<CUSTOMER_ROOT>/raw/models/<Model>/Modules.csv` and
   `Imports.csv`), which the NUX scrape cannot see.

A module with zero NUX exposure is **not** automatically dead - Data, Load, and
Calculation modules in the DISCO pattern are *designed* to be invisible in the
UX; their only consumers are other modules' formulas. Only flag a module when
**both** signals come back empty. Getting this cross-check wrong means telling
the user to delete something that quietly breaks half the model.

## Step 1 - Identify the target model

Ask which model to analyze if it isn't already clear from context. The
cross-reference in Step 4 needs `<CUSTOMER_ROOT>/raw/models/<Model Name>/Modules.csv` (and
ideally `Imports.csv`) to already exist - these are the CSVs the
`wiki-data-ingestion` skill produces from a model's own CSV export. Check the
project's `CLAUDE.md` for its Engine defaults list (which models are
currently ingested, and whether each is Classic or Polaris) - don't assume
either engine, and ask the user if the model isn't listed there yet.

If the requested model has no `<CUSTOMER_ROOT>/raw/models/<Model Name>/` folder yet, tell the
user Step 4's safety cross-check needs at least a `Modules.csv` export dropped
there first (via the `wiki-data-ingestion` skill) - offer to proceed
Excel-only in the meantime, but flag every result as unverified against
internal formula dependencies if they choose that path.

## Step 2 - Make sure the model has a scraper shortcut

`tools/scraper_ux.py` prompts interactively for everything, including a numbered
pick from a live list of every model in the tenant. To automate it safely,
the target model must be a pre-configured shortcut in `tools/models.py` (see
the example entry there) - that turns "pick from a live list" into "type a known
number," which is the only part of the wizard that can't otherwise be
scripted blind.

1. Read `tools/models.py`. It holds a `CUSTOMERS` tree (customer key -> customer
   fields -> nested `models`), not a flat dict; a model counts as a usable
   shortcut only once its customer's `shard`, `folder`, and `customer_id`, plus
   its own `name`, `raw_dir`, `workspace_id`, and `model_id`, are all present
   (`engine` and `workspace_label` are optional). Compute the model's 1-based
   position among *that customer's* usable models, in the order they appear
   under the customer - that number is exactly what the wizard's
   customer-filtered "MODEL SELECTION" menu will show once that customer is
   chosen.
2. If the target model has no shortcut yet, you need its Anaplan model GUID.
   Ask the user for it - they can copy it out of the browser address bar while
   the model is open in Anaplan (`.../models/<GUID>/...`). Then:
   - Add a new entry under the target customer's `models` key in
     `tools/models.py`, giving it `name`, `raw_dir`, `workspace_id`, and
     `model_id` as literals (no `.env` involvement - GUIDs live inline in
     `models.py`, not in environment variables). Reuse the customer's already-
     declared `shard`/`folder`/`customer_id` rather than repeating them.
   - Re-read the file to recompute the shortcut's numeric position.
3. Preflight-check `.env` has what non-interactive login needs, **without
   printing or reading any secret values** - only check presence, e.g.:
   ```
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('ANAPLAN_USERNAME' in os.environ and bool(os.getenv('ANAPLAN_USERNAME')), bool(os.getenv('ANAPLAN_PASSWORD')), bool(os.getenv('ANAPLAN_USE_SSO')))"
   ```
   `ANAPLAN_PASSWORD` in particular is non-negotiable for automation: if it's
   missing, `tools/scraper_ux.py` falls back to `getpass.getpass()`, which cannot be
   fed through a piped stdin sequence and will hang the run. If any of these
   come back `False`, stop and ask the user to fill in `.env` (never ask them
   to paste the value into chat - just tell them which key is missing).

## Step 3 - Run scraper_ux.py

The wizard asks a fixed sequence of questions; with `.env` filled in, every
one of them has a usable default except the model-selection number and the
final "scrape another model?" loop (which defaults to "yes" and must be
stopped explicitly). In order:

1. Customer - accept default, or the customer's number from the menu
2. Email - accept default (password is read from `.env` directly, no prompt)
3. SSO? - accept default
4. Output folder - accept default (`customers/<folder>/UI/`)
5. "Everything correct?" - accept default (yes)
6. Model selection - **the shortcut number from Step 2**
7. "Ready to scrape '<model>'. Continue?" - accept default (yes)
8. "Would you like to scrape another model?" - must answer **no**, or the
   wizard loops back to model selection with no way to feed it a second
   pre-computed choice

The model menu now lists **only the chosen customer's models**, so the
shortcut number is per-customer - re-read it from the menu rather than reusing
a number from a previous run against a different customer.

That means the full stdin payload is the customer number, four blank lines,
the shortcut number, one more blank line, then `n`:

```bash
printf '%s\n\n\n\n\n%s\n\nn\n' "<customer_number>" "<shortcut_number>" | python tools/scraper_ux.py
```

Run this in the background - it opens a real (non-headless) Edge window and
can take several minutes on large models (a large model can easily exceed
400 modules). Tell the
user up front: *"A browser window is about to open. If your organization uses
SSO with MFA, please complete that step in the window when it appears - the
script only pauses briefly after login before it starts pulling data."*
Because the browser isn't headless, the user can freely interact with it on
their own screen even though the wizard's text answers are coming from the
piped stdin.

Wait for the background command to finish, then find the newest file matching
`Anaplan NUX Report - <model name>_*.xlsx` in `customers/<folder>/UI/` — or in
`ANAPLAN_OUTPUT_FOLDER` if that is set in `.env`, which overrides the
per-customer default for every customer.

If the run fails or hangs (most commonly: an SSO/MFA challenge that took
longer than the script's fixed post-login wait, so the subsequent API calls
came back as an HTML login page instead of JSON), tell the user what
happened and offer to retry.

## Step 4 - Cross-reference the report

Run the bundled script:

```bash
python .claude/skills/anaplan-model-optimizer/scripts/analyze_module_usage.py \
  --excel "<path to the NUX report .xlsx>" \
  --model-dir "<CUSTOMER_ROOT>/raw/models/<Model Name>" \
  --model-name "<Model Name>" \
  --out-json "<CUSTOMER_ROOT>/analyses/<Model Name>-module-optimization-<YYYY-MM-DD>.json" \
  --out-markdown "<CUSTOMER_ROOT>/analyses/<Model Name>-module-optimization-<YYYY-MM-DD>.md"
```

This does the actual cross-referencing in code rather than by reading the
spreadsheet by eye, because the safety logic (don't flag something that's
referenced elsewhere) needs to be exact, not approximate. It runs two
passes and writes one combined report:

**Pass 1 - modules.** For each module, in order:

1. NUX usage count > 0 → **active**, definitely keep
2. Referenced by another module's formula (`Modules.csv` "Referenced By") →
   **keep**, it's an internal dependency
3. Modules containing line items used as filter for NUX pages, per the NUX report's `UI Filters` sheet
   (usually named as filter modules, UF XX. or FI XX.)→ **keep**
4. Source or target of an import/export (`Imports.csv`, plus the report's own
   per-model actions sheet) → **keep**
5. Module category headers for auditability purposes, always fully empty 
   (e.g. `◼️ LOAD MODULES` or `◼️ INFORMATION MODULES`) → **keep**
6. None of the above → **candidate for review**

It also separately flags any module the CSV export knows about but the NUX
report doesn't mention at all (name mismatch, or the export predates a rename)
- treat those as a data-quality flag, not a deletion candidate, and ask the
user to double check the name.

**Pass 2 - line items.** Runs only inside modules that survived Pass 1
(verdict `ACTIVE` or `KEEP` - a module already flagged as a deletion
candidate makes its line items moot, so they're skipped). For each line
item in an in-scope module, in order:

1. Shown in a widget or used as a filter, per the NUX report's
   `Views Usage Report - Line Items` and `UI Filters` sheets → **active**
2. Referenced by another line item's formula (`Line Items.csv` "Referenced
   By") → **keep**
3. Named via dot-notation in an `Imports.csv` Source/Target Object
   (best-effort text parse - may find nothing on models with no internal
   cross-module imports, that's expected, not a bug) → **keep**
4. Line items headers in modules for auditabilily purposes (e.g. `---Technical---` or `---CF---`) → **keep**
5. Line items for conditional formatting (e.g. `CF - <line item name>`),
   not possible to capture in the NUX scrape, need user review → **User to verify usage** 
6. None of the above → **candidate for review**

**Manual deletion markers (both passes).** Independently of the above, each
module and line item is checked for a model-owner deletion marker: `Notes`
containing `delete`, `to be deleted`, `obsolete`, `deprecated`, or `remove`
(case-insensitive), or (module-level, inherited by its line items) a
`Functional Area` containing `DELETE`. This never overrides the checks
above - it only annotates: a computed candidate with a marker present is
the highest-confidence recommendation, while a marker present on something
computed as `ACTIVE`/`KEEP` is surfaced separately as a contradiction worth
investigating (deletion was intended but never finished, or the item turned
out to still be load-bearing).

Per the project's `raw/` conventions, never edit the CSVs or the xlsx - this
script only reads them.

## Step 5 - Report in chat

Present the results directly in the conversation, not just a pointer to the
saved file. Modules first, then line items:

- Lead with the module candidate-for-review table (module name + functional
  area + any deletion-marker flag). Frame it as *"these look safe to review
  for deletion"*, not *"delete these"* - text-based reference parsing can
  miss dynamic references (e.g. `SELECT` on a computed string), so recommend
  the user do a final native check in Anaplan (e.g. the module's
  dependency/blueprint view) before deleting anything. Group by functional
  area if there are more than a handful.
- Briefly show the "kept despite zero NUX usage" table too, with the reason
  - this is what lets the user trust the candidate list instead of wondering
  whether the analysis just missed something.
- Then present line-item candidates, grouped by the module they live in
  (module name + functional area + candidate line item names) - only for
  modules that survived Pass 1 and have at least one candidate line item.
  Mention the total count of modules checked with zero line-item candidates
  without listing them individually.
- Show both "flagged for deletion but still active or kept" tables (modules,
  then line items) if either is non-empty - these are model-owner-marked
  items that turned out to still be wired in, worth flagging as a cleanup
  gap even though this skill won't recommend deleting them outright.
- Mention the full report was saved under `<CUSTOMER_ROOT>/analyses/` per this project's
  convention for non-wiki outputs.
- This skill only recommends. Never delete anything - the user removes
  modules or line items from the model themselves in Anaplan.
