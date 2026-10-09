# Operation Log

Append-only. Newest entries at the bottom.

## [2026-08-31] lint | post-restructure wiki-lint pass (verification step of the single→multi-customer restructure)
Scanned `anaplan/` (481 md files) plus cross-domain link targets. Fixes applied in this domain:
- `index.md`: corrected stale "8 standalone patterns" → "7" (a customer-specific naming-convention page had been moved out to that customer's own `wiki/patterns/` earlier in this restructure; `wiki/patterns/index.md`'s own "7 standalone pages" count was already correct — the two pages had drifted apart).
- `wiki/patterns/index.md`: reworded the Number Format Standard summary row from naming a specific customer model to "links to one customer model's audit history" — removes a customer-identifying reference from tracked/public content (Minor per the brief, page body itself was already generic).
- `wiki/functions/index.md` and `wiki/sources/2026-05-02-anapedia-all-functions.md`: fixed two `[[wiki/functions/categories]]` folder-links (Obsidian does not auto-resolve a folder link to its `index.md`) → now point at `wiki/functions/categories/index`.
- `wiki/patterns/data-loading-best-practices.md`: removed two reverse cross-domain references (a body link and a `sources:` frontmatter entry) that pointed into a customer domain's `wiki/sources/...` and `raw/docs/...` — this generic/public pattern page would have shipped a dangling, customer-identifying pointer to template users with no customer tree at all. Replaced with generic, non-linking prose; the page's own guidance content is unchanged.

Verified clean (no fix needed):
- All forward cross-domain links from customer-domain model/source pages into `anaplan/wiki/patterns/*` and `anaplan/wiki/functions/categories/*` (disco, planual chapters, ragged-hierarchy, version-as-list, data-loading-best-practices, circular-reference, number-format-standard) resolve correctly.
- Concept/function/pattern page counts elsewhere in `index.md` and sub-indexes cross-checked against actual file counts — all correct (145 functions/10 categories, 22 core concepts + 2 flat pages, 15-chapter Demand & Inventory app with 4 "-detailed" companions = 19 files, Planual 8 chapters, The Anaplan Way 7 pages).

Flagged, not fixed (needs a human/data decision, no fabrication):
- `wiki/functions/index.md` row for **ACOSH**: links to `raw/docs/ACOSH  Anapedia` which does not exist anywhere in the vault, even though every sibling hyperbolic-function raw doc (ASINH, ATANH, COSH, SINH, TANH) does. Looks like the ACOSH Anapedia page was never actually clipped/ingested despite being listed. Needs either the missing raw doc ingested or the dead raw-source link removed from that row.

## [2026-08-31] ingest | Anapedia clippings batch (10 function docs) from Clippings/
Source: 11 files landed in `Clippings/` (10 Anapedia function pages + 1 unrelated GitHub Copilot article, logged separately under `other-topics/log.md`).

Discovered mid-ingest that 8 of the 10 Anapedia clippings (AGENTS, AGENTSB, CUMIPMT, DECUMULATE, ERLANGB, ERLANGC, HIERARCHYLEVEL, MDURATION) already existed in `raw/docs/` from the 2026-05-02 bulk ingest, with revised content (Anaplan updated the underlying help pages — added Classic/Polaris behavior tables, reworded argument descriptions, expanded examples; no syntax or semantic changes). Confirmed with user to overwrite the 8 raw docs in place (consistent with how this vault already handles CSV re-uploads) and touch wiki only where descriptions changed.

Created:
- wiki/sources/2026-08-31-anapedia-variance-aggregation.md (first-time: VARP, VARS)
- wiki/sources/2026-08-31-anapedia-call-center-refresh.md (AGENTS, AGENTSB, ERLANGB, ERLANGC)
- wiki/sources/2026-08-31-anapedia-financial-refresh.md (CUMIPMT, MDURATION)
- wiki/sources/2026-08-31-anapedia-decumulate-refresh.md (DECUMULATE)
- wiki/sources/2026-08-31-anapedia-hierarchylevel-refresh.md (HIERARCHYLEVEL)

Updated:
- raw/docs/AGENTS  Anapedia.md, AGENTSB  Anapedia.md, CUMIPMT  Anapedia.md, DECUMULATE  Anapedia.md, ERLANGB  Anapedia.md, ERLANGC  Anapedia.md, HIERARCHYLEVEL  Anapedia.md, MDURATION  Anapedia.md — overwritten in place with refreshed Anapedia content
- raw/docs/VARP aggregation function.md, VARS aggregation function.md — new
- wiki/functions/index.md — added VARP/VARS rows, function count 145 → 147, sources frontmatter extended
- wiki/functions/categories/aggregation.md — added VARP/VARS to Members and When-to-use table
- wiki/functions/categories/index.md, index.md — function count 145 → 147
- wiki/sources/index.md — new 2026-08 section, 5 entries

