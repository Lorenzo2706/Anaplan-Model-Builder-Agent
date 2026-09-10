---
title: Integration API — Model Calendar & Versions
type: concept
tags: [anaplan, integration-api, model-calendar, fiscal-year, versions, switchover]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Model calendar.md
  - raw/docs/Get current fiscal year.md
  - raw/docs/Update current fiscal year.md
  - raw/docs/Retrieve current period.md
  - raw/docs/Set current period.md
  - raw/docs/Model versions.md
  - raw/docs/Retrieve version metadata.md
  - raw/docs/Set version switchover date.md
---

# Integration API — Model Calendar & Versions

These endpoints give programmatic control over a model's time context (current period, fiscal year) and its [[../anaplan concepts/22_versions|version]] configuration (switchover dates). All require **Workspace Administrator** authority.

## Fiscal year

| Endpoint | Method & path |
|---|---|
| Get current fiscal year | `GET /workspaces/{workspaceId}/models/{modelId}/modelCalendar` |
| Update current fiscal year | `PUT /workspaces/{workspaceId}/models/{modelId}/modelCalendar/fiscalYear` (body: `{"year": "FY21"}`) |

- The fiscal year's start/end dates come from the model's calendar type and don't always run Jan 1–Dec 31.
- If the calendar type has no fiscal year concept (e.g. **Weeks General**), the API returns an empty `modelCalendar` object rather than a fiscal year.
- Updating to an out-of-range year returns `400 Bad Request` (e.g. `"Specified year is out of range: 2040"`).

Example calendar response:

```json
{
  "modelCalendar": {
    "calendarType": "Calendar Months/Quarters/Years",
    "fiscalYear": { "year": "FY21", "startDate": "2020-03-29", "endDate": "2021-03-27" },
    "pastYearsCount": 0,
    "futureYearsCount": 0,
    "currentPeriod": { "periodText": "", "lastDay": "" },
    "totalsSelection": { "quarterTotals": true, "halfYearTotals": false,
      "yearToDateSummary": false, "yearToGoSummary": false, "totalOfAllPeriods": false }
  }
}
```

## Current period

| Endpoint | Method & path |
|---|---|
| Retrieve current period | `GET /workspaces/{workspaceId}/models/{modelId}/currentPeriod` |
| Set current period | `PUT /workspaces/{workspaceId}/models/{modelId}/currentPeriod` |

- If the current period isn't set, `GET` returns empty strings for `periodText` and `lastDay`.
- `PUT` with a date (e.g. `2020-05-20`) sets the current period to the range containing that date; an empty date value resets the current period to blank.

> [!warning]
> Setting the current period is **potentially destructive**. The new time range may not include previously covered periods — any data in the periods that fall out of range is **deleted from the model**. Treat this like a schema change, not a routine read/write call.

## Model versions

| Endpoint | Method & path | Notes |
|---|---|---|
| Retrieve version metadata | `GET /models/{modelId}/versions` | Only returns versions the caller's model role has read access (or higher) to |
| Set version switchover date | `PUT /models/{modelId}/versions/{versionId}/switchover` (body: `{"date": "{newSwitchoverDate}"}`) | Automates the point where actual data replaces forecast data for a version |

Version metadata fields: `id`, `name`, `isCurrent`, `isActual`, `switchover` (`{periodText, date}`, forecast/variance versions only), `formula` (e.g. `"Actual - 20"`), `editFrom`/`editTo` (each `{periodText, date}`), `notes`. Date format for `editFrom`/`editTo` follows the model calendar setting.

Switchover constraints:

- `{versionId}` must be a version set to `forecast` or `variance` — passing the **actual** version's ID returns `400 Bad Request`.
- The new switchover date must be **after** the existing switchover date.
- To reset a switchover date to blank, pass an empty string in the request body.

## Related

- [[01_overview|Integration API — Overview]]
- [[04_workspaces-and-models|Workspaces & Models]]
- [[../anaplan concepts/12_model-calendar|Model Calendar (concept)]]
- [[../anaplan concepts/22_versions|Versions (concept)]]
