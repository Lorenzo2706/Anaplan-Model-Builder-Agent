---
title: "Retrieve all items in a dimension"
source: "https://help.anaplan.com/retrieve-all-items-in-a-dimension-7cc15f51-2c0d-4fdd-9fd2-1c5ccd5c1787"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the IDs, codes, and names for items in a specified dimension. The dimension must be a list, a list subset, a line item subset, or the Users dimension."
tags:
  - "clippings"
---
Use this call to retrieve the IDs, codes, and names for items in a specified dimension. The dimension must be a list, a list subset, a line item subset, or the Users dimension.

This endpoint helps an integration understand the full set of valid members for a dimension before importing, exporting, mapping, validating, or transforming data.

Calls at model-level don't support the Time dimension. The calls return a `400` response. To avoid this, use the view dimension instead.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- This call is on the model-level. It returns all dimension items as it doesn't have view-level hiding, filtering, or [Selective Access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698). For the view-level endpoint, see [Retrieve selected items in a dimension](https://help.anaplan.com/70aa5711-b17b-4bd4-a565-620fde5d9826).
- If codes haven't been set for an item, then the response excludes the `code` field.
- This call only supports the retrieval of dimensions and items from a dimension that contains a maximum of 1,000,000 items.  
	The call returns a `400` response for any more than that number of items.

GET

`/models/{modelGuid}/dimensions/{dimensionId}/items`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the ID for the dimension - Example: `101000000028` |

`curl -X GET   'https://api.anaplan.com/2/0/models/{modelGuid}/dimensions/{dimensionId}/items'\   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta" : {       "schema" : "https://api.anaplan.com/2/0/objects/dimension"     },     "status" : {       "code" : 200,       "message" : "Success"     },     "items" : [       {         "code" : "N",         "id" : "200000000001",         "name" : "North"       },       {         "code" : "E",         "id" : "200000000002",         "name" : "East"       },       {         "code" : "S",         "id" : "200000000003",         "name" : "South"       },       {         "code" : "W",         "id" : "200000000004",         "name" : "West"       },       {         "id" : "200000000000",         "name" : "Total Company"       }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-all-items-in-a-dimension-7cc15f51-2c0d-4fdd-9fd2-1c5ccd5c1787&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top