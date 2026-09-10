---
title: "Resource structure and parameters"
source: "https://help.anaplan.com/resource-structure-and-parameters-f7d6ca4a-43fc-49b1-b348-a9bd0d2e1675"
author:
published:
created: 2026-09-09
description: "Understand how endpoint paths are constructed, how IDs are obtained, and how path/query parameters affect calls."
tags:
  - "clippings"
---
Understand how endpoint paths are constructed, how IDs are obtained, and how path/query parameters affect calls.

Many endpoint paths contain a chain of parameters that you can build step-by-step. For example, to get the status of an import task, you might use something like this: `/workspaces/{workspaceID}/models/{modelID}/imports/{importID}/tasks/{taskId}`

For example, you need to make this sequence of calls to get the IDs required to get the status of an import task:

1. Log into Anaplan and click the `?` for help. Select **About** from the drop-down list.
2. From the **About** window, copy the `Workspace Id` and `Model Id` values.
3. Manually enter the `workspaceID` to use.
4. Manually enter the `modelID` to use.
5. `GET` the list of `imports` in the model.
6. Choose an `importID` from the list of imports.
7. `POST` the tasks for the import. This returns a `taskID`.
8. `GET` the status of the `taskID` for the import.

**Note:** If you already know some of the required IDs, you can skip those calls and only make calls for the IDs that you do not already know.

These parameter types form the basis of calls you make with the Anaplan Integration API. Path parameters must follow their equivalent parameter without an ID. Typically, you can retrieve the strings or numbers used as parameters through other calls.

The parameters you can use to return information, such as about a workspace or model, apply to the [authenticated](https://anaplanbulkapi20.docs.apiary.io/#/introduction/getting-started/authentication) user's default tenant.

**Note:** All path parameters with a type of string are case sensitive. This means workspace Ids must be input in lowercase, for example `8a8b8c8d8e8f8g8i`, and model Ids must be input in uppercase, for example `75A40874E6B64FA3AE0743278996850F`, otherwise the object will not be recognized.

| **Parameter** | **Path parameter** | **Type** | **Description** |
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

Certain endpoints have query parameters that change the response. The detailed effects of these query parameters are explained in the documentation for each endpoint. The capitalization of each query parameter must match the table below.

| **Query parameter** | **Possible values** | **Description** |
| --- | --- | --- |
| `tenantDetails` | `true`, `false` | A Boolean query parameter. If true, the call response includes the estimated size of a workspace in bytes. |
| `includeAll` | `true`, `false` | A Boolean query parameter. If true, the call response includes additional information about the applicable line item or list. |
| `action` | `add`, `delete` | You can use this to add or delete list items in a call. |
| `showImportDataSource` | `true`, `false` | A Boolean query parameter. If true, the call response includes the ID and format of the import data source. |
| `includesubsidiaryviews` | `true`, `false` | A Boolean query parameter. If true, the call response includes subsidiary views. |
| `format` | `v1` | You can use this to return a JSON response instead of a CSV response when you retrieve cell data for a view. |
| `modelDetails` | `true`, `false` | A Boolean query parameter. If true, the call response includes additional information about a model such as memory usage, creation date, and recent changes. |
| `pages` | `{dimensionId}`, `{itemId}` | You can use this to specify which pages, or list items used as dimensions, to return cell data for. |

You can pass parameters to a process or an import when you `POST` it.

**Note:** You must include a locale when specifying parameters.

For example, you can specify:

- Mapping parameters. For instance, you can specify the Anaplan Version dimension to which data is to be imported. See [Run import process with mapping data](https://help.anaplan.com/e03719fc-c2bc-487d-81a6-d743e0fc3b6c) and [Import with mapping data](https://help.anaplan.com/a819aec7-729d-43a5-bd49-3e4c598fb358)
- The locale for which the information is intended. For instance, you might want the decimal separator to be shown as a comma for certain locales.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fresource-structure-and-parameters-f7d6ca4a-43fc-49b1-b348-a9bd0d2e1675&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>