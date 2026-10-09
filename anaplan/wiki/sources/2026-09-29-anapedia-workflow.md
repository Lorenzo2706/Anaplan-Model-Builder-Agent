---
title: Anapedia Workflow & Workflow Advanced — Clipping Batch (22 files)
type: source
tags: [anaplan, workflow, clippings, sources]
created: 2026-09-29
updated: 2026-09-29
sources: [raw/docs/Workflow  Anapedia.md]
---

# Anapedia Workflow & Workflow Advanced — Clipping Batch (22 files)

**Raw:** 22 Anapedia clippings landed in `Clippings/` and were moved to `raw/docs/` on ingest. Entry points: [[raw/docs/Workflow  Anapedia|Workflow | Anapedia]] and [[raw/docs/Workflow Advanced|Workflow Advanced]].

First-time ingest of Anaplan Workflow documentation — generic, so it lands under `anaplan/`. No prior Workflow content existed.

## Files in the batch

- **Overview / UX:** Workflow Anapedia, Task and template management, Use Workflow in the User Experience, Perform task actions
- **Task types:** Create a page task, Create an offline task, Create a machine task, Create a decision task, Create a hierarchical task, Create a notification step
- **Template & operations:** Build a workflow template, Workflow schedules, Monitor workflows
- **Notifications:** Edit email notifications, Add feedback to a decision task
- **Workflow Advanced:** Workflow Advanced, Create parallel steps, Branch and reconnect steps, Use Value-based decisions, Use send-back loops, Batch workflows and approvals

## Key takeaways

- Workflow and Workflow Advanced are **separately entitled**, tenant-specific services; Workflow Owner is the required role.
- Machine, decision, hierarchical and notification tasks exist only inside templates; page and offline tasks can be stand-alone.
- Assignees can be data-driven from a module line item (Iterate all / specific item / Sync to workflow) or from model roles (needs workspace admin).
- Parallel steps (max 20 per block) cannot be combined with branching; value-based decisions route on a Boolean line item.
- Batch approvals email is sent at 00:00 UTC; approver feedback is limited to 500 characters and not available via email actions.
- Gap: no *Create a group task* page in the batch.

## Wiki pages created

New sub-collection `wiki/concepts/workflow/`:

- [[wiki/concepts/workflow/index|Workflow — Index]]
- [[wiki/concepts/workflow/01_overview|Overview]]
- [[wiki/concepts/workflow/02_task-types-and-templates|Task Types & Templates]]
- [[wiki/concepts/workflow/03_workflow-advanced|Workflow Advanced]]
- [[wiki/concepts/workflow/04_notifications-and-feedback|Notifications & Feedback]]
- [[wiki/concepts/workflow/05_schedules-and-monitoring|Schedules & Monitoring]]
