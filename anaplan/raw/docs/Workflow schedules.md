---
title: "Workflow schedules"
source: "https://help.anaplan.com/workflow-schedules-a324b583-c8dd-404e-8967-16e43988054f"
author:
published:
created: 2026-09-29
description: "As a workflow owner, you can create schedules for workflow templates to set specific times when workflows should run or repeat."
tags:
  - "clippings"
---
As a workflow owner, you can create schedules for workflow templates to set specific times when workflows should run or repeat.

Before you can create a workflow schedule, you must have already created a [workflow template](https://help.anaplan.com/b10a96a3-dbdd-4a95-81f9-e375c2e97f65).

Schedules enable you to keep track of when a workflow started or when it'll next run. Select a schedule to see the workflow template associated with it, and the details of the schedule. You can also see the progress of each workflow run on the schedule.

To create a workflow schedule:

1. Select **Templates**.
2. Select a workflow template > **Start workflow**.
3. Enter a **Workflow name** and **Workflow description**.
4. Select **Start on a certain date, or repeat on a schedule** > **Next**.
5. Specify the parameters for your schedule:
	- **Date:** Select the workflow schedule start date.
		- **Time zone:** Select a time zone.  
		Daylight savings is automatically handled for timezones that observe it, and won't affect the start time of your workflow. For example if you set the schedule to run at 09:00 a.m. BST (UTC+1) every Monday, then it'll run at 09:00 a.m., even after the clocks have been adjusted back an hour for daylight saving.
		- **Time:** Select the workflow start time from the grid.
		- **Change minutes:** You can change the times on the grid to 0, 15, 30, or 45 minutes from the hour.

The **Time** dropdown selections are **00**, **15**, **30**, **45**, representing 15-minute windows for scheduled start times. Start times will be offset based on availability. Once you choose your start time, the system automatically sets the trigger time within your selected 15-minute window. ‌For example, if you set your start time as 08:15 a.m., the workflow may start any time between 08:15 a.m. to 08.29 a.m.

- **Repeats:**
	- **Days of the week**: Select the days of the week that this schedule will repeat.
			- **Dates of the month:** Select the days of the month that this schedule will repeat. Because certain months have fewer days, if you select 29, 30, or 31 as your workflow schedule start date, the workflow won't run on those months.  
		Select **Last day** if you want to schedule your workflow to run on the last day of each month, regardless of the number of days in that month.
	- **Ends:** Select an end for the workflow schedule.
	- **Never**
			- **On this date:** Select the time and date for the workflow schedule to end.
	- **Allow next occurrence to run if previous is not complete:** Select this option if you want the workflow to run as scheduled, even if it wasn't completed the previous time.

To pause/resume a workflow schedule:

1. On the **Schedules** page, select an active schedule.
2. In the right panel, select **Pause schedule**.

When you are ready to resume the workflow schedule, select **Resume schedule** and your workflow will run as scheduled.

To delete a workflow schedule:

1. On the **Schedules** page, select the schedule you want to delete.
2. In the right panel, select **Delete schedule**.  
	This will delete the schedule, and won't affect the workflow template the schedule is applied to.

Enter a schedule name in the search bar to search for a specific schedule.

To filter schedules by user:

1. Select .
2. In the right panel, select a user from the **Created by** list.  
	You can use the search bar to search for a specific user.
3. All the workflow schedules created by your selected user will display.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fworkflow-schedules-a324b583-c8dd-404e-8967-16e43988054f&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>