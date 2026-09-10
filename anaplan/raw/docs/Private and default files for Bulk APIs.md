---
title: "Private and default files for Bulk APIs"
source: "https://help.anaplan.com/private-and-default-files-for-bulk-apis-de9ceea2-4ce3-41c1-a894-8e2d02c36eb2"
author:
published:
created: 2026-09-09
description: "Private files are created when you use the Anaplan API to upload a file or to run the file export action."
tags:
  - "clippings"
---
Private files are created when you use the Anaplan API to upload a file or to run the file export action.

Private files have these characteristics:

- A private import file can only be accessed by the user who originally uploaded the source file to the model.
- A private export file can only be accessed by the user who originally ran the export.

Private files are stored in models and removed if not accessed at least once in 48 hours. If your private file no longer exists for a file Import Data Source or file Export Action, the default file is used instead.

Default files are used when a private file does not exist for a file import data source or export action. Default files can be set for **Admins only** or **Everyone**.

**Note:** Default files can only be set and modified using the Anaplan user interface.

Your workspace role determines whether you can access a default file that is set to be available to **Admins only**. If you do not have access, a `404 not found` error occurs.

Consider the following behavior for default files:

- If a default file is set for **Admins only**, only workspace administrators can download the default file. A '404 not found' error occurs for other API users (end users).
- If a default file is set for **Everyone**, all users (including end users) in your Anaplan environment (tenant) can download the default file.
- If a private file was created during an import or export action that you carried out, you receive that file instead of the default one.

See [Private and shared imports](https://help.anaplan.com/e692a347-854a-486a-9a05-c3b8e5ce9161) and [Private and shared exports](https://help.anaplan.com/acfd6082-a510-4be2-bc25-a9a9f396e163) for more information.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fprivate-and-default-files-for-bulk-apis-de9ceea2-4ce3-41c1-a894-8e2d02c36eb2&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>