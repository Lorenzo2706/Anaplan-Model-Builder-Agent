# Per-domain research agent specs

The canonical outline (see `SKILL.md`) splits cleanly into 6 independent
research domains - independent in the sense that no domain needs to read
another domain's output to do its own job, which is exactly what makes them
safe to hand to 6 concurrent background agents instead of one sequential
agent working through the whole outline. Each spec below is a template for
that domain's agent prompt: copy it, fill in `{MODEL}` and the bracketed
notes with facts about the actual model being documented, and dispatch.

**Every prompt below ends the same way for a reason that matters mechanically,
not just stylistically:** the deliverable's headings must carry the *exact*
numeric prefix from the canonical outline (e.g. `### 2.1.1 Load`, not just
`### Load`). `scripts/md_to_sections.py` derives each heading's real level
from that numeric prefix, because agents left to their own devices pick
wildly inconsistent heading depths relative to each other (one agent's `##`
is another's chapter, another's subsection). Numeric prefixes are the one
thing every agent can get right independently, without needing to coordinate
with the other 5. Sub-headings that are genuinely unnumbered because they're
model-specific (a process-flow stage name, a UX category) don't need a
prefix - the parser nests them one level under whatever numbered heading
came before, which is exactly where they belong.

Adjust the specifics of the STYLE MODEL blocks below if the user gave you a
different reference document to mirror this time - the *shape*
(what gets a table vs. prose, what the table columns are) is what matters,
not the literal content of the original reference doc this skill's default
was extracted from. Re-derive the shape from whatever reference doc is in
play.

---

