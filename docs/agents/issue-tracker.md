# Issue tracker: Local Markdown

Read this file before creating, fetching, or updating engineering tickets or specs.

## Location

- Customer work: `customers/<Customer>/analyses/<feature-slug>/` (gitignored).
- Generic repository engineering work: `.scratch/<feature-slug>/`.
- Other-topic work: `other-topics/analyses/<feature-slug>/`.

Resolve the customer using the repository's Client Resolution rules. Keep customer-specific tickets and evidence in that customer's local tree; publish no customer content to an external tracker.

## Tickets

Write one file per ticket at `<feature-root>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Keep an existing source plan in place and reference it from the feature README. New specs belong at `<feature-root>/spec.md`.

Each ticket contains a title, What to build, Blocked by, Status, and checkbox acceptance criteria. Use the triage vocabulary in `triage-labels.md`; initial implementation tickets use `ready-for-agent`. This status describes specification readiness, not permission to bypass blockers.

List blockers by ticket number and title. Start only when every blocking ticket is complete and any explicit execution authorization is present. Record completion as `Status: resolved` with verification evidence. Append discussions under `## Comments`.

When a skill says publish, create local files. When it says fetch, read the referenced ticket. Never infer authorization to implement from a request to create tickets.

## Wayfinding

Use `<feature-root>/map.md` for Notes, Decisions-so-far, and Fog. Child tickets share the issues directory and carry `Type: research|prototype|grilling|task`. Work the lowest-numbered open, unblocked, unclaimed ticket; set `Status: claimed` before starting. On completion append an Answer, set `Status: resolved`, and add a linked summary to the map.
