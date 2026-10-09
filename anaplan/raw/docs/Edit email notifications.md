---
title: "Edit email notifications"
source: "https://help.anaplan.com/edit-email-notifications-de38fd18-e16d-421a-817b-256b8d9f7340"
author:
published:
created: 2026-09-29
description: "As a workflow owner, you can customize workflow notifications to provide context and actions to users who receive these emails."
tags:
  - "clippings"
---
As a workflow owner, you can customize workflow notifications to provide context and actions to users who receive these emails.

You can create custom notifications for:

- [Page tasks](https://help.anaplan.com/afc734da-cb16-44f6-a0d3-206d2816876d)
- [Offline tasks](https://help.anaplan.com/33b5392e-2c06-4ec3-b75c-f7d04df1a42b)
- [Group tasks](https://help.anaplan.com/751b22cd-6c85-46bc-a071-e0aee9608898)
- [Decision tasks](https://help.anaplan.com/11cd0601-0221-4705-b101-30f00490846a)
- [Hierarchy tasks](https://help.anaplan.com/eb2eaca9-1515-4d0d-a058-92f2787b3e1d)

To edit notifications for a task:

1. In the **Task details** section of the task configuration panel, select **Edit notifications**.  
	For hierarchy tasks, the **Edit notifications** option is in the **Assignment** section of the task configuration panel.
2. Select a notification type from the list. Enter a custom message in the **Subject**, **Introduction**, and **Outro** fields. Any field left blank will default to the system messaging.
3. You can select to copy your custom text in a field across to all other emails.
4. Select **Reset** to reset your changes in the selected email, or **Reset all** to reset all customized messages to the system default.
5. Select **Save**.

Adding line items to a workflow notification email can help add more context.

**Note:** This feature exposes model data via email, so it must be switched on by a Tenant Administrator in **Administration** > **Notifications** before it can be used in your workflow.

To add line items to a notification:

1. In the workflow builder, add a step to your new or existing workflow:
	- For [Group tasks](https://help.anaplan.com/751b22cd-6c85-46bc-a071-e0aee9608898): in the **Assignment** section of the task configuration panel, select **Assign to users from a line item in a module**,then the **Select** button in the **Select line item from a module** field.
		- For [Decision tasks](https://help.anaplan.com/11cd0601-0221-4705-b101-30f00490846a): in the **Approvers** section of the task configuration panel, select **Assign to users from a line item in a module**, then the **Select** button in the **Select line item from a module** field.
		- For [Hierarchy tasks](https://help.anaplan.com/eb2eaca9-1515-4d0d-a058-92f2787b3e1d): in the **Assignment** section of the task configuration panel, select the **Select** button in the **Configure Level** for each hierarchy level.
		- For [Notification tasks](https://help.anaplan.com/27477d8b-ae1e-4dd9-b660-cf1fbf2b5402): select **Assign to users from a line item in a module**,then the **Select** button in the **Select line item from a module** field.
2. Select a module from the dropdown.
3. In the **Notifications** section, you can see a list of line items. Select the line items you want to include in the notification email.

Workflow owners can give ‌approvers the ability to [perform task actions](https://help.anaplan.com/d85f5bc3-00dc-405b-bbae-9fd29e0a6d4f) via their email notifications by embedding **Approve**, **Reject**, and **View** buttons. Approvers can then approve or reject workflow tasks by selecting the button in their email notifications. To do this:

1. In the **Workflow builder** screen, select at the top right corner.
2. In the **Template settings** window, switch on the **Allow approve or reject from email notifications** toggle.
3. Select **Save**.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fedit-email-notifications-de38fd18-e16d-421a-817b-256b8d9f7340&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>