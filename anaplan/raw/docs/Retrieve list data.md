---
title: "Retrieve list data"
source: "https://help.anaplan.com/retrieve-list-data-2309ce30-9f81-40d4-a7c3-473a8ff60667"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve list data for the items in a specified list."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

This supports validation, mapping, reconciliation, or downstream use of list members such as products, employees, regions, accounts, or cost centers.

You can filter on optional fields by setting the `includeAll` query parameter.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- This call only supports the retrieval of list data up to 1,000,000 records. If the specified list contains more than 1,000,000 records, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the records.

The following list data always displays in the query response.

| **Default List Data** | **Description** |
| --- | --- |
| `id` | The Anaplan ID of the item in the list. |
| `name` | The name of the item in the list. |
| `code` | The code value for an item in the list (if specified) |
| `parent` | The name of the parent item in the list. |
| `parentId` | The Anaplan ID of the parent item in the list. |
| `listId` | The Anaplan ID of the list to which the parent item belongs. This ID displays if the list has a **Parent Hierarchy** set under the **Configure** tab in Anaplan. |
| `listName` | The name of list to which the parent item belongs. The name displays if the list has a **Parent Hierarchy** set under the **Configure** tab in Anaplan. |

Set the `includeAll` query parameter to true to display the following optional list data fields in the response.

| **Optional List Data** | **Description** |
| --- | --- |
| `write` | If [Selective Access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698) is enabled for the list, you can add individual users to provide `write` access. Users with `write` access can view and edit data associated with the list items. |
| `read` | If [Selective Access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698) is enabled for the list, you can add individual users to provide `read` access. Users with `read` access can view the data associated with the list items but not edit it. |
| `subsets` | If the value of the subset column is true, the associated item belongs to that subset. You can view subsets under **Subsets** tab in Anaplan. |
| `properties` | The value of each custom list property. |

GET

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?includeAll=true`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: string - Description: determines if optional query fields should display in the response.   	When true, the endpoint returns all the data, including optional fields for the specified list ID.   	When false, the endpoint does not include the optional data fields in the response for the specified list ID. - Example: `101000000001` |

| **Parameter** | **Details** |
| --- | --- |
| `includeAll` | - Optional - Type: Boolean - Example: `?includeAll=True` |

`curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?includeAll=true' \   -H 'Accept: application/json' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "listItems": [         {           "id": "206000000001",           "name": "cake",           "code": "c1"         },         {           "id": "206000000002",           "name": "bread",           "code": "b2"         },         {           "id": "206000000003",           "name": "pastry",           "code": "p3"         }       ]     }`

`id,name,code,parent,parentId,listId,listName   206000000001,cake,c1,,,,   206000000002,bread,b2,,,,   206000000003,pastry,p3,,,,`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "listItems": [         {           "id": "206000000001",           "name": "cake",           "code": "c1",           "subsets": {             "favourite": true           },           "properties": {             "count": "1.0"           }         },         {           "id": "206000000002",           "name": "bread",           "code": "b2",           "subsets": {             "favourite": false           },           "properties": {             "count": "4.0"           }         },         {           "id": "206000000003",           "name": "pastry",           "code": "p3",           "subsets": {             "favourite": true           },           "properties": {             "count": "5.0"           }         }       ]     }`

`id,name,code,parent,parentId,listId,listName,favourite,count   206000000001,cake,c1,,,,true,1.0   206000000002,bread,b2,,,,false,4.0   206000000003,pastry,p3,,,,true,5.0`

Back to top