---
title: "Field notes — building a hierarchy from an uploaded file (DataHub → Spoke)"
source: "dictated by Lorenzo Giori, 2026-09-11 (field experience, not an Anapedia clipping)"
author: "Lorenzo Giori"
created: 2026-09-11
tags:
  - field-notes
  - data-hub
  - hierarchy
---

Procedure as dictated:

- If the file has a unique key, load it directly into the Spoke model where the data is
  needed, since no transformation is required.
- If the file has a unique key but still needs to land in a DataHub load list (rather than
  going straight to the Spoke model), that list is a normal (named) list — it does not need
  to be numbered. The unique key column serves directly as the list's name-based key.
- If the file does not have a unique key, create a **numbered** load list inside DataHub and
  load the file, using a combination of properties as a key. Numbering the list is only
  necessary because a combination-of-properties key is a workaround that named lists can't
  use (a named list's key is always its single Name field) — numbered lists are what makes
  a composite key possible in DataHub's import mapping. Those properties must be equal to
  the column headers of the file that has been uploaded.
- After the load, those properties must carry all of the columns' data.
- A load module inside the tab should be created to make the necessary transformation
  before creating the save view that will be used from the Spoke model to create the
  hierarchy.
- Since usually the file has all the hierarchy levels in different columns, use the
  ISFIRSTOCCURRENCE formula to identify, for each level, which row is the first occurrence
  in the file, and create a save view using that as a filter — one save view per level.
