---
title: "Request and response formats"
source: "https://help.anaplan.com/request-and-response-formats-5fbaa2ab-b5c7-44a4-9cbb-67aee3da0dcb"
author:
published:
created: 2026-09-09
description: "Learn which data formats the API accepts or returns, including JSON, CSV, binary streams, metadata, list data, view data, and file content."
tags:
  - "clippings"
---
Learn which data formats the API accepts or returns, including JSON, CSV, binary streams, metadata, list data, view data, and file content.

The Anaplan Integration API uses request headers, request body formats, and response formats to define how data is sent to and returned from the API.

Most API requests and responses use JSON. Some endpoints return CSV-formatted data, and file chunk endpoints use binary streams.

Each endpoint defines the request headers it supports. Use only the headers documented for the endpoint you are calling.

Common headers include:

| **Header** | **Description** |
| --- | --- |
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Required for authenticated requests. Replace `{anaplan_auth_token}` with a valid Anaplan authentication token. |
| `Content-Type: application/json` | Indicates that the request body is in JSON format. Use this for requests that send JSON data. |
| `Content-Type: application/octet-stream` | Indicates that the request body is a binary stream. Use this for file chunk upload operations. |
| `Accept: application/json` | Indicates that the preferred response format is JSON. Some endpoints require this header, while others treat it as optional. |

Use `Content-Type: application/json` when the endpoint expects a JSON request body.

For example, when you initiate a large read request, the request body can specify the export layout:

`{     "exportType": "TABULAR_MULTI_COLUMN"   }   `

Supported export layout values include:

| **Export type** | **Description** |
| --- | --- |
| `GRID_ALL_PAGES` | Exports data in a grid layout and respects existing sorting and filtering applied to the data grid. |
| `TABULAR_SINGLE_COLUMN` | Exports all dimensions in columns, with the final column reserved for data. |
| `TABULAR_MULTI_COLUMN` | Exports data with multiple data columns. |

These values define the layout of exported data. They are not HTTP media types.

Use `Content-Type: application/octet-stream` when uploading file chunks.

File chunk upload requests send the file content as a binary stream rather than as JSON.

Many API responses return `Content-Type: application/json`.

A typical JSON response can include:

| **Response element** | **Description** |
| --- | --- |
| `meta` | Metadata about the response, such as the schema used for the returned object. |
| `status` | Status information, including a response code and message. |
| Resource-specific data | The returned object or collection, such as `items`, `file`, view metadata, pages, rows, columns, or other endpoint-specific data. |

Example structure:

`{    "meta": {      "schema": "https://api.anaplan.com/2/0/objects/view"    },    "status": {      "code": 200,      "message": "Success"    },    "items": []   }`

Some view data endpoints can return data as a CSV grid response.

For cell data retrieved from a view:

- The first line of the CSV response contains the values of the page selectors.
- If there are no dimensions on pages, the response omits the page selector line.
- When there are multiple dimensions on columns, a line for each dimension follows the first line.
- When there are multiple dimensions on rows, a column displays on the left for each row dimension.
- You can export CSV data in different layouts by passing supported query parameters such as `exportType` and `moduleId`.

Some view cell data endpoints can return JSON instead of CSV.

To request a JSON-formatted response:

1. Pass an `Accept` header of `application/json`.
2. Pass a query parameter with `format` set to `v1`.

The JSON response can include:

| **Response element** | **Description** |
| --- | --- |
| `pages` | A list of selected items for each page selector. If the view has no page selectors, this list may be empty or absent. |
| `columnCoordinates` | A list of coordinates for all values in each column. Each coordinate is represented as a list of one or more values. |
| `rowCoordinates` | A list of coordinates for all values in each row. |
| `data` | The cell values returned for the selected view data. |

A successful API call does not always return a response body.

`204 No Content` means the request was successful, but there is no representation to return. The response body is empty.

This is the expected response for some task-related `POST` requests.

The following HTTP response codes are especially relevant to request and response formats:

| **Status code** | **Meaning** |
| --- | --- |
| `200 OK` | The request was successful. |
| `204 No Content` | The request was successful, but the response body is empty. |
| `400 Bad Request` | The request is incorrect, such as missing required values or specifying invalid values. |
| `405 Method Not Allowed` | The request used the wrong HTTP method for the endpoint. |
| `406 Not Acceptable` | The requested response format cannot be provided. Check the `Accept` header. |
| `415 Unsupported Media Type` | The request body is in an unsupported format. Check the `Content-Type` header. |
| `429 Too Many Requests` | Too many requests were made. Wait briefly, then retry. |

When you build integrations with the Anaplan API, do not assume that response fields are fixed.

Write client parsers so they ignore unknown or extra fields. This helps integrations remain resilient if the API adds fields to a response in the future.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Frequest-and-response-formats-5fbaa2ab-b5c7-44a4-9cbb-67aee3da0dcb&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>