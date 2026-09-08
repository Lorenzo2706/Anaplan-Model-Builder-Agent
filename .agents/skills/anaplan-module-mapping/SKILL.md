---
name: anaplan-module-mapping
description: >
  Provide dual explanations — financial/functional logic AND Anaplan technical mechanics — 
  whenever mapping, wiring, or connecting line items across Anaplan modules. Use this skill 
  whenever the user asks to connect or feed one module into another, requests cross-module 
  formulas (anything using SUM:, LOOKUP:, SELECT:, or dot-notation references across modules), 
  asks what a line item should pull from, asks to explain data flow between modules, or asks 
  why a formula is written a certain way in the context of financial statements or calculations. 
  Always apply the dual-explanation format — even for single formulas, even for "simple" references. 
  The user cannot evaluate correctness without understanding both the business intent and the 
  Anaplan mechanics; skipping either half leaves the formula unverifiable.
---

# Anaplan Module Mapping — Dual Explanation Standard

**Before anything else:** resolve `<CUSTOMER_ROOT>` for the model(s) involved via `customers/registry.md`, per `AGENTS.md` § Client Resolution.

When you map or connect a line item in one Anaplan module to a source in another, always 
deliver two explanations for every formula. Do not combine them into one paragraph — keep 
them distinct so the user can read the one they need without having to parse the other.

## The Two Explanations

### 1. Financial / Functional Logic

Answer: *What does this number represent, and why should it flow from this source?*

- State what the target line item means in business or accounting terms (what it represents 
  on the P&L, balance sheet, cashflow, or other report).
- Explain why the source module is the right place to read it from — what calculation or 
  data it holds, and how that relates to the target.
- Note any classification choices that matter: why something appears on this line rather 
  than another (e.g., why hybrid interest goes to "dividend paid" rather than "interest paid"; 
  why an item is LT vs ST; why a cost appears in OPEX vs CAPEX).
- If the sign is flipped, explain the accounting convention that requires it (costs are 
  positive in a calculation module but negative on a P&L; cash outflows are negative in 
  cashflow statements, etc.).
- If the user's model uses module/LI names in a language other than the user's working 
  language, translate the relevant terms in plain English as part of this section.

### 2. Anaplan Technical Mechanics

Answer: *How does the formula actually work step by step?*

- Identify the dimension mismatch between source and target, and explain what aggregation 
  or lookup resolves it (SUM vs LOOKUP, and why for this specific case).
- Name the mapping line item(s) used and which module they live in — explain what each 
  one contains (e.g., "IM XX.Parent Entity maps each child list member to its parent").
- If Polaris auto-sums residual source dimensions not covered by the explicit SUM: selector, 
  call this out explicitly rather than leaving it implicit.
- Note any sign transformation in formula terms (negation, multiplication by -1, etc.) and 
  distinguish it from the financial reason for the sign (explained in part 1).
- Flag dependencies: mapping LIs that must exist before the formula can be entered, helper 
  line items that need to be pre-built in the source module, etc.
- If the formula uses a helper line item in the source module (e.g., a pre-filtered or 
  pre-aggregated variant), briefly state what that helper does rather than treating it as 
  a black box.

## Output Structure

For each target line item, follow this layout:

```
### `[Target module].[Target LI name]` — [English translation of what it means]

[Formula — paste-ready]

**Financial logic.** [Explanation: what this number is, why it comes from this source, 
sign convention, any classification choice worth knowing.]

**Anaplan mechanics.** [Explanation: dimension mismatch, what the SUM:/LOOKUP: mapping 
does, any auto-aggregation, dependencies, helper LIs.]
```

When multiple target LIs share the same aggregation pattern, you may group the mechanics 
explanation ("same SUM: pattern as above") but always write a separate financial logic 
section — the business meaning of each line is different even when the formula structure 
is identical.

## Dimension Alignment Checklist (run before writing any formula)

Before writing, resolve these in order:

1. **What dimensions does the target module have?** (e.g., Version × Entity × Time)
2. **What extra dimensions does the source module have that the target does not?** These must 
   be explicitly aggregated (SUM:) or the remaining ones will be auto-summed by Polaris.
3. **Are any target dimensions absent from the source?** These need a LOOKUP.
4. **Is the target at a parent level of the source's list?** Use SUM: with a mapping that 
   routes each child item to its parent.
5. **Is the target at a child level of the source's list?** Use LOOKUP to spread the parent 
   value to each child (or use a designated mapping module that selects one child per parent).
6. **What summary method do source line items use?** If Sum summaries are set on a list 
   dimension, note that Polaris leverages these in cross-module aggregation.

## Sign Convention Reference

Keep these consistent across the model:

| Context | Convention |
|---|---|
| Calculation modules | Costs are **positive**; revenues are **positive** (treat separately) |
| P&L / Income Statement | Costs are **negative** (reduce profit); revenues are **positive** |
| Cashflow Statement | Outflows are **negative**; inflows are **positive** |
| Rollforward / Balance movement | Items that reduce a balance are **negative**; additions are **positive** |

Always state which convention applies when explaining a negation.

## Common Mapping Scenarios

### Calculation module → P&L / Income Statement
Source calculation module holds costs as positive values; the P&L requires costs as negative 
(reducing profit). SUM: up any extra source dimensions (e.g., cost category, instrument type) 
that the P&L does not have. Apply `* -1` where the sign convention requires it, and explain 
the accounting reason in the financial logic section.

### Calculation module → Cashflow Statement
Same aggregation pattern as P&L. Cash outflows must be negative. If the source has multiple 
extra dimensions, the explicit SUM: selector handles one; Polaris auto-sums any remaining 
dimensions not covered by it — call this out explicitly so the reader knows what is implicit.

### Calculation module → Rollforward / Balance movement module
Distinguish movement line items (additions, reductions that feed the rollforward formula) 
from position line items (opening/closing balances). Only wire movements from the calculation 
module; closing balances are computed within the rollforward module from those movements.

### Detail list → Summary list (aggregation)
Source is dimensioned by a child list; target is dimensioned by the parent list. Use 
`SUM: <MappingModule>.'<Parent LI>'` where the mapping module is dimensioned by the **source** 
(child) list and holds a reference to each item's parent. Polaris will auto-sum any additional 
source dimensions not explicitly handled by the SUM: selector.

### Summary list → Detail list (distribution)
Target is more granular than the source. Use `LOOKUP: <MappingModule>.'<Source LI>'` where 
the mapping module is dimensioned by the **target** list and points each member to its source 
counterpart. Use this when spreading a parent-level value to child members.

### SUM vs LOOKUP decision rule
- **SUM:** Source list maps → Target list item (source is more granular than target, or has 
  an extra dimension being collapsed). The mapping LI lives in a module dimensioned by the 
  **source** list.
- **LOOKUP:** Target list maps → Source list item (target needs to navigate to the right row 
  in the source). The mapping LI lives in a module dimensioned by the **target** list.
