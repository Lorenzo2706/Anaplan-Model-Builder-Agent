# Polaris Function Compatibility — Authoritative Reference

**Source:** All Anapedia function pages in `<SHARED_ROOT>/raw/docs/` (scraped 2026-05-02).  
**Rule:** Before suggesting any formula for a Polaris model, verify every function used is in the ✅ or ⚠️ columns below — never assume availability.

---

## Quick-Look Status Table

| Function | Polaris | Notes |
|---|---|---|
| **ABS** | ✅ | No differences noted |
| **ACOS** | 🆕 Polaris-only | Trigonometry — Classic engine does not have this |
| **ACOSH** | 🆕 Polaris-only | Trigonometry — Classic engine does not have this |
| **ADDMONTHS** | ⚠️ | NaN for *Number* arg returns blank (Classic: error) |
| **ADDYEARS** | ⚠️ | NaN for *Number* arg returns blank (Classic: error) |
| **AGENTS** | ❌ | Call center — unavailable in Polaris |
| **AGENTSB** | ❌ | Call center — unavailable in Polaris |
| **ALL** | ⚠️ | Default for unmapped cells is FALSE (Classic: TRUE) |
| **ANSWERTIME** | ❌ | Call center — unavailable in Polaris |
| **ANY** | ✅ | No differences noted |
| **ARRIVALRATE** | ❌ | Call center — unavailable in Polaris |
| **ASIN** | 🆕 Polaris-only | Trigonometry |
| **ASINH** | 🆕 Polaris-only | Trigonometry |
| **ATAN** | 🆕 Polaris-only | Trigonometry |
| **ATANH** | 🆕 Polaris-only | Trigonometry |
| **AVERAGE** | ✅ | No differences noted |
| **AVGDURATION** | ❌ | Call center — unavailable in Polaris |
| **AVGWAIT** | ❌ | Call center — unavailable in Polaris |
| **CODE** | ⚠️ | Time period value returns blank (Classic: text); can't use on Formula/Ratio summary LIs |
| **COLLECT** | ✅ | Line item subset collector — no Polaris restrictions noted |
| **COMPARE** | ❌ | Unavailable in Polaris |
| **COS** | 🆕 Polaris-only | Trigonometry |
| **COSH** | 🆕 Polaris-only | Trigonometry |
| **COUPDAYBS** | ❌ | Financial — unavailable in Polaris |
| **COUPDAYS** | ❌ | Financial — unavailable in Polaris |
| **COUPDAYSNC** | ❌ | Financial — unavailable in Polaris |
| **COUPNCD** | ❌ | Financial — unavailable in Polaris |
| **COUPNUM** | ❌ | Financial — unavailable in Polaris |
| **COUPPCD** | ❌ | Financial — unavailable in Polaris |
| **CUMIPMT** | ❌ | Financial — unavailable in Polaris |
| **CUMPRINC** | ❌ | Financial — unavailable in Polaris |
| **CUMULATE** | ⚠️ | Available in both. Can't use on Formula summary LIs in Polaris. *List* arg applies only within subset in Polaris (not whole list) |
| **CURRENTPERIODEND** | ✅ | No differences noted |
| **CURRENTPERIODSTART** | ✅ | No differences noted |
| **CURRENTVERSION** | ✅ | No differences noted |
| **DATE** | ✅ | No differences noted |
| **DAY** | ✅ | No differences noted |
| **DAYS** | ✅ | No differences noted |
| **DAYSINMONTH** | ✅ | No differences noted |
| **DAYSINYEAR** | ✅ | No differences noted |
| **DECUMULATE** | ⚠️ | Available in both. Polaris: can't use on Formula summary LIs. Polaris: extra *List* arg enables any dimension (Classic: time only) |
| **DIVIDE** | ✅ | No differences noted |
| **DURATION** | ⚠️ | Financial — Polaris status not explicitly stated in Anapedia; treat as potentially unavailable; verify in model |
| **E** | 🆕 Polaris-only | Math constant (Euler's number) |
| **END** | ✅ | No differences noted |
| **ERLANGB** | ❌ | Call center — unavailable in Polaris |
| **ERLANGC** | ❌ | Call center — unavailable in Polaris |
| **EXP** | ✅ | No differences noted |
| **FIND** | ⚠️ | Polaris counts all Unicode chars as length 1 (correct); Classic may differ for multi-byte |
| **FINDITEM** | ⚠️ | Can't use on Time dimension in Polaris (Classic: can). Can't use on Formula/Ratio summary LIs |
| **FIRSTNONBLANK** (aggregation) | ❌ | Aggregation variant unavailable in Polaris |
| **FIRSTNONZERO** | ✅ | No differences noted |
| **FV** | ⚠️ | Financial — Polaris status not explicitly stated in Anapedia; treat as potentially unavailable; verify in model |
| **HALFYEARTODATE** | ⚠️ | Polaris: can use with Half-Year timescale LIs (Classic: can't). Can't use on Formula summary LIs in Polaris |
| **HALFYEARVALUE** | ⚠️ | Polaris: requires Half-year Totals enabled in Model Calendar. Can't use in LI with time scale greater than function |
| **HIERARCHYLEVEL** | 🆕 Polaris-only | Miscellaneous — Classic engine does not have this |
| **IF THEN ELSE** | ✅ | Polaris short-circuits (evaluates matching branch only); Classic evaluates both. Safe for formulas |
| **INPERIOD** | ✅ | No differences noted |
| **IPMT** | ❌ | Financial — unavailable in Polaris |
| **IRR** | ⚠️ | Available in both. Behavioral differences: scaling factor, NaN handling, empty transaction list. Dates variant can't be used if module is dimensioned by Transaction list |
| **ISACTUALVERSION** | ✅ | No differences noted |
| **ISANCESTOR** | ⚠️ | Returns FALSE for top-level item with orphan entity in Polaris |
| **ISBLANK** | ⚠️ | Polaris: text of only carriage returns = blank; Classic: not blank |
| **ISCURRENTVERSION** | ✅ | No differences noted |
| **ISFIRSTOCCURRENCE** | ⚠️ | Available in both. Polaris: supports Time list (Classic: can't). No 50M cell limit. Dimension arg must exactly match a dimension of target LI. **⚠️ Known poor performance in Polaris for high-dimensionality — avoid** |
| **ISNOTBLANK** | ⚠️ | Polaris: text of only carriage returns = blank (same as ISBLANK) |
| **ITEM** | ⚠️ | Polaris: can't use on Ratio summary LIs. Two-argument time variant `ITEM(Time, "Feb 10")` not supported. Time always composite in Polaris |
| **ITEMLEVEL** | 🆕 Polaris-only | Miscellaneous — Classic engine does not have this |
| **LAG** | ⚠️ | Polaris: extra *List* arg enables any list dimension (Classic: time only). Must provide *Non-positive behavior* keyword when using LAG on a list |
| **LASTNONBLANK** (aggregation) | ❌ | Aggregation variant unavailable in Polaris |
| **LEAD** | ⚠️ | Polaris: extra *List* arg enables any list dimension (Classic: time only) |
| **LEFT** | ⚠️ | Polaris handles composite/non-BMP Unicode correctly; Classic may not |
| **LENGTH** | ⚠️ | Same Unicode improvement as LEFT |
| **LN** | ✅ | No differences noted |
| **LOG** | ⚠️ | Polaris: positive infinity as *Base* returns NaN |
| **LOOKUP** | ⚠️ | Polaris: returns aggregate value in non-composite hierarchies (Classic: returns default value). Invalid if mapping LI has unrelated dimension or is dimensioned by line item subset. Can't use in result LI with greater time scale than lookup values |
| **LOWER** | ⚠️ | Polaris: *Locale* argument not supported |
| **MAILTO** | ❌ | Unavailable in Polaris |
| **MAKELINK** | ❌ | Unavailable in Polaris |
| **MAX** (numeric) | ✅ | No differences noted |
| **MAX** (aggregation) | ✅ | No differences noted |
| **MDURATION** | ❌ | Financial — unavailable in Polaris |
| **MID** | ⚠️ | Polaris handles composite/non-BMP Unicode correctly |
| **MIN** (numeric) | ⚠️ | Polaris: blank date vs non-blank → returns non-blank |
| **MIN** (aggregation) | ⚠️ | Same blank date behavior as numeric MIN |
| **MOD** | ⚠️ | `MOD(0, NaN)` returns 0 in Polaris, NaN in Classic |
| **MONTH** | ✅ | No differences noted |
| **MONTHTODATE** | ⚠️ | Polaris: usable with Month timescale LIs (Classic: can't). Can't use on Formula summary LIs in Polaris |
| **MONTHVALUE** | ⚠️ | Polaris: can't use in result LI with time scale greater than function |
| **MOVINGSUM** | ⚠️ | Available in both. Polaris: FIRSTNONBLANK, LASTNONBLANK, TEXTLIST aggregation methods not available |
| **MROUND** | ⚠️ | Polaris: NaN or 0 for decimal places returns 0 (Classic: NaN) |
| **NAME** | ✅ | No differences noted |
| **NEXT** | ⚠️ | Polaris: can't use on Formula summary LIs. Polaris: any compatible dimension (not just time) via *List* arg. For versions use NEXTVERSION |
| **NEXTVERSION** | ✅ | No differences noted |
| **NPER** | ❌ | Financial — unavailable in Polaris |
| **NPV** | ⚠️ | Available in both. Behavioral differences: scaling factor, NaN/empty transaction list handling. Dates variant restricted by Transaction list dimension |
| **OFFSET** | ⚠️ | Polaris: works on any dimension except Versions (Classic: time only). NaN offset returns *Substitute value* (Classic: NaN = 0). **Preferred time-shift function in Polaris** |
| **PARENT** | ⚠️ | Polaris: parent of Years = All Periods. Timescale mismatch in formulas = invalid (Classic: coerced) |
| **PERIOD** | ⚠️ | Polaris: only usable in LI of Type = Time Period; result has same timescale as LI |
| **PI** | 🆕 Polaris-only | Math constant |
| **PMT** | ❌ | Financial — unavailable in Polaris |
| **POST** | ⚠️ | Available in both. Polaris: can't use on Formula summary LIs. Polaris: extra *List* arg enables any dimension (Classic: time only) |
| **POWER** | ⚠️ | `POWER(0,0)` returns 0 in Polaris |
| **PPMT** | ⚠️ | Financial — Polaris status not explicitly stated in Anapedia; treat as potentially unavailable; verify in model |
| **PREVIOUS** | ⚠️ | Polaris: can't use on Formula summary LIs. Polaris: any compatible dimension via *List* arg. For versions use PREVIOUSVERSION |
| **PREVIOUSVERSION** | ✅ | No differences noted |
| **PRICE** | ❌ | Financial — unavailable in Polaris |
| **PROFILE** | ⚠️ | Available in both. Polaris: can't use on Formula summary LIs. *Profile* LI's lookup dimension can't be related to any dimension of target LI. Extra *List* arg enables non-time dimensions |
| **PV** | ❌ | Financial — unavailable in Polaris |
| **QUARTERTODATE** | ⚠️ | Polaris: usable with Quarter timescale LIs (Classic: can't). Can't use on Formula summary LIs in Polaris |
| **QUARTERVALUE** | ⚠️ | Polaris: can't use in result LI with time scale greater than function |
| **RANK** | ⚠️ | Available in both. Polaris: invalid when target or source is dimensioned by line item subset. Blank values rank as 0 (Classic: lowest available rank). Text *Ranking groups* not supported in Polaris. **⚠️ Performance risk on large lists in both engines** |
| **RANKCUMULATE** | ⚠️ | Same LI subset restrictions as RANK. Polaris: blank = 0; no cell limit. **⚠️ Performance risk on large lists** |
| **RATE** | ❌ | Financial — unavailable in Polaris |
| **RIGHT** | ⚠️ | Polaris handles composite/non-BMP Unicode correctly |
| **ROUND** | ⚠️ | Polaris: always EXACT rounding method — *Rounding method* arg not supported. Various NaN/Infinity edge cases differ |
| **SELECT** | ⚠️ | Polaris: reference must be literal (exception: literal time offset like `Time.'Feb 23' + 1`). Avoid hard-coded SELECT in both engines |
| **SIGN** | ✅ | No differences noted |
| **SIN** | 🆕 Polaris-only | Trigonometry |
| **SINH** | 🆕 Polaris-only | Trigonometry |
| **SLA** | ❌ | Call center — unavailable in Polaris |
| **SPREAD** | ⚠️ | Available in both. Polaris: can't use on Formula summary LIs. Extra *List* arg enables non-time dimensions (Classic: time only) |
| **SQRT** | ✅ | No differences noted |
| **START** | ✅ | No differences noted |
| **SUBSTITUTE** | ⚠️ | Polaris: does not match base characters of composite characters (â does not contain a) |
| **SUM** | ✅ | No differences noted (Polaris handles sparse data better but formula syntax identical) |
| **TAN** | 🆕 Polaris-only | Trigonometry |
| **TANH** | 🆕 Polaris-only | Trigonometry |
| **TEXT** | ⚠️ | Polaris: returns "NaN" text for NaN numerical value |
| **TEXTLIST** (aggregation) | ❌ | Unavailable in Polaris |
| **TEXTLIST** (text/calculation) | ❌ | Unavailable in Polaris |
| **TIMESUM** | ⚠️ | Available in both. Polaris: aggregates from date through end of time range (Classic: within range). Can produce different results |
| **TODEGREES** | 🆕 Polaris-only | Trigonometry |
| **TORADIANS** | 🆕 Polaris-only | Trigonometry |
| **TRIM** | ❌ | Unavailable in Polaris |
| **UPPER** | ⚠️ | Polaris: *Locale* argument not supported |
| **VALUE** | ⚠️ | Polaris: can't use non-decimal number representations (e.g., `0x11.11p0`) |
| **WEEKDAY** | ⚠️ | Polaris: decimal *Day offset* rounded to nearest whole number; outside 1–7 returns 0 |
| **WEEKTODATE** | ⚠️ | Polaris: usable with Week timescale LIs (Classic: can't). Can't use on Formula summary LIs in Polaris |
| **WEEKVALUE** | ⚠️ | Polaris: can't use in result LI with time scale greater than function |
| **YEAR** | ✅ | No differences noted |
| **YEARFRAC** | ❌ | Financial — unavailable in Polaris |
| **YEARTODATE** | ⚠️ | Polaris: usable with Year timescale LIs (Classic: can't). Can't use on Formula summary LIs in Polaris |
| **YEARVALUE** | ⚠️ | Polaris: can't use in result LI with time scale greater than function |
| **YIELD** | ❌ | Financial — unavailable in Polaris |

**Legend:** ✅ Available, no issues · ⚠️ Available with differences/caveats · ❌ Not available in Polaris · 🆕 Polaris-only (not in Classic)

---

## Functions NOT Available in Polaris — by Category

### Call Center Functions (all unavailable)
`AGENTS`, `AGENTSB`, `ANSWERTIME`, `ARRIVALRATE`, `AVGDURATION`, `AVGWAIT`, `ERLANGB`, `ERLANGC`, `SLA`

### Financial Functions
**❌ Unavailable:** `COUPDAYBS`, `COUPDAYS`, `COUPDAYSNC`, `COUPNCD`, `COUPNUM`, `COUPPCD`, `CUMIPMT`, `CUMPRINC`, `IPMT`, `MDURATION`, `NPER`, `PMT`, `PRICE`, `PV`, `RATE`, `YEARFRAC`, `YIELD`

**⚠️ Available with behavioral differences:** `IRR`, `NPV`

**⚠️ Polaris status unconfirmed (Anapedia page silent — treat as potentially unavailable):** `DURATION`, `FV`, `PPMT`

### Aggregation Functions
`FIRSTNONBLANK` (aggregation), `LASTNONBLANK` (aggregation), `TEXTLIST` (aggregation and text variants)

Within `MOVINGSUM`: the aggregation methods `FIRSTNONBLANK`, `LASTNONBLANK`, and `TEXTLIST` are not available in Polaris.

### Other Unavailable Functions
`COMPARE`, `MAILTO`, `MAKELINK`, `TRIM`

---

## Critical Polaris Restrictions (Common Pitfalls)

### 1. Formula summary method — incompatible functions
Cannot be used on line items with **Formula** summary method in Polaris:
`CUMULATE`, `DECUMULATE`, `NEXT`, `POST`, `PREVIOUS`, `PROFILE`, `SPREAD`,
`HALFYEARTODATE`, `MONTHTODATE`, `QUARTERTODATE`, `WEEKTODATE`, `YEARTODATE`

Also: `CODE` and `FINDITEM` cannot be used on **Formula or Ratio** summary LIs. `ITEM` cannot be used on **Ratio** summary LIs.

### 2. Line Item Subset restrictions
`RANK` and `RANKCUMULATE`: invalid when target LI or referenced LI is dimensioned by a line item subset.
`LOOKUP`: invalid if the mapping LI is dimensioned by a line item subset.
`ISFIRSTOCCURRENCE`: dimension argument must exactly match a dimension of the target LI (can't use a subset of a list).

### 3. Time scale must not exceed function
Cannot use in a result LI with a time scale **greater** than the function:
`MONTHVALUE`, `QUARTERVALUE`, `WEEKVALUE`, `YEARVALUE`, `HALFYEARVALUE`
`LOOKUP` (time variant)

### 4. ISFIRSTOCCURRENCE — performance warning
**Avoid in Polaris for high-dimensionality models.** Known poor performance. Pre-filter population before applying.

### 5. SELECT must be literal in Polaris
`SELECT` references must be literal. Dynamic expressions are invalid.
Exception: `Time.'Feb 23' + 1` (literal offset from current time period).

### 6. OFFSET works across dimensions in Polaris
In Polaris, `OFFSET` works on **any dimension except Versions** (Classic: time only).
This is the **preferred time-shift function** in Polaris.

### 7. No timescale coercion in Polaris
In Polaris, if a formula returns a result at a different timescale than the target LI, the formula is **invalid** — it is not silently coerced as in Classic. Cross-timescale patterns using `PARENT` or time-period references require careful matching.

### 8. LOOKUP dimension alignment
In Polaris, a LOOKUP is invalid if:
- The target LI cannot reference the mapping LI
- The mapping LI has a dimension unrelated to the target LI's dimensions

---

## Functions Only in Polaris (🆕 — do not use in Classic models)

`ACOS`, `ACOSH`, `ASIN`, `ASINH`, `ATAN`, `ATANH`, `COS`, `COSH`, `E`, `HIERARCHYLEVEL`, `ITEMLEVEL`, `PI`, `SIN`, `SINH`, `TAN`, `TANH`, `TODEGREES`, `TORADIANS`

---

## Corrections to `classic-vs-polaris.md`

The existing `classic-vs-polaris.md` in this references folder contains inaccuracies sourced from incomplete knowledge. **This file takes precedence.** Key corrections:

| Claim in classic-vs-polaris.md | Actual (per Anapedia source docs) |
|---|---|
| `POST` listed as "removed in Polaris" / Classic-only | ❌ Wrong. POST **is available in Polaris** with an extra *List* arg. Restriction: can't use on Formula summary LIs |
| `PREVIOUS`/`NEXT` listed as "removed in Polaris" | ❌ Wrong. Both available in Polaris with expanded dimension support. Can't use on Formula summary LIs |
| `COLLECT` listed as Polaris-only hierarchy aggregation | ❌ Wrong. `COLLECT()` is a line item subset function available in **both engines**. No separate hierarchy-COLLECT function exists in Anapedia |
| `CUMULATE` listed as Polaris-only | ❌ Wrong. `CUMULATE` is available in **both Classic and Polaris** (with behavioral differences) |
| `DISTRIBUTE` listed as Polaris-only | ⚠️ No Anapedia doc found in `<SHARED_ROOT>/raw/docs` — existence unconfirmed. Do not suggest until verified |

---

*Last updated: 2026-06-09. Source: `<SHARED_ROOT>/raw/docs/*Anapedia*.md`*