## 1. Introduction + Appendix A (Glossary)

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/index.md` - architecture overview, engine, roles summary
- Any raw CSVs needed to firm up specific facts (`<CUSTOMER_ROOT>/raw/models/{MODEL}/*.csv`)

STYLE MODEL - mirror this shape, not this wording:

  1. Introduction
  1.1 Purpose
    2-3 prose paragraphs: what the model/app supports, why it exists.
    "The {MODEL} model and app have been created to:" + a bulleted list of
    3-5 concrete purposes.
    Closing paragraph on what the consolidated result enables downstream.

  1.2 Scope
    Prose stating what is explicitly OUT of scope / handled elsewhere -
    "This document only describes the {MODEL} model / functionality."
    Paragraph stating the time/version horizon covered.
    Paragraph stating current-version limitations, if any are documented.

  1.3 Terminology
    "A glossary on all abbreviations used in this document is added in
    Appendix A."
    Markdown table: | Term | Description | - one row per key domain/business
    concept (NOT abbreviations - those go in the glossary), each description
    1-3 sentences in plain functional language.

  Appendix A - Glossary
    Markdown table: | Abbreviation | Full term | - every abbreviation used
    anywhere in the full document (you'll need to guess at ones other
    agents will use too, e.g. module-prefix abbreviations like the model's
    own DISCO-style section codes - list generously).

YOUR DELIVERABLE - use these exact headings (the numeric prefixes drive
document structure, do not omit or renumber them):

## 1. Introduction
### 1.1 Purpose
### 1.2 Scope
### 1.3 Terminology (markdown pipe table: | Term | Description |)

# Appendix A - Glossary (markdown pipe table: | Abbreviation | Full term |)

RULES:
- Do not fabricate. Insert `[PLACEHOLDER: <what's missing>]` for anything
  the sources don't confirm - never invent a purpose statement, a scope
  boundary, or a term's definition.
- Return your full markdown deliverable as your final message text (do not
  write files).
```

---

## 2. Data Flows + Administration

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/index.md` - calculation-flow diagram, roles summary
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/roles.md`, if it exists - full roles/access matrix.
  Many models don't have a dedicated roles page - that's normal, not a gap
  to work around silently. If it's missing, check whether `index.md` has a
  roles summary section instead (several models fold this into the main
  page rather than splitting it out); if neither exists,
  `[PLACEHOLDER: role/access matrix not documented]` rather than guessing.
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/versions.md` (or equivalent) - versioning mechanism
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/actions.md` (or equivalent) - atomic actions, for
  admin/maintenance actions

STYLE MODEL - mirror this shape:

  2. Data Flows
  2.1 Process Flow
    One-sentence summary of what the process flow covers end to end.

    2.1.1 [first stage - e.g. Load]
      Prose on what happens; a source/data/grain table if multiple sources
      feed this stage; note any known data-quality/consolidation nuance.

    2.1.2 [second stage - e.g. Input & Review]
      Prose on what can be entered/reviewed and by whom; note any
      carve-outs (some segments locked to a prior load, "as-is" data).
      Use unnumbered H4 sub-splits only when the stage has genuinely
      distinct sub-flows (e.g. two different entry grains for two
      different segments) - don't force a split that isn't real.
      A granularity/overwrite table when review rights differ by segment.

    2.1.3 [third stage - e.g. Calculate & Report]
      Prose on what gets calculated/compared and how; a report-module
      table if there's a report layer.

  2.2 Administration
    Sub-topics as unnumbered H3/H4 (adapt to what the model actually has -
    don't force the reference example's exact 3 sub-topics below if the
    model's admin surface is shaped differently):
    - Version/scenario management - how it's set up, any manual-linkage
      caveat
    - List/hierarchy admin scoping - who can add/delete items, which lists
    - User/Role management - how roles+users are assigned/maintained, and
      a role-access summary table

YOUR DELIVERABLE - determine {MODEL}'s actual process-flow stage names from
its wiki (check the calculation-flow diagram / DISCO module sections) rather
than assuming the reference example's names below - use whatever 2-4 stages
the model's own module structure actually groups into:

## 2. Data Flows
### 2.1 Process Flow
#### 2.1.1 [stage name grounded in {MODEL}'s actual load/input/calc/report grouping]
#### 2.1.2 [...]
#### 2.1.3 [...]
### 2.2 Administration
(with whatever unnumbered sub-topics fit what {MODEL} actually documents)

RULES:
- If {MODEL} has no equivalent to something the style model documents (e.g.
  no "unlock with reason" overwrite mechanic), say so explicitly or insert
  `[PLACEHOLDER: ...]` - don't silently omit the gap.
- Use markdown pipe tables for tabular content.
- Return your full markdown deliverable as your final message text (do not
  write files).
```

---

## 3. Guiding Design Principles + Lists

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/index.md` - architecture-at-a-glance, lists summary
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/lists.md` (or equivalent) - full list catalog
- `<CUSTOMER_ROOT>/raw/models/{MODEL}/General Lists.csv` - exact item counts if needed

STYLE MODEL - mirror this shape:

  3.1 Guiding Design Principles
    A short bulleted list (4-7 items) of structural/architectural choices
    the model makes and WHY - e.g. a hierarchy pattern chosen for a
    specific data-shape reason, a naming discipline, an engine choice
    (Polaris vs Classic) made to handle a specific scale problem.
    Most models won't have a formal design-principles document - that's
    normal, not a gap. Say so with a placeholder, then still list the
    principles you can genuinely infer from the model's actual structure,
    clearly labeled as inferred rather than pretending they're documented.

  3.2 Lists
    "The lists used in the {MODEL} model can be grouped into key
    planning/model lists, versioning lists, and other (technical) lists."

    3.2.1 Key planning/model lists
      Table: | List | Maintenance | - how each key hierarchy/planning list
      is populated (import source + process name, or "manual").
      Prose explaining parent-child relationships, allocation purpose,
      any "not marked production" or similar caveats.

    3.2.2 Versioning lists
      Table: | List | Maintenance |
      Prose on how version lists relate (which is the master/consolidation
      version others map into), and any referential-integrity caveat.

    3.2.3 Other lists
      Table: | List | Purpose |
      One closing sentence on maintenance (manual vs. import/export-driven).

YOUR DELIVERABLE:

## 3.1 Guiding Design Principles
## 3.2 Lists
### 3.2.1 Key planning/model lists
### 3.2.2 Versioning lists
### 3.2.3 Other lists

RULES:
- Use exact list names/counts from the wiki - don't guess.
- `[PLACEHOLDER: maintenance process not documented]` where the source
  doesn't say how a list is populated - don't invent an import mechanism.
- Return your full markdown deliverable as your final message text (do not
  write files).
```

---

## 4. Modules catalog

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/index.md` - architecture-at-a-glance table
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/modules.md` (or equivalent) - full module catalog
- `<CUSTOMER_ROOT>/raw/models/{MODEL}/Modules.csv` - exact names/counts if needed

STYLE MODEL - mirror this shape:

  3.3 Modules
    "For the architectural perspective, Anaplan's DISCO (Data, Input,
    System, Calculation and Output) format is used."

    3.3.1 Data
      Table: | Module | Purpose | - every data-section module, one crisp
      sentence each. Prose on any consolidation modules and what version
      they're stored against.

    3.3.1.1 Input
      Table: | Module | Purpose |

    3.3.1.2 System
      Table: | Module | Purpose | - if the model has a repetitive family
      (e.g. one system module per hierarchy level), it's fine to compress
      them into one table row describing the pattern, as long as every
      individual module name is still listed.

    3.3.1.3 Calculation
      Table: | Module | Purpose | - calculation modules usually deserve
      1-3 sentences each rather than one-liners, since this is where the
      model's actual logic lives.

    3.3.1.4 Output
      Table: | Module | Purpose |
      Closing note on any module-type categories not individually tabled.

YOUR DELIVERABLE - use the model's actual DISCO section prefixes/counts,
don't assume {MODEL} has the same prefix letters as any other model:

## 3.3 Modules
### 3.3.1 Data
#### 3.3.1.1 Input
#### 3.3.1.2 System
#### 3.3.1.3 Calculation
#### 3.3.1.4 Output

RULES:
- Use exact module names/prefixes from the wiki - never invent one.
- If a module's documented purpose is thin, write the best faithful
  one-liner from what IS known rather than leaving the cell blank; use
  `[PLACEHOLDER: purpose not detailed in source]` only when truly nothing
  is known.
- If the wiki flags a suspected formula bug or design flaw anywhere in the
  calculation layer, carry it forward as a callout after the relevant
  table - this is exactly the kind of caveat model documentation exists to
  surface, not smooth over.
- Return your full markdown deliverable as your final message text (do not
  write files).
```

---

## 5. Integrations

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/imports.md` (or equivalent) - import data sources
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/actions.md` (or equivalent) - full actions catalog
- `<CUSTOMER_ROOT>/raw/models/{MODEL}/Source Models.csv`, `Actions.csv` if more detail is
  needed

STYLE MODEL - mirror this shape:

  3.4 Integrations
    3.4.1 Import
      "Within the {MODEL} model there are imports to populate structural
      lists and data modules."
      Table: | List | Source | Process | - one row per list-populating
      import.
      Table: | Module | Source | Process | - one row per data-module
      import.
      Closing note on anything populated by formula instead of import, and
      any bulk-validation-refresh action.

    3.4.2 Other update processes
      Table: | Purpose | Process | - non-import maintenance actions.

    3.4.3 Export
      Table: | Purpose | Process |
      Closing prose identifying the model's MAIN/business export (as
      opposed to technical/working-file exports) and which downstream
      model or process consumes it.

YOUR DELIVERABLE:

## 3.4 Integrations
### 3.4.1 Import
### 3.4.2 Other update processes
### 3.4.3 Export

RULES:
- Use exact source-model and action names - never invent a process name.
- Preserve uncertainty the wiki already flags (e.g. "unconfirmed whether
  this import has actually executed") rather than smoothing it into a
  confident-sounding sentence.
- Return your full markdown deliverable as your final message text (do not
  write files).
```

---

## 6. UX + Appendix B (Model Scheme)

```
You are drafting part of a Word documentation deliverable for the "{MODEL}"
Anaplan model. Vault root: `<vault path>`.

[If a supplementary UX source was requested but turned out to be
inaccessible - e.g. a Miro board blocked by an org policy, a UX export that
doesn't exist yet - say so explicitly here and instruct the agent not to
retry it, just to work from what's available and placeholder the rest.]

READ FIRST:
- `<CUSTOMER_ROOT>/wiki/models/{MODEL}/index.md` - roles summary, architecture table
- `<CUSTOMER_ROOT>/raw/models/{MODEL}/Actions.csv` - action names often hint at
  dashboard/page groupings
- Any other {MODEL} wiki pages mentioning UX/dashboards/pages

STYLE MODEL - mirror this shape:

  UX
    "The '{MODEL}' App is made up of the following categories:" + bulleted
    category list.
    "The purpose of the dashboards within the categories is described
    below."
    One table per category: | Purpose | Dashboard | - Purpose is one
    sentence, Dashboard is the dashboard's name/number if confirmed.

  Appendix B - Model Scheme
    "Below the {MODEL} model scheme on module level and dimensionality
    information:" + (ideally) a diagram image.
    A prose walkthrough of the calculation flow end to end.
    The architecture-at-a-glance table (prefix/section/functional
    area/count).

YOUR DELIVERABLE:

## 3.5 UX
[one H3 per category, unnumbered - these are model-specific names]

# Appendix B - Model Scheme

RULES:
- Be explicit and honest about what's confirmed vs. inferred - this domain
  usually has the least hard data of the whole document (dashboard/page
  structure is rarely captured in a CSV export), so precision about
  confidence level matters more than completeness. If there's no UX export
  and no way to confirm dashboard groupings, infer them from module/action
  naming patterns and label every single one as inferred, or
  `[PLACEHOLDER: ...]` if you can't even infer reasonably.
- If no diagram image is available for Appendix B, insert
  `[PLACEHOLDER: visual model-scheme diagram image - none available]`
  rather than describing a diagram that doesn't exist.
- Return your full markdown deliverable as your final message text (do not
  write files).
```
