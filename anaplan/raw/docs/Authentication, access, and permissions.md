---
title: "Authentication, access, and permissions"
source: "https://help.anaplan.com/authentication-access-and-permissions-62989779-a911-415b-a3b7-6a9241eeab39"
author:
published:
created: 2026-09-09
description: "The Anaplan Integration API uses the permissions of the authenticated Anaplan user. The API does not grant extra access."
tags:
  - "clippings"
---
The Anaplan Integration API uses the permissions of the authenticated Anaplan user. The API does not grant extra access.

If a user cannot access a workspace, model, action, module, view, list, or file in Anaplan, the same restriction applies when that user calls the API.

How permissions are evaluated

When you call the Integration API, Anaplan evaluates access at several levels:

1. **Authentication -** The request must include a valid Anaplan authentication token in the `Authorization` header.
2. **Tenant and workspace access -** The authenticated user must have access to the target tenant, workspace, and model.
3. **Workspace Administrator authority -** Some API endpoints require Workspace Administrator authority. Workspace Administrators can also run any model action through the API, regardless of their assigned model role.
4. **Model role access -** If the authenticated user is not a Workspace Administrator, their assigned model role must grant access to the action, module, view, or list used by the API request.
5. **Object-level permissions -** For endpoints that read or update model objects, the user’s role must allow the required access to the specific object. For example, a user may be able to access a model but not have read access to a specific module or write access to a specific target module.
6. **File access -** Bulk API files can be private or default files. Private files are user-specific. A user can only interact with files they are permitted to access. See [this page](https://help.anaplan.com/de9ceea2-4ce3-41c1-a894-8e2d02c36eb2) for more information.

| **Permission level** | **Applies to** | **What the user can do through the API** |
| --- | --- | --- |
| Authenticated Anaplan user | All API requests | Send API requests with a valid token. The user still needs access to the requested resource. |
| Model role | Model actions and model objects | Run actions, read modules or views, and update data only where the assigned model role allows it. |
| Workspace Administrator | Workspace and model administration, and model actions | Run any action in the model, regardless of model role. Required for some administrative and metadata endpoints. |
| Tenant-level access role | Tenant-level user information | Retrieve user information where the endpoint allows tenant-level access roles. |
| Tenant Security Administrator | Exception user administration | Assign, unassign, and list exception users for workspaces, where the Exception users API is enabled. |
| Tenant Administrator or Encryption Administrator | Administration role management | Use the Administration Roles API to retrieve, assign, or remove supported administration roles. |

Workspace Administrator role is required for several Integration API endpoints that expose or change model structure, model settings, or administrative information.

Examples include:

| **API area** | **Example capability** | **Permission requirement** |
| --- | --- | --- |
| Model state | Close or wake up a model | Workspace Administrator authority in the model. |
| Model metadata | Retrieve some line item, module, or view metadata | Workspace Administrator authority, and in some cases model-role read access to the relevant object. |
| Large volume reads | Initiate or delete large read requests | Workspace Administrator authority. |
| Model calendar | Retrieve or update current period and other calendar settings | Workspace Administrator authority. |
| Lists | Reset a list index | Workspace Administrator authority. |
| Logs | Retrieve Optimizer action logs | Workspace Administrator permissions in the model. |
| Users | Retrieve user information or user lists | Workspace Administrator authority or a tenant-level access role, depending on the endpoint. |

Workspace Administrator access does not remove all other runtime checks. For example, the model must still be in a state that can process the request, and the requested workspace, model, action, file, or object must exist.

If the authenticated user is not a Workspace Administrator, the user’s model role controls what they can do through the API.

The model role must grant access to the action or object used by the request. This applies to actions such as imports, exports, deletes, and processes, and to model objects such as modules, views, lists, and line items.

For example:

| **API request type** | **Required access for non-Workspace Administrators** |
| --- | --- |
| Start an import, export, delete, or process task | The model role must grant access to the action. |
| Retrieve data from a view or module | The model role must grant read access to the source view or module. |
| Update cell data | The model role must grant write access to the target module or line item. |
| Run an import into a module | The model role must grant permission to run the import and write to the target module. |

Workspace Administrators can run any action regardless of their assigned model role. Users who are not Workspace Administrators must have explicit action access through their model role.

Some Anaplan APIs use administration roles rather than model roles.

The Administration Roles API uses Anaplan administration roles to determine who can retrieve, assign, and remove roles. To call the Administration Roles API, the authenticated user must be an active Anaplan user with the required administration role, such as Tenant Administrator or Encryption Administrator.

Some roles are assigned globally, while others are assigned with constraints:

| **Role type** | **Constraint example** | **Description** |
| --- | --- | --- |
| Tenant-level role | Tenant constraint | Applies within a tenant. |
| Workspace-level role | Workspace constraint | Applies to one or more workspaces. |
| Unconstrained role | No constraint | Applies without a workspace or tenant constraint. |

For workspace-scoped roles, such as Workspace Administrator, the role assignment must include the relevant workspace constraint.

If a workspace uses single sign-on and the integration authenticates with basic authentication, the user must be assigned as an exception user. Exception user access allows the user to authenticate outside the enforced SSO flow for supported integration scenarios.

Exception user assignment is managed separately from model roles. A user may be an exception user and still need the correct workspace, model, action, and object permissions to complete API requests.

When a user does not have permission to perform an API request, the API can return different responses depending on the request and resource.

| **Response or error** | **What it usually means** |
| --- | --- |
| `401 Unauthorized` | The authentication token is missing, invalid, or expired. |
| `403 Forbidden` | The user is authenticated but does not have permission to perform the requested action. |
| `404 Not Found` | The resource does not exist, or the user does not have permission to see it. |
| `moduleImportNoWriteAccess` | The user does not have permission to change the target module. |
| `noAccessToModule` | The user’s role does not permit access to the source module. |
| `notAuthorised` | The user is not authorized to run the specified action. |

A `404 Not Found` response can be a permissions issue as well as a missing-resource issue. When troubleshooting, confirm both the resource ID and the authenticated user’s access.

All Anaplan API communication happens over HTTPS with 2048-bit certificates, which provides for data encryption in transit using Transport Layer Security (TLS) 1.3. TLS 1.2 is still supported.

When you build integrations with Anaplan APIs, ensure your integrations are built to use TLS 1.3. Anaplan APIs do not support TLS 1.1.

- Use a dedicated integration user for API automations. Assign only the permissions that the integration needs.
- Grant Workspace Administrator authority only when the integration requires administrative endpoints or must run actions regardless of model role.
- For action-based integrations, prefer model-role permissions that grant access only to the required imports, exports, deletes, or processes.
- For data-read or data-write integrations, confirm that the model role grants access to the specific modules, views, line items, and lists used by the API request.
- For SSO-enabled workspaces that use basic authentication, confirm that the integration user is assigned as an exception user.
- When troubleshooting permissions, check the token, tenant, workspace, model, model state, model role, action access, object access, and file access.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fauthentication-access-and-permissions-62989779-a911-415b-a3b7-6a9241eeab39&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>