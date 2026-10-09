---
title: Workflow Advanced — Parallel, Branching, Value-based, Send-back, Batch
type: concept
tags: [anaplan, workflow, workflow-advanced, approvals, branching]
created: 2026-09-29
updated: 2026-09-29
sources:
  - raw/docs/Workflow Advanced.md
  - raw/docs/Create parallel steps in a workflow.md
  - raw/docs/Branch and reconnect steps in a workflow.md
  - raw/docs/Use Value-based decisions in a workflow.md
  - raw/docs/Use send-back loops in a workflow.md
  - raw/docs/Batch workflows and approvals.md
---

# Workflow Advanced

Extends standard [[01_overview|Workflow]] for complex, non-linear, data-dependent processes.

> [!note] Entitlement
> Workflow Advanced is a **separate subscription**, tenant-specific. Features only display on enabled tenants.

| Feature | What it does | Key constraints |
|---|---|---|
| **Parallel steps** | Several tasks (e.g. approvals from different departments, each with its own page/instructions) run at once; a block is shown in pink | Up to **20 tasks per parallel block**; unlimited blocks; **not compatible with branching** — switch **Enable branching** off on the decision task |
| **Branch & reconnect** | Add steps on the ON REJECT branch and reconnect it into the main flow (valid reconnect points highlighted blue) | Standard decision task alone sends reject to end of workflow |
| **Value-based decision** | A task that reads a **Boolean line item** (workspace → model → module → line item → context) and routes to **TRUE** / **FALSE** — no human decision | Can be nested; combinable with send-back loops |
| **Send-back loop** | Approver can send work back to an earlier step instead of rejecting; a **SEND BACK** branch is created | Toggle **Enable send back for approver**, choose *Send back to* step |
| **Batch run** | Run one template for many list items in one go | See below |
| **Batch approvals** | Approver handles many decision tasks at once | See below |

## Building blocks worth remembering

- **Parallel + machine tasks**: after parallel approvals, add a parallel block of machine tasks to distribute approved data into several models/modules simultaneously.
- **Value-based example**: HR workflow checks a `Filled?` Boolean; TRUE → machine task writes compensation data, FALSE → offline task to a recruiter. The Boolean is normal model logic ([[../anaplan concepts/10_line-item|line items]]), so process routing is driven by formulas.
- **Send-back example**: machine task marks report submitted → two parallel decision tasks (departments) → final decision task with send-back to the parallel step.

## Batch run

Template settings → **Batch run** → *Enable batch run for this template* → select workspace/model/module; **User settings**: *Users line item* (who may run) and *User line item filter* (who is included); **Context setting = Iterate over all**; Publish. On the page: *Configure action* → *Actions* tab → *Workflow templates* → enable the template. See [[../conditional-formatting|page/card configuration]] for cards in general.

## Batch approvals

On the decision task, **Enable batch approval**. Each approver then gets **one email with all pending approvals, sent at 00:00 UTC**. From *View approvals*: open any task in the **Batch approval** pane for context, tick tasks, then Approve or Reject. **Send back** is only available for tasks where *Enable send back for approver* was on. Compatible with [[04_notifications-and-feedback|approver feedback]].

## Related

- [[02_task-types-and-templates]]
- Source: [[../../sources/2026-09-29-anapedia-workflow]]
