---
title: Integration API — Authentication, Access & Permissions
type: concept
tags: [anaplan, integration-api, authentication, permissions, security]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Authentication, access, and permissions.md
---

# Integration API — Authentication, Access & Permissions

The Integration API uses the **permissions of the authenticated Anaplan user** — it grants no extra access. If a user cannot access a workspace, model, action, module, view, list, or file in the Anaplan UI, the same restriction applies when that user calls the API.

## How access is evaluated

Anaplan evaluates access at several levels for every call:

1. **Authentication** — the request must carry a valid Anaplan auth token in the `Authorization` header.
2. **Tenant and workspace access** — the user must have access to the target tenant, workspace, and model.
3. **Workspace Administrator authority** — some endpoints require it outright; Workspace Administrators can also run *any* model action regardless of their assigned [[../anaplan concepts/13_model-roles|model role]].
4. **Model role access** — if the user is not a Workspace Administrator, their model role must grant access to the action, module, view, or list used by the request.
5. **Object-level permissions** — e.g. a user may access a model but lack read access to a specific module, or write access to a specific target module.
6. **File access** — Bulk API files can be private (user-specific) or default; see [[09_bulk-and-large-volume-data|Bulk & large-volume data]] for the private/default file model.

| Permission level | Applies to | What it grants through the API |
|---|---|---|
| Authenticated Anaplan user | All API requests | Send requests with a valid token — still needs resource access |
| Model role | Model actions and objects | Run actions, read modules/views, update data only where the role allows |
| Workspace Administrator | Workspace/model admin + all model actions | Run any action regardless of model role; required for several admin/metadata endpoints |
| Tenant-level access role | Tenant-level user info | Retrieve user information where the endpoint allows it |
| Tenant Security Administrator | Exception user administration | Assign/unassign/list exception users, where enabled |
| Tenant Administrator / Encryption Administrator | Administration role management | Retrieve, assign, or remove supported admin roles via the Administration Roles API |

## Endpoints that require Workspace Administrator authority

| API area | Example capability | Requirement |
|---|---|---|
| Model state | Close or wake up a model | Workspace Administrator authority in the model |
| Model metadata | Retrieve some line item, module, or view metadata | Workspace Administrator authority, sometimes plus model-role read access |
| Large volume reads | Initiate or delete large read requests | Workspace Administrator authority |
| Model calendar | Retrieve/update current period and calendar settings | Workspace Administrator authority |
| Lists | Reset a list index | Workspace Administrator authority |
| Logs | Retrieve Optimizer action logs | Workspace Administrator permissions |
| Users | Retrieve user information or user lists | Workspace Administrator authority, or a tenant-level access role |

Workspace Administrator access does not bypass runtime checks — the model must still be in a processable state and the requested object must exist.

## Model-role-driven access (non-admins)

| Request type | Required access |
|---|---|
| Start an import, export, delete, or process task | Model role grants access to the action |
| Retrieve data from a view or module | Model role grants read access to the source view/module |
| Update cell data | Model role grants write access to the target module/line item |
| Run an import into a module | Model role grants permission to run the import and write to the target module |

## Administration roles (separate from model roles)

The **Administration Roles API** uses Anaplan administration roles (Tenant Administrator, Encryption Administrator, etc.) rather than model roles. Roles can be assigned with different constraint scopes:

| Role type | Constraint | Description |
|---|---|---|
| Tenant-level role | Tenant constraint | Applies within a tenant |
| Workspace-level role | Workspace constraint | Applies to one or more workspaces |
| Unconstrained role | None | Applies without a workspace/tenant constraint |

## SSO and exception users

If a workspace uses single sign-on but an integration authenticates with basic authentication, the calling user must be assigned as an **exception user** — managed separately from model roles. Being an exception user does not substitute for the correct workspace/model/action/object permissions.

## Transport security

All API traffic runs over HTTPS with 2048-bit certificates (TLS in transit). **TLS 1.3** is required for new integrations; **TLS 1.2** is still supported. **TLS 1.1 is not supported** — build integrations against TLS 1.3.

## Permission-related error responses

| Response | Usually means |
|---|---|
| `401 Unauthorized` | Auth token missing, invalid, or expired |
| `403 Forbidden` | Authenticated but not permitted to perform the action |
| `404 Not Found` | Resource doesn't exist, **or** the user lacks permission to see it |
| `moduleImportNoWriteAccess` | No permission to change the target module |
| `noAccessToModule` | Role doesn't permit access to the source module |
| `notAuthorised` | Not authorized to run the specified action |

> [!warning]
> `404 Not Found` can mean either a missing resource or a permissions problem. When troubleshooting, verify both the resource ID and the calling user's access before assuming the object doesn't exist.

## Design recommendations

- Use a dedicated integration user for API automations; grant only the permissions the integration needs.
- Grant Workspace Administrator authority only when administrative endpoints are required, or actions must run regardless of model role.
- For action-based integrations, prefer model-role permissions scoped to only the required imports/exports/deletes/processes.
- For data-read/write integrations, confirm the model role grants access to the specific modules, views, line items, and lists the request touches.
- For SSO workspaces using basic auth, confirm the integration user is an exception user.
- When troubleshooting permissions, check: token → tenant → workspace → model → model state → model role → action access → object access → file access, in that order.

## Related

- [[01_overview|Integration API — Overview]]
- [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]]
- [[../anaplan concepts/02_access-security|Access & Security — Overview]]
- [[../anaplan concepts/13_model-roles|Model Roles]]
