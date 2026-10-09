---
title: Workflow — Task Types & Templates
type: concept
tags: [anaplan, workflow, templates, decision-task, machine-task, hierarchical-task]
created: 2026-09-29
updated: 2026-09-29
sources:
  - raw/docs/Build a workflow template.md
  - raw/docs/Create a page task.md
  - raw/docs/Create an offline task.md
  - raw/docs/Create a machine task.md
  - raw/docs/Create a decision task.md
  - raw/docs/Create a hierarchical task.md
  - raw/docs/Create a notification step.md
  - raw/docs/Task and template management.md
---

# Workflow — Task Types & Templates

## Task types

| Type | Assigned to | Notes |
|---|---|---|
| **Page task** | One user | Single-use, linked to a page. Can be created from a page (*Create task* in the options bar) or from the task inbox (*Create → Task*). *Assign to* lists only users with a role in the page's model |
| **Offline task** | One user | Like a page task but **not linked to a page** (*Create → Task → Offline task*) |
| **Group task** | A group | Any member can complete it |
| **Hierarchical task** | Users per hierarchy level | Sequence of dependent tasks flowing through a hierarchy (see below) |
| **Machine task** | Nobody — automatic | Runs a model action: import, export, data write, Optimizer action, or **Data Orchestrator** action (owner chooses what happens if a Data Orchestrator step fails) |
| **Decision task** | Approver(s) | Approve / reject / send back a preceding step |
| **Notification step** | Users | Sends a custom message as the workflow reaches the step |

Page and offline tasks can be created stand-alone. **Machine, decision, hierarchical and notification tasks only exist inside a template (or its running workflow).**

Task creation dialogs: title + instructions → (page) → assignee → optional due date + time zone (defaults to the creator's).

## Building a template

*Create → Template* → name + description → add steps by clicking in the right panel or drag-and-drop onto the canvas; the plus icon position decides where a new step lands; steps can be dragged to reorder. Finish with **Publish** or **Save as draft**.

- Published templates run via *Templates → Start workflow*, or on a schedule ([[05_schedules-and-monitoring]]).
- **Send notifications to Workflow Owner** toggle is **off by default**; on = general emails, off = only when action is needed (broken, blocked, canceled).
- The Templates page supports start, edit, duplicate, delete and filtering by user/creation date.
- Due dates on template steps: up to **31 business days** ahead.

## Assignee resolution (decision, notification, group, hierarchical)

Three ways to pick users:

1. **Manually** — choose named users.
2. **From a line item in a module** — pick workspace → model → module → line item → *context setting*:
   - **Iterate all** — every user in the line item
   - a **specific item** — the user at that list item
   - **Sync to workflow** — value chosen when the workflow is started
3. **From a model role** — requires being a **workspace administrator** to retrieve roles.

The user line item makes workflows data-driven: assignees live in a module, not in the template.

## Machine task configuration

Select in order: **Action type** → **Workspace** → **Model** → **Process**. A model builder must first create the action/process in the model — so machine tasks depend on well-named [[../anaplan concepts/index|actions and processes]] in the target model.

## Decision task

Splits the workflow into **ON APPROVE** and **ON REJECT** branches; by default reject ends the workflow (extend with [[03_workflow-advanced]]). Config: title, instructions, page, approver(s), due date. Optional approver feedback: see [[04_notifications-and-feedback]].

## Hierarchical task

Flows through a **composite hierarchy** in the model, so branches progress at different speeds and bottlenecks are removed.

- One page drives all levels.
- **Task flow direction**: top-down or bottom-up.
- Toggles: *Hide reject option for approver*; *Skip on blank assignees* (step skipped if the module line item has no assignee).
- Per level: *Omit hierarchy*, or *Configure level* → module (only modules dimensioned by the level's line items appear), assignee line item + line item updated on completion, approver line item + line item updated on approve/reject, context setting, and **Enable completion check** (a Boolean line item verifying the task may complete, plus an optional text line item explaining why not).

## Notification step

Recipients as above. Enable **Bulk notify assignees** to send one email with multiple calls-to-action instead of many. Custom Subject, Introduction, Notification message, Outro.

## Related

- [[01_overview]] · [[03_workflow-advanced]] · [[04_notifications-and-feedback]]
- Source: [[../../sources/2026-09-29-anapedia-workflow]]
