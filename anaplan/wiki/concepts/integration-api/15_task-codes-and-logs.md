---
title: Integration API — Task Result Codes & Logs
type: concept
tags: [anaplan, integration-api, bulk-api, error-codes, troubleshooting, dump-file]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
---

# Integration API — Task Result Codes & Logs

When an import, export, delete, or process task finishes, `result.details[]` carries entries of three kinds: **completion codes** (success summaries), **failure codes** (action-level failure), and **data error/warning codes** (row-level, with counts, mirrored per row in the dump file's `_Error_n_` column — see [[12_import-actions#dump-files]]). The `type` field of each detail entry holds the code. The lists below group the documented codes by family and give the fix; `${…}` are message placeholders.

## Completion codes (success)

| Code | Message pattern |
|---|---|
| `hierarchyRowsProcessed` | `${list}: ${successRowCount} (${create}/${update}) rows successful, ${ignoredCount} ignored` |
| `hierarchyRowsProcessedWithWarnings` / `…WithFailures` / `…WithInvalidNames` / `…WithInvalidNamesAndFailures` | Same, plus warnings / failed / invalid counts |
| `hierarchyRowsProcessedFromLineItem` (+ `WithFailures`) | `${module}: n created, n renamed, n properties updated` — import from a module-sourced list build |
| `hierarchyNoChanges` | `${list}: no changes required` |
| `lineItemRowsProcessed` (+ `WithFailures`, `WithIgnored`, `WithFailuresAndIgnored`) | `${lineItem} cells: ${rowCount} (n failed, n ignored)` — module-data imports report per line item |
| `usersRowsProcessed*`, `usersNoChanges` | Users list imports: created / permissions updated / failed / invalid |
| `versionsRowsProcessed*`, `versionsNoChanges` | Versions imports: created / properties updated / failed |
| `exportSucceeded` | `Export for ${name} completed successfully. ${fileSize} bytes written.` |
| `deleteFromSelectionSucceeded` | `${n} items were deleted from the list ${target} using ${filter}` |
| `taskElementSucceeded` | Generic `${message}` |

> [!note] Reading `successful: true`
> `successful: true` can still come with `ignored` rows or warnings (`W` rows in the dump). Check the counts in `details` — not just the boolean — when data completeness matters.

## Failure codes (action could not complete)

| Family | Codes | Typical fix |
|---|---|---|
| **Missing object** | `failedToLocateEntity`, `…Hierarchy` (list), `…Model`, `…Module`, `…SavedView`, `modelObjectNotLocated`, `modelObjectNotSupported` | The list/module/view/model was renamed, deleted, or archived (unarchive for model) — repoint the action |
| **Permissions** | `notAuthorised`, `moduleImportNoWriteAccess`, `hierarchyImportNoSelectiveEditing`, `noAccessToModule`, `sourceWorkspaceNoAccess` | Grant the integration user a role with access, or run as Workspace Admin ([[02_authentication-and-permissions]]) |
| **Cross-model source** | `sourceModelArchived`, `sourceWorkspaceNotLocated`, `crossCustomerImport` | Source and target workspace must be in the same tenant; unarchive source model |
| **Property-based list import setup** | `hierarchyImportPropertyKey{Calculated,InvalidMissing,InvalidNoDefintion,InvalidSystem,Unmapped}`, `hierarchyImportDuplicate{Source,Target}Key`, `hierarchyImportNameAndCodeUnmapped`, `hierarchyImportNameOrCodeSameAsParent` | Fix the mapping: no calculated property in the key, all key properties mapped, no duplicate keys |
| **Naming/code conflicts** | `hierarchyImportUniqueness` (distinct names for one code), `hierarchyImportInconsistentRenaming` | Make code ↔ name 1:1 in the data or fix mapping |
| **Generic import failure** | `hierarchyImportFailed`, `moduleImportFailed`, `importFailedGeneralError`, `usersImportFailed`, `versionsImportFailed`, `actionFailed`, `taskElementFailed`, `deleteFromSelectionFailed` | Read `${message}`; verify the action definition |
| **Internal error** | `internalError`, `hierarchyImportBombed`, `usersImportBombed`, `versionsImportBombed`, `connectorError`, `hierarchyImportFailedToUpdateProperties` | Retry; if persistent contact Anaplan Support |
| **File / cancel** | `uploadedFileNoLongerAvailable`, `msgImportCancelled`, `msgExportCancelled` | Re-upload (private files expire after 48 h — [[09_bulk-and-large-volume-data]]); cancellation was user-initiated |
| **Export format limits** | `msgTooManyColumns` (> 256), `msgTooManyRows` (> 65,536) | Excel only — switch to CSV/text |
| **Incomplete import** | `missingFields` | Complete the unavailable fields |

## Data error / warning codes (row level)

| Family | Codes | Meaning / fix |
|---|---|---|
| **Date & period parsing** | `dateFormatInvalid`, `dateFormatMalformed`, `invalidDate`, `invalidPeriod`, `periodFormatMalformed`, `expected{D,DD,H,M,MM,MMM,MMMM,Q,W,WW,Y,YY,YYYY,Character,Separator}` | Data doesn't match the import's date/period format — fix format or data. See [[../anaplan concepts/12_model-calendar|Model Calendar]] for period formats |
| **Text parsing** | `columnSeparatorExpected`, `unmatchedTextDelimiter` | Malformed delimiters/quotes in the file |
| **Module import values** | `moduleImportBooleanFormat`, `…DateFormat`, `…NumberFormat`, `…RepeatedNonNumeric` (several values for a non-numeric cell → source not normalized) | Clean the value / de-duplicate the source |
| **Module import identifiers** | `moduleImportInvalidListIdentifier` (item not in list), `…InvalidLineItemIdentifier`, `…InvalidTimeEntityIdentifier`, `…InvalidTimescaleIdentifier`, `…DimensionIdentifiersUnmapped`, `…LineItemIdentifiersUnmapped` | Item missing from the target list/calendar, or column not mapped (these unmapped identifiers are **ignored**, not failed) |
| **List import — structure** | `hierarchyImportInvalid{Code,Name,Parent,Status}`, `…NoNameOrCode`, `…NameOrCodeExists`, `…ParentMustBeLeaf` (children of a parent must all be in the same list), `…NewEntityNumberedList` (can't add new names to a numbered list), `…CannotChangeCodeForTopLevel`, `…EmptyKey`, `…ParseErrorInKey`, `…InvalidEntityIdInKey`, `…DuplicateKeyIn{Source,Target}`, `…FailedDependency` (depends on a rejected row), `…CancelledByUser`, `…PropertyChangeFailed` | Fix the offending rows; dependent rows fail when their parent row is rejected |
| **List import — access** | `hierarchyImportAccess{CantMoveFromParent,CantMoveToParent,NoCreateWithoutParent,NoImplicitAddToTopLevel,NoImplicitCreate,NoMove,NoMoveWithoutParent,NoRemoveParent,NoUpdate}` | Selective-access restrictions on the list — see [[../anaplan concepts/02_access-security|Access & Security]] |
| **Users import** | `usersImport{ConflictingAccessLevel,ConflictingAncestry,ConflictingNames,ConflictingRoles,CreationFailed,FirstNameMissing,LastNameMissing,InvalidEmail,InvalidListIdentifier,InvalidRole,NoSelectiveAccess,SSOStatusChangeFailed}` | User/role data issues (first and last names required for new users) |

## Where else to look

| Need | Source |
|---|---|
| Which rows failed and why | Dump file ([[12_import-actions#dump-files]], [[14_model-actions-delete-and-process]]) |
| Step timing in a process | `includeProcessDetails=true` |
| Optimizer solver output | `optimizeActions/…/solutionLogs` ([[14_model-actions-delete-and-process#optimizer-log]]) |
| HTTP-level errors (4xx/5xx, 429) | [[03_reliability-retries-rate-limits]] |
| Vault-wide diagnostics workflow | Customer `logs/<Model>/` folders hold real import/action error logs; use these codes to interpret them |

## Related

- [[12_import-actions]] · [[13_export-actions]] · [[14_model-actions-delete-and-process]]
- [[../../patterns/data-loading-best-practices|Data loading best practices]]
