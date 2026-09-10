---
title: "Retrieve dimension items for a line item"
source: "https://help.anaplan.com/retrieve-dimension-items-for-a-line-item-6a6d1652-4bf1-42a8-9013-340bd2aeeaed"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve IDs, codes, and names for dimension items that apply for the specified line item."
tags:
  - "clippings"
---
Use this call to retrieve IDs, codes, and names for dimension items that apply for the specified line item.

This helps determine the valid dimensional intersections for a line item before reading, interpreting, or writing related data.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- This call works with any dimension type.
- Your requesting model role must allow read access to the module the line item belongs to. Otherwise, this call returns a `404 Not Found` HTTP status.
- The items in the response are ordered as listed in the Anaplan model.
- The response returns items within a [flat list](https://help.anaplan.com/403a1ed1-ad7b-4ab3-b40c-61dd9d651075) (no hierarchy).
- This returns dimension items that apply to a line item. For the view-level call, see [Retrieve selected items in a dimension](https://help.anaplan.com/70aa5711-b17b-4bd4-a565-620fde5d9826) and for the model-level call, see [Retrieve all items in a dimension](https://help.anaplan.com/7cc15f51-2c0d-4fdd-9fd2-1c5ccd5c1787).
- This call only supports the retrieval of dimension items where the dimension contains a maximum of 1,000,000 items. If the specified dimension contains more than 1,000,000 dimension items, then the call returns a 400 Bad Request HTTP status, instead of a subset of the dimension items.
- Providing a non-existent Line Item ID or Dimension ID returns a 404 Not Found HTTP status.
- If the request provides an invalid line item ID or dimension ID this call returns a `400 Bad Request` HTTP status.

GET

`/models/{modelId}/lineItems/{lineItemId}/dimensions/{dimensionId}/items`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: `String` - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{lineItemId}` | - Required - Type: `Number` - Description: the line item ID - Example: `208000000000` |
| `{dimensionId}` | - Required - Type: `Number` - Description: the dimension ID - Example: `101000000028` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems/{lineItemId}/dimensions/{dimensionId}/items' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/dimension"     },     "status": {       "code": 200,       "message": "Success"     },     "items": [       {         "id": "220000000001",         "name": "England"       },       {         "id": "220000000002",         "name": "Wales"       }     ]   }`

View these endpoints for further details on view data APIs:

- [Initiate large read request](https://help.anaplan.com/741ca811-9e9f-46f2-acc6-3689b9b42434)
- [Retrieve status of large read request](https://help.anaplan.com/6216fdd8-772a-4032-8eb9-cc833c5edb1e)
- [Download pages](https://help.anaplan.com/930acac9-c2b6-49ff-ac84-7b089a98d1ba)
- [Delete read requests](https://help.anaplan.com/71a6b2da-008c-40e7-ba05-103730de30b2)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-dimension-items-for-a-line-item-6a6d1652-4bf1-42a8-9013-340bd2aeeaed&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top