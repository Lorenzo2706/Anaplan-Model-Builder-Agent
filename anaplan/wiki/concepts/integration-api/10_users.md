---
title: Integration API — Users
type: concept
tags: [anaplan, integration-api, users, identity]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Model user information.md
  - raw/docs/Retrieve your user.md
  - raw/docs/Retrieve user information.md
  - raw/docs/Retrieve user list.md
---

# Integration API — Users

User endpoints identify the authenticated caller and retrieve information about other users the caller can see. They provide identity context for access validation, administration, or provisioning workflows (e.g. Salesforce.com Anaplan tab user provisioning) — they don't touch planning data.

These calls only work against the user's **default tenant**; they never return data for other tenants the user is assigned to.

| Endpoint | Method & path | Access requirement |
|---|---|---|
| Retrieve your user | `GET /users/me` | Any authenticated user |
| Retrieve user information | `GET /users/{userId}` | Workspace Administrator, or any [[02_authentication-and-permissions#administration-roles-separate-from-model-roles|tenant-level access role]] |
| Retrieve user list | `GET /users?sort=%2BemailAddress` | Workspace Administrator, or any tenant-level access role |

User object fields: `id`, `active`, `email`, `emailOptIn`, `firstName`, `lastName`, `lastLoginDate`; `/users/me` additionally returns `customerId` (the tenant ID).

```json
{
  "user": {
    "id": "8a8b844a477d5da70147d150ee080b17",
    "active": true,
    "email": "a.user@anaplan.com",
    "emailOptIn": true,
    "firstName": "A",
    "lastName": "User",
    "customerId": "8b81da6f5fb6b75701604d6c950c05b1",
    "lastLoginDate": "2017-09-07T08:05:37.000+0000"
  }
}
```

As a standard (non-admin) user, calls only surface data you already have access to — an unauthorized request returns `401 Not Authorized` rather than a filtered/partial result.

## Related

- [[01_overview|Integration API — Overview]]
- [[02_authentication-and-permissions|Authentication, Access & Permissions]] — tenant-level access roles and Workspace Administrator authority
- [[04_workspaces-and-models|Workspaces & Models]] — the workspace/model context a user's access is evaluated against
