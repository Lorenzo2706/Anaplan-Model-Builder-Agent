---
title: "Retrieve metadata for dimensions on a view"
source: "https://help.anaplan.com/retrieve-metadata-for-dimensions-on-a-view-1a2da490-553a-4949-ba01-b8584e6abb4f"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the name, IDs, and lists of names for the dimensions (columns, pages, rows) on a specified view."
tags:
  - "clippings"
---
Use this call to retrieve the name, IDs, and lists of names for the dimensions (columns, pages, rows) on a specified view.

This helps an integration understand the structure of a view before reading its data, including which dimensions define the rows, columns, and pages.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html)
- If a view has no dimensions on an axis, the call omits the axis field (for example, no `"rows"` field at all instead of `"rows": []`)
- If a view is the default view, its `name` is set to be the same as the module name
- The `viewId` in this request can also be replaced by any valid `lineItemId`. If the Line Item has a changed dimensionality (has a Subsidiary View), the response returns the metadata applicable to that line item. Otherwise, the response returns the default metadata

You can use this API call to [map dimensions to cell data export headers](https://help.anaplan.com/43cd0223-edaa-4289-9833-eb9b73666aac-Map-dimensions-to-cell-data-export-headers) or [transform grid CSV format to tabular single column format](https://help.anaplan.com/c8a665b9-6b23-4254-ac68-816657a6e878-Retrieve-the-view-metadata-and-grid-view-data).

GET

`/models/{modelId}/views/{viewId}`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{viewId}` | - Required - Type: Number - Description: the ID for the view - Example: `102000000000` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/view"     },     "status": {       "code": 200,       "message": "Success"     },     "viewName": "REV01 Price Book",     "viewId" : "102000000000"     "rows": [       {         "id": "101000000000",         "name": "Products"       },       {         "id": "101000000003",         "name": "Regions"       }     ],     "columns": [       {         "id": "101999999999",         "name": "Line items"       }     ],     "pages": [       {         "id": "101000000001",         "name": "Versions"       }     ],   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-metadata-for-dimensions-on-a-view-1a2da490-553a-4949-ba01-b8584e6abb4f&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top