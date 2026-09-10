---
title: "Retrieve selected items in a dimension"
source: "https://help.anaplan.com/retrieve-selected-items-in-a-dimension-70aa5711-b17b-4bd4-a565-620fde5d9826"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve selected IDs, codes, and names for items in a specified dimension."
tags:
  - "clippings"
---
Use this call to retrieve selected IDs, codes, and names for items in a specified dimension.

This endpoint helps an integration work with a targeted subset of dimension members instead of retrieving the full dimension, which is useful for validation, filtering, or mapping workflows.

It returns data as filtered by the page builder when they configure the view. This call respects hidden items, filtering selections, and [Selective Access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698). If the view contains hidden or filtered items, these don't display in the response.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- This call works with any dimension type.
- The items in the response may not be ordered.
- The response returns items within a [flat list](https://help.anaplan.com/403a1ed1-ad7b-4ab3-b40c-61dd9d651075) (no hierarchy).
- This is a view-level call. For the model-level call, see [Retrieve all data for items in a dimension](https://help.anaplan.com/7cc15f51-2c0d-4fdd-9fd2-1c5ccd5c1787).
- This call only supports the retrieval of dimension items within a view that contains a maximum of 1,000,000 cells. If the specified view contains more than 1,000,000 dimension items, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the dimension items. Use the [quick sum bar](https://help.anaplan.com/cb15ce25-b344-4a61-8b02-cd21bc5bfca3) in Anaplan to identify the number of dimension items in a view.
- The `viewId` in this request can also be replaced by any valid `lineItemId`. If the Line Item has a changed dimensionality (has a Subsidiary View), the response returns the applicable dimension items for the given dimension. Otherwise, the response returns all default applicable dimension items for the given dimension.

GET

`/models/{modelId}/views/{viewId}/dimensions/{dimensionId}/items`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{viewId}` | - Required - Type: Number - Description: the ID for the view - Example: `102000000000` |
| `{dimensionId}` | - Required - Type: Number - Description: the ID for the dimension - Example: `101000000028` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/dimensions/{dimensionId}/items' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/dimension"     },     "status": {       "code": 200,       "message": "Success"     },     "items": [{         "id": "220000000001",         "name": "England"       },       {         "id": "220000000002",         "name": "Wales"       }]   }`

View these endpoints for further details on module and view data APIs:

- [Retrieve IDs and names for all modules in a model](https://help.anaplan.com/82183d8b-f928-4604-a20d-30dbb47aca59)
- [Retrieve IDs and names for all views in a model](https://help.anaplan.com/bcc1ed22-52b5-4537-ad90-77c65b77deeb)
- [Retrieve IDs and names for views in a module](https://help.anaplan.com/57540d7f-d05f-42c3-a68e-fb925dabf962)
- [Retrieve metadata for dimensions on a view](https://help.anaplan.com/1a2da490-553a-4949-ba01-b8584e6abb4f)
- [Retrieve cell data for a view](https://help.anaplan.com/677b9c88-5e95-4b9a-a9eb-9e78c00cbcb8)
- [Retrieve all line items in a module](https://help.anaplan.com/bf37fb71-ba13-4f9c-9a0c-bde0b2a99a10)
- [Retrieve dimension items for a line item](https://help.anaplan.com/6a6d1652-4bf1-42a8-9013-340bd2aeeaed)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-selected-items-in-a-dimension-70aa5711-b17b-4bd4-a565-620fde5d9826&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top