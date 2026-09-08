---
name: circular-reference-prevention
description: >
  Use when asked to check an Anaplan model for circular-reference risk, DISCO
  breaks, engine-failure/loop risk from feedback between modules, or whether
  a module tagged Calculation actually behaves as Output. Triggers on
  "circular reference", "DISCO break", "engine failure risk", "loop risk",
  "mislabeled module", or auditing Line Items.csv/Modules.csv for build
  integrity across a whole model.
---

# Circular Reference Prevention

**Before anything else:** resolve `<CUSTOMER_ROOT>` for the model in question via `customers/registry.md`, per `AGENTS.md` § Client Resolution. All paths below are relative to that resolved root.

## Overview

A DISCO break is not "any circular-looking reference" — it is specifically a
calculation retrieved from a module acting as Output that feeds back (directly
or indirectly) into that same Output module in the same time period. Agents
generally get the semantic judgment calls right once the definition is stated
precisely (same-period vs. `PREVIOUS()`-shifted edges, tagged vs. behavioral
Output). What they reliably skip at scale is the two disciplines below —
both non-negotiable.

## When to Use

Circular-reference / loop-risk / engine-failure audits of an Anaplan model;
checking whether a Calculation-tagged module actually behaves as Output; any
whole-model integrity pass over Line Items.csv / Modules.csv.

**Not for:** debugging one specific circular-reference error Anaplan already
reported — that's direct troubleshooting; use `anaplan-formula-agent`.

## The Two Non-Negotiable Disciplines

1. **Independent verification, not self-review.** A candidate cycle or
   mislabeling is confirmed only once a genuinely separate pass — a different
   agent that did not build the original graph — re-derives it from the raw
   formulas and reproduces the same conclusion. Re-reading your own output and
   calling it "spot-checked" does not count; this is the #1 gap baseline
   agents default to.
2. **Orchestrate at scale.** Past a handful of modules, parsing every line
   item and verifying every candidate yourself, sequentially, is how false
   positives and missed cycles survive into the report. Use the `Workflow`
   tool: one phase builds the graph, `pipeline()` fans candidates out to
   independent verifiers concurrently, a parallel phase audits mislabeling
   model-wide, a final phase synthesizes the report.

## Definitions

| Term | Meaning |
|---|---|
| Same-period edge | `A` reads `B`'s current-period value directly. Can close a real cycle. |
| Time-shifted edge | `A` reads `B` via `PREVIOUS()`/`OFFSET()`/`NEXT()`. Resolves sequentially across periods — cannot itself close a real cycle. |
| Tagged Output | Module's DISCO tag/Functional Area says Output/Report. |
| Behavioral Output | Nothing else reads the module's line items for *calculation* (dashboard/export consumption doesn't count against this). Corroborate with `Modules.csv`'s `Used in Dashboards` column and any Export-action source in `Actions.csv`/`Imports.csv`. |
| Mislabeled module | Tagged Calculation but behaviorally Output. Report model-wide — do not restrict to modules already implicated in a cycle. |
| Genuine risk | A cycle where **every** edge is same-period **and** at least one member module is a behavioral Output. |
| Safe pattern | A cycle where at least one edge is time-shifted. Report separately, not as a risk. |

## Implementation

1. **Graph, not prose.** Parse `Line Items.csv` (Formula + Referenced By
   columns) and `Modules.csv` with a real script (Python, real CSV parser —
   Anaplan exports quote fields with embedded commas/newlines). Build the
   graph at **line-item** granularity, never module-only: two modules can
   look mutually connected while no single line item actually loops, which
   would be a false positive at module granularity.
2. **Cross-check, don't trust one column.** Derive edges from `Referenced By`
   (Anaplan's own reverse-dependency data) AND independently from parsing
   `Formula` text. Where they disagree, that's a data-quality flag (stale
   export, rename, alias) — log it, don't silently prefer one source.
3. **Tag every edge** same-period or time-shifted (regex for `PREVIOUS(`/
   `OFFSET(`/`NEXT(` wrapping the reference).
4. **Classify every module's effective role** (behavioral, per Definitions
   table above) — this determines the cycle filter in the next step, so it
   must run before final cycle scoring, not after.
5. **Run real cycle detection** (Tarjan's SCC or equivalent) on the full
   line-item graph. Keep only candidates where every edge is same-period and
   at least one line item belongs to a behaviorally-Output module. Discard
   Parent/Summary rollup "cycles" (that's aggregation, not circularity).
6. **Check engine semantics** before scoring borderline cases — Classic and
   Polaris tolerate circularity differently; consult
   `anaplan-formula-agent`'s `references/classic-vs-polaris.md` if the
   model's engine isn't already known.
7. **Dispatch independent verification** for every surviving candidate and
   every mislabeling candidate (see disciplines above) — each gets re-derived
   from the raw CSVs by a separate agent pass before being allowed into the
   report. Reject anything that can't be independently reproduced; note why.
8. **Fix per finding must be concrete**: name the exact line item(s), the
   exact new formula or module restructuring, not generic DISCO advice.
   Standard remediation patterns: insert a bridge Calculation module so the
   Output becomes a pure leaf; introduce a `PREVIOUS()` lag if a one-period
   delay is business-acceptable; re-tag (not re-wire) if the module is simply
   mislabeled; split a module that's doing both calc and output duty.
9. **Report negative space**: rejected candidates (with the reason), safe
   time-shifted patterns, rejected mislabeling candidates, and data-quality
   flags — an audit that only shows positive findings looks like it skipped
   the hard cases.
10. **Deliverable**: self-contained HTML to `<CUSTOMER_ROOT>/analyses/<Model>-circular-
    reference-audit-<date>.html`, executive-summary-first (ranked findings
    table, readable in under a minute), then a drill-down per confirmed
    finding (diagram + formula table + concrete fix), then the negative-space
    appendix.

For whole-model scale, structure the `Workflow` script as: phase 1 (one
agent, graph-build + classification + raw cycle detection, returns candidate
cycles + mislabel candidates as structured data) → phase 2
(`pipeline(candidateCycles, verifyAgent)`, independent verification,
concurrent) → phase 3 (`pipeline(mislabelCandidates, verifyAgent)`, can run
alongside phase 2) → phase 4 (one agent, synthesize confirmed findings +
negative space into the HTML).

## Common Mistakes

| Mistake | Why it's wrong |
|---|---|
| Detecting cycles at module level only | Two modules can look mutually connected via disjoint line items with no real loop — false positive. |
| Flagging any cycle containing `PREVIOUS()`/`OFFSET()` | Time-shifted edges resolve sequentially; only all-same-period cycles are real risk. |
| Trusting the DISCO tag as the Output test | Misses exactly the mislabeled-module case the user is asking about — check behavior, not the label. |
| Scoping mislabel checks only to cycle-implicated modules | Mislabeling is a standalone finding; scan model-wide. |
| Calling your own re-read of the formulas "verification" | Not independent. Dispatch a separate agent/pass that didn't produce the original graph. |
| Single-threaded pass over a whole model | Doesn't scale past a handful of modules without missed cycles or unchecked candidates. Use `Workflow`. |
| Generic "insert a calc module" advice | Not actionable. Name the exact line item and new formula. |
| Reporting only confirmed findings | Hides whether rejected candidates were actually checked — always show the negative space. |

