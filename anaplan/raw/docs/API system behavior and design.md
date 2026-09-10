---
title: "API system behavior and design"
source: "https://help.anaplan.com/api-system-behavior-and-design-c09efa46-b491-4496-8980-1ff23fd1019c"
author:
published:
created: 2026-09-09
description: "This page describes expected behaviors and design considerations when creating an API integration."
tags:
  - "clippings"
---
The Anaplan Integration API v2.0 has predefined behaviors and processes based on the nature of the requests carried out.

These largely address subjects like permissions, API, task states, chunking of payloads, payload formatting

For example:

- Large imports and exports should be chunked for efficiency and resilience, given the amount of data that is transferred.
- Long-running tasks need to be polled to move on to the next step of the integration.
- Failed imports or exports can be analyzed through a dump file.
- Querying the API server for data may require pagination of results.

Files are model-level objects used by import and export workflows. Upload files can be split into chunks and loaded sequentially. Export files may also be downloaded in chunks.

Chunking helps avoid timeout and payload-size issues for large files.

Actions that take time to complete return a `taskId`. You use the `taskId` to poll the task endpoint.

A task response can include:

- Current task state.
- Current step.
- Progress.
- Result information.
- Failure counts.
- Whether a dump file is available.

Read endpoints return metadata, list data, view data, or file content. Some read requests return JSON. Others return CSV or file streams.

For view data, read the metadata first when you need to map the grid output to dimensions, rows, columns, line items, and page selectors.

Dump files contain details about records or steps that failed during an import or process. Dump files are not the same as export output files.

- Import dumps are associated with import tasks.
- Process dumps are associated with process tasks.
- Export output is downloaded from file chunk endpoints.

Some actions can make a model busy or lock parts of model execution while Anaplan prepares data, runs calculations, loads data, or creates files. Avoid launching conflicting tasks against the same model in parallel unless the workflow has been tested for concurrency.

When the model is busy, retry according to the retry guidance in this guide.

Anaplan supports only `application/json` format for API requests and responses, but a file chunk is returned as a stream of binary data in the `application/octet-stream` format.

If your API calls return a lot of data, you can specify that results are returned in pages. You can specify:

- A `limit` for the number of results to return per page.
- An `offset` to get a specific page of results starting from a particular result.
- An attribute on which to `sort` the results.

**Note:** Paging specifies the number of results returned by an API request in pages. This is not the number of pages in a file.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fapi-system-behavior-and-design-c09efa46-b491-4496-8980-1ff23fd1019c&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>