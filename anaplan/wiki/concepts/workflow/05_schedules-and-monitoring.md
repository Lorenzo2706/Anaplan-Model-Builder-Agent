---
title: Workflow — Schedules & Monitoring
type: concept
tags: [anaplan, workflow, schedules, monitoring, audit]
created: 2026-09-29
updated: 2026-09-29
sources:
  - raw/docs/Workflow schedules.md
  - raw/docs/Monitor workflows.md
---

# Workflow — Schedules & Monitoring

## Schedules

Prerequisite: a published template ([[02_task-types-and-templates]]).

*Templates → select template → Start workflow* → name + description → **Start on a certain date, or repeat on a schedule** → Next.

| Parameter | Behaviour |
|---|---|
| Date / Time zone | Daylight saving handled automatically — 09:00 BST Monday stays 09:00 after clocks change |
| Time | Grid of **00 / 15 / 30 / 45** — a 15-minute *window*; actual trigger is offset by availability (08:15 may start 08:15–08:29) |
| Repeats — days of week | Pick weekdays |
| Repeats — dates of month | Days 29/30/31 skip shorter months; choose **Last day** to always run at month-end |
| Ends | Never, or on a date/time |
| **Allow next occurrence to run if previous is not complete** | Run on schedule even if the previous run is unfinished |

Manage on the **Schedules** page: **Pause / Resume schedule**, **Delete schedule** (template unaffected), search by name, filter by *Created by*. A schedule shows its template, details and the progress of each run.

## Monitoring

| Page | Shows |
|---|---|
| **Usage** | Overview for a From/To period: users who started workflows, templates created, workflows launched from a page; tasks issued/completed; workflows in progress / canceled / failed / completed / rejected / action required. *Total users* lists names + emails |
| **Running** | Each started workflow; *View* the template, see current/completed *Steps*, **Cancel workflow**. Filter by status (**In progress**, **Action required**), *Started by*, start date (today … less than one month ago) |
| **Completed** | Stopped workflows: **Completed, Canceled, Failed, Rejected**. *Steps*, **Delete** the instance, **Export** a CSV log |

**Export log** (CSV): tasks and events with timestamps, plus **GUIDs** for involved users (assigners, assignees, recipients) — useful for audit and for debugging stuck processes, and comparable in role to the diagnostic logs of imports/actions.

## Related

- [[01_overview]] · [[04_notifications-and-feedback]]
- Source: [[../../sources/2026-09-29-anapedia-workflow]]
