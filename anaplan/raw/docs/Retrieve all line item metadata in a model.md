---
title: "Retrieve all line item metadata in a model"
source: "https://help.anaplan.com/retrieve-all-line-item-metadata-in-a-model-961428f6-aa1e-4149-8961-6a8a65c14004"
author:
published:
created: 2026-09-09
description: "Use this call to get all line Items and metadata for a model."
tags:
  - "clippings"
---
GET

`/models/{modelId}/lineItems?includeAll=true`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` |  |
| `includeAll` |  |

``curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems?includeAll=true' \`     -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`     -H 'Accept: application/json'``

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/lineItem"     },     "status": {       "code": 200,       "message": "Success"     },     "items": [{               "moduleId": "102000000001",               "moduleName": "module2",               "id": "206000000006",               "name": "lineitem-child",                              "isSummary": false,               "startOfSection": false,               "broughtForward": false,               "useSwitchover": true,               "breakback": false,                              "cellCount": 51,                              "version": {                   "name": "All",                   "id": "16000000000"               },               "appliesTo": [                   {                       "name": "org-sub1",                       "id": "109000000001"                   },                   {                       "name": "linesubset1",                       "id": "114000000001"                   }               ],               "dataTags": [                   {                       "name": "tag1",                       "id": "127000000002"                   },                   {                       "name": "tag2",                       "id": "127000000001"                   },                   {                       "name": "tag3",                       "id": "127000000000"                   }               ],               "referencedBy": [                   {                       "name": "lineitem5",                       "id": "206000000005"                   }               ],                  "parent": {                   "name": "lineitem5",                   "id": "206000000005"               },               "readAccessDriver": {                   "name": "lineitem2",                   "id": "206000000003"               },               "writeAccessDriver": {                   "name": "lineitem2",                   "id": "206000000003"               },                              "formula": "3 + 9",               "format": "NUMBER",               "formatMetadata": {                   "dataType": "NUMBER",                   "minimumSignificantDigits": 4,                   "decimalPlaces": -1,                   "negativeNumberNotation": "MINUS_SIGN",                   "unitsType": "NONE",                   "unitsDisplayType": "NONE",                   "zeroFormat": "ZERO",                   "comparisonIncrease": "GOOD",                   "groupingSeparator": "COMMA",                   "decimalSeparator": "FULL_STOP"               },                              "summary": "Sum",               "timeScale": "Month",               "timeRange": "timeRange1",                           "formulaScope": "All Versions",               "style": "Normal",               "code": "code7",               "notes": "note1"     }        ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-all-line-item-metadata-in-a-model-961428f6-aa1e-4149-8961-6a8a65c14004&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top