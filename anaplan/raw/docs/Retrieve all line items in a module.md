---
title: "Retrieve all line items in a module"
source: "https://help.anaplan.com/retrieve-all-line-items-in-a-module-bf37fb71-ba13-4f9c-9a0c-bde0b2a99a10"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve identifiers of line items for a specific module."
tags:
  - "clippings"
---
This helps identify the measures or fields available in a module before reading, mapping, or documenting data.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- The Model Role of the user must allow Read access to the module. Otherwise, this call returns a `404 Not Found` HTTP status.
- The items in the response are in the same order that appear in the Anaplan UI.
- This call returns line items for a specific module. For all the line items in the model see [Retrieve All Line Items in a Model](https://help.anaplan.com/5bdf5544-ae86-414e-87f9-f74f3f45bba7).
- If this query contains an invalid or a non-existing Module ID, the API returns a `404 Not Found` HTTP status.

GET

`/models/{modelId}/modules/{moduleId}/lineItems`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{moduleId}` | - Required - Type: Number - Description: the ID for the module - Example: `102000000000` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/lineItems' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/lineItem"       },       "status": {           "code": 200,           "message": "Success"       },       "items": [           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000000",               "name": "Quantity Sold"           },           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000001",               "name": "Price"           },           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000002",               "name": "Revenue"           }       ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-all-line-items-in-a-module-bf37fb71-ba13-4f9c-9a0c-bde0b2a99a10&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top