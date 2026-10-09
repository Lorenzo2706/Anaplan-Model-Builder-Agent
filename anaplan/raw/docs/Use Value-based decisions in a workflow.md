---
title: "Use Value-based decisions in a workflow"
source: "https://help.anaplan.com/use-value-based-decisions-in-a-workflow-f623ee82-d677-49dc-8be8-df139c9c8c00"
author:
published:
created: 2026-09-29
description: "Workflow Advanced enables you to add value-based decision tasks to a workflow."
tags:
  - "clippings"
---
[Workflow Advanced](https://help.anaplan.com/workflow-advanced-f6ad25f7-2e58-4e06-8132-d1cc42dff1b0 "Workflow Advanced ")

Similar to regular decision tasks, value-based decision tasks enable you to add branching logic to your workflow. However, instead of a user making that decision, you can configure a value-based decision task to query the data in a model and make a decision based on the model value, driving automation.

**Note:** Workflow Advanced is an entitled service and requires a separate subscription to enable the feature. Your Account Executive can assist you with this. The features are tenant-specific, so in a multi-tenant environment, the Workflow Advanced features only display on tenants that have the feature enabled.

![](https://assets-us-01.kc-usercontent.com/cddce937-cf5a-003a-bfad-78b8fc29ea3f/137a078c-4c9d-40cf-94a7-643c90cc8f23/valuebaseddecisions.png)

To create a workflow with value-based decision tasks:

1. Add a **Value-based** task to a new or existing [workflow template](https://help.anaplan.com/46e9d0c5-c59c-4a70-853e-5586c0f616cc). This automatically splits your workflow into two branches, **TRUE** and **FALSE**. When your workflow reaches this step, the value-based task will look at a Boolean line item in your selected line item to decide which branch the workflow will continue onto.  
	For example, you might be building a workflow for your human resources department, and you want your value-based task to check whether a position in your organization was filled within a certain time period.
2. Enter a **Task title.**
3. Select a **Workspace**, **Model**, **Module**, **Line item**, and context. In this example, your line item might be 'Filled?', and your context might be the time period and a position in your organization.
4. Now, when your workflow runs, it'll look at the line item you've set, and check whether it's TRUE or FALSE and follow the appropriate path.
5. You can now add more steps to your workflow on either branch. For example, if the position is filled and follows the TRUE branch, you might want to write the compensation data for that position into an expenses module with a [machine task](https://help.anaplan.com/f7efde27-771e-4d5a-bb8c-3c1316e35b48). If ‌the position was not active and follows the FALSE branch, you might add an [offline task](https://help.anaplan.com/33b5392e-2c06-4ec3-b75c-f7d04df1a42b) and assign it to a recruiter in your organization who will take action to recruit for the position.
6. You can add a due date in the **Due** section on the right panel.
7. Once you are happy with your template and are ready to start using it, select **Publish.**

Value-based decision tasks can be nested to create complex workflows based on the formulas and logic configured in your models. It can also be used in conjunction with [send-back loops](https://help.anaplan.com/9ec4f9ba-5194-4a9b-b31e-d283735206bc) to create different paths for [decision tasks](https://help.anaplan.com/11cd0601-0221-4705-b101-30f00490846a) that have been sent back for a second approval.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fuse-value-based-decisions-in-a-workflow-f623ee82-d677-49dc-8be8-df139c9c8c00&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>