---
title: Workflow — Notifications & Approver Feedback
type: concept
tags: [anaplan, workflow, notifications, email, approvals]
created: 2026-09-29
updated: 2026-09-29
sources:
  - raw/docs/Edit email notifications.md
  - raw/docs/Add feedback to a decision task.md
  - raw/docs/Perform task actions.md
---

# Workflow — Notifications & Approver Feedback

## Custom email notifications

Available for page, offline, group, decision and hierarchy tasks.

- **Edit notifications** (task *Task details* section; for hierarchy tasks, the *Assignment* section) → pick a notification type → customize **Subject**, **Introduction**, **Outro**. Blank fields fall back to system text. Options: copy text to all emails, **Reset** (one) / **Reset all**, then **Save**.
- The notification *step* additionally has a free **Notification message** — see [[02_task-types-and-templates]].

### Line items in emails

Adds model data as context to the email (group, decision, hierarchy, notification tasks): after choosing *Assign to users from a line item in a module* → module, the **Notifications** section lists line items to include.

> [!warning] Exposes model data via email
> A **Tenant Administrator** must first enable it under **Administration → Notifications**.

### Approve / Reject from email

Workflow builder → Template settings → switch on **Allow approve or reject from email notifications** → Save. Emails then carry **Approve**, **Reject**, **View** buttons; unauthenticated users log in first.

## Approver feedback on decision tasks

Approvers can comment when they approve, reject or send back; the comment is written **back to the model** against the line item.

Setup: decision task → *Approver* section → **Assign to users from a line item in a module** → module → **Line item for feedback notes** (must be **text**-formatted).

- Comment up to **500 characters**; a new comment **overwrites** the previous one.
- **Not available** when approving/rejecting via email.
- Works with [[03_workflow-advanced|batch approvals]].
- > [!warning] Populating many text cells adds density and can slow the model — a modeling consideration (see [[../../patterns/index|Patterns]]).

## Related

- [[01_overview]] · [[05_schedules-and-monitoring]]
- Source: [[../../sources/2026-09-29-anapedia-workflow]]
