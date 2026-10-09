---
title: "Branch and reconnect steps in a workflow"
source: "https://help.anaplan.com/branch-and-reconnect-steps-in-a-workflow-45b1cd25-c944-46c0-8b4f-aa5e428e7f67"
author:
published:
created: 2026-09-29
description: "Add a decision task to a workflow to automatically create approval and rejection branches, with the rejection branch leading to the end of the workflow. With Workflow Advanced, you can add steps onto a rejection branch and reconnect the branch back into the workflow."
tags:
  - "clippings"
---
[Workflow Advanced](https://help.anaplan.com/workflow-advanced-f6ad25f7-2e58-4e06-8132-d1cc42dff1b0 "Workflow Advanced ")

Add a decision task to a workflow to automatically create approval and rejection branches, with the rejection branch leading to the end of the workflow. With Workflow Advanced, you can add steps onto a rejection branch and reconnect the branch back into the workflow.

**Note:** Workflow Advanced is an entitled service and requires a separate subscription to enable the feature. Your Account Executive can assist you with this. The features are tenant-specific, so in a multi-tenant environment, the Workflow Advanced features only display on tenants that have the feature enabled.

![](https://assets-us-01.kc-usercontent.com/cddce937-cf5a-003a-bfad-78b8fc29ea3f/a4a8d3b1-c85a-47fa-8579-617307a8a962/branchandreconnect.png)

To use branching and reconnect in a workflow:

1. Add a [decision task](https://help.anaplan.com/11cd0601-0221-4705-b101-30f00490846a) to a new or existing [workflow template](https://help.anaplan.com/46e9d0c5-c59c-4a70-853e-5586c0f616cc). Following the example above, we'll create a workflow where an approver is deciding whether data is ready to be imported into a module.
2. Enter a **Task title** and **Instructions** for the task assignee.
3. From the **Select page** section, you can use the search function to find a page and select it.
4. In the **Approver** section, select one or more approvers for your decision task.
5. A decision task automatically splits your workflow into two branches, **ON APPROVE** and **ON REJECT**.
	- **ON APPROVE**: Select the plus icon on this branch and add a [machine task](https://help.anaplan.com/f7efde27-771e-4d5a-bb8c-3c1316e35b48) to import data.
		- **ON REJECT**: Select the plus icon on this branch. You can add one or more tasks to this branch. This might be two [page tasks](https://help.anaplan.com/afc734da-cb16-44f6-a0d3-206d2816876d), one to be assigned to a user to update the data, and another assigned to another user to review the data.
6. After the data is updated and reviewed again‌, we want the branch to reconnect into the workflow. Select the reconnect icon below the end of the branch to configure the joining point.
7. The steps that can be used as reconnect points are highlighted in blue. Select a step to reconnect the branch to it. In this case, we want to reconnect the reject branch to the machine task we created on the approve branch.
8. Your workflow will reconfigure on the canvas and connect the two branches.  
	You can now add more steps to your workflow.
9. You can add a due date in the **Due** section on the right panel.
10. Once you are happy with your template and are ready to start using it, select **Publish.**

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fbranch-and-reconnect-steps-in-a-workflow-45b1cd25-c944-46c0-8b4f-aa5e428e7f67&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>