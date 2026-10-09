---
title: "Use send-back loops in a workflow"
source: "https://help.anaplan.com/use-send-back-loops-in-a-workflow--9ec4f9ba-5194-4a9b-b31e-d283735206bc"
author:
published:
created: 2026-09-29
description: "Send-back loops enable approvers to send things back to a previous step in the process so work can be re-done and re-submitted for approval, instead of rejecting outright and ending the workflow."
tags:
  - "clippings"
---
[Workflow Advanced](https://help.anaplan.com/workflow-advanced-f6ad25f7-2e58-4e06-8132-d1cc42dff1b0 "Workflow Advanced ")

Send-back loops enable approvers to send things back to a previous step in the process so work can be re-done and re-submitted for approval, instead of rejecting outright and ending the workflow.

**Note:** Workflow Advanced is an entitled service and requires a separate subscription to enable the feature. Your Account Executive can assist you with this. The features are tenant-specific, so in a multi-tenant environment, the Workflow Advanced features only display on tenants that have the feature enabled.

![](https://assets-us-01.kc-usercontent.com/cddce937-cf5a-003a-bfad-78b8fc29ea3f/f34b9eb5-73e6-442a-a75d-88618cd790bd/sendbackloop.png)

To create a workflow with a send-back loop:

1. Open a new or existing [workflow template](https://help.anaplan.com/46e9d0c5-c59c-4a70-853e-5586c0f616cc). Following the example above, we'll build a workflow where once a report is submitted, it must go through a few approval steps. We'll also give the final approver the ability to not only approve or reject the report, but send it back.
2. In our workflow, we might have a [machine task](https://help.anaplan.com/f7efde27-771e-4d5a-bb8c-3c1316e35b48) to mark our report as submitted. We'll then add two [parallel decision tasks](https://help.anaplan.com/6418169c-dfe5-47d1-9220-309b27d03b5d) as the next step in our workflow for two different departments to approve the report.  
	Switch off the **Enable branching** toggle to enable parallel decision tasks.
3. Below the parallel block, add another [decision task](https://help.anaplan.com/11cd0601-0221-4705-b101-30f00490846a) for final approval. This automatically splits your workflow into two branches, **ON APPROVE** and **ON REJECT**.
4. Switch on the **Enable send back for approver** toggle.
5. Select a step from the **Send back to** dropdown. An additional branchis created from the decision step that will send the workflow back to the step you selected.  
	Now, when your workflow runs, the approver in the final decision step can send the report back if they are unhappy with it, instead of rejecting it.
6. You can add steps to the **SEND BACK** branch, such as a [page task](https://help.anaplan.com/afc734da-cb16-44f6-a0d3-206d2816876d) to assign a user to update the report, or a [notification step](https://help.anaplan.com/27477d8b-ae1e-4dd9-b660-cf1fbf2b5402) to inform all parties involved that the report has been sent back.
7. You can add a due date in the **Due** section on the right panel.
8. Once you are happy with your template and are ready to start using it, select **Publish.**

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fuse-send-back-loops-in-a-workflow--9ec4f9ba-5194-4a9b-b31e-d283735206bc&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>