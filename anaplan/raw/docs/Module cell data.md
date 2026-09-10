---
title: "Module cell data"
source: "https://help.anaplan.com/module-cell-data-b7c91527-989e-429b-87a5-8a1b1532ecc4"
author:
published:
created: 2026-09-09
description: "Module cell data requests are mainly used to update cell values directly in a module, rather than using a file-based import."
tags:
  - "clippings"
---
Module cell data requests are mainly used to update cell values directly in a module, rather than using a file-based import.

This endpoint provides targeted, transactional write access to module cell data. You use it to determine if it is possible to update specific cells in an Anaplan module directly.

Ensure the request body is an array of `CellWrite` objects (see below). Each object is for an updated individual cell and its full set of dimensions.

The response contains a summary of the number of cells updated successfully and the details of why some cells that could not be updated.

**Notes:**

- Ensure the user has write access enabled.
- Ensure the request includes all of the required fields.
- Ensure the request has a `value` field that is either a string, number or boolean and is compatible with the line item format/data type.
- If one cell cannot update, the other cells in the request still continue to update.
- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- Workspace administrators can import data into any cell (except aggregate cells, see below), including read-only and invisible cells.
- You can update a maximum of 100,000 cells or 15 MB of data (whichever is lower), in a single API call. For larger scale payloads, we recommend you use the [import API](https://anaplanbulkapi20.docs.apiary.io/#reference).
- Write cell data does not apply to aggregate cells.
	- An aggregate cell is a cell where one of its dimension items has it’s own child items
		- This includes aggregate cells for line Items with breakback enabled
		- For a line Item that is dimensioned by a composite list, the only writeable cells are the child items, that are defined directly in the dimension list and not defined in a parent list.

Each `CellWrite` Object is a request to set a value in a cell. A cell is identified by the line item it belongs to as well as an item for each of the dimensions that apply to the line item (this includes **Time** and **Versions**).

This table details the fields that are in a cell write object:

| **Field** | **Details** |
| --- | --- |
| `lineItemId` | - Required - Ensure you specify a `lineItemId` or `lineItemName` Description: The ID of the line item that belongs to the module |
| `lineItemName` | - Ensure you specify a `lineItemId` or `lineItemName` - Description: The name of the line item that belongs to the module |
| `dimensions` | - This field can be omitted if the line item is a single cell without any dimensions applied to it. - Description: An array of dimension coordinates |
| `dimensionId` | - Required   	Ensure you specify a `dimensionId` or `dimensionName` - Description: The ID of the dimension that is on the line item |
| `dimensionName` | - Ensure you specify a `dimensionId` or `dimensionName` - Description: The name of the dimension that is on the line item |
| `itemId` | - Required - Description: The ID of the dimension item that is on the dimension |
| `itemName` | - Ensure you specify a `itemId`, `itemName` or `itemCode` - Description: The name of the item on the dimension |
| `itemCode` | - Ensure you specify a `itemId`, `itemName` or `itemCode` - Description: The name of the item on the dimension |
| `value` | - Required - Description: The value to set for the cell - Cannot be `null` |

There are multiple formats for line items. Ensure the value specified in the value field aligns with the line item format. Below is a table of the different line item formats we support and examples of values you can use:

| **Line Item Format** | **Details** |
| --- | --- |
| `Number` | - Can be specified as a number with or without quotes - Example: `"value": 123.45` or `"value": "123.45"` - Only string specified values that are parsed successfully can be written to. |
| `Text` | - Specified as a string - Example: `"value": "Text to set"` |
| `Boolean` | - Specified as a boolean - Example: `"value": true` or `"value": false` |
| `Date` | - Specified as a string - Ensure you specify the year in the `YYYY-MM-DD` format where Y = “year”, M = “month” and D = “date of month” - Example: `"value": "2020-12-31"` |
| `Time Period` for example, `Week`, `Month`, `Quarter`, `Half-Year` or `Year` | - Specified as a string - Ensure you specify the time period as a label (see View in the UI) - Example: `"value": "Week 1 FY20" for Week`, `"value": "Dec 20"` for `Month`, `"value": "Q1 FY20"` for `Quarter`, `"value": "H1 FY20"` for `Half-Year` and `"value": "FY20"` for `Year` |
| `List` (list-formatted Line Item) | - Specified as a string - Ensure you specify the string as the name of an entity from the list that is configured for this line item - Example: If the list configured for this line item is `Countries` which contains `UK` as an item then a valid value would be `"value": "UK"` |

For more information on Javascript primitive types see:

[https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data\_structures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures)

POST

`/models/{modelId}/modules/{moduleId}/data`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the supported request - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the dimension ID. This value must be the ID for any of these dimension types: 	- Lists 		- Time periods 		- Users 		- Versions - Example: `101000000001` |

`curl -X POST 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/data' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\   -H 'Accept: application/json'   -H 'Content-Type: application/json'   --data-raw '<see_below>'`

A successful response is in `Content-Type: application/json` format:

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/writeCellDataResponse"     },     "status": {       "code": 200,       "message": "Success"     },     "numberOfCellsChanged": 42,     "failures": [         {             "requestIndex": 0,             "failureType": "cellIsCalculated",             "failureMessageDetails": "the cell is a calculated/aggregate cell and is not writeable"         },         {             "requestIndex": 9,             "failureType": "cellIsInvalid",             "failureMessageDetails": "the cell could not be found or resolved"         }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fmodule-cell-data-b7c91527-989e-429b-87a5-8a1b1532ecc4&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top