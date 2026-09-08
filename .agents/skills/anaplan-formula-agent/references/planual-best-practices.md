# Planual Best Practices - Main reference

Apply these rules everytime. Reference: [Planual](`.\Anaplan LLM wiki\wiki\patterns\planual`) and
[Anapedia](https://help.anaplan.com, if you cannot find relevant information in the wiki).

1. **Break complex formulas into intermediate line items.** If a formula
   cannot be described in one sentence, split it. Never nest more logic than
   necessary.

2. **Replace nested IFs with LOOKUP on a mapping module.** If more than ~3
   `IF THEN ELSE IF` blocks appear, recommend restructuring with a constants
   or mapping module.

3. **No hard-coded SELECT on list members.** Use a SYS/constants module and
   LOOKUP instead of `SELECT(List.'Item')` embedded in formulas.

4. **Booleans over text flags.** Use Boolean-formatted line items in SYS
   modules rather than text string comparisons.

5. **Guard FINDITEM with ISNOTBLANK.**
   `IF ISNOTBLANK(text) THEN FINDITEM(List, text) ELSE BLANK`

6. **No POST for time offsets.** Use `OFFSET`, `LAG`, or `MOVINGSUM`.
   (POST is available in Polaris but cannot be used on Formula summary line items; prefer OFFSET.)

7. **Flag single-threaded functions.** `RANK`, `RANKCUMULATE`, and
   `ISFIRSTOCCURRENCE` are single-threaded — warn the user if the target list
   is large (>10k items).

8. **TIMESUM only for non-time-dimensioned line items.** If the source is
   already time-dimensioned, use `MOVINGSUM` or `YEARTODATE` instead.

9. **Minimize text concatenation (`&`) in large modules.** Pre-compute in a
   smaller SYS module and reference the result.

10. **Calculate once, reference many times.** Never duplicate formula logic
    across line items — build an intermediate and reference it.

11. **Use SYS modules for static/reference data.** Data that does not change
    with user input belongs in a SYS or PARAM module, not inline.

12. **Name intermediate line items clearly.** Prefix with `x ` (helper) or
    `SYS ` (system) per Planual naming conventions.

13. **Avoid circular references.** If a formula references itself (directly or
    indirectly), restructure the model to eliminate the circularity. This means to always follow DISCO principles. 
    Example: Reporting module should not reference a Calculation module that references back to the Reporting module. 
    Always pay attention to dependencies and data flow. 

14. **Never combine SUM with LOOKUP in the same line item formula.** It leads to long calcualtion time. 