## [2026-09-09] ingest | Anaplan Integration API v2.0 — Anapedia clipping batch (70 files) from Clippings/
Source: 70 Anapedia web clippings landed in `Clippings/` (Integration API v2.0 documentation set — getting started, object model, system behavior, resource structure, request/response formats, auth/permissions, retry strategy, workspaces/models incl. lifecycle, model calendar/versions, lists, modules/views/line items, cell data read/write, large-volume reads, file transfer, users). All generic/customer-agnostic per user instruction — moved to `raw/docs/` (Clippings/ is gitignored, files were untracked). First-time ingest; no prior Integration API content existed in this wiki.

Created:
- wiki/concepts/integration-api/ — new sub-collection: index.md + 10 pages (01_overview, 02_authentication-and-permissions, 03_reliability-retries-rate-limits, 04_workspaces-and-models, 05_model-calendar-and-versions, 06_lists-and-dimension-items, 07_modules-views-line-items, 08_cell-data-read-write, 09_bulk-and-large-volume-data, 10_users)
- wiki/sources/2026-09-09-anaplan-integration-api.md

Updated:
- raw/docs/ — 70 clipping files moved in from Clippings/
- wiki/concepts/index.md — added Integration API sub-collection line
- index.md (anaplan) — Concepts summary line updated
- wiki/sources/index.md — new 2026-09 section

Design note: per the function-pages policy precedent, did not create one wiki page per raw doc (several raw docs are one-paragraph stub/intro pages with no content beyond a topic sentence). Grouped into 10 workflow-oriented pages instead, each citing every raw doc it draws from.

## [2026-09-09] ingest | Anapedia — Breakback (dedicated page) from Clippings/
Source: 1 Anapedia clipping (`Breakback  Anapedia.md`) — a re-clip of a page already tracked in git from an earlier scraper pass but never actually ingested into the wiki. Moved to `raw/docs/` alongside the Integration API batch above (same domain, unrelated topic — processed as a separate batch per Phase 1 grouping).

Breakback was already covered as a section in wiki/concepts/anaplan concepts/14_modules.md (sourced from `raw/docs/Configure modules.md`). Per "prefer updating an existing page over creating a near-duplicate," enriched that section instead of creating a new page: added the Hold feature, the simple-hierarchy/time-dimension-only restriction, the 1,000,000-cell warning threshold, and the change-history behavior.

Created:
- wiki/sources/2026-09-09-anapedia-breakback.md

Updated:
- wiki/concepts/anaplan concepts/14_modules.md — Breakback section extended; sources: frontmatter gained raw/docs/Breakback  Anapedia.md; updated date bumped
- wiki/sources/index.md — added to the new 2026-09 section

## [2026-09-10] lint | Wiki sanity check
Scanned the shared Anaplan index cascade and all 114 non-raw Markdown files, with cross-domain targets resolved.

Issues found and fixed:
1. `wiki/concepts/index.md` still described two sub-collections after the Integration API collection was added; corrected it to three sub-collections and two flat pages.
2. Restored the missing KWS and Stedin entries in the vault-root customer router.

Issues flagged for manual review:
- `wiki/functions/index.md` still links ACOSH to missing raw clipping `raw/docs/ACOSH  Anapedia.md`; ingest the source or remove the raw-source link.

Verified clean: page/function/category counts, orphan-page coverage, companion-file documentation, and shared-link resolution. No unresolved Anaplan-domain contradictions found beyond the already-flagged missing ACOSH source.

## [2026-09-11] ingest | Field notes — Hierarchy load from file (DataHub → Spoke)
Source: dictated by Lorenzo Giori (field experience, not a clipping) — no existing wiki page covered this specific unique-key vs. composite-key/numbered-list branch, or the per-level `ISFIRSTOCCURRENCE` save-view technique for hierarchy sources. Mid-ingest, user corrected an over-generalization: a numbered load list is only needed as a workaround when the file has no single unique key (composite-properties key); a file with a unique key uses a normal named list, whether loading straight to the Spoke model or staging through a DataHub load list.

Created:
- raw/docs/2026-09-11-hierarchy-load-from-file-fieldnotes.md
- wiki/patterns/hierarchy-load-from-file.md ("Building a Hierarchy from an Uploaded File (DataHub → Spoke)")
- wiki/sources/2026-09-11-hierarchy-load-from-file.md

Updated:
- wiki/patterns/data-loading-best-practices.md — cross-link added under "Without a unique key" to the new hierarchy-specific page
- wiki/patterns/index.md — new row, standalone pattern count 7 → 8
- index.md (anaplan) — Patterns summary line updated
- wiki/sources/index.md — new 2026-09 entry

Also produced a standalone step-by-step Markdown "manual" (delivered directly to the user, not stored in the wiki — `anaplan/` has no `analyses/` folder for non-wiki deliverables).

No issues flagged — wiki is consistent.

## [2026-09-29] ingest | Anapedia Workflow & Workflow Advanced (22 clippings)
Moved 22 files from `Clippings/` to `raw/docs/`. Created: wiki/sources/2026-09-29-anapedia-workflow.md; wiki/concepts/workflow/ (index + 01_overview, 02_task-types-and-templates, 03_workflow-advanced, 04_notifications-and-feedback, 05_schedules-and-monitoring).
Updated: wiki/concepts/index.md (new sub-collection), wiki/sources/index.md (new 2026-09 entry).
Gap: no "Create a group task" page in the batch.
