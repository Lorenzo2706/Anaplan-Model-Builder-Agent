---
title: "Download pages"
source: "https://help.anaplan.com/download-pages-a5f7505d-acc0-4039-8738-eb9aa2cdf9a3"
author:
published:
created: 2026-09-09
description: "Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items."
tags:
  - "clippings"
---
Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items.

This enables large datasets to be retrieved in manageable chunks, reducing the risk of timeouts or oversized responses.

You can download pages while the export is in progress. You can download up to `availablePages` number of pages returned by the export status API.

Note that page numbers start with zero. That means if 10 pages are available, you can download from page=0 through page=9.

**Note:**

- To use this call, you must be a [**Workspace Administrator**](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use the [**Delete read requests**](https://help.anaplan.com/71a6b2da-008c-40e7-ba05-103730de30b2) call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.

GET

`/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}/pages/{pageNo}`

| **Header** | **Details** |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token. |
| `Accept: text/csv` | - Required - Description: This indicates the preferred response is `text/csv` format. |

| **Query** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe`. |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F`. |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001`. |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC`. |
| `{pageNo}` | - Required - Type: `Number` - Description: The page number (starting from 0) - Example: `0` |

`curl --{location} \   -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}/pages/{pageNo}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: text/csv'`

`Pasta,Line Items,Jan 17,Feb 17,Mar 17,Q1 FY17,Apr 17,May 17,Jun 17,Q2 FY17,Jul 17,Aug 17,Sep 17,Q3 FY17,Oct 17,Nov 17,Dec 17,Q4 FY17,FY17   Corn,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Corn,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Corn,Owner,,,,,,,,,,,,,,,,,   Whole Wheat,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Whole Wheat,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Whole Wheat,Owner,,,,,,,,,,,,,,,,,   Lentil,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Lentil,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Lentil,Owner,,,,,,,,,,,,,,,,,   Millet,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Millet,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Millet,Owner,,,,,,,,,,,,,,,,,   Rice,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Rice,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   Rice,Owner,,,,,,,,,,,,,,,,,   Lasagne,Cost,21.33,21,18.25,60.58,22.35,16.69,23.21,62.25000000000001,18.68,19.94,20,58.620000000000005,23.1,24.64,23.43,71.17,252.62   Lasagne,Weight,6,5,7,18,0,0,0,0,0,0,0,0,0,0,0,0,18`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fdownload-pages-a5f7505d-acc0-4039-8738-eb9aa2cdf9a3&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top