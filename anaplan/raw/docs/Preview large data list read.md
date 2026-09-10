---
title: "Preview large data list read"
source: "https://help.anaplan.com/preview-large-data-list-read-a0221392-106e-47a6-a100-e1f666c14a9b"
author:
published:
created: 2026-09-09
description: "Use this to preview ‌large datasets, that allows you to quickly read a limited subset of records without loading the entire data list."
tags:
  - "clippings"
---
Use this to preview ‌large datasets, that allows you to quickly read a limited subset of records without loading the entire data list.

This helps confirm that the integration is targeting the correct list and that the output structure is suitable before requesting a larger dataset.

GET

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/preview`

| **Parameter** | **Required** | **Type** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| `{workspaceId}` | Yes | String | The workspace ID | `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | Yes | String | The model ID | `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | Yes | Number | The list ID | `101000000001` |

``curl --location --request GET`     'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/preview'`     -H 'Authorization: {anaplan_auth_token}'`     -H 'Accept: text/csv'``

`,Parent,Code   Closed No Decision,,   Closed Lost,,   Disqualified,,   5. Closed Won,,   0. 1st Meeting/Discovery,,   1. Qualification and Discovery,,   2. Solution Development,,   3. Solution Validation,,   4. Negotiate and Close,,`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fpreview-large-data-list-read-a0221392-106e-47a6-a100-e1f666c14a9b&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top