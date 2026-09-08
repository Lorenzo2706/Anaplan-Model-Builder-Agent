---
name: anaplan-model-documentation
description: >
  Generate a comprehensive, structured Word documentation deliverable for an
  Anaplan model in this vault - Introduction, Data Flows, Technical Set-up
  (Lists/Modules/Integrations/UX), and Appendices (Glossary, Model Scheme) -
  by dispatching parallel background research agents against the model's
  wiki pages and raw CSV export, then assembling the results into a
  validated .docx with explicit placeholders for anything unconfirmed. Use
  this skill whenever the user asks to document, draft documentation for,
  write up, or create a Word/docx deliverable for any Anaplan model in this
  vault (whether already ingested or newly added) - even if they don't mention
  chapters, DISCO, or Word explicitly. Also trigger when they ask for
  onboarding material, a model handbook, a build-spec write-up, or want an
  existing model doc "redrafted"/"updated" to match a reference document's
  house style. This is heavy-duty (it fans out 6 background agents plus a
  docx build) - don't attempt it as a single inline pass.
---

# Anaplan Model Documentation

**Before anything else:** resolve `<CUSTOMER_ROOT>` for the model in question via `customers/registry.md`, per `AGENTS.md` § Client Resolution. All paths below are relative to that resolved root.

Produces a full Word documentation deliverable for one Anaplan model,
following a fixed-but-flexible chapter structure. "Fixed" means the top-level
chapter numbering and titles are the same for every model documented with
this skill (so two model docs in this vault always look and navigate the
same way); "flexible" means the *content inside* certain sections - process-
flow stage names, UX category names, whether a Guiding Design Principles
section exists at all - adapts to what the specific model actually is.

This is deliberately heavy machinery: a real model has enough independent
facets (lists, five DISCO module categories, integrations, roles, UX) that
one agent researching all of it sequentially either runs out of context or
produces a shallow pass on the later sections. Splitting the outline into 6
independent research domains and running them as concurrent background
agents (see `superpowers:dispatching-parallel-agents` if that skill is
available) gets a deeper result in less wall-clock time, because none of
the 6 domains needs another domain's findings to do its own job.

## The canonical outline

```
1. Introduction                                    [fixed]
   1.1 Purpose
   1.2 Scope
   1.3 Terminology

2. Data Flows                                      [fixed]
   2.1 Process Flow
       2.1.x [model-specific process stages]        [flexible]
   2.2 Administration                                [fixed]

3. Technical Set-up                                 [fixed]
   3.1 Guiding Design Principles                     [flexible - omit or
                                                       clearly mark inferred
                                                       if the model has no
                                                       real design rationale
                                                       documented]
   3.2 Lists
       3.2.1 Key planning/model lists
       3.2.2 Versioning lists
       3.2.3 Other lists
   3.3 Modules
       3.3.1 Data
             3.3.1.1 Input
             3.3.1.2 System
             3.3.1.3 Calculation
             3.3.1.4 Output
   3.4 Integrations
       3.4.1 Import
       3.4.2 Other update processes
       3.4.3 Export
   3.5 UX
       3.5.x [model-specific screen/page groupings]  [flexible]

Appendix A – Glossary                                [fixed]
Appendix B – Model Scheme                            [fixed]
```

If the user gives you a different outline explicitly, use theirs instead -
this one is the sensible default this vault has converged on (it's the house
style prior model docs in this vault have used, and that others were
redrafted to match), not a hard requirement. Whatever outline you use, keep
every heading's numeric
prefix intact in the research agents' output - see Step 2, it's load-bearing
for the assembly step, not cosmetic.

## Step 0 - Scope and style discovery

Before dispatching anything, pin down three things:

1. **Which model, and is it in the wiki yet?** Check `<CUSTOMER_ROOT>/wiki/models/<Model>/`
   for an existing `index.md`. If it doesn't exist, this skill can still
   work directly from `<CUSTOMER_ROOT>/raw/models/<Model>/*.csv`, but the output will be
   thinner - tell the user the `wiki-data-ingestion` skill would give richer
   source material first, and let them decide whether to ingest first or
   proceed straight to documentation.
2. **Engine.** Polaris vs. Classic changes how you should describe
   sparsity/LOOKUP/aggregation behavior in the Modules section. Check
   `AGENTS.md`'s model list or the wiki page; if genuinely unknown, flag it
   rather than guessing (see `anaplan-formula-agent`'s engine-determination
   gate for the same principle).
3. **House style.** Did the user provide (or reference) an example document
   to mirror the structure/formatting of? If yes, read
   `references/docx-style-guide.md` for how to extract its color/table/font
   conventions into a style-override JSON. If no, use the bundled default
   style - it's already the accumulated house style of this vault's prior
   model docs, not an arbitrary placeholder.

## Step 1 - Dispatch the 6 research agents

Read `references/section-specs.md` - it has a ready-to-fill prompt template
for each of the 6 domains below. Fill in `{MODEL}` and the specific wiki/raw
paths for the model in question, then dispatch all 6 as background
`general-purpose` agents in the same turn (so they run concurrently, not
sequentially):

1. Introduction + Appendix A (Glossary)
2. Data Flows + Administration
3. Guiding Design Principles + Lists
4. Modules catalog
5. Integrations
6. UX + Appendix B (Model Scheme)

Every prompt carries the same two non-negotiable instructions, because the
assembly step in Step 2 depends on them:

- **Placeholder policy**: insert `[PLACEHOLDER: <what's missing>]` for
  anything the sources don't confirm. A documentation deliverable that
  quietly papers over a gap is worse than useless - it looks authoritative
  while being wrong. Every research prompt in `section-specs.md` already
  says this; don't relax it even under time pressure.
