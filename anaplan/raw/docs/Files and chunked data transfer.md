---
title: "Files and chunked data transfer"
source: "https://help.anaplan.com/files-and-chunked-data-transfer-58f1e789-8d8c-468c-9925-21ae9aebf9e1"
author:
published:
created: 2026-09-09
description: "You can upload files to Anaplan, split large upload files into chunks, download export files in chunks, and delete private file content that you uploaded through the API."
tags:
  - "clippings"
---
You can upload files to Anaplan, split large upload files into chunks, download export files in chunks, and delete private file content that you uploaded through the API.

Chunking is useful for large files because it helps make uploads and downloads more resilient.

Use chunking when:

- You want to resume a transfer if the connection is lost during an upload.
- You are extracting data from a database and want to push it to the server without holding all the results in memory.
- You need to upload a file larger than 1 MB.
- You need to download an exported file in multiple parts.

The file list endpoint returns import and export files for a model. You can identify files by their metadata and `id`.

File metadata can include:

| **Property** | **Description** |
| --- | --- |
| `id` | The file ID. |
| `name` | The file name. |
| `chunkCount` | The number of chunks in the file. |
| `delimiter` | The delimiter character used in the file. |
| `encoding` | The file encoding. |
| `firstDataRow` | The first row after the row that contains column names. |
| `format` | The file format. |
| `headerRow` | The row that contains column names. |
| `separator` | The file separator. |

Export files have fewer metadata properties than import files.

Chunked file transfer is often part of a larger integration workflow.

For imports:

1. Upload the file or file chunks.
2. Mark the upload complete.
3. Start the import task.
4. Poll the import task until it completes.
5. Check or download dump files if the import has failures.

For exports:

1. Start the export task.
2. Poll the export task until it completes.
3. Get the export file.
4. Get the chunks in the file.
5. Download each chunk.

You can see an example of a chunked file upload process, [here](https://help.anaplan.com/64df7566-f12f-45f0-a2f9-a992688ebc47).

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Ffiles-and-chunked-data-transfer-58f1e789-8d8c-468c-9925-21ae9aebf9e1&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>