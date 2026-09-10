---
title: "Reset numbered list index"
source: "https://help.anaplan.com/reset-numbered-list-index-02e0b698-9a3f-461d-b61c-75437a0a205d"
author:
published:
created: 2026-09-09
description: "Use this API to reset the index on lists. This ensures that as you add items, they stay within the maximum amount allowed."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

Use this API to reset the index on lists. This ensures that as you add items, they stay within the maximum amount allowed.

This helps maintain list indexing after item changes, especially where index values matter for model behavior or downstream processing.

**Notes:**

- To use this API call and reset the index on a list, the list must be empty, otherwise you will receive a `400 Bad Request` error.
- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration).

POST

`/models/{modelId}/lists/{listId}/resetIndex`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: String - Description: the list ID - Example: `3010000001` |

``curl -X POST 'https://api.anaplan.com/2/0/models/{modelId}/lists/{listId}/resetIndex' \`     -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`     -H 'Accept: application/json'``

A successful index reset will provide a `200 OK` response. The API will return a 400-type error if you attempt to reset the index on a list that is not empty.

A successful response does not return a message body.

`application/json`

`{       "status": {           "code": 400,           "message": "We can't reset the list item index of a list that contains data. Select an empty list that doesn't contain any list items."       },       "path": "/2/0/models/567CF3F6A9B346718F7BE5C749857523/lists/101000000000/resetIndex",       "timestamp": "2023-04-26T13:51:59.102661Z"   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Freset-numbered-list-index-02e0b698-9a3f-461d-b61c-75437a0a205d&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top