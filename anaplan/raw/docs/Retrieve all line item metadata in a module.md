---
title: "Retrieve all line item metadata in a module"
source: "https://help.anaplan.com/retrieve-all-line-item-metadata-in-a-module-c8c41f1d-dd4e-4ca6-ac92-1a3d6c46bfeb"
author:
published:
created: 2026-09-09
description: "Use this call when you want to get all line items and metadata in a module."
tags:
  - "clippings"
---
Use this call when you want to get all line items and metadata in a module.

**Notes:**

- Only [workspace administrators](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html) can use this call.
- You need **Read** access to the module. Otherwise, you receive a `404` response.
- The items in the response are in the same order that they appear on the user interface.
- This returns line items for a specific module. For all the line items in the model see [Retrieve all line items in the model](https://help.anaplan.com/5bdf5544-ae86-414e-87f9-f74f3f45bba7).
- An invalid or a non-existing module ID returns a 404 response.

GET

`/models/{modelId}/modules/{moduleId}/lineItems?includeAll=true`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{moduleId}` | - Required - Type: String - Description: the model ID - Example: `89AA40874E6B64FA3AE07432789967048` |

``curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/lineItems?includeAll=true' \`     -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`     -H 'Accept: application/json'``

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/lineItem"     },     "status": {       "code": 200,       "message": "Success"     },     "items": [{               "moduleId": "102000000001",               "moduleName": "module2",               "id": "206000000006",               "name": "lineitem-child",                              "isSummary": false,               "startOfSection": false,               "broughtForward": false,               "useSwitchover": true,               "breakback": false,                              "cellCount": 51,                              "version": {                   "name": "All",                   "id": "16000000000"               },               "appliesTo": [                   {                       "name": "org-sub1",                       "id": "109000000001"                   },                   {                       "name": "linesubset1",                       "id": "114000000001"                   }               ],               "dataTags": [                   {                       "name": "tag1",                       "id": "127000000002"                   },                   {                       "name": "tag2",                       "id": "127000000001"                   },                   {                       "name": "tag3",                       "id": "127000000000"                   }               ],               "referencedBy": [                   {                       "name": "lineitem5",                       "id": "206000000005"                   }               ],                  "parent": {                   "name": "lineitem5",                   "id": "206000000005"               },               "readAccessDriver": {                   "name": "lineitem2",                   "id": "206000000003"               },               "writeAccessDriver": {                   "name": "lineitem2",                   "id": "206000000003"               },                              "formula": "3 + 9",               "format": "NUMBER",               "formatMetadata": {                   "dataType": "NUMBER",                   "minimumSignificantDigits": 4,                   "decimalPlaces": -1,                   "negativeNumberNotation": "MINUS_SIGN",                   "unitsType": "NONE",                   "unitsDisplayType": "NONE",                   "zeroFormat": "ZERO",                   "comparisonIncrease": "GOOD",                   "groupingSeparator": "COMMA",                   "decimalSeparator": "FULL_STOP"               },                              "summary": "Sum",               "timeScale": "Month",               "timeRange": "timeRange1",                           "formulaScope": "All Versions",               "style": "Normal",               "code": "code7",               "notes": "note1"     }        ]   }`

View the following endpoints for further details on other model metadata APIs:

- [Lookup dimension items by name or code](https://help.anaplan.com/7662bf9b-efdb-41c3-a1c5-4d71a8833d53)
- [Retrieve all items in a dimension](https://help.anaplan.com/7cc15f51-2c0d-4fdd-9fd2-1c5ccd5c1787)
- [Retrieve selected items in a dimension](https://help.anaplan.com/70aa5711-b17b-4bd4-a565-620fde5d9826)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-all-line-item-metadata-in-a-module-c8c41f1d-dd4e-4ca6-ac92-1a3d6c46bfeb&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top