- **Heading numbering**: every heading in the returned markdown must carry
  its exact numeric prefix from the canonical outline (e.g. `### 2.1.1
  Load`, not `### Load`). Unnumbered sub-headings are fine *only* for
  genuinely model-specific names nested under a numbered heading (a
  process-flow stage, a UX category) - the parser in Step 2 nests those
  automatically one level deeper than the last numbered heading it saw.

Track the 6 dispatches with `TaskCreate`/`TaskUpdate` and wait for their
task-notifications rather than polling - this can take several minutes per
agent since each one is reading multiple wiki pages and CSVs.

## Step 2 - Turn the 6 markdown deliverables into a docx

1. Save each agent's returned markdown to a file, named so their filesystem
   order matches the canonical outline order (e.g. `sec1_intro.md`,
   `sec2_dataflows.md`, ... `sec6_ux_scheme.md`) - the parser processes
   files in the order given and that order becomes the document order.
2. Run the bundled parser:
   ```bash
   python .agents/skills/anaplan-model-documentation/scripts/md_to_sections.py \
     <output>/sections.json sec1_intro.md sec2_dataflows.md sec3_lists.md \
     sec4_modules.md sec5_integrations.md sec6_ux_scheme.md
   ```
   This reads each file's own heading numbering to derive the TRUE absolute
   heading level (see the comment at the top of the script for why raw
   markdown `#`/`##`/`###` depth can't be trusted directly - the 6 agents
   pick inconsistent depths independently of each other). It prints a
   heading/level/block-count summary - skim it for anything that looks
   wrong (a heading at the wrong level, a section with 0 blocks that should
   have content) before moving on.
3. Build the docx:
   ```bash
   NODE_PATH="$(npm root -g)" node .agents/skills/anaplan-model-documentation/scripts/build_docx.js \
     <output>/sections.json <output>/<Model>-Model-Documentation.docx \
     "<Model> — <one-line model description>" "Model documentation" \
     [<output>/style-override.json]
   ```
   The `NODE_PATH` prefix is only needed if `docx` isn't resolvable from the
   working directory (it usually is only installed globally, not per
   project) - try without it first, add it if `node` complains it can't
   find the module.

If a step in this pipeline errors on an unexpected markdown shape (e.g. a
table with a ragged number of columns, a nested list), fix the specific
markdown file rather than patching the parser for one-off input - the
parser is intentionally simple, and research agents occasionally produce
malformed tables that are faster to hand-fix than to generalize for.

**Known gotcha:** research-agent output sometimes comes back with `&`, `>`,
`<` HTML-escaped (`&amp;`, `&gt;`, `&lt;`) - an artifact of the
message-passing layer, not something the agent chose to do. `md_to_sections.py`
already unescapes these before doing any structural parsing, so callout
markers (`> [!note]`) and table rows still get detected correctly even when
escaped - you don't need to hand-fix this yourself, but if you ever see a
`> [!note]` block render as a plain paragraph instead of a styled callout,
this is the first thing to check.

## Step 3 - Validate

Neither `python-docx`, LibreOffice, nor `pandoc` are guaranteed to be
installed, and the `docx` skill's own `validate.py` has been observed to
crash on Windows consoles over a Unicode-vs-cp1252 mismatch that isn't a
real defect in the file. Use the bundled validator instead, which checks
zip integrity and XML well-formedness directly without that failure mode:

```bash
python .agents/skills/anaplan-model-documentation/scripts/validate_docx.py <path-to.docx>
```

It also prints heading/table/placeholder counts - sanity-check them against
what you'd expect from the 6 markdown files you fed in (roughly count the
`|`-tables you can see in each), not against a fixed number: a model with
100+ modules across many DISCO prefixes will legitimately produce far more
tables than a small one, so don't second-guess a high count just because
it's high. What's actually worth investigating is a count that's much
*lower* than the source markdown suggests (a sign a table got misparsed) or
a table/heading count of 0 (a sign the whole pipeline silently produced an
empty document). Recommend the user do a quick open-in-Word pass regardless
- structural validation confirms the file isn't corrupt, not that every
table reads well.

## Step 4 - Deliver

- Save to `<CUSTOMER_ROOT>/analyses/<Model>-Model-Documentation.docx` - never into `<CUSTOMER_ROOT>/wiki/`,
  per this vault's convention that non-wiki outputs live in `<CUSTOMER_ROOT>/analyses/`.
- If that filename is locked (the user has it open in Word - `cp`/`mv` will
  fail with a "resource busy" style error), don't force it: save alongside
  with a `-v2` suffix (or next available number) and tell the user which
  file is which, rather than silently overwriting or failing outright.
- Add or update a "Key cross-references" pointer in
  `<CUSTOMER_ROOT>/wiki/models/<Model>/index.md` linking to the deliverable, so future wiki
  queries about this model surface the doc.
- Report a summary in chat: chapters produced, notable tables/counts, every
  placeholder inserted (list them, don't just say "some placeholders
  exist" - the user needs the list to go chase down real answers), and any
  caveats the research agents surfaced (suspected formula bugs, unconfirmed
  renames, blocked data sources). This is the same standard
  `anaplan-model-optimizer` holds itself to for its own findings: present
  results in the conversation, not just a pointer to a saved file.

## Bundled resources

- `scripts/md_to_sections.py` - markdown → structured JSON block tree,
  with numbering-based heading-level inference
- `scripts/build_docx.js` - JSON block tree → validated .docx via `docx-js`,
  with an overridable style (see `references/docx-style-guide.md`)
- `scripts/validate_docx.py` - zip/XML integrity check without relying on
  LibreOffice/pandoc/python-docx
- `references/section-specs.md` - the 6 per-domain research-agent prompt
  templates
- `references/docx-style-guide.md` - default style tokens and how to mirror
  a different reference document's house style instead
