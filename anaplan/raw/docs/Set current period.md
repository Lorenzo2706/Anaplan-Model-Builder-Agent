---
title: "Set current period"
source: "https://help.anaplan.com/set-current-period-b273f11e-73e8-44c4-998b-ab09abf59abd"
author:
published:
created: 2026-09-09
description: "Use this call to change or reset the current period in Anaplan."
tags:
  - "clippings"
---
[Model calendar](https://help.anaplan.com/model-calendar-a7bedbbb-c170-4f0b-9ac6-42669af1cfc6 "Model calendar")

This enables an integration to advance or change the model calendar as part of a scheduled planning, forecasting, or period-close process.

When this call contains a specified date (for example, 2020-05-20), the API determines what period range contains the specified data and sets that range as the current period. When the date value is set to blank in this call, the API resets the current period to blank.

**Warning**: A change to your time settings is a potentially destructive action and may lead to data loss. The new range of time periods may not include previous time periods. Any data in the removed time periods is deleted from the model.

**Note**: To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html)

PUT

`/workspaces/{workspaceId}/models/{modelId}/currentPeriod`

`curl -X PUT https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/currentPeriod\   -H 'Accept: application/json' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json'`

`Content-Type: application/json`

`{      "meta":{         "schema":"https://api.anaplan.com/2/0/objects/currentPeriod"      },      "status":{         "code":200,         "message":"Success"      },      "currentPeriod":{         "periodText":"May 20",         "lastDay":"2020-05-31",         "calendarType":"Calendar Months/Quarters/Years"      }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fset-current-period-b273f11e-73e8-44c4-998b-ab09abf59abd&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top