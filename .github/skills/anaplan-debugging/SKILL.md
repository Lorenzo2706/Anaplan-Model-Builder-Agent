---
name: anaplan-debugging
description: >
  Debug an Anaplan formula or module that returns wrong, zero, blank or
  unexpected values, by forming hypotheses from the model metadata and then
  validating each one against live cell data with tools/fetch_model_data.py.
  Use whenever the user says a line item "shows nothing", "is zero", "doesn't
  calculate", "gives the wrong number", asks why a module output is off, wants
  to verify a formula against real data, or asks to "debug", "trace" or
  "check the values" in a model - even if they never mention fetch_model_data.
  Needs a resolvable customer model (customers/registry.md).
---

# Anaplan Debugging

Debug by evidence, not by reading formulas and guessing. A formula that looks
right can still return nothing because of a dimension, time-scale or
data-type mismatch that only shows up in live values. So every hypothesis gets
tested against real cells before you propose a fix, and every fix gets
re-tested after the user applies it.

## Step 0 - Ask for the test case (always first)

Before touching any tool, ask the user with AskUserQuestion:

> Do you have a specific test case (an item and, if relevant, a period or
> scenario where you know the expected value), or should I find a relevant one
> myself?

- **User supplies one** - record: module + line item, the row item(s), period /
  scenario / version, and the expected value. This is your oracle.
- **Find it autonomously** - go on, but pick the case in Step 2 and state it
  back to the user so they can confirm it is a sensible oracle. An
  autonomously found case has no known expected value: say so, and ask the user
  to confirm what "right" looks like before declaring anything fixed.

## Step 1 - Resolve the model and read its definition

1. Resolve customer, model and engine via `customers/registry.md` (CLAUDE.md
   *Client Resolution*). The engine changes which functions exist.
2. Read the wiki pages and raw `Line Items.csv` / `Modules.csv` for the module:
   formula, Applies To, Time Scale, Summary, format, who references it.
3. **Treat the export as possibly stale.** Models change between scrapes: in a
   past case the live blueprint had new line items the export lacked. Refresh
   the metadata into a scratchpad folder (never over `raw/`):
   `python tools/scrape_model_data.py <customer:model> --customer <key> --rest-only --out <scratchpad>/fresh`
   and re-read the line item you are debugging after every change the user makes.
4. Verify every function and its syntax in `anaplan/wiki/functions/index.md`
   before putting it in a proposal (project rule: do not guess formulas).

## Step 2 - Form hypotheses, then test the cheapest first

List 2-4 candidate causes before fetching anything. Typical ones:

- **Dimension mismatch** - the line item and its sources have different
  dimensions or a different Time Scale (a LOOKUP mapping with a Month axis
  feeding a time-less target; a time-less cell referencing a monthly one).
- **Wrong mapping type** - LOOKUP mappings must be a list, date or time-period
  line item. A Boolean cannot map, and a LOOKUP can only return one period.
- **Inputs really are blank or zero** - the formula is fine and upstream is
  empty, or the scenario / version / access selection differs from what you
  assumed.
- **Settings upstream** - current period, scenario start period and other flags
  in `SYS` modules that gate the calculation.
- **Summary / aggregation** - a Summary of None hides a total.

Then fetch (Step 3) the target, then each upstream input and each settings
module the formula depends on, working back until a hypothesis is confirmed or
killed. If no test case was supplied, choose here: sample the target output
and pick a populated row whose upstream source is non-zero.

## Step 3 - Fetching live values

Read `docs/FETCH_MODEL_DATA.md` first. Basics:

```bash
python tools/fetch_model_data.py module <customer:model> "<Module name>" \
  --out-dir <scratchpad> --sample 8 \
  [--page "Scenario:<item>"] [--line-items "A,B"] [--periods "Jan 26:Dec 26"]
```

- `--out-dir` is required and must be the session scratchpad, never inside the
  repo. Count zero / blank / non-zero from the full CSV it writes rather than
  trusting the short sample.
- Page-dimension items may show internal names (for example `#1`) that differ
  from the display name; if a `--page` value is rejected, the error lists the
  valid items.
- **The 1M-cell limit.** Anaplan rejects any view over 1,000,000 cells, and the
  check runs on the whole view before rows return. `--line-items` and
  `--periods` only narrow after download, and there is no API row limit
  (`limit`, `maxRows`, `rows`, `rowLimit` were tested and refused). Only page
  dimensions narrow. Do not keep retrying. Instead:
  1. fetch an upstream or sibling module that is small enough;
  2. ask the user to read the item in the UI;
  3. propose a temporary check module applied to the page dimension only (for
     example Scenario), with one line item per value using
     `Source[SELECT: List.'item']`, which you can then fetch in one call.
  This is a known tooling gap, tracked in
  `customers/KWS/analyses/fetch-large-view-row-narrowing/`.
- Fetched cells are live customer data. Quote them in chat if useful, but
  **never write them into `wiki/`, `analyses/` or `log.md`**. Tickets and
  write-ups may state counts and structure, not values.

## Step 4 - Conclude and propose

State the confirmed cause with the evidence (what you fetched, what it showed).
Then propose the fix:

- Give the exact formula and the blueprint settings that go with it (Applies
  To, Time Scale, Summary, format). Settings are part of the fix: a correct
  formula on a wrongly scaled line item still shows 0.
- Explain why in one or two lines, and name any assumption about intended
  meaning. If two readings fit the evidence (for example "value at one period"
  versus "cumulative over past periods"), present both and ask. Do not pick one
  silently because the oracle number happens to fit.
- Say what the fix should return for the oracle item, so the check is concrete.

## Step 5 - Verify after the user applies it

You cannot edit a model: the scrape and fetch tools are read-only. Tell the
user plainly that they must apply the change, then:

1. Re-scrape the line item and confirm the formula **and** the blueprint
   settings actually changed (a fix can land with the formula changed but the
   Time Scale or Summary untouched).
2. Re-fetch the target and compare against the oracle.
3. If it still does not match, treat that as a new observation, not a failed
   plan: form the next hypothesis (for example other periods contribute to a
   cumulative total) and repeat from Step 2.

Stop and report honestly when the tools cannot go further (view too large, no
way to read the needed row). Say what is unverified and what would settle it.

## Output

Keep chat updates short: hypothesis, what you fetched, result. If the finding
is substantive and reusable, offer to file it as an analysis under
`<CUSTOMER_ROOT>/analyses/` (no cell values), and as a ticket per
`docs/agents/issue-tracker.md` if it exposes a tooling limitation.
