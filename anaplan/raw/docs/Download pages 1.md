---
title: "Download pages"
source: "https://help.anaplan.com/download-pages-930acac9-c2b6-49ff-ac84-7b089a98d1ba"
author:
published:
created: 2026-09-09
description: "Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items."
tags:
  - "clippings"
---
Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items.

This enables large datasets to be retrieved in manageable chunks, supporting retry logic and more reliable processing.

You can download pages while the export is in progress. You can download up to `availablePages` number of pages returned by the export status API. Note that page numbers start with zero. That means if 10 pages are available, you can download from page=0 through page=9.

**Note:** Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).

`curl --{location} \   -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}/pages/{pageNo}' \   -H 'Authorization: AnaplanAuthToken{anaplan_auth_token}' \   -H 'Accept: text/csv'`

GET

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}/pages/{pageNo}`

| **Parameters** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |
| `{pageNo}` |  |

`curl --{location} \   -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}/pages/{pageNo}' \   -H 'Authorization: AnaplanAuthToken{anaplan_auth_token}' \   -H 'Accept: text/csv'`

`,Parent,Write,Read,Code,favourite,count   cake,,"gord.like@anaplan.com, adam.minister@anaplan.com",,c1,true,1   bread,,,adam.minister@anaplan.com,b2,false,4   pastry,,gord.like@anaplan.com,,p3,true,5`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fdownload-pages-930acac9-c2b6-49ff-ac84-7b089a98d1ba&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top