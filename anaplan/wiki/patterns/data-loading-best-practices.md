---
title: Data Loading Best Practices
type: pattern
tags: [anaplan, pattern, data-hub, data-loading, save-view, best-practices]
created: 2026-08-10
updated: 2026-09-11
sources: []
---

# Data Loading Best Practices

General guidance for loading external data into Anaplan (Data Hub / spoke-model load modules),
captured from field experience running Data Hub onboarding sessions across customer engagements
(session notes, where ingested, live under the sourcing customer's own `wiki/sources/`).
Complements [[wiki/patterns/disco|DISCO]] (which module category holds what) — this pattern is
about *how* the loading itself should be built.

## With a unique key (preferred)

1. Load the key into a **numbered list**.
2. Load all data into a **load module** keyed on that list.
3. Create **save views** as needed downstream (e.g. to feed a spoke model or another hub area).

### Update process (3-step, key-based)

1. Clear the key column.
2. Re-upload the file to update the list.
3. Delete items with no key (i.e. items no longer present in the source).

This is more efficient than deleting and re-adding every item on each refresh — only the delta
moves.

## Without a unique key

Load directly into properties and mark items as uniquely identified by a **combination** of
properties. Less efficient: requires clearing and a full reload every time, since there's no
single key to diff against.

When the file being loaded this way is a **hierarchy source** — one row per leaf item, with
each hierarchy level in its own column — see
[[Building a Hierarchy from an Uploaded File (DataHub → Spoke)|Hierarchy Load from File]] for
the load-module + `ISFIRSTOCCURRENCE` + per-level-save-view recipe that turns this shape into
a proper composite hierarchy in the Spoke model.

## Design and process hygiene

- **Avoid unnecessary transformations and checks** — e.g. redundant "find item" logic that repeats
  work already done elsewhere in the pipeline. Keep processes as lean as possible.
- **Use backwards induction**: identify what the *spoke model* actually needs as the end result
  first, then determine the simplest path to get there — rather than building forward from
  whatever the source system happens to export.

## File handling conventions

- Set uploaded file sharing to **"Everyone"** — a more restrictive setting makes the file
  disappear and become inaccessible to the import action.
- File names should match what's referenced in import actions, for traceability.
- Trigger load actions **from a dashboard**, not the backend, so the system prompts for a fresh
  file upload each time instead of silently reusing whatever file is already sitting there.

## Where this applies in this vault

- A planned profit-center/afdeling hierarchy rebuild for one customer engagement (see that
  customer's own `wiki/sources/` for the migration notes, if ingested there) follows this exact
  shape: key list → load module → save view → import downstream.
