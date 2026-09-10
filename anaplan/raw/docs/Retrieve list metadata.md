---
title: "Retrieve list metadata"
source: "https://help.anaplan.com/retrieve-list-metadata-13c7d130-2db0-4c31-b2b1-0928a7b32cf4"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve metadata for a specified list."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

This helps confirm that the integration is targeting the correct list and understand its structure before working with its items.

| **Metadata** | **Description** |
| --- | --- |
| `category` | The category to which the list is assigned. |
| `dataTags` | The data tags associated with the list. |
| `displayNameProperty` | If present it indicates the name of the property set on the list. |
| `hasSelectiveAccess` | If the value is true, this list uses [selective access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html). |
| `id` | The list ID. This corresponds to the `listId` parameter. |
| `itemCount` | The number of list items present in the list. |
| `managedBy` | Not currently used. |
| `name` | The list name. |
| `nextitemIndex` | Contains the index of the next new item in the list. Used only by numbered lists. |
| `numberedList` | A true value indicates this is a numbered list. |
| `parent` | The parent hierarchy, which includes this information for the parent list:  - `id` - `name` |
| `permittedItems` | Indicates how many more items you can add to the existing list. This value changes when the number of items in the list change. |
| `productionData` | A true value indicates this is a production list in [Application Lifecycle Management (ALM)](https://help.anaplan.com/anapedia/Content/ALM/Application_Lifecycle_Management.htm). |
| `properties` | The list properties, which include:  - `dataTags` - `format` - `formula` - `notes` - `referencedBy` |
| `subsets` | A list of subsets associated with the list hierarchy, which includes the following information for the parent list:  - `id` - `name` |
| `topLevelItem` | If present, indicates the top level item in a hierarchy. |
| `useTopLevelAsPageDefault` | A true value indicates this list is the default item in a page selector. |
| `workflowEnabled` | A true value indicates this list is enabled for [Workflow](https://help.anaplan.com/anapedia/Content/Modeling/Manage_Models/Workflow.html). |

If any of the metadata values are not set for a list (for example, no parent or no top-level item), then the result omits the metadata entry.

**Note**: To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

GET

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: string - Description: The list ID. - Example: `101000000001` |

`curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}' \   -H 'Accept: application/json' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/models/102B/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "metadata": {           "id": "101000000001",           "name": "Sales Reps",           "properties": [               {                   "name": "Salesforce",                   "format": "TEXT",                   "notes": "",                   "referencedBy": ""               },               {                   "name": "Mail",                   "format": "TEXT",                   "notes": "",                   "referencedBy": ""               }           ],           "hasSelectiveAccess": false,           "parent": {               "id": "101000000000",               "name": "Organization"           },           "managedBy": "",           "numberedList": false,           "useTopLevelAsPageDefault": false,           "itemCount": 1,           "workflowEnabled": false,           "productionData": false       }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-list-metadata-13c7d130-2db0-4c31-b2b1-0928a7b32cf4&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top