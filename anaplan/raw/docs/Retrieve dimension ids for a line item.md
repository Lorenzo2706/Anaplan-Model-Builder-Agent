---
title: "Retrieve dimension ids for a line item"
source: "https://help.anaplan.com/retrieve-dimension-ids-for-a-line-item-6d28276e-393b-40c8-8546-c68bdf12175f"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the Ids of dimensions that define a line item."
tags:
  - "clippings"
---
For reference, see [Retrieve dimension items for a line item](https://help.anaplan.com/6a6d1652-4bf1-42a8-9013-340bd2aeeaed).

**Notes:**

- To retrieve the IDs for the dimensions, use a `GET` request with this URL: `https://api.anaplan.com/2/0/models/{modelId}/lineitems/{lineItem_Id}/dimensions` where `{lineItemId}` is a placeholder for the retrieved line item ID.
- This returns a list of all the dimensions that apply to that line item.

GET

`/models/{modelId}/lineitems/{lineItem_Id}/dimensions`

| **Parameter** | **Required** | **Type** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| `{modelId}` | Required | String | The ID for the model | `75A40874E6B64FA3AE0743278996850F` |
| `{lineItemId}` | Required | Number | The line item Id | `208000000000` |

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/dimension"       },       "status": {           "code": 200,           "message": "Success"       },       "dimensions": [           {               "id": "20000000003",               "name": "Time"           },           {               "id": "20000000020",               "name": "Versions"           },           {               "id": "101000000001",               "name": "Products"           },           {               "id": "101000000002",               "name": "Regions"           }       ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-dimension-ids-for-a-line-item-6d28276e-393b-40c8-8546-c68bdf12175f&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top