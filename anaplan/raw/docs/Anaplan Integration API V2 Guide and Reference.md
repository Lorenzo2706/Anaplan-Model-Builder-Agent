---
title: "Anaplan Integration API V2 Guide and Reference"
source: "https://anaplan.docs.apiary.io/#/reference/workspaces"
author:
  - "[[Apiary]]"
published:
created: 2026-10-23
description: "A place where APIs are kept."
tags:
  - "clippings"
---
### Introduction

> ### ⚠️ Service Sunset Notice
> 
> **Please Note:** This service is scheduled to be decommissioned by **October 31, 2026**.
> 
> To ensure uninterrupted access to this content, please update your bookmarks and refer to the official documentation on **[Anapedia](https://help.anaplan.com/844c6d40-a21c-423d-8435-ebaaa0372b76)**.

---

This section contains an introduction to using the latest version of the Anaplan Integration API (v2.0). See the Reference section for the API Reference.

**Notes**: If you are looking for the v1.3 documentation, please refer to [this page](https://anaplanapiv13.docs.apiary.io/).

#### URL, IP, and allowlist requirements

To set your allowlists for API calls, see: [URL, IP, and allowlist requirements](https://support.anaplan.com/url-ip-and-allowlist-requirements-c8235c7d-8af2-413b-a9ff-d465978806b9)

## Transactional API Index

To learn more about when to use Transactional APIs see [Transactional or Bulk: When to use which API?](https://community.anaplan.com/discussion/128878/transactional-or-bulk-when-to-use-which-api)

[Workspaces](#Workspaces)

- [List user workspaces](#ListUserWorkspaces)
- [Retrieve workspace information](#RetrieveWorkspaceInfo)

[Models](#Models)

[Line Items](#LineItems)

- [Retrieve dimension Ids for a line item](#RetrieveDimensionIdsLineItem)
- [Retrieve all line items in a model](#RetrieveAllLineItemsModel)
- [Retrieve all line item metadata in a model](#Retrievealllineitemmetadatainamodel)
- [Retrieve all line item metadata in a module](#Retrievealllineitemmetadatainamodule)

[Other Model Metadata](#OtherModelMetadata)

- [Lookup dimension items by name or code](#LookupDimensionItemsNameCode)
- [Retrieve all items in a dimension](#RetrieveItemsDimension)
- [Retrieve selected items in a dimension](#RetrieveSelectedItemsDimension)

[Read module, view metadata and limited volume cell data](#ModuleAndViewData)

- [Retrieve Ids and names for all modules in a model](#RetrieveIDNamesModuleModel)
- [Retrieve Ids and names for all views in a model](#RetrieveIDNamesViewsModel)
- [Retrieve Ids and names for views in a module](#RetrieveIDsNamesViewsModule)
- [Retrieve metadata for dimensions on a view](#RetrieveMetadataDimensionView)
- [Retrieve cell data for a view](#RetrieveCellDataView)
- [Retrieve all line items in a module](#RetrieveAllLineItemsModule)
- [Retrieve dimension items for a line item](#RetrieveDimensionsLineItem)

[Read large volume view data](#ReadLargeVolumeViewData)

- [Initiate large read request](#InitiateLargeReadRequestVD)
- [Retrieve status of large read request](#RetrieveStatusLargeReadRequestVD)
- [Download pages](#DownloadIntermediateExportFileStoreVD)
- [Delete read requests](#DeleteReadRequestsVD)

[Update module cell data](#UpdateModuleCellData)

- [Write cell data to module by coordinate or name](#WriteCellDataByCoordinateorName)

[Model lists](#Lists)

- [Retrieve lists](#RetrieveLists)
- [Retrieve list metadata](#RetrieveListMetadata)
- [Retrieve list data](#RetrieveListData)
- [Add list items](#AddListItems)
- [Update list items](#UpdateListItems)
- [Delete list items](#DeleteListItems)
- [Reset list index](#ResetListIndex)

[Read large volume list item data](#ReadLargeVolumeListItemData)

- [Preview large data list read](#PreviewLargeDataListRead)
- [Initiate large read request](#InitiateLargeReadRequest)
- [Retrieve status of large read request](#RetrieveStatusLargeReadRequest)
- [Download pages](#DownloadIntermediateExportFileStore)
- [Delete read requests](#DeleteReadRequests)

[Model Calendar](#ModelCalendar)

- [Retrieve current period](#RetrieveCurrentPeriod)
- [Set current period](#SetCurrentPeriod)
- [Get current fiscal year](#GetCurrentFiscalYear)
- [Update current fiscal year](#UpdateCurrentFiscalYear)

[Model versions](#ModelVersions)

- [Retrieve version metadata](#RetrieveVersionMetadata)
- [Set version switchover date](#SetVersionSwitchoverDate)

[Users](#Users)

- [Retrieve your user](#RetrieveYourUser)
- [Retrieve user information](#RetrieveUserInformation)
- [Retrieve user list](#RetrieveUserList)

## Bulk API Index

To learn more about when to use Bulk APIs see [Transactional or Bulk: When to use which API?](https://community.anaplan.com/discussion/128878/transactional-or-bulk-when-to-use-which-api)

[Upload Files for Actions](#Upload-files)

- [Get the ID and information for the model file to upload](#GetIdInfoModelUpload)
- [Set the chunk count](#SetChunkCount)
- [Upload file as a single chunk](#UploadFileSingleChunk)
- [Upload a file in chunks](#UploadAFileInChunks)
- [Complete the upload](#CompleteTheUpload)

[Import Actions](#Import)

- [Get the import ID](#GetImportID)
- [Start the import](#StartTheImport)
- [Get a list of the import tasks](#GetListImportTasks)
- [Monitor the import tasks](#MonitorImportTasks)
- [Check dump file for failures](#CheckDumpFile)
- [Download dump file chunks](#DownloadDumpFileChunks)
- [Get the metadata for an import definition](#GetMetadataImportDefinition)

[Export Actions](#Export)

- [List the available export definitions as a JSON array](#ListExportDefinitions)
- [Get the metadata for an export definition](#GetMetadataExportDefinition)
- [Start the export](#StartTheExport)
- [Monitor the export tasks](#MonitorExportTasks)
- [Download exported data](#DownloadExportedData)

[Completion, failure, and data error/warning codes for import and export actions](#CompletionFailureAndDataErrorWarningCodes)

[Retrieve logs](#Logging)

[Download Files for Actions](#Download-files)

- [Get the list of export files](#GetListExportFiles)
- [Get the chunks in a file](#GetTheChunksInAFile)
- [Get the data in a chunk](#GetDataInAChunk)
- [Delete files](#DeleteFiles)

[Get model actions](#Actions)

- [List model actions](#list-model-actions)
- [Retrieve metadata for model action](#retrieve-action-metadata)

[Delete Actions](#Delete)

- [List the actions in the model as a JSON array](#ListActionsInAModel)
- [Start deletion](#StartDeletion)
- [Monitor the deletion tasks](#MonitorDeletionTasks)

[Process Actions](#Process)

- [List the process definitions available in a model as a JSON array](https://anaplan.docs.apiary.io/ListProcessDefinitions)
- [Retrieve metadata for a process](#RetrieveMetadataProcess)
- [Start the process](#StartTheProcess)
- [Monitor the process tasks](#MonitorTheProcessTasks)
- [Check dump file for failures](#CheckDumpFileForFailures)

## API use requirements

As a best practice for using our APIs, you should be familiar with RESTful APIs, command-line interfaces such as [cURL](https://curl.se/docs/ "cURL"), and exploratory API tools similar to Postman. Each endpoint in this document is described with its required request header and body elements, which enables users to carry out the call.

## What can I do with the API?

You can use the Anaplan RESTful API to carry out these actions:

| Action | Description |
| --- | --- |
| [Import](#Import) | Bring data into Anaplan. |
| [Download Files](#Download-files) | Download files from Anaplan. For instance, you can download files created during an export or download files that were uploaded. |
| [Export](#Export) | Get data from Anaplan. |
| [Get model actions](#Actions) | List actions and get metadata on individual actions. |
| [Delete](#Delete) | Automates the "Delete from List using Selection" feature for the removal of specific items from a list. Within the Anaplan graphical user interface, this type of action belongs to "Other actions". |
| [Process](#Process) | Container for multiple actions to be executed in a specific sequence. The actions can be any combination of imports, exports, and deletes. |
| [Upload Files](#Upload-files) | Upload files to Anaplan. For instance, you can upload a file and then import its data into Anaplan. |
| [Users](#Users) | Get information about the workspaces and models to which your Anaplan user has access. |

To carry out an import:

- You must have a file to be imported to Anaplan and know where it is in the file system.
- You must know the workspace ID and model ID of your Import definition.

## Getting Started

This section contains general information to help you start using the Anaplan API.

## Implementation considerations

When integrating with our API, clients must not assume the response fields are fixed and should write their parsers to gracefully ignore unknown or extra fields.

## Authentication

**Note**: If your workspace uses single sign-on (SSO), your user must be assigned as an Exception User to use basic authentication and obtain an Anaplan authentication token. For more information on exception users in Anaplan, see [Assign Exception Users](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Security/Single_Sign-on/Enforcing_SAML_Authentication.html "Assign Exception Users") in Anapedia.

To use this API, you must send requests using an Anaplan authentication token. This is in the form of a JSON Web Token. This must be in the Authorization header of the API request. For example: `Authorization:AnaplanAuthToken {anaplan_auth_token}` Where `{anaplan_auth_token}` is replaced with your authentication token. For more information, see [Authentication Service API](https://anaplanauthentication.docs.apiary.io/ "Authentication Service API")

## Data encryption

All Anaplan API communication happens over HTTPS with 2048-bit certificates, which provides for data encryption in transit using Transport Layer Security (TLS) 1.3. TLS 1.2 is still supported.

## TLS support in integration clients

When you build integrations with Anaplan APIs, ensure your integrations are built to use TLS 1.3. Anaplan APIs do not support TLS 1.1.

## Definitions

### Dimension

A dimension is a data item, measure, or characteristic that you can calculate or manipulate. Dimensions enable you to answer business questions, observe trends, or assess *What If* situations for planning purposes.

### List

Lists are groups of related items, such as people in a department, products on a shopping list, or the regions comprising a geographic area. They are fundamental to Anaplan as they define the structure and content of a model.

Lists are a type of dimension.

## HTTP Verbs

To carry out actions using the Anaplan API, you can use these HTTPS verbs.

| Verb | Description |
| --- | --- |
| DELETE | Deletes a resource. In this API you can DELETE a file that was uploaded or exported and you can DELETE tasks that you want to cancel. |
| GET | Retrieves a list of resources. |
| POST | Creates or updates a resource. In this API, you can POST an update to the metadata of file (such as its chunkCount), and you can POST the tasks for an import, export, process, or delete action, and the task ID is returned. |
| PUT | Updates a resource. In this API, you can PUT the chunks of a file for import. |

## cURL Examples

This API Reference includes [cURL](https://curl.haxx.se/ "Learn about cURL") examples and responses.

If you want to ensure that the response to a curl request includes the HTTP request headers, include the optional verbose flag `-v` or `--verbose`.

To view an example cURL request and server response:

1. Click an item in the Reference section of the navigation pane on the left.
2. Click a colored textbox in the middle pane.
3. In the example that appears, select cURL from the drop-down nearest the Try button.

**Note:** Anaplan has not set up a live server for use through this Apiary website. If you have credentials, you can use the examples in this help system as a guide when sending requests to the server that Anaplan has provided.

## HTTP responses

Anaplan APIs return HTTP responses in the `2XX`, `4XX`, and `5XX` categories.

- `2XX` responses indicate a success with the API call.
- `4XX` responses indicate an issue with the request. Check for mandatory request parameters. Then check the request parameters and body contain the appropriate values and types. There should be an error message in the response body to help diagnose the error.
- `429` responses can result from rate limiting or concurrent request limiting on some API calls. If you receive a 429 response, wait for a brief period and retry.

The table below displays the expected HTTP responses for Anaplan’s APIs.

| Status code | Meaning |
| --- | --- |
| `200 OK` | The request was successful. |
| `204 No Content` | The request was successful, but there’s no representation to return. This means that the response is empty. This is the expected response to a `POST` for tasks. |
| `400 Bad Request` | The request is incorrect in some way, perhaps specifying incorrect values, or missing some out. The `400 Bad Request` is accompanied by a clarifying message. |
| `401 Unauthorized` | Your user credentials are incorrect, or your token has expired. |
| `403 Forbidden` | Your user does not have permission to perform the requested action. |
| `404 Not Found` | The requested resource does not exist, or your user does not have permission to see it. |
| `405 Method Not Allowed` | Wrong HTTP verb for this call (for example, using `POST` or `PUT` to an call that only allows `GET`). |
| `406 Not Acceptable` | The data request is in a format the server cannot provide. Check the Accept header. |
| `409 Conflict` | An attempt to change a resource in a way that it cannot be changed. For example, if you attempt to add something that has already been added. |
| `410 Gone` | The requested resource, such as a workspace, has been moved. If you receive this response, try again. The request is rerouted and should succeed on a subsequent try. |
| `415 Unsupported Media Type` | The request body is in an unsupported format. Adjust to a supported format in the `Content-Type` header of your call. |
| `422 Model archived` | The model you are trying to access has been archived. Unarchive your model, then try your request again. |
| `423 Model locked` | The model you are trying to update is locked. Unlock the model and try the request again. |
| `424 Model offline` | The model you are trying to access is offline. Bring your model online, then retry your request. |
| `425 Model deployed` | The model you are trying to change is in deployed mode. Changes should be made to the development model. |
| `429 Too Many Requests` | You're making too many requests. Wait and try your request again. |
| `500 Internal Server Error` | Error processing the request. |
| `502 Bad Gateway` | Network problems. |
| `503 Service unavailable` | Service unable to accept the request. |
| `504 Gateway Timeout` | Network problems. |

## Chaining Parameters

Many endpoint paths contain a chain of parameters that you can build step-by-step. For example, to get the status of an import task, you might use something like this: `/workspaces/{workspaceID}/models/{modelID}/imports/{importID}/tasks/{taskId}`

In this example, you need to make this sequence of calls to get the Ids required to get the status of the import task:

1. Log into Anaplan and click the `?` for help. Select `About` from the drop-down list.
2. From the About window, copy the `Workspace Id` and `Model Id` values.
3. Manually enter the `workspaceID` to use.
4. Manually enter the `modelID` to use.
5. GET the list of `imports` in the model.
6. Choose an `importID` from the list of imports.
7. POST the tasks for the import. This returns a `taskID`.
8. GET the status of the `taskID` for the import.

**Note:** If you already know some of the required Ids, you can skip those calls and only make calls for the Ids that you do not already know.

## API behavior when the model is busy

Due to ongoing model actions, automation, or even maintenance, your API call may behave differently, depending on whether the model is busy. The following actions will return information, even if the model is busy:

| Action type | Endpoints |
| --- | --- |
| Import action | - Get the import Id - Start the import - Get a list of the import tasks - Monitor the import tasks - Check dump file for failures - Download dump file chunks - Get the metadata for an import definition |
| Export action | - List the available export definitions as a JSON array - Get the metadata for an export definition - Start the export - Monitor the export tasks |
| Process action | - List the process definitions available in a model as a JSON array - Retrieve metadata for a process - Start the process - Monitor the process tasks - Check dump file for failures |
| Delete action | - List the actions in the model as a JSON array - Start deletion - Monitor the deletion tasks |

All other endpoints will wait for the model to be available again, before completing their run.

## API rate limitation

To make our API service more robust and resilient, there is a flat 600-requests-per-minute rate limit. That’s equivalent to 10 requests per second (RPS). Rate limiting helps us protect our API service and platform from attacks like distributed denial of service (DDoS) and other malicious actions. This practice improves resource utilization and raises quality of service for all our customers.

### How does rate limitation work?

The rate limit algorithm is based on a token bucket algorithm. This allows us to plan for a long-term number of customer requests, while permitting intermittent bursts of activity.

The algorithm works as follows:

- A token is added to the bucket every 60 seconds / 600 requests = 0.1 seconds
- When there are 600 tokens in the bucket, no more are added.
- Each request removes a token from the bucket.
- When the bucket is empty, requests are denied.
- The rate limit applies at the tenant level, so all workspaces in a single tenant share the same limit.

If your integration hits the RPS limit, you get a `429 Too Many Requests` error message. Once you reach the limit, you will need to wait for a period of time for a token to be added to the bucket — this time is returned in the `Retry-After` header of the `429` response.

In case of a `429` error, we recommend that you hardcode a 10 second timeout into your integration. If you have difficulties to stay within the rate limit, reach out to [Anaplan Support](https://support.anaplan.com/).

## Formats

Anaplan supports only `application/json` format for API requests and responses, but a file chunk is returned as a stream of binary data in the `application/octet-stream` format.

## Headers

Anaplan APIs only support the indicated headers for each endpoint.

## Pagination

If your API calls return a lot of data, you can specify that results are returned in pages. You can specify:

- A `limit` for the number of results to return per page.
- An `offset` to get a specific page of results starting from a particular result.
- An attribute on which to `sort` the results.

**Note:** Paging specifies the number of results returned by an API request in pages. This is not the number of pages in a file.

See [Display pages of results](#Display-pages-results).

## Parameter Types

These parameter types form the basis of calls you make with the Anaplan Integration API V2. Path parameters must follow their equivalent parameter without an ID. Typically, you can retrieve the strings or numbers used as parameters through other calls.

The parameters you can use to return information, such as about a workspace or model, apply to the [authenticated](https://anaplanbulkapi20.docs.apiary.io/#/introduction/getting-started/authentication) user's default tenant.

**Note:** All path parameters with a type of string are case sensitive. This means workspace Ids must be input in lowercase, for example `8a8b8c8d8e8f8g8i`, and model Ids must be input in uppercase, for example `75A40874E6B64FA3AE0743278996850F`, otherwise the object will not be recognized.

| Parameter | Path parameter | Path parameter type | Description |
| --- | --- | --- | --- |
| `workspaces` | `{workspaceId}` | string | Returns the IDs of, and information about, workspaces. Use the `{workspaceId}` path parameter to specify a single workspace.  You can also use these parameters in other calls to specify a workspace for the call to apply to.  Please note that `{workspaceId}` strings are case-sensitive and should be submitted in **lowercase**, for example `8a8b8c8d8e8f8g8i`. |
| `models` | `{modelId}` | string | Returns the IDs of, and information about, models. Use the `{modelId}` path parameter to specify a single model.  You can also use these parameters in other calls to specify a model for the call to apply to.  Please note that `{modelId}` strings are case-sensitive and should be submitted in **uppercase**, for example `FC12345678912343455667`. |
| `imports` | `{importId}` | number | Returns the IDs of, and information about, imports. Use the `{importId}` path parameter to specify a single import.  You can also use these parameters in other calls (typically including the *tasks* parameter) to specify an import. A failed import generates a dump file. |
| `exports` | `{exportId}` | number | Returns the IDs of, and information about, exports. Use the `{exportId}` path parameter to specify a single export.  You can also use these parameters in other calls (typically including the *tasks* parameter) to specify an export. |
| `files` | `{fileId}` | number | Returns the IDs of, and information about, files. Use the `{fileId}` path parameter to specify a single file.  You can also use these parameters in other calls to specify a file, often for an action, such as to delete or upload a file. |
| `chunks` | `{chunkId}` | string | Sets the number of, or interacts with, chunks in a file that you import or export.  Splitting a file into chunks enables you to continue an action from an intermediate point if it fails and you have to start again. We recommend that you set an import chunk size of between 1 MB and 50 MB. The default size is 10 MB, although the final chunk is smaller. |
| `processes` | `{processId}` | number | Returns the IDs of, and information about, processes. Use the `{processId}` path parameter to specify a single process. You can also use these parameters in other calls (typically including the *tasks* parameter) to specify an process.  A process can contain both imports and exports, which means it can result in a dump file generated through a failed import. |
| `actions` | `{actionId}` | number | Returns the IDs of, and information about, actions. |
| `task` | `{taskId}` | string | Returns the IDs of, and information about, tasks. A task is used, and a `{taskId}` generated, when you carry out an action such as an import, an export, a process, or a delete. The `{taskId}` is removed when the model is unloaded. For instance, a model is unloaded when all users log out.  A given task, such as an import action, might have two different IDs if you run the action again before the first `{taskID}` is removed from the server. |
| `dumps` | `{objectId}` | number | Returns the dump file, which contains information about failed imports.  The dump file contains a copy of each row that failed, along with a message about the failure. A file within the dump can have one or more chunks. Only an import can result in a dump file. |
| `user` | `{userId}` | string | Returns information about the authenticated user or other users in the workspace. This can be useful if you require user provisioning for the Salesforce.com Anaplan tab. |
| `pages` | `{pageNo}` | number | Specifies which pages of a read request to download. The {pageNo} path parameter specifies which page to start the download from. |
| `readRequests` | `{requestId}` | number | Initiates a read request for a large volume read of data. Use the {requestId} path parameter to specify a read request to perform an action with, such retrieving its status or deleting it. |

### Query parameters

Certain endpoints have query parameters that change the response. The detailed effects of these query parameters are explained in the documentation for each endpoint. The capitalization of each query parameter must match the table below.

| Query parameter | Possible values | Description |
| --- | --- | --- |
| `tenantDetails` | `true`, `false` | A Boolean query parameter. If true, the call response includes the estimated size of a workspace in bytes. |
| `includeAll` | `true`, `false` | A Boolean query parameter. If true, the call response includes additional information about the applicable line item or list. |
| `action` | `add`, `delete` | You can use this to add or delete list items in a call. |
| `showImportDataSource` | `true`, `false` | A Boolean query parameter. If true, the call response includes the ID and format of the import data source. |
| `includesubsidiaryviews` | `true`, `false` | A Boolean query parameter. If true, the call response includes subsidiary views. |
| `format` | `v1` | You can use this to return a JSON response instead of a CSV response when you retrieve cell data for a view. |
| `modelDetails` | `true`, `false` | A Boolean query parameter. If true, the call response includes additional information about a model such as memory usage, creation date, and recent changes. |
| `pages` | `{dimensionId}`, `{itemId}` | You can use this to specify which pages, or list items used as dimensions, to return cell data for. |

## Post runtime parameters to a process or an import

You can pass parameters to a process or an import when you POST it.

**Note:** You must include a locale when specifying parameters.

For example, you can specify:

- Mapping parameters. For instance, you can specify the Anaplan Version dimension to which data is to be imported. See [Run import process with mapping data](#Run-import-process-with-mapping-data) and [Import with mapping data](#Import-with-mapping-data)
- The [locale](#Locale-example) for which the information is intended. For instance, you might want the decimal separator to be shown as a comma for certain locales.

## Permission to run actions

Unless you're a workspace administrator, your assigned [Model Role](https://help.anaplan.com/anapedia/Content/Modeling/Users/Roles.html) must grant you access to the action you want to run using the API. Workspace administrators can run any action regardless of their assigned role. API requests without Workspace Administator role or permissions, may result in errors or unexpected results.

## Private and Default Files for Bulk APIs

Private files are created when you use the Anaplan API to:

- Upload a file.
- Run the file export action.

Private files have these characteristics:

- A private import file can only be accessed by the user who originally uploaded the source file to the model.
- A private export file can only be accessed by the user who originally ran the export.
- Private files are stored in models and removed if not accessed at least once in 48 hours. If your private file no longer exists for a file Import Data Source or file Export Action, the default file is used instead.

Default files are used when a private file does not exist for a file import data source or export action. Default files can be set for **Admins only** or **Everyone**.

**Note:** Default files can only be set and modified using the Anaplan user interface.

Your workspace role determines whether you can access a default file that is set to be available to **Admins only**. If you do not have access, a '404 not found' error occurs.

- If a default file is set for **Admins only**, only workspace administrators can download the default file. A '404 not found' error occurs for other API users (end users).
- If a default file is set for **Everyone**, all users (including end users) in your Anaplan environment (tenant) can download the default file.
- If a private file was created during an import or export action that you carried out, you receive that file instead of the default one.

See the [Overview of Private and Default Files](https://help.anaplan.com/anapedia/default.htm#cshid=1670 "Overview of Private and Default Files") for more information.

---

### Reference

## Workspaces

---

View the following endpoints for further details on workspaces APIs:

- [List user workspaces](#ListUserWorkspaces)
- [Retrieve workspace information](#RetrieveWorkspaceInfo)

---

## List user workspaces

`/workspaces`

Retrieves all workspaces a user has access to within the user's default tenant.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces?tenantDetails=true \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |

### Request parameters

| Parameter | Details |
| --- | --- |
| `tenantDetails` | - Optional - Type: Boolean - Description: When set to true, this call returns an estimate of the current size (`currentSize`) of the workspace from all the models it contains and the alotted quota (`sizeAllowance`). When set to false, or not defined, this call does not return an estimated current size of the workspace. - Example: true |

### Response headers

`Content-Type: application/json`

### Response 200 body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/workspace",
    "paging": {
      "currentPageSize": 1,
      "totalSize": 1,
      "offset": 0
    }
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "workspaces": [
    {
    "id": "8a8b8c8d8e8f8g8i",
    "name": "Financial Planning",
    "active": true,
    "sizeAllowance": 1073741824,
    "currentSize": 873741824
    }
  ]
}
```

---

## Retrieve workspace information

`/workspaces/{workspaceId}`

Retrieves information on a specific workspace if the user has access.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}?tenantDetails=true \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |

### Request parameters

| Parameter | Details |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `tenantDetails` | - Optional - Type: Boolean - Description: When set to true, this call returns an estimate of the current size (`currentSize`) of the workspace from all the models it contains and the alotted quota (`sizeAllowance`). When set to false, or not defined, this call does not return an estimated current size of the workspace. - Example: true |

### Response headers

`Content-Type: application/json`

### Response 200 body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/workspace"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "workspace": {
    "id": "8a8b8c8d8e8f8g8i",
    "name": "Financial Planning",
    "active":true,
    "sizeAllowance": 1073741824,
    "currentSize": 873741824
  }
}
```

---

## Models

---

View the following endpoints for further details on models APIs:

- [Retrieve models](#RetrieveModels)
- [Retrieve a specific model](#RetrieveSpecificModel)
- [Bulk delete models](#BulkDeleteModels)
- [Check model status](#CheckModelStatus)
- [Close model](#CloseModel)
- [Wake up model](#WakeModel)

---

## Retrieve models

`/models`  
Retrieves information about all models in the user's default tenant, unless the user is not a Workspace Administrator. In that case it returns only the models the user has been given access to.

**Note:** If no `offset` or `limit` parameters are used in the request, results will be limited to the first 5000 models.

If your call returns a lot of data, you can specify that results are returned in pages. You can specify:

- A `limit` for the number of results to return per page.
- An `offset` to get a specific page of results starting from a particular result.

The `paging` attribute specifies the number of results returned by an API request in pages. This is not the number of pages in a file.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/models \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}`

#### Request parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| `{modelDetails}` | Optional | Boolean | When set to `true`, this call returns the available model memory usage in bytes. When set to `false`, or not defined, this call does not return the model memory usage. | `?modelDetails=true` |
| `{offset}` | Optional | Numeric | Sets the starting point from which models are returned. | `?offset=5` |
| `{limit}` | Optional | Numeric | Sets the number of models to be returned by the request. | `?limit=10` |

### Responses

#### Response 200 (application/json)

```json
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/model",
    "paging": {
      "currentPageSize": 1,
      "totalSize": 1,
      "offset": 0
    }
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "models": [{
      "id": "FC12345678912343455667",
      "activeState": "UNLOCKED",
      "name": "FP&A",
      "currentWorkspaceId": "8a8b8c8d8e8f8g8i",
      "currentWorkspaceName": "Financial Planning",
      "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",
      "categoryValues": []
   }]
}
```

---

## Retrieve models for a specific workspace

`/workspaces/{workspaceId"}/models`

Retrieves information about all models in the specified workspace.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models?modelDetails=true \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}`

### Request parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelDetails` | - Optional - Type: Boolean - Description: When set to `true`, this call returns the available model memory usage in bytes. When set to `false`, or not defined, this call does not return the model memory usage. - Example: `true` |

### Response 200 (application/json)

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/model",
    "paging": {
      "currentPageSize": 4,
      "totalSize": 4,
      "offset": 0
    }
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "models": [
    {
      "id": "8BA821045BB34083B467C0082781DA69",
      "name": "Budgeting, Planning and Forecasting",
      "activeState": "UNLOCKED",
      "lastSavedSerialNumber": 2010876,
      "lastModifiedByUserGuid": "8a80da97613fc3d50161443501710056",
      "memoryUsage": 163950621,
      "currentWorkspaceId": "8a8196a258539d4c0158b0f9abe70bfd",
      "currentWorkspaceName": "ZZZ Sorting",
      "modelUrl": "https://api.anaplan.com/anaplan/framework.jsp?selectedWorkspaceId=8a8196a258539d4c0158b0f9abe70bfd&selectedModelId=8BA821045BB34083B467C0082781DA69",
      "categoryValues": [
        {
          "id": "8a8208a36543ed8f01655aff2edf264a",
          "attribute": "Sales",
          "categoryId": "15f6fd454b3a11ea814a026d2ec6a15d",
          "categoryName": "Business Function",
          "customerId": "8a8208a36543ed8f01655aff2ed52645"
        }
      ],
      "isoCreationDate": "2017-11-13T21:20:10.000+0000",
      "lastModified": "2020-11-26T00:29:01.000+0000"
    },
    {
      "id": "E216CF62E3F84342879E8480236AE78E",
      "name": "zmodel",
      "activeState": "UNLOCKED",
      "lastSavedSerialNumber": 2000035,
      "lastModifiedByUserGuid": "8a80da97613fc3d50161443501710056",
      "memoryUsage": 763180,
      "currentWorkspaceId": "8a8196a258539d4c0158b0f9abe70bfd",
      "currentWorkspaceName": "ZZZ Sorting",
      "modelUrl": "https://api.anaplan.com/anaplan/framework.jsp?selectedWorkspaceId=8a8196a258539d4c0158b0f9abe70bfd&selectedModelId=E216CF62E3F84342879E8480236AE78E",
      "categoryValues": [
        {
          "id": "8a8208a36543ed8f01655aff2edf2655",
          "attribute": "Planning, Budgeting and Forecasting",
          "categoryId": "15f70a644b3a11ea814a026d2ec6a15d",
          "categoryName": "App",
          "customerId": "8a8208a36543ed8f01655aff2ed52645"
        },
        {
          "id": "8a8208a36543ed8f01655aff2edf264b",
          "attribute": "Finance",
          "categoryId": "15f6fd454b3a11ea814a026d2ec6a15d",
          "categoryName": "Business Function",
          "customerId": "8a8208a36543ed8f01655aff2ed52645"
        }
      ],
      "isoCreationDate": "2016-11-29T16:45:02.000+0000",
      "lastModified": "2020-11-30T19:46:53.000+0000"
    },
    {
      "id": "1A0D320FF0C644479E98A207A5003E1A",
      "name": "zz archive",
      "activeState": "ARCHIVED",
      "lastSavedSerialNumber": 2000013,
      "lastModifiedByUserGuid": "8a80da97613fc3d50161443501710056",
      "currentWorkspaceId": "8a8196a258539d4c0158b0f9abe70bfd",
      "currentWorkspaceName": "ZZZ Sorting",
      "modelUrl": "https://api.anaplan.com/anaplan/framework.jsp?selectedWorkspaceId=8a8196a258539d4c0158b0f9abe70bfd&selectedModelId=1A0D320FF0C644479E98A207A5003E1A",
      "categoryValues": [
        {
          "id": "8a8208a36543ed8f01655aff2edf264d",
          "attribute": "Marketing",
          "categoryId": "15f6fd454b3a11ea814a026d2ec6a15d",
          "categoryName": "Business Function",
          "customerId": "8a8208a36543ed8f01655aff2ed52645"
        }
      ],
      "isoCreationDate": "2018-09-25T18:26:00.000+0000",
      "lastModified": "2018-09-25T18:26:00.000+0000"
    },
    {
      "id": "71B2E50D32664AF1B60FBC0C72B339AF",
      "name": "ZZmodel_Archive",
      "activeState": "UNLOCKED",
      "lastSavedSerialNumber": 2000015,
      "lastModifiedByUserGuid": "8a80da97613fc3d50161443501710056",
      "memoryUsage": 672300,
      "currentWorkspaceId": "8a8196a258539d4c0158b0f9abe70bfd",
      "currentWorkspaceName": "ZZZ Sorting",
      "modelUrl": "https://api.anaplan.com/anaplan/framework.jsp?selectedWorkspaceId=8a8196a258539d4c0158b0f9abe70bfd&selectedModelId=71B2E50D32664AF1B60FBC0C72B339AF",
      "categoryValues": [
        {
          "id": "8a8208a36543ed8f01655aff2ede2646",
          "attribute": "IT",
          "categoryId": "15f6fd454b3a11ea814a026d2ec6a15d",
          "categoryName": "Business Function",
          "customerId": "8a8208a36543ed8f01655aff2ed52645"
        }
      ],
      "isoCreationDate": "2018-08-17T18:05:23.000+0000",
      "lastModified": "2020-09-29T01:04:08.000+0000"
    }
  ]
}
```

---

## Retrieve a specific model

`/models/{modelId}`  
Retrieves information about a specific model in the user's default tenant, if the user has access to the model.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/models/{modelId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}`

### Parameters

| Parameter | Description |
| --- | --- |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |
| `modelDetails` | - Optional - Type: Boolean - Description: When set to `true`, this call returns the available model memory usage in bytes and models status information. When set to `false`, or not defined, this call does not return the model memory usage. - Example: `?modelDetails=true` |

### Response 200 (application/json)

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/model"
  },
  "model": {
    "id": "FC12345678912343455667",
    "activeState": "UNLOCKED",
    "name": "PF&A",
    "currentWorkspaceId": "8a8b8c8d8e8f8g8i",
    "currentWorkspaceName": "Financial Planning",
    "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",
    "categoryValues": []
  },
  "status": {
    "code": 200,
    "message": "Success"
  }
}
```

### Response 200 (application/json) when modelDetails=true

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/model"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "model": {
        "id": "FC12345678912343455667",
        "name": "PF&A",
        "activeState": "UNLOCKED",
        "lastSavedSerialNumber": 2000000,
        "modelTransactionRunning": false,
        "lastModifiedByUserGuid": "5c8f44f65d3a11ea95e4026d2ec6a15d",
        "memoryUsage": 474900,
        "currentWorkspaceId": "8a8b8c8d8e8f8g8i",
        "currentWorkspaceName": "Financial Planning",
    "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",
        "categoryValues": [],
        "isoCreationDate": "2022-02-10T19:14:23.000+0000",
        "lastModified": "2022-02-10T19:14:24.000+0000"
    }
}
```

---

## Bulk delete models

`/workspaces/{workspaceId}/bulkDeleteModels`

Use this call to delete one or more models in a workspace. The models **must be closed** before they can be deleted. Failure to delete one of the models for some reason, for example the calling user not having access to that model, will not affect the deletion of the rest of the specified models.

**Notes:**

- The user must be a workspace administrator in the specified workspace and have access to the specified models.
- This is a destructive action - be careful when deleting models.

### Request

```json
curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/bulkDeleteModels' \ 
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
-H 'Content-Type: application/json'
--data-raw '{ 
  "modelIdsToDelete": ["<model_id_to_delete_1", "<model_id_to_delete_2" ...]
}'
```

#### Request Headers

| Header | Required | Details |
| --- | --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Yes | The Anaplan authentication token |
| `Content-Type: application/json` | Yes | Describes the media type of the request body |
| `Accept: application/json` | Yes | Describes the media type of the response body |

#### Request parameters

| Parameter | Required | Type | Details |
| --- | --- | --- | --- |
| `{workspaceId}` | Yes | String | The workspace ID to delete models in. Example: `75A40874E6B64FA3AE0743278996850F` |

#### Request body

```json
{ 
  "modelIdsToDelete": ["<model_id_to_delete_1", "<model_id_to_delete_2" ...]
}
```

| JSON element | Required | Details |
| --- | --- | --- |
| `modelIdsToDelete` | Yes | Contains the IDs of the models in the workspace to be deleted. Must be a JSON array of strings. |

### Successful response

If your response is successful, you receive a `200 OK` HTTP status with a response body.

#### Response header

`Content-Type: application/json`

#### Response 200 body

If all the specified models were successfully deleted:

```json
{
   "meta":{
      "schema": "https://api.anaplan.com/2/0/objects/bulkDeleteModelsResponse"
   },
   "status":{
      "code": 200,
      "message": "Success"
   },
   "modelsDeleted": 4,
   "bulkDeleteModelsFailures": []
}
```

#### Response if some of the specified models were not deleted

When some of the models were not deleted, their ID will be shown alongside a message:

```json
{
   "meta":{
      "schema": "https://api.anaplan.com/2/0/objects/bulkDeleteModelsResponse"
   },
   "status":{
      "code": 200,
      "message": "Success"
   },
   "modelsDeleted": 1,
   "bulkDeleteModelsFailures": [
      {
        "modelId": "BC24B51B39CF4701ACF7CBFD2ED93C36",
        "message": "Model is open. Please close the model before trying again." 
      },
      {
        "modelId": "EA8467B737A144C5B73CD56BA86085A0",
        "message": "Something went wrong. Deleting this model failed."
      },
      {
        "modelId": "Incorrect_Model_Id",
        "message": "Model ID does not exist."
      }
   ]
}
```

### Error responses

| Code | Message | Required amendments |
| --- | --- | --- |
| 400 | `Error parsing request body as JSON` | Check you have all the right elements in the request body. |
|  | `Unrecognised property detected` | Ensure only the supported properties are included in the request body. |
|  | `Expected mandatory field 'modelIdsToDelete'` | Add the mandatory fields for the call to be successful. |
|  | Other messages | Specific messages may be returned to the user if the JSON request body is invalid. |
| 403 | `Forbidden` | Check if the user is a workspace administrator. |
| 404 | `Not Found` | Check if the workspace ID specified in the URL is correct. |

## Check model status

`2/0/workspaces/{workspaceId}/models/{modelId}/status`

Certain actions such as imports, exports, or writeback actions require exclusive access to a model during their execution. These actions lock the model. Any attempt to read information via the API is blocked as they require an exclusive transaction to run. This endpoint provides a status for the model.

### Request

```json
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/status' \ 
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
-H 'Content-Type: application/json'
```

#### Request Headers

| Header | Required | Details |
| --- | --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Yes | The Anaplan authentication token |
| `Content-Type: application/json` | Yes | Describes the media type of the request body |
| `Accept: application/json` | Yes | Describes the media type of the response body |

### Response

#### Response 200 when there is an ongoing export task

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/dimension"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
   "requestStatus":{
      "exportTaskType":null,
      "taskId":"6EB7F52C07CA4E86909A213C608765A1-11",
      "currentStep":"Processing ...",
      "tooltip":"The system is currently processing an Export:\n\nExport started by user Jesse Smith (jesse.smith@yourcompany.com)\n\nExport started at 11:23 (UTC)\nTasks can be cancelled in Model Management.",
      "progress":0.44110000000000005,
      "creationTime":1578569563167
   }
}
```

#### Response 200 when there is an ongoing import task

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/dimension"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    {
    "requestStatus": {
        "peakMemoryUsageEstimate": null,
        "peakMemoryUsageTime": null,
        "progress": 0.0,
        "currentStep": "Processing ...",
        "tooltip": "The system is currently processing an Import:\n\nImport started by user Jesse Smith (jesse.smith@yourcompany.com)\n\nImport started at 00:51 (UTC)\nTasks can be cancelled in Model Management.",
        "exportTaskType": null,
        "creationTime": 1645577520129,
        "taskId": "E9CB709BD63D4003ACFB60CADFC2FC0B"
    }
}
```

#### Response 200 when there is an ongoing writeback task

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/dimension"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    {
    "requestStatus": {
        "creationTime": 1646264082002,
        "progress": -1.0,
        "taskId": null,
        "currentStep": "Updating",
        "tooltip": null,
        "exportTaskType": null,
        "peakMemoryUsageEstimate": null,
        "peakMemoryUsageTime": null
    }
}
```

#### Response 200 when there is no ongoing task

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/dimension"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "requestStatus": {
        "peakMemoryUsageEstimate": null,
        "peakMemoryUsageTime": null,
        "progress": -1.0,
        "currentStep": "Open",
        "tooltip": null,
        "exportTaskType": null,
        "creationTime": 1645577591822,
        "taskId": null
    }
}
```

From the above responses, the `currentStep` property returns the status of the model under different scenarios -

- `Open` - When no process is running on the model.
- `Processing` - When import/export task is being processed on the model.
- `Updating` - When any update is being performed on the model, eg. cell write.
- `Closed` - When model is in maintenance state.

The `tooltip` returns details about the transaction being performed on the model and the user information who initiated the transaction along-with the progress information.

---

## Close model

`/close`

This endpoint enables a workspace administrator to close a model without having to wait for a timeout. This is particularly useful for root cause analysis when an error occurs.

To use this endpoint, you must supply a valid authentication and the model id.

### Request

```shell
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/close \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
-H 'Content-Type: application/json'
```

#### Headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization:AnaplanAuthToken {anaplan_auth_token}` | Yes | The Anaplan authentication token. |
| `Content-Type: application/json` | Yes | Describes the media type of the request body. |

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |

### Response

#### Response 200

A successful close action will provide a `200 OK` response.

#### Response 204

A successful close action will provide a `200 No content` response.

#### Response 401

An unsuccessful close action will provide a `401 Unauthorized` response if a valid authentication token was not provided.

#### Response 403

An unsuccessful close action will provide a `403 Forbidden` response if your user authentication lacks workspace administrator permissions.

#### Response 404

An unsuccessful close action will provide a `404 Not found` response if the {modelId} or {workspaceId} is not found.

#### Response 422

An unsuccessful close action will provide a `422 Unprocessable identity` response if the model is currently in a state that cannot process the action, for example, if the model is archived.

---

## Wake up model

`/workspaces/{workspaceID}/models/{modelID}/open`

Use this request to wake up a model (either upgrading from metadata-only, or opening from closed). As some very large models have long load times, you can build this into your automations to have them fully load before your model builders start working on them.

**Note**: To wake up a model, you must have Workspace Administrator authority in the model.

---

**Fair use policy**

This API endpoint is designed to support standard, day-to-day operations of your Anaplan users. Excessive or abnormal usage patterns that negatively impact system performance or stability are strictly prohibited. Examples of prohibited activity include (but are not limited to):

- Repeated requests to open models that are already open as a means of maintaining a "keep-alive", when unaccessed models time out and offload after 60 minutes.
- Requests designed to open or query a large number of models simultaneously or otherwise place excessive load on backend infrastructure.
- Repeated requests to open models that are already open as a means of artificially maintaining their loaded state. For performance and security purposes, Anaplan monitors model usage and offloads unaccessed models after a period of inactivity.

---

### Request

```js
curl -X POST \ https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/open \ 
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Content-Type: application/json'
```

#### Request headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}`

### Response

The endpoint only returns a status code response. Possible status codes include:

| Response | Reason |
| --- | --- |
| 404 | The endpoint returns a `404 Not found` if the resource is disabled, if the request is used repeatedly over a short period of time, or if the user lacks sufficent model permissions (Workspace administrator), or if the model has been deleted. |
| 422 | The endpoint returns a `422 Unprocessable content` response if the model is archived. |
| 424 | The endpoint returns a `424 Failed dependency` response if the model is in maintenance. |
| 200 | The endpoint returns a `200 OK` response if the model is open, or opened very quickly. |
| 202 | The endpoint returns a `202 Accepted` response if the model is in the process of opening, or promotion from metadata-only mode to full data load has started. |

---

## Line Items

---

View the following endpoints for further details on line items APIs:

- [Retrieve all line items in a model](#RetrieveAllLineItemsModel)
- [Retrieve dimension Ids for a line item](#RetrieveDimensionIdsLineItem)
- [Retrieve all line item metadata in a model](#Retrievealllineitemmetadatainamodel)
- [Retrieve all line item metadata in a module](#Retrievealllineitemmetadatainamodule)

---

## Retrieve all line items in a model

`/models/{modelId}/lineItems`

Use this call to retrieve identifiers of all line items in a model.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").
- The returned line items are restricted just to those in modules to which the model role of the user has Read access.
- The response returns Items within a [flat list](https://help.anaplan.com/anapedia/Content/Modeling/Dimensions/Lists.html) (no hierarchy).
- This returns all the line items in the model. For line items in a specific module see [Retrieve Line Items For a Module](#RetrieveAllLineItemsModule).

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/lineItem"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "items": [
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000000",
            "name": "Quantity Sold"
        },
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000001",
            "name": "Price"
        },
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000002",
            "name": "Revenue"
        },
        {
            "moduleId": "102000000001",
            "moduleName": "Profit",
            "id": "208000000000",
            "name": "Commission"
        },
        {
            "moduleId": "102000000001",
            "moduleName": "Profit",
            "id": "208000000001",
            "name": "Cost"
        },
        {
            "moduleId": "102000000001",
            "moduleName": "Profit",
            "id": "208000000002",
            "name": "Profit"
        }
    ]
}
```

---

## Retrieve dimension Ids for a line item

`/models/{modelId}/lineItems/{lineItem_Id}/dimensions`

Use this call to retrieve the Ids of dimensions that define a line item.

For reference, see [Retrieve dimension items for a line item](#RetrieveDimensionsLineItem).

**Notes**:

- To retrieve the IDs for the dimensions, use a `GET` request with this URL: `https://api.anaplan.com/2/0/models/{modelId}/lineitems/{lineItem_Id}/dimensions` where `{lineItemId}` is a placeholder for the retrieved line item ID.
- This returns a list of all the dimensions that apply to that line item.

### Request headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Required | The Anaplan authentication token |
| `Accept: application/json` | Optional | This indicates the preferred response is `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| `{modelId}` | Required | String | The ID for the model | `75A40874E6B64FA3AE0743278996850F` |
| `{lineItemId}` | Required | Number | The line item Id | `208000000000` |

## Response

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/dimension"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "dimensions": [
        {
            "id": "20000000003",
            "name": "Time"
        },
        {
            "id": "20000000020",
            "name": "Versions"
        },
        {
            "id": "101000000001",
            "name": "Products"
        },
        {
            "id": "101000000002",
            "name": "Regions"
        }
    ]
}
```

---

## Retrieve all line item metadata in a model

Use this call to get all line Items and metadata for a model.

### Request

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems?includeAll=true' \`  
`-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`  
`-H 'Accept: application/json'`

### Request Headers

| **Header** | **Details** |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This call uses a content type of `application/json`. |

### Request parameters

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `includeAll` | - Required - Type: boolean - Description: true or false - Example: `includeAll=true` |

### Response header

`Content-Type: application/json`

### Response 200 body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/lineItem"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "items": [{
            "moduleId": "102000000001",
            "moduleName": "module2",
            "id": "206000000006",
            "name": "lineitem-child",
            
            "isSummary": false,
            "startOfSection": false,
            "broughtForward": false,
            "useSwitchover": true,
            "breakback": false,
            
            "cellCount": 51,
            
            "version": {
                "name": "All",
                "id": "16000000000"
            },
            "appliesTo": [
                {
                    "name": "org-sub1",
                    "id": "109000000001"
                },
                {
                    "name": "linesubset1",
                    "id": "114000000001"
                }
            ],
            "dataTags": [
                {
                    "name": "tag1",
                    "id": "127000000002"
                },
                {
                    "name": "tag2",
                    "id": "127000000001"
                },
                {
                    "name": "tag3",
                    "id": "127000000000"
                }
            ],
            "referencedBy": [
                {
                    "name": "lineitem5",
                    "id": "206000000005"
                }
            ],

            "parent": {
                "name": "lineitem5",
                "id": "206000000005"
            },
            "readAccessDriver": {
                "name": "lineitem2",
                "id": "206000000003"
            },
            "writeAccessDriver": {
                "name": "lineitem2",
                "id": "206000000003"
            },
            
            "formula": "3 + 9",
            "format": "NUMBER",
            "formatMetadata": {
                "dataType": "NUMBER",
                "minimumSignificantDigits": 4,
                "decimalPlaces": -1,
                "negativeNumberNotation": "MINUS_SIGN",
                "unitsType": "NONE",
                "unitsDisplayType": "NONE",
                "zeroFormat": "ZERO",
                "comparisonIncrease": "GOOD",
                "groupingSeparator": "COMMA",
                "decimalSeparator": "FULL_STOP"
            },
            
            "summary": "Sum",
            "timeScale": "Month",
            "timeRange": "timeRange1",            
            "formulaScope": "All Versions",
            "style": "Normal",
            "code": "code7",
            "notes": "note1"
  }   
  ]
}
```

## Retrieve all line item metadata in a module

Use this call when you want to get all line items and metadata in a module.

**Notes:**

- Only [workspace administrators](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html) can use this call.
- You need **Read** access to the module. Otherwise, you receive a `404` response.
- The items in the response are in the same order that they appear on the user interface.
- This returns line items for a specific module. For all the line items in the model see [Retrieve all line items in the model](#RetrieveAllLineItemsModel).
- An invalid or a non-existing module ID returns a 404 response.

### Request

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/lineItems?includeAll=true' \`  
`-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`  
`-H 'Accept: application/json'`

#### Request Headers

| **Header** | **Details** |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This call uses a content type of `application/json`. |

#### Request parameters

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{moduleId}` | - Required - Type: String - Description: the model ID - Example: `89AA40874E6B64FA3AE07432789967048` |

#### Query parameters

| Query parameter | Possible values | Description |
| --- | --- | --- |
| `includeAll` | `true`, `false` | A Boolean query parameter. If true, the call response includes additional information about the applicable line item or list. |

### Response header

`Content-Type: application/json`

### Response 200 body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/lineItem"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "items": [{
            "moduleId": "102000000001",
            "moduleName": "module2",
            "id": "206000000006",
            "name": "lineitem-child",
            
            "isSummary": false,
            "startOfSection": false,
            "broughtForward": false,
            "useSwitchover": true,
            "breakback": false,
            
            "cellCount": 51,
            
            "version": {
                "name": "All",
                "id": "16000000000"
            },
            "appliesTo": [
                {
                    "name": "org-sub1",
                    "id": "109000000001"
                },
                {
                    "name": "linesubset1",
                    "id": "114000000001"
                }
            ],
            "dataTags": [
                {
                    "name": "tag1",
                    "id": "127000000002"
                },
                {
                    "name": "tag2",
                    "id": "127000000001"
                },
                {
                    "name": "tag3",
                    "id": "127000000000"
                }
            ],
            "referencedBy": [
                {
                    "name": "lineitem5",
                    "id": "206000000005"
                }
            ],

            "parent": {
                "name": "lineitem5",
                "id": "206000000005"
            },
            "readAccessDriver": {
                "name": "lineitem2",
                "id": "206000000003"
            },
            "writeAccessDriver": {
                "name": "lineitem2",
                "id": "206000000003"
            },
            
            "formula": "3 + 9",
            "format": "NUMBER",
            "formatMetadata": {
                "dataType": "NUMBER",
                "minimumSignificantDigits": 4,
                "decimalPlaces": -1,
                "negativeNumberNotation": "MINUS_SIGN",
                "unitsType": "NONE",
                "unitsDisplayType": "NONE",
                "zeroFormat": "ZERO",
                "comparisonIncrease": "GOOD",
                "groupingSeparator": "COMMA",
                "decimalSeparator": "FULL_STOP"
            },
            
            "summary": "Sum",
            "timeScale": "Month",
            "timeRange": "timeRange1",            
            "formulaScope": "All Versions",
            "style": "Normal",
            "code": "code7",
            "notes": "note1"
  }   
  ]
}
```

## Other Model Metadata

---

View the following endpoints for further details on other model metadata APIs:

- [Lookup dimension items by name or code](#LookupDimensionItemsNameCode)
- [Retrieve all items in a dimension](#RetrieveItemsDimension)
- [Retrieve selected items in a dimension](#RetrieveSelectedItemsDimension)

---

## Lookup dimension items by name or code

Retrieve the items from a dimension that match one of a list of names or a list or codes.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- This call does not return results for names or codes for which an item does not exist.
- If the given workspace, model, or dimension do not exist, this call returns a `404` code.
- If the dimension does not support codes and codes are provided, this call returns a `400` code.
- Supported dimensions are:
	- Lists - the request must include `Name` or `Code` of list item must be provided as input.
		- Time - the request must include the time period name (as visible in Anaplan UI, e.g. "May 21") as input.
		- Version - the request must include the name of the version as input.
		- Users - the request must include the user name as input.

### Requests that support this feature

```js
curl -X POST https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/dimensions/{dimensionId}/items \
-H ‘Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' --data-raw '<see Request body>'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required in the supported request - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the dimension ID. This value must be the ID for any of these dimension types: 	- Lists 		- Time periods 		- Users 		- Versions - Example: `101000000001` |

### Request body

| JSON Element | Description |
| --- | --- |
| `names` | The case-insensitive strings that match the name of a returned item. |
| `codes` | The case-insensitive strings that match the code of a returned item. |

Example:

```js
{
    "names": ["South", "East"],
    "codes": ["N", "W"]
}
```

Note that the `names`, `codes`, or both fields in the request body must contain a non-empty value. If the request body does not include at least one of these fields, the response returns an error.

### Response 200 Body

```js
{
  "meta" : {
      "schema":"https://api.anaplan.com/2/0/objects/dimension"
  },
  "status" : {
    "code":200,
    "message":"Success"
  },
  "items":[
    {
      "name":"South",
      "id":"208000000001",
      "code":"S"
    },
    {
      "name":"West",
      "id":"208000000004",
      "code":"W"
    }
  ]
}
```

---

## Retrieve all items in a dimension

`/models/{modelGuid}/dimensions/{dimensionId}/items`

Use this call to retrieve the IDs, codes, and names for items in a specified dimension. The dimension must be a list, a list subset, a line item subset, or the Users dimension.

Calls at model-level do not support the Time dimension. The calls return a `400` response. To avoid this, use the view dimension instead.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").
- This call is on the model-level. It returns all dimension items as it does not have view-level hiding, filtering, or [Selective Access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html "Selective Access"). For the view-level endpoint, see [Retrieve selected items in a dimension](#RetrieveSelectedItemsDimension).
- If codes have not been set for an item, then the response excludes the `code` field.
- This call only supports the retrieval of dimensions and items from a dimension that contains a maximum of 1,000,000 items.  
	The call returns a `400` response for any more than that number of items.

### Request

```js
curl -X GET
'https://api.anaplan.com/2/0/models/{modelGuid}/dimensions/{dimensionId}/items'\
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the ID for the dimension - Example: `101000000028` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta" : {
    "schema" : "https://api.anaplan.com/2/0/objects/dimension"
  },
  "status" : {
    "code" : 200,
    "message" : "Success"
  },
  "items" : [
    {
      "code" : "N",
      "id" : "200000000001",
      "name" : "North"
    },
    {
      "code" : "E",
      "id" : "200000000002",
      "name" : "East"
    },
    {
      "code" : "S",
      "id" : "200000000003",
      "name" : "South"
    },
    {
      "code" : "W",
      "id" : "200000000004",
      "name" : "West"
    },
    {
      "id" : "200000000000",
      "name" : "Total Company"
    }
  ]
}
```

---

## Retrieve selected items in a dimension

`/models/{modelId}/views/{viewId}/dimensions/{dimensionId}/items`

Use this call to retrieve selected IDs, codes, and names for items in a specified dimension. This call returns data as filtered by the page builder when they configure the view. This call respects hidden items, filtering selections, and [Selective Access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html "Selective Access"). If the view contains hidden or filtered items, these do not display in the response.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")
- This call works with any dimension type
- The items in the response may not be ordered
- The response returns Items within a [flat list](https://help.anaplan.com/anapedia/Content/Modeling/Dimensions/Lists.html "flat list") (no hierarchy)
- This is a view-level call. For the model-level call, see [Retrieve all data for items in a dimension](#RetrieveItemsDimension)
- This call only supports the retrieval of dimension items within a view that contains a maximum of 1,000,000 cells. If the specified view contains more than 1,000,000 dimension items, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the dimension items. Use the [quick sum bar](https://help.anaplan.com/anapedia/Content/New_User_Experience/Use/Worksheets/Grid/Quick-sum-bar.htm "quick sum bar") in Anaplan to identify the number of dimension items in a view
- The `viewId` in this request can also be replaced by any valid `lineItemId`. If the Line Item has a changed dimensionality (has a Subsidiary View), the response returns the applicable dimension items for the given dimension. Otherwise, the response returns all default applicable dimension items for the given dimension

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/dimensions/{dimensionId}/items' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{viewId}` | - Required - Type: Number - Description: the ID for the view - Example: `102000000000` |
| `{dimensionId}` | - Required - Type: Number - Description: the ID for the dimension - Example: `101000000028` |

### Response header

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/dimension"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "items": [{
      "id": "220000000001",
      "name": "England"
    },
    {
      "id": "220000000002",
      "name": "Wales"
    }]
}
```

---

## Read module, view metadata and limited volume cell data

---

View the following endpoints for further details on module and view data APIs:

- [Retrieve IDs and names for all modules in a model](#RetrieveIDNamesModuleModel)
- [Retrieve IDs and names for all views in a model](#RetrieveIDNamesViewsModel)
- [Retrieve IDs and names for views in a module](#RetrieveIDsNamesViewsModule)
- [Retrieve metadata for dimensions on a view](#RetrieveMetadataDimensionView)
- [Retrieve cell data for a view](#RetrieveCellDataView)
- [Retrieve all line items in a module](#RetrieveAllLineItemsModule)
- [Retrieve dimension items for a line item](#RetrieveDimensionsLineItem)

---

## Retrieve IDs and names for all modules in a model

`/models/{modelId}/modules`

Use this call to retrieve the IDs and names of all modules for a specified model.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "paging": {
      "currentPageSize": 1,
      "offset": 0,
      "totalSize": 1
    },
    "schema": "https://api.anaplan.com/2/0/objects/module"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "modules": [{
      "id": "102000000125",
      "name": "REV01 Price Book"
    },
    {
      "id": "102000000121",
      "name": "REV02 Volume Inputs"
    }]
}
```

---

## Retrieve IDs and names for all views in a model

`/models/{modelId}/views`

Use this call to retrieve the ID and name of all views for a model. The results include default and saved views. If you add the query parameter `includesubsidiaryviews=true`, this includes unsaved subsidiary views in the results. This call also retrieves the ID of the module that the views belong to.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")
- Single quotes enclose the module and view names that have special characters

### Default views

For default views:

- The value of the {viewId} is identical to the value of the {moduleId}
- The value of the name is identical to the value of the module

### Saved views

For saved views:

- The `name` consists of the module name, a period, and the saved view name. For example, `REP01 Profit & Loss Report.P & L by Country`

For unsaved subsidiary views:

- The name consists of the module name and the line item name that the subsidiary view is created from
- These are separated by a period(.)

### Request

```js
curl -X GET
'https://api.anaplan.com/2/0/models/{modelId}/views' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Query parameter

| Parameter | Details |
| --- | --- |
| `{includesubsidiaryviews}` | - Optional (default false) - Type: String - Description: Whether the response should include unsaved subsidiary views. The field is interpreted as false if anything other than `true` is specified - Example: `?includesubsidiaryviews=true` |

### Response header

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "paging": {
      "currentPageSize": 1,
      "offset": 0,
      "totalSize": 1
    },
    "schema": "https://api.anaplan.com/2/0/objects/view"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "views": [
    {
      "code": "",
      "id": "102000000000",
      "name": "StrategicPlanning",
      "moduleId": "102000000000"
    },
    {
      "code": "",
      "id": "207000000000",
      "name": "StrategicPlanning.UK Financial forecast",
      "moduleId": "102000000000"
    },
    {
      "code": "",
      "id": "207000000001",
      "name": "StrategicPlanning.EMEAforecastreport",
      "moduleId": "102000000000"
    },
    {
      "code": "",
      "id": "207000000002",
      "name": "StrategicPlanning.'accountSummary&overview/US$'",
      "moduleId": "102000000000"
    },
    {
      "code": "",
      "id": "237000000001",
      "name": "'StrategicPlanning/2020'.'accountSummary&overview/US$'",
      "moduleId": "102000000001"
    }
  ]
}
```

---

## Retrieve IDs and names for views in a module

`/models/{modelId}/modules/{moduleId}/views`

Use this call to retrieve all view IDs and names for a specified module. This call also returns the default view for the module. If the user adds the query parameter `includesubsidiaryviews=true`, unsaved subsidiary views will also be included in the results.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")
- For the default view, the `{viewId}` is the same as the `{moduleId}`
- For unsaved subsidiary views, the `{viewId}` and `{viewName}` are the same as the `{lineItemId}` and `{lineItemName}` that the subsidiary view is created from

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/views' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{moduleId}` | - Required - Type: number - Description: the ID for the module - Example: `102000000028` |
| `{includesubsidiaryviews}` | - Optional (default false) - Type: String - Description: Whether the response should include unsaved subsidiary views. The field is interpreted as false if anything other than `true` is specified - Example: `?includesubsidiaryviews=true` |

### Response header

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "paging": {
      "currentPageSize": 1,
      "offset": 0,
      "totalSize": 1
    },
    "schema": "https://api.anaplan.com/2/0/objects/view"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "views": [
    {
      "code": "",
      "id": "102000000000",
      "name": "default",
      "moduleId": "102000000000"
    },
    {
      "code": "",
      "id": "203000000000",
      "name": "SavedView",
      "moduleId": "102000000000"
    }
  ]
}
```

---

## Retrieve metadata for dimensions on a view

`/models/{modelId}/views/{viewId}`

Use this call to retrieve the name, IDs, and lists of names for the dimensions (columns, pages, rows) on a specified view.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")
- If a view has no dimensions on an axis, the call omits the axis field (for example, no `“rows”` field at all instead of `“rows”: []`)
- If a view is the default view, its `name` is set to be the same as the module name
- The `viewId` in this request can also be replaced by any valid `lineItemId`. If the Line Item has a changed dimensionality (has a Subsidiary View), the response returns the metadata applicable to that line item. Otherwise, the response returns the default metadata

You can use this API call to [map dimensions to cell data export headers](https://help.anaplan.com/43cd0223-edaa-4289-9833-eb9b73666aac-Map-dimensions-to-cell-data-export-headers) or [transform grid CSV format to tabular single column format](https://help.anaplan.com/c8a665b9-6b23-4254-ac68-816657a6e878-Retrieve-the-view-metadata-and-grid-view-data).

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{viewId}` | - Required - Type: Number - Description: the ID for the view - Example: `102000000000` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/view"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "viewName": "REV01 Price Book",
  "viewId" : "102000000000"
  "rows": [
    {
      "id": "101000000000",
      "name": "Products"
    },
    {
      "id": "101000000003",
      "name": "Regions"
    }
  ],
  "columns": [
    {
      "id": "101999999999",
      "name": "Line items"
    }
  ],
  "pages": [
    {
      "id": "101000000001",
      "name": "Versions"
    }
  ],
}
```

---

## Retrieve cell data for a view

Use this call to retrieve the cell data for a view. You can either query for the default page, or provide page selectors to query for other pages. This call returns data in either a CSV grid response or as JSON.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/018991f4-e5ae-4628-8ea8-51782e50d347).
- This call only supports the retrieval of cells from a view that contains a maximum of 1,000,000 cells. If the specified view contains more than 1,000,000 cells, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the cells. Use the [quick sum bar](https://help.anaplan.com/cb15ce25-b344-4a61-8b02-cd21bc5bfca3) in Anaplan to identify the number of cells in a view.
- If you call several times in a short amount of time, you may receive a `429` response.
- You can replace the `viewId` with any valid `lineItemId`. If the line item has a subsidiary view, the response returns the data as seen in that subsidiary view.
- For line items without a subsidiary view, the response returns data for the default view of the line item.

### CSV responses

The first line of the CSV response contains the values of the page selectors. The response omits this line when there are no dimensions on pages. When there are multiple dimensions on columns, a line for each dimension follows the first line that contains the values of the page selectors. When there are multiple dimensions on rows, a column displays on the left, before the data, for each dimension on rows. You can export the CSV data in different layouts by passing two query parameters exportType and moduleId together.

### JSON responses

To receive a JSON-formatted response instead of a CSV-formatted response:

1. Pass an `Accept` header of `application/json`.
2. Pass a query parameter of format set to `v1`.

All other parameters are the same as a CSV-formatted response.

The response returns `Content-Type` `application/json` with this format:

- A `pages` key with a value that is a list of the selected items for each page selector. If no page selectors exist for this view, the list displays as empty or absent.
- A `columnCoordinates` key with a value that is a list of the coordinates for all values in that column. Each list item is itself a list containing one or more values. The length of each list equals the number of dimensions on columns.
- A `rows` key with a value that is a list of row objects. Each row object contains:
- A `rowCoordinates` key with a value that is a list of the coordinates for all values in the current row. Each list item is itself a list that contains one or more values. The length of each list equals the number of dimensions on rows.
- A `cells` key with a value, which is a list of all the cell values in the current row. To get the full coordinates for each cell, use the position of the cell value in the `cells` list, and find the column coordinates at the same position in the `columnCoordinates` list. Then, to uniquely specify the cell, combine the column coordinates with the `rowCoordinates` for the current row and any selected pages.

## Request

```js
curl -X GET
'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1' \ 
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request to export CSV data in Tabular Single Column Layout

```js
curl -X GET
'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1&exportType={TABULAR_SINGLE_COLUMN}&moduleId={moduleId}' \ 
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: text/csv'
```

### Request to export CSV data in Tabular Multi Column Layout

```js
curl -X GET
'https://api.anaplan.com/2/0/models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1&exportType={TABULAR_SINGLE_COLUMN}&moduleId={moduleId}' \ 
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: text/csv'
```

## Request headers

| **Header** | **Details** |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json`      or      `Accept: text/csv`      or      `Accept: text/csv;escaped=true` | - Required - Description: The format to return cell data as. This call can provide content type of `text/csv` or `application/json`. - In some cases, we do not allow standard csv exports for security reasons. In these cases, calls to `text/csv` result in an error message. You can request a csv with sensitive fields encapsulated in quotes by appending the ‘escaped’ parameter to the Accept csv header. For example: `text/csv;escaped=true` |

## Request parameters

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

## Responses

### CSV

#### Response header

Content-Type: `text/csv`

#### Response body

```js
| Yesterday   |            |         |        |        |         |         |         |         |         |         |
|             |            | Apples  | Apples | Apples | Bananas | Bananas | Bananas | Carrots | Carrots | Carrots |
|             |            | English | French | German | English | French  | German  | English | French  | German  |
| Line item 1 | Baguette   | 1       | 2      | 3      | 5       | 6       | 7       | 9       | 10      | 11      |
| Line item 1 | Large loaf | 12      | 13     | 14     | 15      | 16      | 17      | 18      | 19      | 20      |
| Line item 1 | Small loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |
| Line item 2 | Baguette   | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |
| Line item 2 | Large loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |
| Line item 2 | Small loaf | 0       | 0      | 0      | 0       | 0       | 0       | 0       | 0       | 0       |
```

### JSON

#### Response header

Content-Type: `application/json`

#### Response body

```json
{
        "pages": [ "Value", "23mm" ],
        "columnCoordinates": [ ["Jan 13"], ["Feb 13"], ["Mar 13"], ["Q1 FY13"], ["Apr 13"], ["May 13"], ["Jun 13"], ["Q2 FY13"], ["H1 FY13"], ["Jul 13"], ["Aug 13"], ["Sep 13"], ["Q3 FY13"], ["Oct 13"], ["Nov 13"], ["Dec 13"], ["Q4 FY13"], ["H2 FY13"], ["FY13"] ],
        "rows": [
          {
            "rowCoordinates": [ "Durham" ],
            "cells": [
              "64.6", "57.94", "108.36", "230.97", "173.46", "321.17", "398.7", "893.43", "1124.3", "433.05", "435.52", "421.46", "1290.03", "300.11", "150.53", "70.23", "520.87", "1810.9", "2935.3"
            ]
          },
          {
            "rowCoordinates": [ "Newcastle upon Tyne" ],
            "cells": [
              "96.33", "92.69", "136.24", "325.27", "234.81", "468.96", "489.6", "1193.38", "1518.65", "535.86", "531.8", "542.6", "1610.25", "346.22", "171.65", "84.72", "602.6", "2212.85", "3731.5"
            ]
          },
          {
            "rowCoordinates": [ "Sunderland" ],
            "cells": [
              "57.06", "63.73", "56.33", "177.13", "124.52", "236.29", "286.86", "647.67", "824.8", "301.15", "302.13", "299.61", "902.9", "145.01", "115.58", "65.05", "325.65", "1228.55", "2053.35"
            ]
          }
        ]
      }
```

In a JSON-formatted response, the system will perform substitutions to the following invalid characters:

| Character in JSON | Meaning | Replaced by |
| --- | --- | --- |
| \\b | backspace | \\\\b |
| \\t | tab | \\\\t |
| \\n | new line | \\\\n |
| \\f | newline+space | \\\\f |
| \\r | carriage return | \\\\r |
| " | double quote | \\\\ |
| / | forward slash | \\/\\ |
| \\ | backslash | \\\\\\ |

## Retrieve all line items in a module

`/models/{modelId}/modules/{moduleId}/lineItems`

Use this call to retrieve identifiers of line items for a specific module.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").
- The Model Role of the user must allow Read access to the module. Otherwise, this call returns a `404 Not Found` HTTP status.
- The items in the response are in the same order that appears in the Anaplan UI.
- This call returns line items for a specific module. For all the line items in the model see [Retrieve All Line Items in a Model](#RetrieveAllLineItemsModel).
- If this query contains an invalid or a non-existing Module ID, the API returns a `404 Not Found` HTTP status.

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/lineItems' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{moduleId}` | - Required - Type: Number - Description: the ID for the module - Example: `102000000000` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/lineItem"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "items": [
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000000",
            "name": "Quantity Sold"
        },
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000001",
            "name": "Price"
        },
        {
            "moduleId": "102000000000",
            "moduleName": "Sales Entry",
            "id": "206000000002",
            "name": "Revenue"
        }
    ]
}
```

---

## Retrieve dimension items for a line item

`/models/{modelId}/lineItems/{lineItemId}/dimensions/{dimensionId}/items`

Use this call to retrieve IDs, codes, and names for dimension items that apply for the specified line item.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- This call works with any dimension type.
- Your requesting model role must allow read access to the module the line item belongs to. Otherwise, this call returns a `404 Not Found` HTTP status.
- The items in the response are ordered as listed in the Anaplan model.
- The response returns items within a [flat list](https://help.anaplan.com/anapedia/Content/Modeling/Dimensions/Lists.html) (no hierarchy).
- This returns dimension items that apply to a line item. For the view-level call, see [Retrieve selected items in a dimension](#RetrieveSelectedItemsDimension) and for the model-level call, see [Retrieve all items in a dimension](#RetrieveItemsDimension).
- This call only supports the retrieval of dimension items where the dimension contains a maximum of 1,000,000 items. If the specified dimension contains more than 1,000,000 dimension items, then the call returns a 400 Bad Request HTTP status, instead of a subset of the dimension items.
- Providing a non-existent Line Item ID or Dimension ID returns a 404 Not Found HTTP status.
- If the request provides an invalid line item ID or dimension ID this call returns a `400 Bad Request` HTTP status.

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems/{lineItemId}/dimensions/{dimensionId}/items' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: `String` - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{lineItemId}` | - Required - Type: `Number` - Description: the line item ID - Example: `208000000000` |
| `{dimensionId}` | - Required - Type: `Number` - Description: the dimension ID - Example: `101000000028` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/dimension"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "items": [
    {
      "id": "220000000001",
      "name": "England"
    },
    {
      "id": "220000000002",
      "name": "Wales"
    }
  ]
}
```

---

## Read large volume view data

---

View the following endpoints for further details on view data APIs:

- [Initiate large read request](#InitiateLargeReadRequestVD)
- [Retrieve status of large read request](#RetrieveStatusLargeReadRequestVD)
- [Download pages](#DownloadIntermediateExportFileStoreVD)
- [Delete read requests](#DeleteReadRequestsVD)

## Initiate large read request

Use this call to initiate a large volume read request of view data. This enables you to read data from views that are larger than a million cell count.

**Note:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use the [Delete read requests](#DeleteReadRequestsVD) call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.

### Request supporting this feature

---

```js
curl --location --request POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/' \
--header 'Authorization: AnaplanAuthToken AnaplanToken' \
--header 'Accept: application/json'
--data-raw '{
"exportType" : "TABULAR_MULTI_COLUMN"
}'
```

### Request Body

---

This API supports exporting data in the following formats:

| Type | Description | More information |
| --- | --- | --- |
| `GRID_ALL_PAGES` | This layout respects the existing sorting and filtering you have imposed on a data grid before you launch the export. | [Export grid](https://help.anaplan.com/Import_and_Export/Export_Layouts/Export_Data_in_Grid_Layout.html) |
| `TABULAR_SINGLE_COLUMN` | This layout takes all dimensions and puts them in columns, with the final column reserved for data. | [Export tabular single column](https://help.anaplan.com/Import_and_Export/Export_Layouts/Export_Data_in_Tabular_Single_Column_Layout.html) |
| `TABULAR_MULTI_COLUMN` | This layout enables you to export multiple data columns. | [Export Tabular Multiple Column](https://help.anaplan.com/Import_and_Export/Export_Layouts/Export_Data_in_Tabular_Multiple_Column_Layout.html) |

### Request headers

---

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

---

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |

### Response 200 body

---

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "viewReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "requestState": "IN_PROGRESS",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}"
    }
}
```

If the request is just submitted and not started the response resembles:

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "viewReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "requestState": "NOT_STARTED",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/view/{viewId}/readRequests/{requestId}"
    }
}
```

---

## Retrieve status of large read request

Use this call to check the status of an export action after a bulk data long request is initiated. You can use it to check how many pages are available to download.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

### Request

---

```js
curl -X GET /
'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

---

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

---

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

### Response scenarios

---

- When `requestState` is `COMPLETE` and `successful` is `true`, the export has completed successfully and the user can download all the pages.
- When `requestState` is `COMPLETE` and `successful` is `false`, this means the export failed. Retry and initiate a new export.
- When `requestState` is `IN_PROGRESS` the export has not yet completed, but you can download the available pages indicated by the `availablePages` field.
- When `requestState` is `NOT_STARTED` then simply check the status again.
- When `requestState` is `CANCELLED` then this request is completed by a 'DELETE' call.

We recommend you delete the last failed export before initiating a new export, using the delete export endpoint.

### Response 200 body

---

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "viewReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "viewId": 101000000014,
        "requestState": "COMPLETE",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}",
        "availablePages": 100,
        "successful": true
    }
}
```

Following is the response when the large read request is in progress

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "viewReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "viewId": 101000000014,
        "requestState": "IN_PROGRESS",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}",
        "availablePages": 50,
        "successful": true
    }
}
```

---

## Download pages

Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items.

You can download pages while the export is in progress. You can download up to `availablePages` number of pages returned by the export status API.

Note that page numbers start with zero. That means if 10 pages are available, you can download from page=0 through page=9

**Note:**

- To use this call, you must be a [**Workspace Administrator**](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use the [**Delete read requests**](#DeleteReadRequestsVD) call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.

## Request supporting this feature

```js
curl --{location} \
-X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}/pages/{pageNo}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: text/csv'
```

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token. |
| `Accept: text/csv` | - Required - Description: This indicates the preferred response is `text/csv` format. |

## Request parameters

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe`. |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F`. |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001`. |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC`. |
| `{pageNo}` | - Required - Type: `Number` - Description: The page number (starting from 0) - Example: `0` |

## Response 200 body

```js
Pasta,Line Items,Jan 17,Feb 17,Mar 17,Q1 FY17,Apr 17,May 17,Jun 17,Q2 FY17,Jul 17,Aug 17,Sep 17,Q3 FY17,Oct 17,Nov 17,Dec 17,Q4 FY17,FY17
Corn,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Corn,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Corn,Owner,,,,,,,,,,,,,,,,,
Whole Wheat,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Whole Wheat,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Whole Wheat,Owner,,,,,,,,,,,,,,,,,
Lentil,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Lentil,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Lentil,Owner,,,,,,,,,,,,,,,,,
Millet,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Millet,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Millet,Owner,,,,,,,,,,,,,,,,,
Rice,Cost,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Rice,Weight,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Rice,Owner,,,,,,,,,,,,,,,,,
Lasagne,Cost,21.33,21,18.25,60.58,22.35,16.69,23.21,62.25000000000001,18.68,19.94,20,58.620000000000005,23.1,24.64,23.43,71.17,252.62
Lasagne,Weight,6,5,7,18,0,0,0,0,0,0,0,0,0,0,0,0,18
```

---

## Delete read requests

Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request.

**Notes**:

- To use this call, you must be a [**Workspace Administrator**](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use this call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.
- An expiration timer starts after the read request is initiated, with the following conditions:
	- 30 minutes after no activity is recorded for that read request, the system will reclaim that space.
		- The expiration timer resets back to 30 minutes if the requested page number is divisible by 100, including page 0.

## Request supporting this feature

```js
curl -X DELETE 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token. |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format. |

## Request parameters

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

## Response 200 body

When the delete request completes, the API returns the following response:

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "viewReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "viewId": 101000000014,
        "requestState": "CANCELLED",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewIdƒ}/readRequests/{requestId}",
        "successful": true
    }
}
```

---

## Download list subset items

---

View the following endpoints for further details on downloading list item subsets:

- [Retrieve lists](#RetrieveLists)
- [Retrieve list metadata](#RetrieveListMetadata)
- [Lookup dimension items by name or code](#LookupDimensionItemsNameCode)

---

## Retrieve lists

`/workspaces/{workspaceId}/models/{modelId}/lists`

Use this call to retrieve lists for a specified workspace and model.

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Response 200 Body

```json
{
    "meta": {
        "paging": {
            "currentPageSize": 5,
            "offset": 0,
            "totalSize": 5
        },
        "schema": "https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "lists": [
        {
            "id": "101000000000",
            "name": "Organization"
        },
        {
            "id": "101000000001",
            "name": "opportunities"
        },
        {
            "id": "101000000002",
            "name": "sales rep"
        },
        {
            "id": "101000000003",
            "name": "Bakery"
        },
        {
            "id": "101000000004",
            "name": "List2"
        }
    ]
}
```

---

## Retrieve list metadata

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}`

Use this call to retrieve the following metadata for a specified list:

| Metadata | Description |
| --- | --- |
| `category` | The category to which the list is assigned. |
| `dataTags` | The data tags associated with the list. |
| `displayNameProperty` | If present it indicates the name of the property set on the list. |
| `hasSelectiveAccess` | If the value is true, this list uses [selective access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html "selective access"). |
| `id` | The list ID. This corresponds to the `listId` parameter. |
| `itemCount` | The number of list items present in the list. |
| `managedBy` | Not currently used. |
| `name` | The list name. |
| `nextitemIndex` | Contains the index of the next new item in the list. Used only by numbered lists. |
| `numberedList` | A true value indicates this is a numbered list. |
| `parent` | The parent hierarchy, which includes this information for the parent list:   - `id` - `name` |
| `permittedItems` | Indicates how many more items you can add to the existing list. This value changes when the number of items in the list change. |
| `productionData` | A true value indicates this is a production list in [Application Lifecycle Management (ALM)](https://help.anaplan.com/anapedia/Content/ALM/Application_Lifecycle_Management.htm "Application Lifecyle Management (ALM)"). |
| `properties` | The list properties, which include:   - `dataTags` - `format` - `formula` - `notes` - `referencedBy` |
| `subsets` | A list of subsets associated with the list hierarchy, which includes the following information for the parent list:   - `id` - `name` |
| `topLevelItem` | If present, indicates the top level item in a hierarchy. |
| `useTopLevelAsPageDefault` | A true value indicates this list is the default item in a page selector. |
| `workflowEnabled` | A true value indicates this list is enabled for [Workflow](https://help.anaplan.com/anapedia/Content/Modeling/Manage_Models/Workflow.html "Workflow"). |

If any of the metadata values are not set for a list (for example, no parent or no top level item), then the result omits the metadata entry.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |
| `Content-Type: application/json` | - Optional - Description: The endpoint uses a content type of `application/json`. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: string - Description: The list ID. - Example: `101000000001` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/102B/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "metadata": {
        "id": "101000000001",
        "name": "Sales Reps",
        "properties": [
            {
                "name": "Salesforce",
                "format": "TEXT",
                "notes": "",
                "referencedBy": ""
            },
            {
                "name": "Mail",
                "format": "TEXT",
                "notes": "",
                "referencedBy": ""
            }
        ],
        "hasSelectiveAccess": false,
        "parent": {
            "id": "101000000000",
            "name": "Organization"
        },
        "managedBy": "",
        "numberedList": false,
        "useTopLevelAsPageDefault": false,
        "itemCount": 1,
        "workflowEnabled": false,
        "productionData": false
    }
}
```

---

## Lookup dimension items by name or code

Retrieve the items from a dimension that match one of a list of names or a list or codes.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- This call does not return results for names or codes for which an item does not exist.
- If the given workspace, model, or dimension do not exist, this call returns a `404` code.
- If the dimension does not support codes and codes are provided, this call returns a `400` code.

### Requests that support this feature

```js
curl -X POST https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/dimensions/{dimensionId}/items \
-H ‘Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' --data-raw '<see Request body>'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required in the supported request - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the dimension ID. This value must be the ID for any of these dimension types: 	- Lists 		- Time periods 		- Users 		- Versions - Example: `101000000001` |

### Request body

| JSON Element | Description |
| --- | --- |
| `names` | The case-insensitive strings that match the name of a returned item. |
| `codes` | The case-insensitive strings that match the code of a returned item. |

Example:

```json
{
    "names": ["South", "East"],
    "codes": ["N", "W"]
}
```

Note that the `names`, `codes`, or both fields in the request body must contain a non-empty value. If the request body does not include at least one of these fields, the response returns an error.

### Response 200 Body

```json
{
  "meta" : {
      "schema":"https://api.anaplan.com/2/0/objects/dimension"
  },
  "status" : {
    "code":200,
    "message":"Success"
  },
  "items":[
    {
      "name":"South",
      "id":"208000000001",
      "code":"S"
    },
    {
      "name":"West",
      "id":"208000000004",
      "code":"W"
    }
  ]
}
```

---

## Update module cell data

---

View the following endpoints for further details on lists APIs:

- [Write cell data to module by coordinate or name](#WriteCellDataByCoordinateorName)

---

Note: When an update to cell data completes successfully, all downstream calculations are also complete. This includes cells linked by formulas to the cells being updated.

## Write cell data by coordinate or name

`/models/{modelId}/modules/{moduleId}/data`

Use this call to set cell values in a module.

Ensure the request body is an array of `CellWrite` objects. Each object is for an updated individual cell and its full set of dimensions.

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

## Request

```js
curl -X POST 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/data' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Accept: application/json'
-H 'Content-Type: application/json'
--data-raw '<see_below>'
```

## Request Body

An example request body using IDs:

```js
[
    {
      "lineItemId": "206000000000",
      "dimensions": [
          { "dimensionId": "101000000001", "itemId": "202000000001" },
          { "dimensionId": "20000000003", "itemId": "5438300031" },
          { "dimensionId": "20000000020", "itemId": "107000000001" }
      ],
      "value": 1111
    },
    {
      "lineItemId": "206000000001",
      "dimensions": [
          { "dimensionId": "101000000001", "itemId": "202000000001" },
          { "dimensionId": "20000000003", "itemId": "5438300031" },
          { "dimensionId": "20000000020", "itemId": "107000000001" }
      ],
      "value": "Some text value"
    }
]
```

An example request body using names:

```js
[
    {
      "lineItemName": "Products",
      "dimensions": [
          { "dimensionName": "Product", "itemCode": "SKU1234" },
          { "dimensionName": "Time", "itemName": "Jan 21" },
          { "dimensionName": "Version", "itemName": "Actual" }
      ],
      "value": 1111
    },
    {
      "lineItemName": "Sales",
      "dimensions": [
          { "dimensionName": "Region", "itemName": "UK" },
          { "dimensionName": "Time", "itemName": "Dec 21" },
          { "dimensionName": "Version", "itemName": "Forecast" }
      ],
      "value": "Some text value"
    }
]
```

### The CellWrite Object

Each `CellWrite` Object is a request to set a value in a cell. A cell is identified by the line item it belongs to as well as an item for each of the dimensions that apply to the line item (this includes **Time** and **Versions**).

This table details the fields that are in a cell write object:

| Field | Details |
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

### Line item API Endpoints

Use the following endpoints to retrieve IDs of line items, dimensions and dimension items:

- To retrieve line items IDs, either retrieve line items for a module, or all line items in a model
- To retrieve dimension IDs, retrieve dimensions for a line item
- To retrieve dimension item IDs, retrieve dimension items for a line item

### Line Item Values

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

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |
| `Content-Type: application/json` | - Required - Description: This indicates the request type is `application/json` format. |

## Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{moduleId}` | - Required - Type: Number - Description: the ID for the module - Example: `102000000000` |

## Response headers

`Content-Type: application/json`

## Response body

If the request body is valid then the user will receive a `200 OK` response no matter how many cells were updated. The response body is similar to the example below:

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/writeCellDataResponse"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "numberOfCellsChanged": 42,
  "failures": [
      {
          "requestIndex": 0,
          "failureType": "cellIsCalculated",
          "failureMessageDetails": "the cell is a calculated/aggregate cell and is not writeable"
      },
      {
          "requestIndex": 9,
          "failureType": "cellIsInvalid",
          "failureMessageDetails": "the cell could not be found or resolved"
      }
  ]
}
```

### 400 response body

If the request has some missing mandatory fields or the `value` field type is incompatible, this returns a `400` response. To find out which values you need to amend in the request, look for the `failureType` values identified in the `400` response.

This table details the different `failureType` values that the response can identify to help you can make your amendments.

| **Possible** `failureType` **values** | **Description** |
| --- | --- |
| `missingRequiredField` | There is a required field missing in the request (either `lineItemId`, `value`, `dimensionId` or `itemId`) |
| `unsupportedValueType` | The specified `value` in the `value` field is not supported. Ensure the field is either a string, number, or boolean. |
| `cellIsInvalid` | The cell could not be found or resolved. |
| `cellIsNotWriteable` | The cell is not writeable. The user may not have the correct permissions to write to it. |
| `cellIsCalculated` | The cell is a calculated/aggregate cell and cannot be written to. |
| `valueDataTypeMismatch` | The value type (`value` field) is not compatible with the data type / format of the line item. |
| `unsupportedCellDataType` | The data type / format of this cell or line item is not supported. |
| `invalidListItemValue` | The value specified (`value` field) does not reference a valid item from the list configured for the list-formatted line item. |
| `invalidDateValue` | This only applies to line items in the `Date` format.   The specified `value` is: - Not a valid date (e.g. 2020-13-32) - Not in the expected ISO date format YYYY-MM-DD - Falls outside the date range allowed in an Anaplan model |
| `invalidTimeScaleValue` | This only applies to line items in the `Time Period` format.   The specified `value` does not match a value from the time scale. |
| `invalidId` | The id specified in one of the fields is not valid. |
| `invalidLineItem` | The specified `lineItemId` is not a valid line item. |
| `invalidDimension` | The specified `dimensionId` cannot be found on the `lineItemId`. |
| `invalidItem` | The specified `itemId` cannot be found on the dimension `dimensionId`. |

---

## Model lists

---

View the following endpoints for further details on lists APIs:

- [Retrieve lists](#RetrieveLists)
- [Retrieve list metadata](#RetrieveListMetadata)
- [Retrieve list data](#RetrieveListData)
- [Add list items](#AddListItems)
- [Update list items](#UpdateListItems)
- [Delete list items](#DeleteListItems)
- [Reset numbered list index](#ResetNumberedListIndex)

---

## Retrieve lists

`/workspaces/{workspaceId}/models/{modelId}/lists`

Use this call to retrieve lists for a specified workspace and model.

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Response 200 Body

```js
{
    "meta": {
        "paging": {
            "currentPageSize": 5,
            "offset": 0,
            "totalSize": 5
        },
        "schema": "https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "lists": [
        {
            "id": "101000000000",
            "name": "Organization"
        },
        {
            "id": "101000000001",
            "name": "opportunities"
        },
        {
            "id": "101000000002",
            "name": "sales rep"
        },
        {
            "id": "101000000003",
            "name": "Bakery"
        },
        {
            "id": "101000000004",
            "name": "List2"
        }
    ]
}
```

---

## Retrieve list metadata

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}`

Use this call to retrieve the following metadata for a specified list:

| Metadata | Description |
| --- | --- |
| `category` | The category to which the list is assigned. |
| `dataTags` | The data tags associated with the list. |
| `displayNameProperty` | If present it indicates the name of the property set on the list. |
| `hasSelectiveAccess` | If the value is true, this list uses [selective access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html "selective access"). |
| `id` | The list ID. This corresponds to the `listId` parameter. |
| `itemCount` | The number of list items present in the list. |
| `managedBy` | Not currently used. |
| `name` | The list name. |
| `nextitemIndex` | Contains the index of the next new item in the list. Used only by numbered lists. |
| `numberedList` | A true value indicates this is a numbered list. |
| `parent` | The parent hierarchy, which includes this information for the parent list:   - `id` - `name` |
| `permittedItems` | Indicates how many more items you can add to the existing list. This value changes when the number of items in the list change. |
| `productionData` | A true value indicates this is a production list in [Application Lifecycle Management (ALM)](https://help.anaplan.com/anapedia/Content/ALM/Application_Lifecycle_Management.htm "Application Lifecyle Management (ALM)"). |
| `properties` | The list properties, which include:   - `dataTags` - `format` - `formula` - `notes` - `referencedBy` |
| `subsets` | A list of subsets associated with the list hierarchy, which includes the following information for the parent list:   - `id` - `name` |
| `topLevelItem` | If present, indicates the top level item in a hierarchy. |
| `useTopLevelAsPageDefault` | A true value indicates this list is the default item in a page selector. |
| `workflowEnabled` | A true value indicates this list is enabled for [Workflow](https://help.anaplan.com/anapedia/Content/Modeling/Manage_Models/Workflow.html "Workflow"). |

If any of the metadata values are not set for a list (for example, no parent or no top level item), then the result omits the metadata entry.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |
| `Content-Type: application/json` | - Optional - Description: The endpoint uses a content type of `application/json`. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: string - Description: The list ID. - Example: `101000000001` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/102B/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "metadata": {
        "id": "101000000001",
        "name": "Sales Reps",
        "properties": [
            {
                "name": "Salesforce",
                "format": "TEXT",
                "notes": "",
                "referencedBy": ""
            },
            {
                "name": "Mail",
                "format": "TEXT",
                "notes": "",
                "referencedBy": ""
            }
        ],
        "hasSelectiveAccess": false,
        "parent": {
            "id": "101000000000",
            "name": "Organization"
        },
        "managedBy": "",
        "numberedList": false,
        "useTopLevelAsPageDefault": false,
        "itemCount": 1,
        "workflowEnabled": false,
        "productionData": false
    }
}
```

---

## Retrieve list data

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items`

Use this call to retrieve list data for the items in a specified list.

You can filter on optional fields by setting the `includeAll` query parameter.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- This call only supports the retrieval of list data up to 1,000,000 records. If the specified list contains more than 1,000,000 records, then the call returns a `400 Bad Request` HTTP status, instead of a subset of the records.

The following list data always displays in the query response:

| Default List Data | Description |
| --- | --- |
| `id` | The Anaplan ID of the item in the list. |
| `name` | The name of the item in the list. |
| `code` | The code value for an item in the list (if specified) |
| `parent` | The name of the parent item in the list. |
| `parentId` | The Anaplan ID of the parent item in the list. |
| `listId` | The Anaplan ID of the list to which the parent item belongs. This ID displays if the list has a **Parent Hierarchy** set under the **Configure** tab in Anaplan. |
| `listName` | The name of list to which the parent item belongs. The name displays if the list has a **Parent Hierarchy** set under the **Configure** tab in Anaplan. |

Set the `includeAll` query parameter to true to display the following optional list data fields in the response.

| Optional List Data | Description |
| --- | --- |
| `write` | If [Selective Access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html) is enabled for the list, you can add individual users to provide `write` access. Users with `write` access can view and edit data associated with the list items. |
| `read` | If [Selective Access](https://help.anaplan.com/anapedia/Content/Modeling/Users/Selective_Access.html) is enabled for the list, you can add individual users to provide `read` access. Users with `read` access can view the data associated with the list items but not edit it. |
| `subsets` | If the value of the subset column is true, the associated item belongs to that subset. You can view subsets under **Subsets** tab in Anaplan. |
| `properties` | The value of each custom list property. |

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?includeAll=true' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
```

or

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?includeAll=true' \
-H 'Accept: text/csv' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json`   or   'Accept: text/csv' | - Optional - Description: This indicates the preferred response is either `application/json` or `text/csv` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: string - Description: determines if optional query fields should display in the response.   	When true, the endpoint returns all the data, including optional fields for the specified list ID.   	When false, the endpoint does not include the optional data fields in the response for the specified list ID. - Example: `101000000001` |

### Query parameters

| Parameter | Details |
| --- | --- |
| `{includeAll}` | - Required - Type: Boolean - Description: The workspace ID - Example: `true` |

### Response 200 Body

#### Example with application/json and includeAll=false

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listItems": [
      {
        "id": "206000000001",
        "name": "cake",
        "code": "c1"
      },
      {
        "id": "206000000002",
        "name": "bread",
        "code": "b2"
      },
      {
        "id": "206000000003",
        "name": "pastry",
        "code": "p3"
      }
    ]
  }
```

#### Example with text/csv and includeAll=false

```js
id,name,code,parent,parentId,listId,listName
206000000001,cake,c1,,,,
206000000002,bread,b2,,,,
206000000003,pastry,p3,,,,
```

#### Example with application/json and includeAll=true

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listItems": [
      {
        "id": "206000000001",
        "name": "cake",
        "code": "c1",
        "subsets": {
          "favourite": true
        },
        "properties": {
          "count": "1.0"
        }
      },
      {
        "id": "206000000002",
        "name": "bread",
        "code": "b2",
        "subsets": {
          "favourite": false
        },
        "properties": {
          "count": "4.0"
        }
      },
      {
        "id": "206000000003",
        "name": "pastry",
        "code": "p3",
        "subsets": {
          "favourite": true
        },
        "properties": {
          "count": "5.0"
        }
      }
    ]
  }
```

#### Example with text/csv and includeAll=true

```js
id,name,code,parent,parentId,listId,listName,favourite,count
206000000001,cake,c1,,,,true,1.0
206000000002,bread,b2,,,,false,4.0
206000000003,pastry,p3,,,,true,5.0
```

---

## Add list items

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=add'`

Use this call to add items to a list. You must provide the list ID and data for each item. You can add one or more items in each request.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be added with a single call.

### Requests that support this feature

```js
curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=add' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |
| `action=add` | - Required - Type: query parameter - Description: The Anaplan Add action. This query parameter must be included in the URL as shown in the Requests section above. - Example: `action=addRequest` |

### Request body

| List Data | Description |
| --- | --- |
| `{name}` | The name value for the item in the list. |
| `{code}` | The code value for the item in the list. |
| `{parent}` | The name of the parent item in the list |
| `{properties}` | The value of each custom list property. |
| `{subsets}` | The value of each custom list subset. |

Example:

```js
{
  "items": [
    {
      "name": "mike",
      "code": "id1",
      "parent": "west",
      "properties": {
        "p-text":"hello world",
        "p-number":"123456",
        "p-boolean": "true",
        "p-list": "east",
        "p-period": "Sep 20"
      },
    "subsets": {
      "s11": true
    }
  },
    {
      "name": "cindy",
      "code": "id2",
      "properties": {
        "p-text":"hello world",
        "p-number":"wrong format for number",
        "p-boolean": "true",
        "p-list": "east",
        "p-period": "Sep 20"
      },
      "subsets": {
        "s11": true
      }
    }
  ]
}
```

### Logic for add items

The add list items behavior uses specific logic with names and codes. This logic varies between [general lists](https://help.anaplan.com/f7f01453-71bc-4046-935a-b9d7cb47d15a-General-Lists) and [numbered lists](https://help.anaplan.com/54b75174-848f-482b-a051-a9a063ece50c-Numbered-Lists) in Anaplan.

#### Add items to a general list

| Scenario | Existing | Input in API | Behavior | Result |
| --- | --- | --- | --- | --- |
| Add a new list Item | There are no existing items | name=n1   code=c1 | Success.   A new list item is created. | name=n1   code=c1 |
| Add list item with name conflicts | name=n1   code=c1 | name=n1   code=c2 | There is a duplicate name. A new list item is not added. | An error message returns. |
| Add list item with code conflicts | name=n1   code=c1 | name=n2   code=c1 | There is a duplicate name. A new list item is not added. | An error message returns. |
| Add list item without name | There are no existing items | code=c1 | There is a missing name. A new list item is not added. | An error message returns. |

#### Add items to a numbered list

For a numbered list, the name column is used for the index. The name is automatically generated. When you add an item, the API does not allow a name as an input.

| Scenario | Existing | Input in API | Behavior | Result |
| --- | --- | --- | --- | --- |
| Add a new list Item | There are no existing items | name=n1   code=c1 | A name is not a valid input. A new list item is not added. | An error message returns. |
| Add a new list item | There are no existing items | code=c1 | Success.   A new item is added. | success code=c1 |
| Add a list item with a conflicting code | code=c1 | code=c1 | There is a duplicate code. A new list item is not added. | An error message returns. |

### Response 200 Body

The response body contains a JSON object that contains `total` (total number of items in request), `ignored` (number of items ignored), `added` (number of items added), and `failures` (a description of the reason of each failure) fields. In the `failures` response, each field contains failures information about any errors encountered while performing the add action. `requestIndex` is the index in input items array.

```js
{
    "meta": {
        "schema": "https://anaplan.api.com/2/0/objects/item"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "added": 1,
    "ignored": 1,
    "total": 2,
    "failures": [
        {
            "requestIndex": 1,
            "failureType": "INCORRECT_FORMAT",
            "failureMessageDetails": "incorrect format -- column name:p-number, value:wrong value for number"
        }
    ]
}
```

---

## Update list items

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items`

Use this call to update items to a list. You must provide the model ID and list ID on the request URL. There are two kinds of lists in Anaplan: standard list and numbered list. For a standard list, the API identifies the item using the id, code, or name. For numbered list, the API uses the id or code. If property or subset is not specified in the input, the existing value is not updated. You can update one or more items in each request.

When you specify the list item identifier, select one of the appropriate identifiers (id, code, or name). If the request contains multiple identifiers, the API returns an error.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be updated with a single call.
- The update list items allows updates or lists and numbered Lists.

Note: When an update to a list item completes successfully, all downstream calculations are also complete. This includes cells linked by formulas to the cells being updated.

### Requests that support this feature

```js
curl -X PUT 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |

### Request body

| List Data | Description |
| --- | --- |
| `{name}` | The name value for the item in the list. |
| `{code}` | The code value for the item in the list. |
| `{id}` | The Anaplan ID of the item in the list. |
| `{parent}` | The name of the parent item in the list |
| `{properties}` | The value of each custom list property. |
| `{subsets}` | The value of each custom list subset. |

Example:

```js
{
  "items": [
    {
      "name": "n1",
      "code": "c1",
      "properties": {
        "p-text":"hello world",
        "p-number":"1111",
        "p-boolean": "true",
        "p-list": "east",
        "p-period": "Sep 21"
      },
    "subsets": {
      "s11": true
    }
  },
    {
      "name": "n1",
      "code": "c2",
      "properties": {
        "p-text":"hello world",
        "p-number":"wrong format for number",
        "p-boolean": "true",
        "p-list": "east",
        "p-period": "Sep 21"
      },
      "subsets": {
        "s11": true
      }
    }
  ]
}
```

### Update logic

The update list item endpoint logic varies by the update scenario.

| Scenario | Existing | Input in API | Behavior | Result |
| --- | --- | --- | --- | --- |
| Update list item | name=n1   code=c1 | name=n1   code=c1 | Success | name=n1   code=c1 |
| Update name | name=n1   code=c1 | name=n2   code=c1 | Success | name=n2   code=c1 |
| Update code | id=id1   name=n1   code=c1 | id=id1   name=n1   code=c2 | Success | id=id1   name=n1   code=c2 |
| Update code without existing code | id=id1   name=n1 | id=id1   name=n1   code=c2 | Success | id=id1   name=n1   code=c2 |
| Update code   (removing existing code) | id=id1   name=n1   code=c1 | id=id1   name=n1   code="" | This scenario does not provide a new code to replace the existing value. An error returns. | error: `INCOMPLETE_DATA` |
| Update code without an existing code   (assign a code without the id) | name=n1 | name=n1   code=c1 | Success | name=n1   code=c1 |
| Update code with same name | name=n1   code=c1 | name=n1   code=c2 | The name is already used. An error returns. | error: `INCOMPLETE_DATA` |
| Update value with code only | name=n1   code=c1   properties{p1=1234} | code=c1   properties{p1=1234} | Success   It's valid to use the code to identify the record. | code=c1   properties {p1=4321} |
| Update value with name only.   Do not specify the code | name=n1   code=c1   properties{p1=1234} | name=n1   properties{p1=1234} | The code is required to identify the record. An error returns. | error: `INCOMPLETE_DATA` |
| Update value with name only | name=n1   properties{p1=1234} | name=n1   properties{p1=4321} | Success   When the code is not defined, the API can still update with the name. | name=n1   properties{p1=4321} |

### Response 200 body

The response body contains a JSON object that contains `total` (total number of items in request), `updated` (number of items updated), `ignored` (number of items ignored), and `failures` fields. On `failures`, each field contains information about any errors encountered while performing the update action. `requestIndex` is the index in the input items array.

```js
{
    "meta": {
        "schema": "https://anaplan.api.com/2/0/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "total": 2,
    "ignored": 1,
    "updated": 1,
    "failures": {
       {
          "failureType": "INCORRECT_FORMAT",
          "failureMessageDetails": "incorrect format -- column name:p-number, value:wrong format for number",
          "requestIndex": 1
       }
    }
}
```

---

## Delete list items

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=delete`

Use this call to delete items from a list. You must provide the list ID or Code to identify each list item. You can delete one or more list items in one API call by providing different identifiers for each item. For example, provide the ID for one item and code for another.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be deleted with a single call.

### Requests that support this feature

```js
curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=delete' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'
```

and

```js
curl -X POST 'https://api.anaplan.com/2/0/models/{modelId}/lists/{listId}/items?action=delete' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |

### Request body

| List Data | Description |
| --- | --- |
| `{id}` | The ID for the item in the list. |
| `{code}` | The code value for the item in the list. |

Example:

```js
{
  "items": [
    {
      "id": 201000000000
    },
    {
      "code": "Region 1"
    },
    {
      "id": 201000000001,
      "code": "i1"
    }
  ]
}
```

### Response 200 Body with successful deletion

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "deleted": 2
}
```

### Response 200 Body when id or code does not exist

The response body contains a JSON object which has a `deleted` field and a `failures` field that contains information about any errors encountered while performing the delete action. Each item contains the identifier specified in the request.

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/list"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "result": {
        "numberOfItemsDeleted": 1,
        "failures": [
            {
                "requestIndex": 1,
                "failureType": "Not found",
                "failureMessageDetails": "Code 'Region 1' not found"
            },
            {
                "requestIndex": 2,
                "failureType": "Ambiguous criteria",
                "failureMessageDetails": "Specifying both ID and code not supported (201000000001:i1)"
            }
        ]
    }
}
```

---

## Reset list index

Use this API to reset the index on lists. This ensures that as you add items, they stay within the maximum amount allowed.

**Notes:**

- To use this API call and reset the index on a list, the list must be empty, otherwise you will receive a `400 Bad Request` error.
- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration "Workspace Administrator").

## Request

`curl -X POST 'https://api.anaplan.com/2/0/models/{modelId}/lists/{listId}/resetIndex' \`  
`-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \`  
`-H 'Accept: application/json'`

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This call uses a content type of `application/json` |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: String - Description: the list ID - Example: `3010000001` |

## Response

### Response 200 header

A successful index reset will provide a `200 OK` response. The API will return a 400-type error if you attempt to reset the index on a list that is not empty.

#### Response 200 body

A successful response does not return a message body.

### Response 400 header

`application/json`

#### Response 400 body

```json
{
    "status": {
        "code": 400,
        "message": "We can't reset the list item index of a list that contains data. Select an empty list that doesn't contain any list items."
    },
    "path": "/2/0/models/567CF3F6A9B346718F7BE5C749857523/lists/101000000000/resetIndex",
    "timestamp": "2023-04-26T13:51:59.102661Z"
}
```

## Read large volume list item data

---

View the following endpoints for further details on lists APIs:

- [Preview large data list read](#PreviewLargeDataListRead)
- [Initiate large read request](#InitiateLargeReadRequest)
- [Retrieve status of large read request](#RetrieveStatusLargeReadRequest)
- [Download pages](#DownloadIntermediateExportFileStore)
- [Delete read requests](#DeleteReadRequests)

## Preview large data list read

### Description

This endpoint enables you to create an integration that previews the source data before an export. Use this call to get the data preview of the list data, up to 1000 records, before starting the export.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

### Request

`curl --location --request GET`  
`'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/preview'`  
`-H 'Authorization: {anaplan_auth_token}'`  
`-H 'Accept: text/csv'`

#### Request Headers

| **Header** | **Required** | **Details** |
| --- | --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Yes | The Anaplan authentication token |
| `Accept: text/csv` | Yes | This indicates the preferred response is `text/csv` format. |

#### Request parameters

| **Parameter** | **Required** | **Type** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| `{workspaceId}` | Yes | String | The workspace ID | `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | Yes | String | The model ID | `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | Yes | Number | The list ID | `101000000001` |

### Response 200 body

```js
,Parent,Code
Closed No Decision,,
Closed Lost,,
Disqualified,,
5. Closed Won,,
0. 1st Meeting/Discovery,,
1. Qualification and Discovery,,
2. Solution Development,,
3. Solution Validation,,
4. Negotiate and Close,,
```

## Initiate large read request

Use this call to initiate a large volume read request on a list. This enables you to read data from lists that are larger than a million lines.

**Note**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use the [Delete read requests](#DeleteReadRequests) call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.

## Request supporting this feature

```js
curl -X POST /'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestID}' /
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' /
-H 'Content-Type: application/json' /
-H 'Accept: application/json'
```

## Request headers

|  |  |
| --- | --- |
| **Header** | **Details** |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format. |

## Request parameters

|  |  |
| --- | --- |
| **Parameters** | **Details** |
| `{workspaceId}` | - Required in the first supported request (see *Requests supporting this feature*) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID. - Example: `101000000001` |

## Response 200 body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "requestState": "IN_PROGRESS",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}"
    }
}
```

If the request is just submitted and not started the response resembles:

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "requestState": "NOT_STARTED",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}"
    }
}
```

---

## Retrieve status of large read request

Use this call to check on the status of an export action after a bulk data long request is initiated. This enables you to start the download of the pages from the directory where you download the export file.

**Note**: To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

## Request supporting this feature

```js
curl -X GET / 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestID}' /
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' /
-H 'Accept: application/json'
```

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format. |

## Request parameters

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

## Response scenarios

- When `requestState` is `COMPLETE` and `successful` is `true`, the export has completed successfully and the user can download all the pages.
- When `requestState` is `COMPLETE` and `successful` is `false`, this means the export failed. Retry and initiate a new export.
- When `requestState` is `IN_PROGRESS` the export has not yet completed, but you can download the available pages indicated by the `availablePages` field.
- When `requestState` is `NOT_STARTED` then simply check the status again.
- When `requestState` is `CANCELLED` then this request is completed by a 'DELETE' call.

## Response 200 body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "listId": 101000000014,
        "requestState": "COMPLETE",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",
        "availablePages": 100
        "successful": true
    }
}
```

Following is the response when the large read request is in progress

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "listId": 101000000014,
        "requestState": "IN_PROGRESS",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",
        "availablePages": 50,
        "successful": true
    }
}
```

---

## Download pages

Use this call to download the available pages, either when the read request is in progress, or when the request is completed. This request returns a CSV format response of the export list items.

You can download pages while the export is in progress. You can download up to `availablePages` number of pages returned by the export status API. Note that page numbers start with zero. That means if 10 pages are available, you can download from page=0 through page=9

**Note**: To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

Request supporting this feature

```js
curl --{location} \
-X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}/pages/{pageNo}' \
-H 'Authorization: AnaplanAuthToken{anaplan_auth_token}' \
-H 'Accept: text/csv'
```

---

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: text/csv` | - Required - Description: This indicates the preferred response is `text/csv` format. |

## Request parameters

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |
| `{pageNo}` | - Required - Type: `Number` - Description: The page number (starting from 0) - Example: `0` |

## Response 200 body

```js
,Parent,Write,Read,Code,favourite,count
cake,,"gord.like@anaplan.com, adam.minister@anaplan.com",,c1,true,1
bread,,,adam.minister@anaplan.com,b2,false,4
pastry,,gord.like@anaplan.com,,p3,true,5
```

---

## Delete read requests

Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request.

**Note**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- As a best practice, use this call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.
- An expiration timer starts after the read request is initiated, with the following conditions:
	- 30 minutes after no activity is recorded for that read request, the system will reclaim that space.
		- The expiration timer resets back to 30 minutes if the requested page number is divisible by 100, including page 0.

## Request supporting this feature

```js
curl -X DELETE 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'
```

## Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is `application/json` format |

## Request parameters

| Parameters | Details |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

## Response 200 body

When the initiated read request ID completes and you delete it, the API returns the following response:

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "listId": 101000000014,
        "requestState": "COMPLETE",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",
        "successful": true
    }
}
```

If the read request is in progress and you initiate the delete call, the API returns the following response:

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "listReadRequest": {
        "requestId": "0A06B0739F0E47BB92E2326C603D86EC",
        "listId": 101000000014,
        "requestState": "CANCELLED",
        "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",
        "successful": true
    }
}
```

---

## Model Calendar

---

View the following endpoints for further details on model calendar APIs:

- [Retrieve current period](#RetrieveCurrentPeriod)
- [Set current period](#SetCurrentPeriod)
- [Get current fiscal year](#GetCurrentFiscalYear)
- [Update current fiscal year](#UpdateCurrentFiscalYear)

---

## Retrieve current period

`/workspaces/{workspaceId}/models/{modelId}/currentPeriod`

Use this call to determine the value of the current period in Anaplan.

If the current period is not set in Anaplan, this call returns empty strings for the `periodText` and `lastDay` values of the `currentPeriod`.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator").

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/currentPeriod' \
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta" : {
    "schema" : "https://api.anaplan.com/2/0/objects/currentPeriod"
  },
  "status" : {
    "code" : 200,
    "message" : "Success"
  },
  "currentPeriod" : {
    "periodText" : "May 20",
    "lastDay" : "2020-05-31",
    "calendarType" : "Calendar Months/Quarters/Years"
  }
}
```

---

## Set current period

`/workspaces/{workspaceId}/models/{modelId}/currentPeriod`

Use this call to change or reset the current period in Anaplan. When this call contains a specified date (for example, 2020-05-20), the API determines what period range contains the specified data and sets that range as the current period. When the date value is set to blank in this call, the API resets the current period to blank.

**Warning**: A change to your time settings is a potentially destructive action and may lead to data loss. The new range of time periods may not include previous time periods. Any data in the removed time periods is deleted from the model.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html "Workspace Administrator")

### Request

```js
curl -X PUT https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/currentPeriod\
-H 'Accept: application/json' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is `application/json` format. |
| `Content-Type: application/json` | - Required - Description: This indicates the call uses a content type of `application/json`. |

### Request parameter

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

### Request body

| Body | Details |
| --- | --- |
| `{date}` | - Required - Type: String - Description: The date to use to set, or reset, the current period. The date format is YYYY-MM-DD.   	If the `date` parameter is left blank (for example, `/currentperiod?date=`) the current period resets.   	If the date is not provided in the YYYY-MM-DD format, the call returns a `400 Bad Request` response with this message: `Invalid ISO date format '{date}'. Date should match format YYYY-MM-DD`   	If this value falls outside of a valid range, the call returns a `400 Bad Request` response with this message: `Specified date '{date}' is out of timescale range {start of timescale} - {end of timescale}`. - Example: 2010-05-20 |

### Example of request body

```js
{
       "date":"2020-05-20"
    }
```

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/objects/currentPeriod"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "currentPeriod":{
      "periodText":"May 20",
      "lastDay":"2020-05-31",
      "calendarType":"Calendar Months/Quarters/Years"
   }
}
```

---

## Get current fiscal year

`/workspaces/{workspaceId}/models/{modelId}/modelCalendar`

Use this call to get the current fiscal year with the start and end date from the model calendar. The value of the start and end date is determined by the calendar type set in the model. This value is not always a range from Jan 1 to Dec 31. The API returns an empty value If the calendar type does not have an available fiscal year (for example, Weeks General).

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration "Workspace Administrator").

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/modelCalendar' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "modelCalendar": {
        "fiscalYear": {
            "year": "FY21",
            "startDate": "2021-01-01",
            "endDate": "2021-12-31"
        }
    }
}
```

### Example 1: Calendar Type: weeks 4-4-5,4-5-4 or 5-4-4

#### Model Calendar

In Anaplan, the **Current Fiscal Year** in the **Model Calendar** is set to *FY21: 29 Mar 2020 - 27 Mar 2021*.

#### Response

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "modelCalendar": {
    "calendarType": "Calendar Months/Quarters/Years",
    "fiscalYear": {
      "year": "FY21",
      "startDate": "2020-03-29",
      "endDate": "2021-03-27"
    },
    "pastYearsCount": 0,
    "futureYearsCount": 0,
    "currentPeriod": {
      "periodText": "",
      "lastDay": ""
    },
    "totalsSelection": {
      "quarterTotals": true,
      "halfYearTotals": false,
      "yearToDateSummary": false,
      "yearToGoSummary": false,
      "totalOfAllPeriods": false
    }
  }
}
```

#### Example 2: Calendar Type: weeks general

#### Model Calendar

In Anaplan, the **Calendar Type** in the **Model Calendar** is set to *weeks general*.

#### Response

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "modelCalendar": {}
}
```

---

## Update current fiscal year

`/workspaces/{workspaceId}/models/{modelId}/modelCalendar/fiscalYear`

Use this call to update the current fiscal year for the model calendar. The year input value has to be a valid fiscal year supported by the model calendar in Anaplan. If successful, this call returns the updated fiscal year with start and end date associated with current model calendar type. This call returns a `400 bad request` message if the input value is out of range or model calendar type does not have an available fiscal year (for example, Weeks General).

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration "Workspace Administrator").

### Request

```js
curl -X PUT 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/modelCalendar/fiscalYear' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
--data-raw '{
    "year": "{fiscal year}"
}'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional |
| `Content-Type: application/json` | - Required |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "modelCalendar": {
        "fiscalYear": {
            "year": "FY21",
            "startDate": "2021-01-01",
            "endDate": "2021-12-31"
        }
    }
}
```

### Example: Out of range error

Input value for `year`

```js
{
    "year": "FY40"
}
```

Response

```js
{
    "status": {
        "code": 400,
        "message": "Specified year is out of range: 2040"
    }
}
```

---

## Model versions

---

- [Retrieve version metadata](#RetrieveVersionMetadata)
- [Set version switchover date](#SetVersionSwitchoverDate)

## Retrieve version metadata

`/models/{modelId}/versions`

Use this call to get information about the model versions. The response contains a list of the versions that the user has access to, and the model metadata that can be viewed from the UI.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- The returned versions only include the user’s model role with read access or higher.
- If the value for a field is set, it will be returned in the results.

### Requests

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/versions' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

### Response header

`Content-Type: application/json`

### Response 200 body

The date format for `editFrom` and `editTo` depends on the model calendar setting.

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/version"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "versionMetadata": [
        {
            "id": "107000000001",
            "name": "Actual",
            "isCurrent": false,
            "isActual": true,
            "editFrom": {
                "periodText": "Start of Timescale",
                "date": "1900-01-01"
            },
            "editTo": {
                "periodText": "End of Timescale",
                "date": "2399-12-31"
            },
            "notes": "This version data is updated every Monday"
        },
        {
            "id": "107000000002",
            "name": "Variance",
            "isCurrent": false,
            "isActual": false,
            "switchover": {
                "periodText": "Mar 20",
                "date": "2020-03-01"
            },
            "formula": "Actual - 20",
            "editFrom": {
                "periodText": "Jan 20",
                "date": "2020-01-01"
            },
            "editTo": {
                "periodText": "Dec 20",
                "date": "2020-12-31"
            }
        }
    ]
}
```

---

## Set version switchover date

`/models/{modelId}/versions/{versionId}/switchover`

Use this call to set the switchover date for a version. The response contains the response code, as well as the date and human-readable date period as shown in the UI.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- To apply a switchover date, ensure the `versionID` corresponds to a version in Anaplan that is set to either `forecast` or `variance`.
- Ensure the switchover date is after the existing version switchover date.
- To reset the switchover date to Blank, pass an empty string in the request body.

### Request

```js
curl -X PUT 'https://api.anaplan.com/2/0/models/{modelId}/versions/{versionId}/switchover' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"date":"{newSwitchoverDate}"}'
```

### Request body

```js
{
    "date" : "{date}"
}
```

| JSON element | Details |
| --- | --- |
| `date` | - Required - Description: An ISO-formatted (YYYY-MM-DD) date string is used to set the switchover date. An empty string resets the switchover date.   	Dates earlier than the current switchover date (for example, `2021-01-01` when the current switchover is `2021-06-01`) or dates outside the current model year return a `400 Bad Request` response. - Example: `2021-06-01` |

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Content-Type: application/json` | - Required - Description: This indicates the request format is `application/json`. |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{versionId}` | - Required - Type: String - Description: the version ID. The ID of the actual version returns a `400 Bad Request` response - Example: `107000000002` |

### Response header

`Content-Type: application/json`

### Response 200 Body

```js
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/objects/switchover"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "versionSwitchover": {
        "periodText": "May 13",
        "date": "2013-05-01",
        "calendarType": "Calendar Months/Quarters/Years"
    }
}
```

---

## Users

---

Endpoints that enable you to obtain user information accessible to you using your authentication token.

As a standard user, you can access the data to which you have been granted access. Endpoints respond with `401 Not Authorized` if you are not authorized to access the data that you are requesting.

Note that these API calls only work with the user's default tenant. They will not return data for any additional tenants the user is assigned to.

View the following endpoints for further details on users APIs:

- [Retrieve your user](#RetrieveYourUser)
- [Retrieve user information](#RetrieveUserInformation)
- [Retrieve user list](#RetrieveUserList)

---

## Retrieve your user

`/users/me`

Retrieves your user based on your Anaplan authentication token.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/users/me \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Required - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/objects/user"
   },
   "user":{
      "id":"8a8b844a477d5da70147d150ee080b17",
      "active":true,
      "email":"a.user@anaplan.com",
      "emailOptIn":true,
      "firstName":"A",
      "lastName":"User",
      "customerId":"8b81da6f5fb6b75701604d6c950c05b1",
      "lastLoginDate":"2017-09-07T08:05:37.000+0000"
   },
   "status":{
      "code":200,
      "message":"Success"
   }
}
```

---

## Retrieve user information

`/users/{userId}`  
Retrieves information about the specified user.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration "Workspace Administrator"), or have any [tenant-level access role](https://help.anaplan.com/09e4cbb5-963d-41b9-a11a-42cc192680d4-Administration "tenant-level access role").

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/users/{userId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

### Parameters

| Parameter | Description |
| --- | --- |
| `userId` | - Optional - Type: string - Description: The user ID - Example: `8a8196a55b193fa0015b1e57f3da172c` |

### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/objects/user"
   },
   "user":{
      "id":"8a8196a55b193fa0015b1e57f3da172c",
      "active":true,
      "email":"a.user@anaplan.com",
      "emailOptIn":true,
      "firstName":"A",
      "lastName":"User",
      "lastLoginDate":"2017-09-07T08:05:37.000+0000"
   },
   "status":{
      "code":200,
      "message":"Success"
   }
}
```

## Retrieve user list

`/users`

Retrieves a list of users.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09-Workspace-administration "Workspace Administrator"), or have any [tenant-level access role](https://help.anaplan.com/09e4cbb5-963d-41b9-a11a-42cc192680d4-Administration "tenant-level access role").

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/users?sort=%2BemailAddress \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

### Headers

| Header | Details |
| --- | --- |
| `Authorization:AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: The Anaplan authentication token |
| `Content-Type:application/json` | - Required - Description: Specifies the content type as `application/json` |

### Parameters

Use the `?sort=%2BemailAddress` parameter to sort the results by email address when you retrieve the results.

### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/objects/user"
   },
   "user":{
      "id":"8a8196a55b193fa0015b1e57f3da172c",
      "active":true,
      "email":"a.user@company.com",
      "emailOptIn":true,
      "firstName":"A",
      "lastName":"User",
      "lastLoginDate":"2017-09-07T08:05:37.000+0000"
   },
   "status":{
      "code":200,
      "message":"Success"
   }
}
```

---

## Upload Files for Actions

---

View the following endpoints for further details on upload files for actions APIs:

- [Get the ID and information for the model file to upload](#GetIdInfoModelUpload)
- [Set the chunk count](#SetChunkCount)
- [Upload file as a single chunk](#UploadFileSingleChunk)
- [Upload a file in chunks](#UploadAFileInChunks)
- [Complete the upload](#CompleteTheUpload)

---

You can either upload a file as a single chunk, or in several chunks. We recommend that you upload files in several chunks. This enables you to resume an upload that fails before the final chunk is uploaded. In addition, you can compress files on the upload action. We recommend compressing single chunks that are larger than 50 MB. This creates a [Private File](#Private-Default-Files).

**Note:** To upload a file using the API that file must exist in Anaplan. If the file has not been previously uploaded, you must upload it initially using the Anaplan user interface. You can then carry out subsequent uploads of that file using the API.

To upload a file:

1. [Set the chunk count](#Set-chunk-count).
2. Upload the file as [a single chunk](#Uploading-single-file) or [in several chunks](#Uploading-chunks).

**Important:** When uploading a file and the default file is set for **Admins only** or **Everyone**, you **MUST** [Set the chunk count](#Set-chunk-count) **BEFORE** uploading it.

## Get the ID and information for the model file to upload

`/workspaces/{workspaceId}/models/{modelId}/files`

To upload a file, you need its ID in Anaplan:

- `id` is the ID that you need to upload the file.
- `name` is the filename of the file.
- `chunkCount` is the number of chunks in the file.
- `delimiter` is double-quotes for columns and fields. For example, "Versions","Opportunities"," "Version 1","Opportunity 0001".
- `encoding` determines the way in which bytes in a file map to Unicode character code points. See [Common Character Encodings](https://en.wikipedia.org/wiki/Character_encoding#Common_character_encodings "Common Character Encodings on Wikipedia") on Wikipedia.
- `firstDataRow` is the first row after the row containing column names.
- `format` is text, as opposed to a binary stream.
- `headerRow` is the row that contains column names.
- `separator` is the token that separates fields. This is typically a comma, for example, "Versions","Opportunities"," "Version 1","Opportunity 0001".

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files \
-H 'Authorization: AnaplanAuthToken {token_value}'
-H 'Accept:application/json'
```

### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Accept:application/json`

### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |

### Response 200 (application/json)

```js
{
  "meta": {
    "paging": {
      "currentPageSize": 9,
      "offset": 0,
      "totalSize": 9
    },
      "schema": "https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/file"
    },
    "status": {
      "code": 200,
      "message": "Success"
    },
  "files": [
    {
      "id": "113000000000",
      "name": "#T & #R.csv",
      "chunkCount": 0,
      "delimiter": "\"",
      "encoding": "ISO-8859-1",
      "firstDataRow": 2,
      "format": "txt",
      "headerRow": 1,
      "separator": ","
    },
    {
      "id": "113000000001",
      "name": "#T & #R-1.csv",
      "chunkCount": 0,
      "delimiter": "\"",
      "encoding": "ISO-8859-1",
      "firstDataRow": 2,
      "format": "txt",
      "headerRow": 1,
      "separator": ","
    },
    {
      "id": "113000000002",
      "name": "Sales metrics (1) - POC load.csv",
      "chunkCount": 0,
      "delimiter": "\"",
      "encoding": "UTF-8",
      "firstDataRow": 2,
      "format": "txt",
      "headerRow": 1,
      "separator": ","
    },
    {
      "id": "116000000001",
      "name": "ExportGrid - ORG2Test.xls",
      "chunkCount": 1,
      "firstDataRow": 0,
      "headerRow": 0
    }
  ]
}
```

---

## Set the Chunk Count

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}`

To upload a file, we recommend setting the `chunkcount` metadata of an upload so that the server knows how many chunks to process during an upload. Set the `chunkcount` to -1 if you do not know how many chunks there will be and will be [marking the upload complete](#Mark-upload-complete) when all chunks have been uploaded. If you want to upload the file in a single chunk, see [Upload file as a single chunk](#Uploading-single-file).

Use chunking:

- If you want to be able to resume the transfer after the connection is lost during an upload.
- If you are extracting data from a database and want to push it to the server without holding all the results in memory.

To avoid consuming large amounts of memory on the server, a chunk is expected to be between 1 and 50 MB. The chunk count might change if the file to upload has become larger or smaller than the server's version of that file:

- `id` is the ID of the file for which the chunk count is to be updated.
- `name` is the filename of the file.
- `chunkCount` is the number of chunks in the file.
- `delimiter` is double-quotes for columns and fields. For example, "Versions","Opportunities"," "Version 1","Opportunity 0001".
- `encoding` determines the way in which bytes in a file map to Unicode character code points. See [Common Character Encodings](https://en.wikipedia.org/wiki/Character_encoding#Common_character_encodings "Common Character Encodings on Wikipedia") on Wikipedia.
- `firstDataRow` is the first row after the row containing column names.
- `format` is text, as opposed to a binary stream.
- `headerRow` is the row that contains column names.
- `separator` is the token that separates fields. This is typically a comma, for example, "Versions","Opportunities"," "Version 1","Opportunity 0001".

### Post the chunk count

#### Request

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId} \
-H 'Authorization: AnaplanAuthToken auth_token' \
-H 'Content-Type: application/json' \
-d '{"chunkCount":1}'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `113000000008` |

#### Response 200 (application/json)

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/file"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "file": {
    "id": "113000000008",
    "name": "Tests.txt",
    "chunkCount": 1,
    "delimiter": "\"",
    "encoding": "ISO-8859-1",
    "firstDataRow": 2,
    "format": "txt",
    "headerRow": 1,
    "separator": "\t"
  }
}
```

---

## Upload file as a single chunk

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId} --upload-file Tests.txt`

You can upload a single file to the server.

**Note:** You cannot compress a file that you are uploading as a single file. If the file is smaller than 1 MB, we recommend you PUT it onto the server by streaming it as an octet stream.

### Upload a single chunk

#### Request

```js
curl -X PUT \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId} \
-H 'authorization: AnaplanAuthToken {auth_token}' \
-H 'Content-Type:application/octet-stream' --upload-file Tests.txt
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/octet-stream`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `113000000008` |

#### Response 204

---

## Upload a file in chunks

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks/{chunkId} -X --upload-file chunk-aa`

Use chunking:

- If you want to be able to resume the transfer after the connection is lost during an upload.
- If you are extracting data from a database and want to push it to the server without holding all the results in memory.

You can split a file into a set of chunks using a shell command such as `split` in shell with this syntax: `split -b [number of bytes] [path and filename] [prefix for output files]` For example: `split -b 15360 ArchivedOpportunities.csv chunk-`

The first chunk might represent the entire file, or the file might consist of multiple chunks. If the file is larger than 1 megabyte, PUT it onto the server by streaming each "chunk" as an octet stream. To do this, specify the header `Content-Type:application/octet-stream`.

We recommend that you specify a chunk size no larger than 50MB of uncompressed data with no more than 1,000 chunks per file. To reduce the upload time for larger chunks, compress the chunks. You can compress the chunks in a folder using a shell command. For example, this command compresses all files within the current folder and those below it if they do not have the file extension.gz:

`find . -type f ! -name '*.gz' -exec gzip "{}" \;`

If you have compressed your chunk files, specify the header `Content-Type:application/x-gzip` instead of `Content-Type:application/octet-stream`. This compresses each chunk with the [gzip format](https://tools.ietf.org/html/rfc1952).

### Upload a file chunk as an octet stream

#### Request

```js
curl -X PUT \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks/0 \
-H 'authorization: AnaplanAuthToken auth_token' \
-H 'Content-Type:application/octet-stream' --upload-file chunk-aa
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/octet-stream`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `113000000008` |
| `chunkId` | - Required - Type: string - Description: The chunk ID of the file. In this case, the first chunk. - Example: `0` |

#### Response 204

---

## Complete the upload

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/complete`

After carrying out an upload with `chunkCount` set to -1, mark it complete.

### Mark the upload complete

#### Request

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/complete \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json' \
-d '{"id":"113000000008","name":"Tests.txt","chunkCount" : 1,"firstDataRow":2,"headerRow":1}'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace Id - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model Id - Example: `FC12345678912343455667` |
| `fileId` | - Required - Type: number - Description: The file Id - Example: `113000000008` |

#### Response 200 (application/json)

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/file"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "file": {
    "id": "113000000008",
    "name": "achunky-aa",
    "chunkCount": 1,
    "delimiter": "\"",
    "encoding": "ISO-8859-1",
    "firstDataRow": 2,
    "format": "txt",
    "headerRow": 1,
    "separator": "\t"
  }
}
```

---

## Import Actions

---

View the following endpoints for further details on import actions APIs:

- [Get the import Id](#GetImportId)
- [Start the import](#StartTheImport)
- [Get a list of the import tasks](#GetListImportTasks)
- [Monitor the import tasks](#MonitorImportTasks)
- [Check dump file for failures](#CheckDumpFile)
- [Download dump file chunks](#DownloadDumpFileChunks)
- [Get the metadata for an import definition](#GetMetadataImportDefinition)
- [Completion failure and data error/warning codes](#CompletionFailureAndDataErrorWarningCodes)

---

You can bring data into Anaplan by importing it with the API. For instance, you can import a file that you have uploaded.

To import your data using the API:

1. [Upload files](#Upload-files).
2. [Get the import id](#Get-import-id) and [Start the import](#Start-import).
3. [Monitor each import task](#Monitor-import-task) using the id that was returned when you [started the import](#Start-import). If you are importing a large file, it might take some time depending on the way in which you import it.
4. [Check for failures in each import task when the import is complete](#Check-for-import-failures).

**Note:** Workspace administrators can run any action regardless of their assigned model role. For example, if you are a Workspace Administrator, an import ignores any [Selective access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698-Selective-Access) and [Dynamic Cell Access](https://help.anaplan.com/55ae93e6-5139-4bbf-93f9-c8cb06f68f75-Dynamic-cell-access) restrictions, in the same way as the desktop experience.

When an import action completes successfully, all downstream calculations are also complete. This includes cells linked by formulas to the cells being updated.

## Getting the import id

`/workspaces/{workspaceId}/models/{modelId}/imports/`

To run an import, you need its id. You can skip this step if you already know the import id.

### Get the import ids

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

#### Response 200 (application/json)

```js
{
  "meta": {
    "paging": {
      "currentPageSize": 8,
      "offset": 0,
      "totalSize": 8
    },
    "schema": "https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/import"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "imports": [
    {
    "id": "112000000007",
    "name": "ORG2Test from Organization.txt",
    "importDataSourceId": "113000000006",
    "importType": "HIERARCHY_DATA"
    }
  ]
}
```

---

## Start the import

`/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/`

You start the import using the POST command. This also receives the task ID value as a JSON object. Once you have started the import, you can use GET to receive a list of the import tasks as a JSON array. You can use this to monitor the status of the import tasks.

**Note:** If GET does not return any tasks, the import is not running or might have completed. Tasks sort in ascending order of creation time, with the newest task at the top of the list. To sort in descending order, append `?sort =- creationTime` to the URL.

### Run the import

#### Request

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json' \
-d "{\"localeName\": \"en_US\"}"
```

#### Request headers

| Header | Details |
| --- | --- |
| `Authorization:AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: The Anaplan authentication token |
| `Content-Type:application/json` | - Required - Description: Specifies the content type as `application/json` |

#### Request Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |

#### Request Body

| Body | Description |
| --- | --- |
| `{"localeName": "en_US"}` | - Required - Description: Specifies the language to use for task status and error messages. `en_US` is the only supported language type. |

#### Response 200 (application/json)

```js
{
 "taskId" : "5E6331685CC648A29B725923B8FAEA1C"
}
```

---

### Get a list of the import tasks

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |

#### Response 200 (application/json)

The IDs are sorted in ascending order of creation, identified by the `creationTime` value.

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/models/F1111111C11111111B11111F1111E11F/objects/task"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "task": {
    "taskId": "9530E1C5CAEB440DAC4E669178787160",
    "taskState": "COMPLETE",
    "creationTime": 1535145471641
  }
}
```

---

## Monitor the import tasks

`/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId}`

### Get the status of an import task

Use this endpoint to get the status of an ongoing import task.

**Notes:**

- As a best practice, we recommend you check the status of an ongoing import action no more than once every 5 seconds. For long running imports it is suggested to check at even longer intervals.
- You can cancel an ongoing monitoring task if you make the same call using the `DELETE` verb instead of the `GET` one.

In the response:

- `currentStep` is the task associated with the specified `taskID`.
- `taskState` is the status that import task.
- `progress` is a double that is typically 1.0.
- `result` is a JSON object that indicates whether a failure dump file was created, the object ID, and whether the task succeeded.
- `taskID` is the ID that you specified in the request.

Here is a list of each possible `taskState`:

| Status | Description |
| --- | --- |
| `NOT_STARTED` | The task is scheduled to run, but has not started yet. |
| `IN_PROGRESS` | The task is currently running. |
| `COMPLETE` | The task has finished running whether successful or not. |
| `CANCELLING` | The task is currently being canceled. Cancellation is not yet complete. |
| `CANCELLED` | The task has been canceled and the changes have been rolled back. |

If failures occur during the import task:

- `details` contains a JSON array that contains debug information
- If a dump file is available, `failureDumpAvailable` is true and `objectId` contains the ID of the dump file. The dump file contains details of the failures that occurred during the import. You can use the `objectId` to [get the dump file](#Check-for-import-failures).

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |
| `taskID` | - Required - Type: string - Description: The task ID - Example: `88E90CC3E2B545C99A262284317F92EB` |

#### Response 200 (application/json)

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/models/F1111111C11111111B11111F1111E11F/objects/task"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "task": {
    "taskId": "1B1D84DDD53847BAA621810B593C3FC1",
    "currentStep": "Complete.",
    "progress": 1.0,
    "result": {
      "details": [
        {
        "localMessageText": "Employees: 90 (0/90) rows successful, 5 ignored ",
        "occurrences": 0,
        "type": "hierarchyRowsProcessed",
        "values": [
          "hierarchyName",
          "Employees",
          "successRowCount",
          "90",
          "successCreateCount",
          "0",
          "successUpdateCount",
          "90",
          "warningsRowCount",
          "0",
          "warningsCreateCount",
          "0",
          "warningsUpdateCount",
          "0",
          "failedCount",
          "0",
          "ignoredCount",
          "5",
          "totalRowCount",
          "95",
          "totalCreateCount",
          "0",
          "totalUpdateCount",
          "90",
          "invalidCount",
          "0",
          "updatedCount",
          "90",
          "renamedCount",
          "90",
          "createdCount",
          "0"
          ]
        }
      ],
    "failureDumpAvailable": false,
    "objectId": "112000000009",
    "successful": true
    },
  "taskState": "COMPLETE",
  "creationTime": 1571258347545
  }
}
```

---

## Check dump file for failures

`/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId}/dump`

If data could not be imported for an import task, a 'dump' file is created depending on the failure. This contains details of the failures that occurred. Use this information to fix the problems and then try the import again.

**Note:** To prevent timeouts on large files, download the dump file in chunks. It is possible to download dump files without chunking, but it is strongly recommended that chunking is used instead.

1. Query the number of chunks in a dump file.
2. Download the chunks sequentially.
3. Concatenate the chunks on your host.

Dump files are:

- Removed 48 hours after the last access of the file or the next time an import task successfully executes with no errors.
- Maintained on a user-by-user basis and overwritten when the user performs the same import.

When an import task has errors, the API maintains a dump file for the task ID with the error. Any earlier task IDs are erased, though `failureDumpAvailable` can be True for those task IDs. If a dump file is removed or replaced, then attempting to download the dump file via the API results in a 404 (Not found) HTTP status.

If you use `/tasks?sort=-creationDate` in the URL, it is possible for tasks created by other users to appear first for which the dump file is unavailable to the accessing user. It is also possible that a task that the accessing user ran, and for which a dump file is still available, to be further down on the same list.

**Note:** The `taskID` is the last task of the user who carried out the specified import.

### Query the number of chunks in a dump file

Begin by querying the number of chunks using the `/chunks` endpoint.

It is possible for a dump file to be very large. To help manage the size of a dump file and prevent timeouts, download the dump file in chunks. Chunks are 10mb or less and numbered sequentially from 0.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId}/dump/chunks
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |
| `taskID` | - Required - Type: string - Description: The task ID - Example: `88E90CC3E2B545C99A262284317F92EB` |

#### Response 200 (application/json)

```js
"_Status_","Column 1","Parent","Code","Start Date","Leave Date","Column 6","Column 7","Start Dates","Column 9","Column 10","Column 11","_Line_","_Error_1_"
{
"meta" : {
    "paging" : {
    "currentPageSize" : 1,
    "offset" : 0,
    "totalSize" : 3
    },
    "schema" : "https://api.anaplan.com/2/0/models/CB0A5A4D5C5943B5837FF42C5FAA95E1/objects/chunk"
},
"status" : {
    "code" : 200,
    "message" : "Success"
},
"chunks" : [ {
    "id" : "0",
    "name" : "Chunk 0"
},
{
    "id" : "1",
    "name" : "Chunk 1"
},
{
    "id" : "2",
    "name" : "Chunk 2"
},
{
    "id" : "3",
    "name" : "Chunk 3"
} ]
```

---

### Download dump file chunks

Once you have the chunk count, download them sequentially and concatenate. The request below downloads chunk 0.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId}/dump/chunks/0
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |
| `taskID` | - Required - Type: string - Description: The task ID - Example: `88E90CC3E2B545C99A262284317F92EB` |

#### Response 200 (application/json)

```js
"_Status_","Column 1","Parent","Code","Start Date","Leave Date","Column 6","Column 7","Start Datesss","Column 9","Column 10","Column 11","_Line_","_Error_1_"
"W","Max Warren",",,","","4/16/12","","","","4/16/12","","","","151","Invalid parent"
"W","Carolyn Tabor","Supply Chain","",",,,","6/30/09","","","6/30/06","","","","153","Invalid date: ,,,"
"E","","Parent","Code","Start Date","Leave Date","","","Start Datesss","","","","11522","Invalid name: Code"
"E","","Parent","Code","Start Date","Leave Date","","","Start Datesss","","","","23043","Invalid name: Code"
```

---

### Get the dump file for an import task (no chunking)

**Note:** To prevent issues that may arise when downloading large dump files, we recommend that dump files are downloaded in chunks. Please see above sections for steps.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/{taskId}/dump
-H authorization:'AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000007` |
| `taskID` | - Required - Type: string - Description: The task ID - Example: `88E90CC3E2B545C99A262284317F92EB` |

#### Response 200 (application/json)

```js
...
  Invalid line item identifier: 00A Partner","Invalid line item identifier: Column 85717 (""02 Customer"")","Invalid line item identifier: Column 85718 (""Existing"")","Invalid line item identifier: Column 85719 (""0"")"
```

---

## Get the metadata for an import definition

`/workspaces/{workspaceId}/models/{modelId}/imports/{importId}`

You can use the API to obtain metadata for an import definition for module and list imports using the import ID. This enables you to use mappings on your imports without querying the import file itself. You can retrieve:

- Name
- Type
- Source
- Column Count

### Get the metadata for an import definition

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` | - Required - Type: number - Description: The import ID - Example: `112000000059` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/importMetadata"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "importMetadata":{
      "name":"Employees from Employees.txt",
      "type":"FILE",
      "source":{
         "textEncoding":"ISO-8859-1",
         "columnSeparator":"\t",
         "textDelimiter":"\"",
         "headerRow":1,
         "firstDataRow":2,
         "decimalSeparator":".",
         "headerNames":[
            "Name",
            "Sales Region",
            "Parent",
            "Code",
            "Sales Team",
            "Start Date",
            "Leave Date",
            "Salary",
            "Address",
            "Quota",
            "Bonus %",
            "Sales Rep",
            "Staff",
            "Exec"
         ],
         "columnCount":14
      }
   }
}
```

#### Response 200 when Type=MODEL (application/json)

```json
{
    "meta": {
        "schema": "https://api.chimera.anaplan.com/2/0/models/F54977A16CEB42EA973197C4B8B9E42B/objects/importMetadata"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "importMetadata": {
        "name": "NCL - Import New G/L Account Code from SAP (B/S)",
        "type": "MODEL"
    }
}
```

---

## Export Actions

---

View the following endpoints for further details on export actions APIs:

- [List the available export definitions as a JSON array](#ListExportDefinitions)
- [Get the metadata for an export definition](#GetMetadataExportDefinition)
- [Start the export](#StartTheExport)
- [Monitor the export tasks](#MonitorExportTasks)
- [Download exported data](#DownloadExportedData)

---

You can retrieve data from Anaplan using an API-driven Export. This creates a [Private File](#Private-Default-Files). When the export is complete, you can download its files. To export data using the API:

1. [GET a list of available Export definitions](#Get-export-id).
2. [POST the export task to run the export](#Post-export-task).
3. [Monitor each export task](#Monitor-export-task) using the ID that was returned when you [started the export](#Post-export-task). If you are exporting a large file, it might take some time.
4. When the export is complete, [download the files](#Download-files).

## List the available export definitions as a JSON array

`/workspaces/{workspaceId}/models/{modelId}/exports`

To run an export, you need the ID of its export definition. You can get a list of the export definitions with their ID for models in your workspace. This enables you to decide on the Export action to carry out. If you already know the ID of the export definition, you can skip this step.

### Get the export definitions for the specified modelID

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/exports \
 -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
 -H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":2,
         "offset":0,
         "totalSize":2
      },
      "schema":"https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/export"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "exports":[
      {
         "id":"116000000000",
         "name":"Deployed quota - Deployed quota.txt",
         "exportType":"TABULAR_MULTI_COLUMN"
      },
      {
         "id":"116000000001",
         "name":"ExportGrid - ORG2Test.xls",
         "exportType":"GRID_CURRENT_PAGE"
      }
   ]
}
```

---

## Get the metadata for an export definition

`/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}`  
You can use the API to obtain metadata, such as column names, data types, and export format, for an export definition, using the model's ID.

- If the export has its line items in columns, `dataTypes` shows the types. `"ENTITY"` is any member of a List.
- If the export has its line items in rows or pages, Anaplan does not know the types and `dataTypes` shows `"MIXED"`.

### Get the metadata for an export definition

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/exports/{exportId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}` `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `exportId` | - Required - Type: number - Description: The export definition ID - Example: `116000000001` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api-stg.anaplan.com/2/0/models/28D168FB7385407A8AC0026487733564/objects/exportMetadata"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "exportMetadata":{
      "columnCount":16,
      "dataTypes":[
         "ENTITY",
         "MIXED",
         "MIXED",
         "MIXED",
         "MIXED"
      ],
      "delimiter":"\"",
      "encoding":"UTF-8",
      "exportFormat":"text/csv",
      "headerNames":[
         "ListWithSemiColonAsSeparator",
         "Parent",
         "Code",
         "DepProjects",
         "col1",
         "col2",
         "col3",
         "col4",
         "data",
         "delete"
      ],
      "listNames":[
         "",
         "",
         "",
         ""
      ],
      "rowCount":20432,
      "separator":","
   }
}
```

**Note:** The `rowCount` value in the response provides an *estimate* of the number of rows for the resulting export. The `rowCount` will likely be slightly different from the exported data.

---

## Start the export

`/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}/tasks`  
You can POST an export task to start the export. This returns a new `taskID`. Once you have started the export, you can use GET to receive a list of the export tasks as a JSON array. You can use this to monitor the status of the export tasks.

### Run the export

This creates a task with the specified exportID and returns the newly-created taskID.

#### Request

Ensure your request contains the body `{"localeName": "en_US"}`. If this is not included the action will not start, and the system will return a `400 Bad Request` response.

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'  \
-H 'Content-Type:application/json' \
-d '{"localeName": "en_US"}'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Body

{"localeName": "en\_US"}

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `exportId` | - Required - Type: number - Description: The export definition ID - Example: `116000000001` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com//2/0/models/736367E9DB484E3AB3A50C3704FD33ED/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "taskId":"F362B99442C54425970E200037D48A91"
   }
}
```

---

### Get a list of the export tasks

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `exportId` | - Required - Type: number - Description: The export definition ID - Example: `116000000001` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":2,
         "offset":0,
         "totalSize":2
      },
      "schema":"https://api.anaplan.com//2/0/models/736367E9DB484E3AB3A50C3704FD33ED/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "tasks":[
      {
         "taskId":"08990C16C3464583B6E16BD851E0F8AE",
         "taskState":"IN_PROGRESS",
         "creationTime":1535145394668
      }
   ]
}
```

---

## Monitor the export tasks

`/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}/tasks/{taskId}`

### Get the status of an export task

Use this endpoint to get the status of a specific export task.

**Notes:**

- As a best practice, we recommend you check the status of an ongoing export action no more than once every 5 seconds. For long running exports it is suggested to check at even longer intervals.
- You can cancel an ongoing monitoring task if you make the same call using the `DELETE` verb instead of the `GET` one.

In the response:

- `currentStep` is the task associated with the specified `taskID`.
- `taskState` is the status of that export task.
- `progress` is a double that is typically 1.0.
- `result` is a JSON object that indicates the object ID, and whether the task succeeded.
- `taskId` is the ID that you specified in the request.

Here is a list of each possible `taskState`:

| Status | Description |
| --- | --- |
| NOT\_STARTED | The task is scheduled to run, but has not started yet. |
| IN\_PROGRESS | The task is currently running. |
| COMPLETE | The task has finished running whether successful or not. |
| CANCELLING | The task is currently being canceled. Cancellation is not yet complete. |
| CANCELLED | The task has been canceled and the changes have been rolled back. |

If failures occur during the export task `details` contains a JSON array that contains debug information

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/exports/{exportId}/tasks/{taskId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `exportId` | - Required - Type: number - Description: The export definition ID - Example: `116000000001` |
| `taskId` | - Required - Type: string - Description: The task ID - Example: `81374848BFED4C52A9927048FA77AA05` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com//2/0/models/736367E9DB484E3AB3A50C3704FD33ED/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "type":"taskInformation",
      "taskId":"BFEC582EBD4146068FE4061831C8F0F0",
      "currentStep":"Complete.",
      "progress":1,
      "result":{
         "failureDumpAvailable":false,
         "objectId":"116000000002",
         "successful":true
      },
      "taskState":"COMPLETE"
   }
}
```

---

## Download exported data

After completing the export of data, you need to download it. For this, please refer to [Download Files for Actions](#Download-files).

---

## Completion, failure, and data error/warning codes for import and export actions

---

### Headers

`Content-Type: application/json`

#### Completion codes

The following detail elements summarise the successful completion of an action.

| Code | Message |
| --- | --- |
| `deleteFromSelectionSucceeded` | ${affectedItems} items were deleted from the list ${targetName} using ${filterName} |
| `exportSucceeded` | Export for ${exportName} completed successfully. ${fileSize} bytes written. |
| `hierarchyNoChanges` | \`${hierarchyName}: no changes required |
| `hierarchyRowsProcessedFromLineItem` | ${module name}: ${createdCount} created, ${renamedCount} renamed, ${updatedCount} properties updated |
| `hierarchyRowsProcessed` | ${hierarchyName}: ${successRowCount} (${successCreateCount}/${successUpdateCount}) rows successful, ${ignoredCount} ignored |
| `hierarchyRowsProcessedWithFailuresFromLineItem` | ${module name}: ${createdCount} created, ${renamedCount} renamed, ${updatedCount} properties updated, ${failedCount} failed |
| `hierarchyRowsProcessedWithFailures` | ${hierarchyName}: ${successRowCount} (${successCreateCount}/${successUpdateCount}) rows successful, ${warningsRowCount} (${warningsCreateCount}/${warningsUpdateCount}) rows has warnings, ${failedCount} failed, ${ignoredCount} ignored |
| `hierarchyRowsProcessedWithInvalidNamesAndFailures` | ${hierarchyName}: ${createdCount} created / ${renamedCount} renamed (${invalidCount} invalid), ${updatedCount} properties updated, ${failedCount} failed |
| `hierarchyRowsProcessedWithInvalidNames` | ${hierarchyName}: ${createdCount} created / ${renamedCount} renamed (${invalidCount} invalid), ${updatedCount} properties updated |
| `hierarchyRowsProcessedWithWarnings` | ${hierarchyName}: ${successRowCount} (${successCreateCount}/${successUpdateCount}) rows successful, ${warningsRowCount} (${warningsCreateCount}/${warningsUpdateCount}) rows has warnings, ${ignoredCount} ignored |
| `lineItemRowsProcessed` | ${lineItemName} cells: ${rowCount} |
| `lineItemRowsProcessedWithFailuresAndIgnored` | ${lineItemName} cells: ${rowCount} (${failureCount} failed, ${ignoredCount} ignored) |
| `lineItemRowsProcessedWithFailures` | ${lineItemName} cells: ${rowCount} (${failureCount} failed) |
| `lineItemRowsProcessedWithIgnored` | ${lineItemName} cells: ${rowCount} (${ignoredCount} ignored) |
| `taskElementSucceeded` | ${message} |
| `usersNoChanges` | Users: no changes required |
| `usersRowsProcessed` | Users: ${createdCount} created, ${updatedCount} permissions updated |
| `usersRowsProcessedWithFailures` | Users: ${createdCount} created, ${updatedCount} permissions updated (${failedCount} failed) |
| `usersRowsProcessedWithInvalidNamesAndFailures` | Users: ${createdCount} created (${invalidCount} invalid), ${updatedCount} permissions updated (${failedCount} failed) |
| `usersRowsProcessedWithInvalidNames` | Users: ${createdCount} created (${invalidCount} invalid), ${updatedCount} permissions updated |
| `versionsNoChanges` | Versions: no changes required |
| `versionsRowsProcessed` | Versions: ${createdCount} created, ${updatedCount} properties updated |
| `versionsRowsProcessedWithFailures` | Versions: ${createdCount} created, ${updatedCount} properties updated (${failedCount} failed) |

#### Failure codes

If an action could not complete, one of the following detail elements will provide more detail.

| Code | Message | Required amendments |
| --- | --- | --- |
| `actionFailed` | Action failed. ${failureDetails} | Check the action was set up correctly. |
| `connectorError` | Failed to read data: ${message} | Please try again or contact support. |
| `crossCustomerImport` | Both target and source workspaces must be associated with the same customer | Use a target and source workspace that have the same tenant. |
| `deleteFromSelectionFailed` | Deleting from the list ${targetName} using ${filterName} failed: ${errorMessage} | Check if the list is set up correctly. |
| `failedToCreateRevision` | ${title}. ${subtitle} ${messageText} | Please read the message text and resolve. |
| `failedToLocateEntity` | Failed to locate ${entityType} ${entityName} | Check if this has removed. |
| `failedToLocateHierarchy` | Failed to locate list ${entityName} | Check if the list has been removed. |
| `failedToLocateModel` | Failed to locate model (${modelName}) | Check if this model still exists or if it's needs to be unarchived. |
| `failedToLocateModule` | Failed to locate module ${entityName} | Check if this module still exists. |
| `failedToLocateSavedView` | Failed to locate saved view ${entityName} | Check if this saved view was deleted. |
| `hierarchyImportBombed` | Import into ${hierarchyName} list failed an internal error occurred | Please try again or contact support. |
| `hierarchyImportDuplicateSourceKey` | Property-based list import has disallowed duplicate properties for given key in source data - cannot proceed | Remove the duplicates. |
| `hierarchyImportDuplicateTargetKey` | Property-based list import has disallowed duplicate properties for given key in target data - cannot proceed | Remove the duplicates. |
| `hierarchyImportFailed` | Import into ${hierarchyName}list failed ${message} | Check if your import was set up correctly. |
| `hierarchyImportFailedToUpdateProperties` | An internal error occurred and properties were not updated | Please try again or contact support. |
| `hierarchyImportInconsistentRenaming` | Import into ${hierarchyName} list failed: inconsistent renaming found for same code - check mapping and/or data | Check if your mapping set up is correct or if you need to make changes to your data. |
| `hierarchyImportNameAndCodeUnmapped` | The import has both Name and Code unmapped - cannot proceed | Make sure you have the correct map settings and try again. |
| `hierarchyImportNameOrCodeSameAsParent` | The import has name or code mapped to same source as parent - cannot proceed | Use a different source. |
| `hierarchyImportNoSelectiveEditing` | You are not authorised to make changes to list: ${hierarchyName} - cannot proceed | Check if you can change your permissions to make this change. |
| `hierarchyImportPropertyKeyCalculated` | Property-based import uses a calculated property in its key, but this is not permitted - cannot proceed | Remove the calculated property in the key. |
| `hierarchyImportPropertyKeyInvalidMissing` | Property-based import uses an invalid key (property missing) - cannot proceed | Include the missing property in the key. |
| `hierarchyImportPropertyKeyInvalidNoDefintion` | Property-based import uses an invalid key (no property definition) - cannot proceed | Use a valid key. |
| `hierarchyImportPropertyKeyInvalidSystem` | Property-based import uses an invalid key (disallowed property) - cannot proceed | Use a valid key. |
| `hierarchyImportPropertyKeyUnmapped` | Property-based import has one of the key properties unmapped - cannot proceed | Make sure you have the correct map settings and try again. |
| `hierarchyImportUniqueness` | Import into ${hierarchyName} list failed: distinct names found for same code - check mapping and/or data | Check if your mapping set up is correct or if you need to make changes to your data. |
| `importFailedGeneralError` | ${errorMessage} | Check if the import is set up correctly. |
| `internalError` | An internal error occurred: ${message} | Please try again or contact support. |
| `missingFields` | Warning: Import is incomplete as the following fields are unavailable: ${fields} | Complete the missing fields. |
| `modelObjectNotLocated` | Model object "${modelObject}" could not be located | Check if the model object still exists. |
| `modelObjectNotSupported` | Model object "${modelObject}" is not a supported source | Use a supported model object. |
| `moduleImportFailed` | Import into ${moduleName} module failed: ${message} | Check if the module still exists. If it does, please try again or contact support. |
| `moduleImportNoWriteAccess` | You are not authorised to make changes to module: ${moduleName} - cannot proceed | You do not have permissions to make changes to this module. Check with your workspace administrator if they can grant you permissions. |
| `msgExportCancelled` | Export cancelled by user | \--- |
| `msgImportCancelled` | Import cancelled by user | \--- |
| `msgTooManyColumns` | Excel workbooks cannot support more than 256 columns | Make sure you have no more than 256 columns, or use a different export format. |
| `msgTooManyRows` | Excel workbooks cannot support more than 65536 rows | Make sure you have no more than 65536 rows, or use a different export format. |
| `noAccessToModule` | Your role does not permit any access to the source module. | Ask your workspace administrator to give you access to the model. |
| `notAuthorised` | You are not authorised to run ${actionName} | Check if you can change your permissions so you can run the action. |
| `sourceModelArchived` | Source model is archived (${modelId}/${modelName}) | Unarchive the model to use it as a source model. |
| `sourceWorkspaceNoAccess` | You do not have access to the source workspace | Ask your tenant administrator for access. |
| `sourceWorkspaceNotLocated` | Failed to locate source workspace | Check if this workspace was deleted. |
| `taskElementFailed` | ${errorMessage} | Check if you can amend the error. |
| `uploadedFileNoLongerAvailable` | The uploaded file is no longer available. Please upload the file again. | Upload the file again. |
| `usersImportBombed` | Import into Users list failed: An internal error occurred | Please try again or contact support. |
| `usersImportFailed` | Import into Users list failed: ${message} | Please read the message text and resolve. |
| `versionImportPropertyChangeFailed` | Failed to update version property | Check your versions are set up correctly. |
| `versionsImportBombed` | Import into Versions failed: An internal error occurred | Please try again or contact support. |
| `versionsImportFailed` | Import into Versions failed: ${message} | Check your versions are set up correctly. |

#### Data error/warning codes

If one or more data rows could not be accepted during an import, additional detail entries will be provided with counts.

| Code | Message | Required amendments |
| --- | --- | --- |
| `columnSeparatorExpected` | Column separator expected at line ${lineNumber}, character ${position} | Include the column separator and missing character. |
| `dateFormatInvalid` | Date format is invalid: ${format} | Check the date format is correct. |
| `dateFormatMalformed` | Date format is malformed: ${format} | Check the date format is correct. |
| `expectedCharacter` | Expected character in date/period | Check the date format is correct. |
| `expectedDD` | Expected 2-digit day number in date/period | Check the date format is correct. |
| `expectedD` | Expected day number in date/period | Check the date format is correct. |
| `expectedH` | Expected year half number in date/period | Check the date format is correct. |
| `expectedM` | Expected month name or number in date/period | Check the date format is correct. |
| `expectedMM` | Expected 2-digit month number in date/period | Check the date format is correct. |
| `expectedMMM` | Expected abbreviated month name in date/period | Check the date format is correct. |
| `expectedMMMM` | Expected full month name in date/period | Check the date format is correct. |
| `expectedQ` | Expected fiscal quarter number in date/period | Check the date format is correct. |
| `expectedSeparator` | Expected separator in date/period | Check the date format is correct. |
| `expectedW` | Expected week number in date/period | Check the date format is correct. |
| `expectedWW` | Expected 2-digit week number in date/period | Check the date format is correct. |
| `expectedY` | Expected 2 or 4-digit year in date/period | Check the date format is correct. |
| `expectedYY` | Expected 2-digit year in date/period | Check the date format is correct. |
| `expectedYYYY` | Expected 4-digit year in date/period | Check the date format is correct. |
| `hierarchyImportAccessCantMoveFromParent` | You are not authorised to move item from parent: ${parent} | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessCantMoveToParent` | You are not authorised to move item to parent: ${parent} | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoCreateWithoutParent` | You are not authorised to insert an item without a parent | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoImplicitAddToTopLevel` | You are not authorised to insert ${parent} below ${topLevel} | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoImplicitCreate` | You are not authorised to insert parent: ${parent} | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoMoveWithoutParent` | You are not authorised to move an item without a parent | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoMoveWithoutParent` | You are not authorised to move an item without a parent | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoMove` | You are not authorised to move this entity | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoRemoveParent` | You are not authorised to remove the parent from this entity | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoRemoveParent` | You are not authorised to remove the parent from this entity | Check if you can change your permissions to make this change. |
| `hierarchyImportAccessNoUpdate` | You are not authorised to update this entity | Check if you can change your permissions to make this update. |
| `hierarchyImportCancelledByUser` | Properties were not updated as import was cancelled | Reset the import. |
| `hierarchyImportCannotChangeCodeForTopLevel` | Cannot change code for list's top level item | \--- |
| `hierarchyImportDuplicateKeyInSource` | Another row has already been processed with this key | This process has already completed so there's no need to duplicate it. |
| `hierarchyImportDuplicateKeyInTarget` | Key for this row maps to more than one list member | Make sure the row can only map to one list item. |
| `hierarchyImportEmptyKey` | Error parsing key for this row; no values | Add some values. |
| `hierarchyImportFailedDependency` | Has dependency on rejected row | Reset the dependency structure. |
| `hierarchyImportInvalidCode` | Invalid code | Use an valid code. |
| `hierarchyImportInvalidEntityIdInKey` | Error in key for this row; refers to invalid list item: ${value} | Use valid list items only. |
| `hierarchyImportInvalidName` | Invalid name | Use a valid name. |
| `hierarchyImportInvalidParent` | Invalid parent | Use a valid parent. |
| `hierarchyImportInvalidStatus` | Invalid workflow status | Use a valid workflow status. |
| `hierarchyImportNameOrCodeExists` | New property combination found but name or code already exists | Use a different name. |
| `hierarchyImportNewEntityNumberedList` | Cannot import record into numbered list as it has a new name (${name}) | Reset the import to be compatible with the new name. |
| `hierarchyImportNoNameOrCode` | New property combination found but no name or code is provided | Provide a name. |
| `hierarchyImportParentMustBeLeaf` | Parent item has a child item that is in a different list: You can only add a child to a parent item, if any existing children of that parent item belong to the same list. | Use a child item that is in the same list as the parent item. |
| `hierarchyImportParseErrorInKey` | Error parsing key for this row; invalid data: ${value} | Use valid data. |
| `hierarchyImportPropertyChangeFailed` | Failed to create property change: ${message} | Please try again or contact support. |
| `invalidDate` | Invalid date for format ${format} | Check the date format is correct. |
| `invalidPeriod` | Invalid period for format ${format} | Check the time period format is correct. |
| `moduleImportBooleanFormat` | Invalid Boolean (yes/no/true/false) | Use a valid Boolean. |
| `moduleImportDateFormat` | Invalid date | Use a valid date. |
| `moduleImportDimensionIdentifiersUnmapped` | ${count} ${dimension} identifier(s) (${items}) were not mapped and ignored | These dimensions were not mappable. Change your column mapping setup to map these dimensions. |
| `moduleImportInvalidLineItemIdentifier` | Invalid line item identifier | Use a valid line item identifier. |
| `moduleImportInvalidListIdentifier` | Item not located in ${hierarchyName} list | The item does not display in this list. Use an item that exists in this list. |
| `moduleImportInvalidTimeEntityIdentifier` | Item not located in calendar for period type ${periodType} | Use a different item or change your calendar settings to include this item. |
| `moduleImportInvalidTimescaleIdentifier` | Invalid date or timescale identifier | Use a valid time dimension. |
| `moduleImportLineItemIdentifiersUnmapped` | ${count} Line Item identifier(s) (${items}) were not mapped and ignored | These items were not mappable. Change your column mapping setup to map these items. |
| `moduleImportNumberFormat` | Invalid number | Use a valid number. |
| `moduleImportRepeatedNonNumeric` | More than one data value has been provided for a non-numeric cell. | Check the data source is normalized. |
| `periodFormatMalformed` | Period format is malformed: ${format} | Check the time period format is correct. |
| `unmatchedTextDelimiter` | Unmatched delimiter character at line ${lineNumber}, character ${position} | Check you've only used valid characters. |
| `usersImportConflictingAccessLevel` | Conflicting access levels | Check the access levels are issued correctly. |
| `usersImportConflictingAncestry` | Access to parent item overrides that to child item | Check the set up for parent to child items is correct. |
| `usersImportConflictingNames` | Conflicting names for user | Use one full name only for each user. |
| `usersImportConflictingRoles` | Conflicting roles for user | Check the user's roles are assigned correctly. |
| `usersImportCreationFailed` | User creation failed | Check you have used the correct settings. |
| `usersImportFirstNameMissing` | First name missing for new user | Include the user's first name. |
| `usersImportInvalidEmail` | Invalid email address | Use a valid email address. |
| `usersImportInvalidListIdentifier` | Item not located in ${list Name} list | Use an item that's part of this list. |
| `usersImportInvalidRole` | Invalid role | Select a valid role. |
| `usersImportLastNameMissing` | Last name missing for new user | Include the user's last name. |
| `usersImportNoSelectiveAccess` | List ${list Id} no longer has selective access control | Apply selective access to the list. |
| `usersImportSSOStatusChangeFailed` | User SSO status change failed | Check the user's SSO settings are correct. |

---

## Retrieve logs

---

## Retrieve Optimizer action log

`/workspaces/{workspaceId}/models/{modelId}/optimizeActions/{actionId}/tasks/{correlationId}/solutionLogs`

This endpoint enables a workspace administrator to download the Anaplan Optimizer log. This is useful for root cause analysis when an error occurs.

To use this endpoint, you must supply a valid authentication, the Optimizer action id (see [List model actions](#list-model-actions)), and the correlation id, obtained from the Anaplan UI.

**Note:**

- Anaplan Optimizer logs are automatically removed 48 hours after the last access.
- You must have Workspace Administrator permissions in the model.

### Request

```shell
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/optimizeActions/{actionId}/tasks/{correlationId}/solutionLogs \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'
-H 'Accept:text/plain'
```

#### Headers

| Header | Details |
| --- | --- |
| `Authorization:AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: The Anaplan authentication token |
| `Content-Type:text/plain` | - Required - Description: Specifies the content type as `text/plain` |

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |
| `actionId` | - Required - Type: string - Description: The Optimizer action's ID, obtained from [List model actions](#list-model-actions). - Example:`117000000002` |
| `correlationId` | - Required - Type: string - Description: The Optimizer log's correlation ID, obtained from the Anaplan UI, after running an Optimizer action. - Example:`C73885D890BC44BD8000A910A5CFF3C2` |

### Response

#### Response 200

```js
Optimize a model with 4 rows, 4 columns and 16 nonzeros
Model fingerprint: 0x331b37fc
Variable types: 0 continuous, 4 integer (0 binary)
Coefficient statistics:
Matrix range     [3e+00, 3e+02]
Objective range  [2e+01, 3e+02]
Bounds range     [7e+00, 7e+00]
RHS range        [7e+02, 7e+02]
Found heuristic solution: objective 2394.0000000
Presolve time: 0.00s
Presolved: 4 rows, 4 columns, 16 nonzeros
Variable types: 0 continuous, 4 integer (0 binary)
Found heuristic solution: objective 2208.0000000
 
Root relaxation: objective 1.398644e+03, 3 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |         Work   
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time
 
   0     0 1398.64424    0    3 2208.00000 1398.64424  36.7%     -    0s
   H    0     0                    1820.0000000 1398.64424  23.2%     -    0s

Explored 1 nodes (3 simplex iterations) in 0.01 seconds (0.00 work units)

Solution count 3: 1820 2208 2394 

Optimal solution found (tolerance 1.00e-04)
Best objective 1.820000000000e+03, best bound 1.820000000000e+03, gap 0.0000%

User-callback calls 152, time in user-callback 0.00 sec
```

---

## Download Files for Actions

---

View the following endpoints for further details on download files for actions APIs:

- [Get the list of export files](#GetListExportFiles)
- [Get the chunks in a file](#GetTheChunksInAFile)
- [Get the data in a chunk](#GetDataInAChunk)
- [Delete files](#DeleteFiles)

---

You can download files that were uploaded or download files after carrying out an export.

## Get the list of export files

`/workspaces/{workspaceId}/models/{modelId}/files`

### file list

This gets a list of both the import and export files for a model. You can identify an export file by its metadata and `id`. Export files have fewer metadata properties and the start of the first part of their ID is different to that of an import file:

- `id` is the file id.
- `name` is the file name.
- `chunkCount` is the number of chunks in the file.
- `firstDataRow` is the first row after the row containing column names.
- `headerRow` is the row that contains column names.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":3,
         "offset":0,
         "totalSize":3
      },
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/file"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "files":[
      {
         "id":"113000000000",
         "name":"UploadedWork.csv",
         "chunkCount":0,
         "delimiter":"\"",
         "encoding":"UTF-8",
         "firstDataRow":2,
         "format":"txt",
         "headerRow":1,
         "separator":","
      },
      {
         "id":"113000000003",
         "name":"FileUploadB2.csv",
         "chunkCount":1,
         "delimiter":"\"",
         "encoding":"UTF-8",
         "firstDataRow":2,
         "format":"txt",
         "headerRow":1,
         "separator":","
      },
      {
         "id":"116000000000",
         "name":"ExportFile12.csv",
         "chunkCount":0,
         "firstDataRow":0,
         "headerRow":0
      }
   ]
}
```

---

## Get the chunks in a file

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks`

To download a file in chunks, you need the ID of each chunk that you want.

### Get each chunk ID and name

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `116000000005` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":4,
         "offset":0,
         "totalSize":4
      },
      "schema":"https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/chunk"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "chunks":[
      {
         "id":"0",
         "name":"Chunk 0"
      },
      {
         "id":"1",
         "name":"Chunk 1"
      },
      {
         "id":"2",
         "name":"Chunk 2"
      },
      {
         "id":"3",
         "name":"Chunk 3"
      }
   ]
}
```

---

## Get the data in a chunk

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks/{chunkId}`

Once you know the ID of the chunk you want, the next step is to get the data for that chunk.

### Get a chunk of data

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks/{chunkId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `116000000005` |
| `chunkId` | - Required - Type: string - Description: The chunk ID of the file. In this case, the first chunk. - Example: `0` |

#### Response 200 (application/json)

```js
...
Week 31 FY15 Angrezani, Katia Giovana Viegas 248641 0 0
Week 31 FY15 Dias, Katiucia Oliveira 248247 0 0
Week 31 FY15 da Conceicao, Rafael Gomes 247118 0 0
```

---

## Delete Files

`/workspaces/{workspaceId}/models/{modelId}/files/{fileId}`

You can delete files that you have uploaded using the API.

**Note:** This only removes private content. Default content and the import data source model object remain.

### Delete a file that you have uploaded

#### Request

```js
curl -X DELETE \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `fileId` | - Required - Type: number - Description: The file ID - Example: `113000000002` |

#### Response 204

---

## Get model actions

---

View the following endpoints for more information on retrieving model actions:

- [List model actions](#list-model-actions)
- [Retrieve metadata for model action](#retrieve-action-metadata)

## Retrieve model actions

`/workspaces/{workspaceId}/models/{modelId}/actions`

This lists the actions available for the given model ID. The response comes in the form of a JSON array containing the list of actions that you can carry out, with the following values:

- `id` is the Id of the action that you can carry out in the specified model.
- `actionType` is the type of action contained in the model.
- `name` is the name of the action that you can carry out. You can view these actions in the Anaplan user interface in the Action settings for the model.

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

### Response 200 (application/json)

```json
{
    "meta": {
        "paging": {
            "currentPageSize": 11,
            "offset": 0,
            "totalSize": 11
        },
        "schema": "https://api.anaplan.com/2/0//models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "actions": [
        {
            "id": "117000000011",
            "actionType": "DELETE_BY_SELECTION",
            "name": "Delete From List Action"
        },
        {
            "id": "117000000010",
            "actionType": "ORDER_HIERARCHY",
            "name": "Order List Action"
        },
        {
            "id": "117000000009",
            "name": "Open Dashboard Action"
        },
        {
            "id": "117000000008",
            "actionType": "SIMPLE_CREATE",
            "name": "Create Action"
        },
        {
            "id": "117000000007",
            "actionType": "BULK_DELETE_ENTITIES",
            "name": "Delete Branch Action"
        },
        {
            "id": "117000000006",
            "actionType": "SELECT_CHILDREN",
            "name": "Assign Action"
        },
        {
            "id": "117000000005",
            "actionType": "UPDATE_CURRENT_PERIOD",
            "name": "Update Current Period Action"
        },
        {
            "id": "117000000003",
            "actionType": "BULK_ENTITY_COPY",
            "name": "Copy Branch Action"
        },
        {
            "id": "117000000004",
            "actionType": "COPY_TO_NUMBERED_LIST",
            "name": "Assign Only Action"
        },
        {
            "id": "117000000002",
            "actionType": "OPTIMIZER",
            "name": "Optimizer Action"
        },
        {
            "id": "117000000001",
            "actionType": "BULK_COPY",
            "name": "Bulk Copy Action Via Versions"
        }
    ]
}
```

---

## Retrieve action metadata

`/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}`

### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions/{actionId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

### Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| `workspaceId` | Yes | string | The workspace ID | `8a8b8c8d8e8f8g8i` |
| `modelId` | Yes | string | The model ID | `75A40874E6B64FA3AE0743278996850F` |
| `actionId` | Yes | string | The action ID | `117000000019` |

### Response

#### Response 200 for a delete from list action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000011",
        "listId": "101000000015",
        "filterLineItemId": "503000000001",
        "actionType": "DELETE_BY_SELECTION",
        "name": "Delete From List Action"
    }
}
```

#### Response 200 for order list action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000010",
        "listId": "101000000004",
        "sortOrder": "Descending",
        "lineItemId": "411000000002",
        "actionType": "ORDER_HIERARCHY",
        "name": "Order List Action"
    }
}
```

#### Response 200 for open dashboard action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000009",
        "name": "Open Dashboard Action"
    }
}
```

#### Response 200 for create action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000008",
        "actionType": "SIMPLE_CREATE",
        "name": "Create Action"
    }
}
```

#### Response 200 for delete branch action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000007",
        "actionType": "BULK_DELETE_ENTITIES",
        "name": "Delete Branch Action"
    }
}
```

#### Response 200 for assign action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000006",
        "actionType": "SELECT_CHILDREN",
        "name": "Assign Action"
    }
}
```

#### Response 200 for update current period

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000005",
        "actionType": "UPDATE_CURRENT_PERIOD",
        "name": "Update Current Period Action"
    }
}
```

#### Response 200 for copy branch action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000003",
        "actionType": "BULK_ENTITY_COPY",
        "name": "Copy Branch Action"
    }
}
```

#### Response 200 for assign only action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000004",
        "actionType": "COPY_TO_NUMBERED_LIST",
        "name": "Assign Only Action"
    }
}
```

#### Response 200 for Optimizer action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000002",
        "actionType": "OPTIMIZER",
        "name": "Optimizer Action"
    }
}
```

#### Response 200 for bulk copy action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000001",
        "targetMember": "107000000002",
        "listId": "9000000002",
        "sourceMember": "107000000001",
        "actionType": "BULK_COPY",
        "name": "Bulk Copy Action Via Versions"
    }
}
```

#### Response 200 for a long action name (max. 60 chars) with special characters

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000001",
        "targetMember": "107000000002",
        "listId": "9000000002",
        "sourceMember": "107000000001",
        "actionType": "BULK_COPY",
        "name": "longactionname±!@£$%^&*💖}{\\\":<?>±!@£$%^?éâîôñ\\\"~\`-=\\\\'./,]["
    }
}
```

#### Response 200 for update current period action

```json
{
    "meta": {
        "schema": "https://api.anaplan.com/2/0/models/F7F3D1004C214A00A44C1655DE413B50/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000005",
        "actionType": "UPDATE_CURRENT_PERIOD",
        "name": "Update Current Period Action"
    }
}
```

#### Response 200 for a related line item which has been deleted

```json
{
    "meta": {
        "schema": "https://api.r2p2.anaplan.com/2/0/models/CB6CD83523D84EC8803E29DBAD5CF1E1/objects/action"
    },
    "status": {
        "code": 200,
        "message": "Success"
    },
    "action": {
        "id": "117000000010",
        "sortOrder": "Descending",
        "listId": "101000000004",
        "lineItemId": "",
        "actionType": "ORDER_HIERARCHY",
        "name": "Order List Action"
    }
}
```

#### Response 404 for invalid action Id

```json
{
    "status": {
        "code": 404,
        "message": "Not Found"
    },
    "path": "/2/0/workspaces/e4c0824a889f59d601889f5f236b0001/models/F7F3D1004C214A00A44C1655DE413B50/actions/33",
    "timestamp": "2023-06-09T12:07:17.659388Z"
}
```

---

## Delete Actions

---

View the following endpoints for further details on delete actions APIs:

- [List the actions in the model as a JSON array](#ListActionsInAModel)
- [Start deletion](#StartDeletion)
- [Monitor the deletion tasks](#MonitorDeletionTasks)

---

You can use this API to automate the the removal of specific items from a list using the 'Delete from List Using Selection' functionality in Anaplan.

**Tip:** To use this functionality, an appropriate 'Delete from list Using Selection' action must exist in the model that you want to delete from a list. You can create a control module to select the items to be deleted from the list and then create a 'Delete from List using Selection' action. See [Delete from List using Selection](https://help.anaplan.com/anapedia/default.htm#cshid=1196) for further information.

To carry out a delete operation using the API:

1. [Verify that the delete action is available](#list-available-operations).
2. [Run the delete action](#Start-deletion).
3. [Get a list of deletion tasks](#Get-deletion-tasks) and [monitor each deletion task](#Monitor-deletion-task).

## List the actions in the model as a JSON array

`/workspaces/{workspaceId}/models/{modelId}/actions`

This lists the delete actions available for the given model ID. This returns a JSON array containing the list of delete actions that you can carry out:

- `id` is the Id of the action that you can carry out in the specified model.
- `name` is the name of the action that you can carry out. You can view these actions in the Anaplan user interface in the Action settings for the model.

### Get the deletion actions

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

#### Response 200 (application/json)

```js
{
   "actions":[
      {
         "id":"117000000019",
         "name":"Delete From Org 2"
      },
      {
         "id":"117000000018",
         "name":"Open Other Buttons"
      },
      {
         "id":"117000000017",
         "name":"Delete Branch"
      }
   ]
}
```

---

## Start deletion

`/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}/tasks`

You can POST a deletion task to start the delete. This returns a new `taskID`. Once you have started the delete, you can use GET to receive a list of the deletion tasks as a JSON array. You can use this to monitor the status of the delete.

### Run deletion

#### Request

Ensure your request contains the body `{"localeName": "en_US"}`. If this is not included the action will not start, and the system will return a `400 Bad Request` response.

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Content-Type:application/json' \
-d '{"localeName": "en_US"}'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Body

{"localeName": "en\_US"}

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `actionId` | - Required - Type: number - Description: The ID for the Delete action. - Example: `117000000019` |

#### Response 200 (application/json)

```js
{
   "task":{
      "taskId":"0690AA1C761F48549C3442A02F91D962"
   }
}
```

---

### Get a list of deletion tasks

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `actionId` | - Required - Type: number - Description: The ID for the Delete action. - Example: `117000000019` |

#### Response 200 (application/json)

```js
{
   "tasks":[
      {
         "taskId":"F37EA1512BC448D3B223431C33B844B6",
         "taskState":"COMPLETE",
         "creationTime":1535145589808
      }
   ]
}
```

---

## Monitor the deletion tasks

`/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}/tasks/{taskId}`

### Get the status of a deletion task

Use this call to get the status of an ongoing deletion task.

**Note:** You can cancel an ongoing monitoring task if you make the same call using the `DELETE` verb instead of the `GET` one.

In the response:

- `currentStep` is the task associated with the specified `taskID`.
- `taskState` is the status of that deletion task.
- `progress` is a double that is typically 1.0.
- `result` is a JSON object that indicates the object ID, and whether the task succeeded. **Note:** For a deletion action, `failureDumpAvailable` is always false.
- `taskID` is the ID that you specified in the request.

Here is a list of each possible `taskState`:

| Status | Description |
| --- | --- |
| NOT\_STARTED | The task is scheduled to run, but has not started yet. |
| IN\_PROGRESS | The task is currently running. |
| COMPLETE | The task has finished running whether successful or not. |
| CANCELLING | The task is currently being canceled. Cancellation is not yet complete. |
| CANCELLED | The task has been canceled and the changes have been rolled back. |

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/actions/{actionId}/tasks/{taskId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `actionId` | - Required - Type: number - Description: The ID for the Delete action. - Example: `117000000019` |
| `taskId` | - Required - Type: string - Description: The ID for the Delete task. - Example: `0690AA1C761F48549C3442A02F91D962` |

#### Response 200 (application/json)

```js
{
   "task":{
      "type":"taskInformation",
      "taskId":"0690AA1C761F48549C3442A02F91D962",
      "currentStep":"Complete.",
      "progress":1,
      "result":{
         "failureDumpAvailable":false,
         "objectId":"117000000019",
         "successful":true
      },
      "taskState":"COMPLETE"
   }
}
```

---

## Process Actions

---

View the following endpoints for further details on process actions APIs:

- [List the process definitions available in a model as a JSON array](https://anaplan.docs.apiary.io/ListProcessDefinitions)
- [Retrieve metadata for a process](#RetrieveMetadataProcess)
- [Start the process](#StartTheProcess)
- [Monitor the process tasks](#MonitorTheProcessTasks)
- [Check dump file for failures](#CheckDumpFileForFailures)

---

A Process is a single container that enables several actions to run in a particular order. Processes can be configured on the Anaplan user interface by an Administrator user. A process can contain any combination of import, export, and deletion actions. To run an API-driven process:

1. [List the process definitions available to your model](#list-available-processes).
2. [Run a process](#Run-a-process).
3. [Get a list of tasks in a the process definition](#list-tasks-in-process) and [monitor each process task](#Monitor-process-task).
4. [Check for failures in each process task when the process is complete](#Check-for-process-failures).

## List the process definitions available in a model as a JSON array

`/workspaces/{workspaceId}/models/{modelId}/processes`

This lists the processes available for the given modelID. This returns a JSON array containing the list of processes that you can run for that model:

- `id` is the Id of the process that you can run on the specified model.
- `name` is the name of the process that you can run.

### Get a list of processes

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

#### Response 200 (application/json)

```js
[
   {
      "id":"118000000001",
      "name":"Process1"
   },
   {
      "id":"118000000002",
      "name":"Process2"
   }
]
```

---

## Retrieve metadata for a process

`/models/{modelId}/processes/{processId}`

Use this call to retrieve the names and actions for a given Process in an Anaplan model.

**Notes**:

- Actions which are imports or exports (`actionType` field is `IMPORT` or `EXPORT`) contain additional fields in the response (see below). Other actions just contain the `id`, `name`, and `actionType`.
- Actions are ordered in the sequence that they run when the Process itself is executed.
- For an action with `actionType` of `IMPORT`, you can use the `importDataSourceId` value as the ID of a file for the `fileId` parameter when you [upload or download files](https://anaplanbulkapi20.docs.apiary.io/#reference/upload-files)
- For actions with `actionType` of `EXPORT` or `IMPORT`, you can find more information about them if you use the IDs as `exportId` or `importId` in the [export](https://anaplanbulkapi20.docs.apiary.io/#reference/export) and [import](https://anaplanbulkapi20.docs.apiary.io/#reference/import) metadata endpoints.
- The possible values for actionType (non-exhaustive list):
	- IMPORT
		- EXPORT
		- DELETE\_BY\_SELECTION
		- ORDER\_HIERARCHY
		- OPTIMIZER
- To include additional information regarding the import data source in an import action, add the `?showImportDataSource=true` query parameter to the request.

### Request

```js
curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/processes/{processId}' \
-H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\
-H 'Accept: application/json'
```

### Request headers

| Header | Details |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | - Required - Description: the Anaplan authentication token |
| `Accept: application/json` | - Optional - Description: This indicates the preferred response is either `application/json` format. Note that this call only outputs in `application/json` format. |

### Request parameters

| Parameter | Details |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{processId}` | - Required - Type: Number - Description: the ID for the process - Example: `118000000001` - Note that you can get the process ID from the list of process for a model API |
| `{showImportDataSource}` | - Optional - Type: Boolean - Description: defines whether the response should include additional information regarding the import data source. The field is interpreted as `false` if anything other than `true` is specified. - Example: `?showImportDataSource=true` |

### Response headers

`Content-Type: application/json`

### Response 200 Body

```js
{
  "meta": {
    "schema": "https://api.anaplan.com/2/0/objects/process"
  },
  "status": {
    "code": 200,
    "message": "Success"
  },
  "processMetadata": {
    "name": "ProcessWithActions",
    "actions": [
      {
        "id": "112000000000",
        "name": "Sales from import-sales.csv",
        "actionType": "IMPORT",
        "importDataSourceId": "113000000000",
        "importType": "MODULE_DATA",
        "importDataSource": {
          "importDataSourceId": "113000000000",
          "type": "FILE"
        }
      },
      {
        "id": "116000000000",
        "name": "Sales - Revenue.xls",
        "actionType": "EXPORT",
        "exportType": "GRID_CURRENT_PAGE",
        "exportFormat": "application/vnd.ms-excel",
        "layout": "GRID_CURRENT_PAGE"
      },
      {
        "id": "117000000000",
        "name": "Delete from Products",
        "actionType": "DELETE_BY_SELECTION"
      }
    ]
  }
}
```

---

## Start the process

`/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks`

You can POST a process task to run a process. This returns a new `taskID`. Once you have started the process, you can use GET to receive a list of tasks as a JSON array. You can use this to monitor the status of each task.

**Note:** You can cancel an ongoing monitoring task if you make the same call using the `DELETE` verb instead of the `GET` one.

### Run the process

#### Request

Ensure your request contains the body `{"localeName": "en_US"}`. If this is not included the action will not start, and the system will return a `400 Bad Request` response.

```js
curl -X POST \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json' \
-d '{"localeName": "en_US"}'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Body

{"localeName": "en\_US"}

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |

#### Response 200 (application/json)

```js
{
  "taskId" : "E1F648F527AF4297B09E06C278B99F4C"
}
```

---

### Get the list of tasks for the process

This lists the tasks in the process for the given processID. This returns a JSON array containing the list of tasks in the process definition.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- 'Authorization:AnaplanAuthToken {anaplan\_auth\_token}'
- 'Content-Type:application/json'

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |

#### Response 200 (application/json)

```js
{
   "taskId":"BAB7819744034F25BF73EA1B41804478",
   "taskState":"IN_PROGRESS",
   "creationTime":1535145539157
}
```

---

## Monitor the process tasks

`/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId}`

### Get the status of a process task

Use this endpoint to get the status of a specific export task.

You can use optional query parameter `includeProcessDetails` to get the start time and duration of each step.

**Note:** As a best practice, we recommend you check the status of an ongoing process no more than once every 5 seconds. For long running processes it is suggested to check at even longer intervals.

In the response:

- `currentStep` is the task associated with the specified `taskId`.
- `taskState` is the status of the process task.
- `progress` is a double that is typically 1.0.
- `result` is a JSON object that indicates whether a failure dump file was created, the `objectId`, and whether the task succeeded.
- `failureDumpAvailable` indicates whether this process container or an action within it has a failure dump file. **Note:** For a deletion action, `failureDumpAvailable` is always false.
- `nestedResults` indicates whether the actions carried out in the process were successful. This contains details in the form of a JSON array, which also contains some debug information when failures occur. [Get the failure dump file](#Check-for-process-failures) to view the complete debug information.
- `objectID` is the identifier of the process task or a task that it includes. For instance, if `nestedResults` has `failureDumpAvailable` true, you need the `objectID` within that section to obtain the related 'dump' file.
- `taskID` is the ID that you specified in the request.
- `duration` is the overall processing time.
- `startTime` is the time when the step started.

Here is a list of each possible `taskState`:

| Status | Description |
| --- | --- |
| NOT\_STARTED | The task is scheduled to run, but has not started yet. |
| IN\_PROGRESS | The task is currently running. |
| COMPLETE | The task has finished running whether successful or not. |
| CANCELLING | The task is currently being canceled. Cancellation is not yet complete. |
| CANCELLED | The task has been canceled and the changes have been rolled back. |

#### Request

```js
curl -X GET /
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId} \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

`Authorization:AnaplanAuthToken {anaplan_auth_token}` `Content-Type:application/json`

#### Parameters

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| `workspaceId` | Yes | string | The workspace ID. Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | Yes | string | The model ID. Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | Yes | number | The process ID. Example: `118000000002` |
| `taskId` | Yes | string | The task ID. Example: `5B882A63354A4B45A21C16F3644C9C1B` |

#### Query Parameters

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| `includeProcessDetails` | Optional | boolean | If set to `TRUE` the request returns two additional values: `duration` and `startTime`. |

#### Response 200 (application/json)

```json
{
   "meta":{
      "schema":"https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "type":"taskInformation",
      "taskId":"2846F8E2FD624F7FA91EC6E2F6E318C0",
      "currentStep":"Complete.",
      "progress":1,
      "result":{
         "failureDumpAvailable":false,
         "nestedResults":[
            {
               "failureDumpAvailable":false,
               "objectId":"117000000015",
               "successful":true
            }
         ],
         "objectId":"118000000002",
         "successful":true
      },
      "taskState":"COMPLETE"
   }
}
```

---

#### Response 200 (application/json) with includeProcessDetails

```json
{
   "meta":{
      "schema":"https://api.anaplan.com//2/0/models/75A40874E6B64FA3AE0743278996850F/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "type":"taskInformation",
      "taskId":"2846F8E2FD624F7FA91EC6E2F6E318C0",
      "currentStep":"Complete.",
      "progress":1,
      "result":{
         "failureDumpAvailable":false,
         "nestedResults":[
            {
               "failureDumpAvailable":false,
               "objectId":"117000000015",
               "successful":true,
               "duration": "1112",
               "startTime": "1677624625790"
            }
         ],
         "objectId":"118000000002",
         "successful":true,
         "duration": "868",
         "startTime": "1677624626034"
      },
      "taskState":"COMPLETE"
   }
}
```

---

## Check dump file for failures

`/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId}/dumps/{objectId}`

If failures occur during import actions in a process, dump files are created for each failed import action. This contains details of the failures that occurred. Use this information to fix the problems and then try the process again.

**To prevent timeouts on large files, download the dump file in chunks.**  
It is possible to download dump files without chunking, but it is strongly recommended that chunking is used instead.  
**1.** Query the number of chunks in a dump file.  
**2.** Download the chunks sequentially.  
**3.** Concatenate the chunks on your host.

**Note:** The `taskID` is the last task of the user who carried out the specified task.

### Query the number of chunks in a dump file

Begin by querying the number of chunks using the `/chunks` endpoint. It is possible for a dump file to be very large. To help manage the size of a dump file and prevent timeouts, download the dump file in chunks. Chunks are 10mb or less and numbered sequentially from 0. In order to get the dump file for a particular action in the process, use the ObjectID. The ObjectID can be obtained from the `/tasks/{taskId}` endpoint.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId}/dumps/{objectId}/chunks \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |
| `taskId` | - Required - Type: string - Description: The task ID - Example: `5B882A63354A4B45A21C16F3644C9C1B` |
| `objectId` | - Required - Type: number - Description: The ID of the specified dump object - Example: `117000000015` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":1,
         "offset":0,
         "totalSize":3
      },
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/chunk"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "chunks":[
      {
         "id":"0",
         "name":"Chunk 0"
      },
      {
         "id":"1",
         "name":"Chunk 1"
      },
      {
         "id":"2",
         "name":"Chunk 2"
      },
      {
         "id":"3",
         "name":"Chunk 3"
      }
   ]
}
```

### Download the chunks

Download the chunks sequentially and then concatenate them on your host. The request below downloads chunk 0.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId}/dumps/{objectId}/chunks/0 \
-H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |
| `taskId` | - Required - Type: string - Description: The task ID - Example: `5B882A63354A4B45A21C16F3644C9C1B` |
| `objectId` | - Required - Type: number - Description: The ID of the specified dump object - Example: `117000000015` |

#### Response 200 (application/json)

```js
"_Status_","Column 1","Parent","Code","Start Date","Leave Date","Column 6","Column 7","Start Datesss","Column 9","Column 10","Column 11","_Line_","_Error_1_"
"W","Max Warren",",,","","4/16/12","","","","4/16/12","","","","151","Invalid parent"
"W","Carolyn Tabor","Supply Chain","",",,,","6/30/09","","","6/30/06","","","","153","Invalid date: ,,,"
"E","","Parent","Code","Start Date","Leave Date","","","Start Datesss","","","","11522","Invalid name: Code"
"E","","Parent","Code","Start Date","Leave Date","","","Start Datesss","","","","23043","Invalid name: Code"
```

---

### Get the dump file for a process task (no chunking)

**Note:** To prevent issues that may arise when downloading large dump files, we recommend that dump files are downloaded in chunks. Please see above sections for steps.

#### Request

```js
curl -X GET \
https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks/{taskId}/dumps/{objectId} \
-H authorization:'AnaplanAuthToken {anaplan_auth_token}' \
-H 'Content-Type:application/json'
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |
| `taskId` | - Required - Type: string - Description: The task ID - Example: `5B882A63354A4B45A21C16F3644C9C1B` |
| `objectId` | - Required - Type: number - Description: The ID of the specified dump object - Example: `117000000015` |

#### Response 200 (application/json)

```js
"_Status_","Product Type - L01","Parent","Code","Display Name","Hierarchy Type","_Line_","_Error_1_"
"E","All Combined Products","","","","","12","Error parsing key for this row; no values"
```

---

## Examples

---

This section contains examples of calls to the Anaplan API with various attributes.

## Displaying Pages of Results

`/workspaces/{workspaceId}/models/{modelId}/files?sort=name&limit=2&offset=1`

This example returns a list of files for the given model and workspace ID with:

- the `sort` parameter set to name, which sorts the results by their name
- a `limit` of two results per page
- a result `offset` of 1.

| Metadata | Description |
| --- | --- |
| `currentPageSize` | Number of results displayed as specified in the `limit`. |
| `next` | URL to the next page of results. |
| `offset` | Number to add to the first result to reach the results that you want. |
| `previous` | URL to the previous page of results. |
| `totalSize` | Number of results available. |

### Request

```js
curl -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' -H 'Content-Type:application/json' https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files
```

### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |

### Response 200 (application/json)

```js
{
   "meta":{
      "paging":{
         "currentPageSize":2,
         "next":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/files?limit=2&offset=3&sort=name",
         "offset":1,
         "previous":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/files?limit=2&offset=0&sort=name",
         "totalSize":11
      },
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/file"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "files":[
      {
         "id":"113000000000",
         "name":"#T & #R.csv",
         "chunkCount":0,
         "delimiter":"\"",
         "encoding":"ISO-8859-1",
         "firstDataRow":2,
         "format":"txt",
         "headerRow":1,
         "separator":","
      },
      {
         "id":"113000000009",
         "name":"ATests.txt",
         "chunkCount":1,
         "delimiter":"\"",
         "encoding":"ISO-8859-1",
         "firstDataRow":4,
         "format":"txt",
         "headerRow":3,
         "separator":"\t"
      }
   ]
}
```

---

## Run Import Process with Mapping Data

`/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks`

This example uses a process to carry out an import, which takes a mapping parameter to import data into the Actual Version dimension.

### Run the import

#### Request

```js
curl -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' -H 'Content-Type:application/json' https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{processId}/tasks/
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Body

{"localeName": "en\_GB","mappingParameters":\[{"entityType":"Version", "entityName":"Actual"}\]}

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `processId` | - Required - Type: number - Description: The process ID - Example: `118000000002` |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "taskId":"895F524FDAC64764AB4E7EA02F952446"
   }
}
```

---

## Import with Mapping Data

`/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks`

This example imports some data into a model and uses a mapping parameter to import data into the Actual Version dimension. Note that the mapping parameter is preceded by the locale.

### Run the import

#### Request

```js
curl -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' -H 'Content-Type:application/json' https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/imports/{importId}/tasks/
```

#### Headers

- `Authorization:AnaplanAuthToken {anaplan_auth_token}`
- `Content-Type:application/json`

#### Body

{"localeName": "en\_GB","mappingParameters":\[{"entityType":"Version", "entityName":"Actual"}\]}

#### Parameters

| Parameter | Description |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `importId` |  |

#### Response 200 (application/json)

```js
{
   "meta":{
      "schema":"https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/task"
   },
   "status":{
      "code":200,
      "message":"Success"
   },
   "task":{
      "taskId":"310296FE3D914C84AC813E7758A085DB"
   }
}
```