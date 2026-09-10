---
title: "Retrieve cell data for a view"
source: "https://help.anaplan.com/retrieve-cell-data-for-a-view-677b9c88-5e95-4b9a-a9eb-9e78c00cbcb8"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the cell data for a view. You can either query for the default page, or provide page selectors to query for other pages. This call returns data in either a CSV grid response or as JSON."
tags:
  - "clippings"
---
Use this call to retrieve the cell data for a view. You can either query for the default page, or provide page selectors to query for other pages. This call returns data in either a CSV grid response or as JSON.

This supports lightweight data reads where a full bulk export is unnecessary, such as previewing values, validating mappings, or retrieving small targeted datasets.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- This call only supports the retrieval of cells from a view that contains a maximum of 1,000,000 cells. If the specified view contains more than 1,000,000 cells, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the cells. Use the [quick sum bar](https://help.anaplan.com/cb15ce25-b344-4a61-8b02-cd21bc5bfca3) in Anaplan to identify the number of cells in a view.
- If you call several times in a short amount of time, you may receive a `429` response.
- You can replace the `viewId` with any valid `lineItemId`. If the line item has a subsidiary view, the response returns the data as seen in that subsidiary view.
- For line items without a subsidiary view, the response returns data for the default view of the line item.

The first line of the CSV response contains the values of the page selectors. The response omits this line when there are no dimensions on pages. When there are multiple dimensions on columns, a line for each dimension follows the first line that contains the values of the page selectors. When there are multiple dimensions on rows, a column displays on the left, before the data, for each dimension on rows. You can export the CSV data in different layouts by passing two query parameters exportType and moduleId together.

To receive a JSON-formatted response instead of a CSV-formatted response:

1. Pass an `Accept` header of `application/json`.
2. Pass a query parameter with format set to `v1`.

All other parameters are the same as a CSV-formatted response.

The response returns `Content-Type` `application/json` with this format:

- A `pages` key with a value that is a list of the selected items for each page selector. If no page selectors exist for this view, the list displays as empty or absent.
- A `columnCoordinates` key with a value that is a list of the coordinates for all values in that column. Each list item is itself a list containing one or more values. The length of each list equals the number of dimensions on the columns.
- A `rows` key with a value that is a list of row objects. Each row object contains:
- A `rowCoordinates` key with a value that is a list of the coordinates for all values in the current row. Each list item is itself a list that contains one or more values. The length of each list equals the number of dimensions on the rows.
- A `cells` key with a value, which is a list of all the cell values in the current row. To get the full coordinates for each cell, use the position of the cell value in the `cells` list, and find the column coordinates at the same position in the `columnCoordinates` list. Then, to specify the cell, uniquely, combine the column coordinates with the `rowCoordinates` for the current row and any selected pages.

GET

`/models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1`

| **Parameter** | **Required** | **Type** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| `{modelId}` | Required | String | The model ID | `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | Required | Number | The view ID | `102000000000` |
| `pages` | Optional | Multi-valued, colon-separated | The page selector values that identify the page to retrieve | `pages=101000000026:330000000028,20000000012:587000000000` or `pages=101000000026:330000000028&pages=20000000012:587000000000` |
| `{dimensionId}` | Optional | Number | The dimension ID | `20000000003` |
| `{itemId}` | Optional | Number | The item ID | `5438900031` |
| `format` | See Description | See Description | Valid only when you query for JSON. Can currently only be set to `v1`. | `v1` |
| `exportType` | See Description | See Description | Required with `{moduleId}` when you export data in the following layouts: `TABULAR_SINGLE_COLUMN` and `TABULAR_MULTI_COLUMN`. | `GRID_CURRENT_PAGE`, `GRID_ALL_PAGES`, `TABULAR_SINGLE_COLUMN` and `TABULAR_MULTI_COLUMN` |
| `{moduleId}` | See Description | See Description | ID of the parent module of the view. Required with `exportType` |  |
| `{maxRows}` | Optional | Number | Limits the number of exported rows to `{maxRows}` not including the header |  |

`curl -X GET   'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1' \    -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

Content-Type: `text/csv`

`  | Yesterday   |            |         |        |        |         |         |         |         |         |         |         |             |            | Apples  | Apples | Apples | Bananas | Bananas | Bananas | Carrots | Carrots | Carrots |         |             |            | English | French | German | English | French  | German  | English | French  | German  |         | Line item 1 | Baguette   | 1       | 2      | 3      | 5       | 6       | 7       | 9       | 10      | 11      |         | Line item 1 | Large loaf | 12      | 13     | 14     | 15      | 16      | 17      | 18      | 19      | 20      |         | Line item 1 | Small loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |         | Line item 2 | Baguette   | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |         | Line item 2 | Large loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |         | Line item 2 | Small loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |`

Content-Type: `application/json`

`{           "pages": [ "Value", "23mm" ],           "columnCoordinates": [ ["Jan 13"], ["Feb 13"], ["Mar 13"], ["Q1 FY13"], ["Apr 13"], ["May 13"], ["Jun 13"], ["Q2 FY13"], ["H1 FY13"], ["Jul 13"], ["Aug 13"], ["Sep 13"], ["Q3 FY13"], ["Oct 13"], ["Nov 13"], ["Dec 13"], ["Q4 FY13"], ["H2 FY13"], ["FY13"] ],           "rows": [             {               "rowCoordinates": [ "Durham" ],               "cells": [                 "64.6", "57.94", "108.36", "230.97", "173.46", "321.17", "398.7", "893.43", "1124.3", "433.05", "435.52", "421.46", "1290.03", "300.11", "150.53", "70.23", "520.87", "1810.9", "2935.3"               ]             },             {               "rowCoordinates": [ "Newcastle upon Tyne" ],               "cells": [                 "96.33", "92.69", "136.24", "325.27", "234.81", "468.96", "489.6", "1193.38", "1518.65", "535.86", "531.8", "542.6", "1610.25", "346.22", "171.65", "84.72", "602.6", "2212.85", "3731.5"               ]             },             {               "rowCoordinates": [ "Sunderland" ],               "cells": [                 "57.06", "63.73", "56.33", "177.13", "124.52", "236.29", "286.86", "647.67", "824.8", "301.15", "302.13", "299.61", "902.9", "145.01", "115.58", "65.05", "325.65", "1228.55", "2053.35"               ]             }           ]         }`

In a JSON-formatted response, the system will perform substitutions to these invalid characters:

| **Character in JSON** | **Meaning** | **Replaced by** |
| --- | --- | --- |
| \\b | backspace | \\\\b |
| \\t | tab | \\\\t |
| \\n | new line | \\\\n |
| \\f | newline+space | \\\\f |
| \\r | carriage return | \\\\r |
| " | double quote | \\\\ |
| / | forward slash | \\/\\ |
| \\ | backslash | \\\\\\ |

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-cell-data-for-a-view-677b9c88-5e95-4b9a-a9eb-9e78c00cbcb8&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top