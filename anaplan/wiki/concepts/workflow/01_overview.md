---
title: Workflow — Overview
type: concept
tags: [anaplan, workflow, ux, tasks, task-inbox]
created: 2026-09-29
updated: 2026-09-29
sources:
  - raw/docs/Workflow  Anapedia.md
  - raw/docs/Task and template management.md
  - raw/docs/Use Workflow in the User Experience.md
  - raw/docs/Perform task actions.md
---

# Workflow — Overview

**Workflow** designs, runs and manages automated business processes inside the Anaplan user experience (UX). A workflow owner creates one-off tasks or multi-step **templates**, assigns them to stakeholders, and Anaplan tells each user what they own, when it is due and how to complete it.

> [!note] Entitlement
> Workflow is an **entitled service**, bought separately. It is tenant-specific: in a multi-tenant environment it only appears on tenants where it is enabled. Full use also needs the **Workflow Owner** role (an administration role) — see [[../anaplan concepts/index|core concepts]] for roles in general. The extra capabilities in [[03_workflow-advanced]] need a *further* separate subscription.

## What Workflow provides

- Visual workflow designer (template builder), fully integrated with the UX and the modeling experience
- Workflow **actions** that can be placed on pages; progress monitoring and tracking (see [[05_schedules-and-monitoring]])
- Task-level approvals; reassignment and delegation
- Notifications on web, email and mobile (Anaplan mobile app can action tasks) — see [[04_notifications-and-feedback]]
- Reusable templates + scheduling
- Event auditability for Tenant Auditors
- Machine tasks that drive **Anaplan Data Orchestrator** actions and **Anaplan Optimizer** actions

## Core building blocks

| Term | Meaning |
|---|---|
| **Task** | An action an assignee must undertake, tied to a page (board/worksheet) — so it can use grids, charts, actions. Every task has a title, description, one or more assignees and an optional due date; may require an approver |
| **Template** | Blueprint for a workflow: two or more back-to-back tasks, reusable and adjustable per run |
| **Workflow (running)** | Instance created when a template is started; the same template can run many times concurrently |
| **Workflow owner** | Creates/edits/deletes tasks and templates, schedules, monitors |
| **Task assignee / approver** | End users who action tasks |

Task types and how to build them: [[02_task-types-and-templates]].

Typical uses: an annual operations-planning (AOP) template run once a year; an escalation-handling template started ad hoc; an expense-approval process.

## The end-user experience

Users get Anaplan, email and (mobile app) push notifications, and can action a task straight from the notification or from the **task inbox** (Anaplan Home → Workflow, or nav menu → Workflow).

Inbox categories:

| Category | Contents |
|---|---|
| **Open** | Not yet started or in progress |
| **Completed** | Completed, canceled, rejected or approved |
| **Created by me** | Tasks the user created (workflow owners), any status |
| **Task approvals** | Anything subject to an approver: decision tasks for the user, plus page/group tasks awaiting the user's approval |

The main view filters by name, status, due date or creator. The task detail pane offers **Details** (instructions, due date), **Comments** (`@<username>` mentions notify that user) and **Timeline** (assignment, start, overdue, completion events). *View task* opens the task's page; the user can mark it complete.

### Actioning tasks

- Read the instructions in the detail pane → **View task** → do the work on the page.
- If the owner enabled it, **Approve / Reject / View** buttons in the email perform the action and open the relevant page (see [[04_notifications-and-feedback]]). Users not logged in must authenticate first.

## Related

- [[02_task-types-and-templates]]
- [[../conditional-formatting|Conditional Formatting]] — UX page configuration
- [[../../patterns/index|Patterns index]]
- Source: [[../../sources/2026-09-29-anapedia-workflow]]
