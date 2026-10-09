# Handoff: Configure OAuth 2.0 on Anaplan Request Tab

## Task
Configure OAuth 2.0 Authorization Code flow on the active Postman request tab, then attempt to send the request.

## Context
- **Active tab ID**: `8e398c37-5d24-46ad-9cad-66c3beb87f55`
- **Request**: `GET https://api.anaplan.com/2/0/workspaces/d53a5d8ad8a7422f9662778676709e1d/models`
- **Current status**: 401 Not Authenticated — no Bearer token is attached
- **Active environment**: KWS (Postman UID: `c5d94694-4ceb-4a61-8b1a-6c69bdc12ead`)
- The environment already has `ANAPLAN_KWS_OAUTH_CLIENT_ID` and `ANAPLAN_KWS_OAUTH_CLIENT_SECRET` set with real values.

## What to do

### Step 1 — Set OAuth 2.0 auth on the active tab

Use `editHTTPRequest` on tab `8e398c37-5d24-46ad-9cad-66c3beb87f55` with the following auth config:

```json
{
  "type": "oauth2",
  "oauth2": [
    { "key": "grant_type",           "value": "authorization_code" },
    { "key": "callBackUrl",          "value": "https://oauth.pstmn.io/v1/callback" },
    { "key": "authUrl",              "value": "https://eu3.app.anaplan.com/auth/authorize" },
    { "key": "accessTokenUrl",       "value": "https://eu3.app.anaplan.com/oauth/token" },
    { "key": "clientId",             "value": "{{ANAPLAN_KWS_OAUTH_CLIENT_ID}}" },
    { "key": "clientSecret",         "value": "{{ANAPLAN_KWS_OAUTH_CLIENT_SECRET}}" },
    { "key": "scope",                "value": "openid profile email offline_access" },
    { "key": "tokenName",            "value": "Anaplan KWS Token" },
    { "key": "addTokenTo",           "value": "header" },
    { "key": "headerPrefix",         "value": "Bearer" },
    { "key": "client_authentication","value": "header" }
  ]
}
```

Set `activeTabView` to `"auth"`.

### Step 2 — Send the request

After configuring auth, send the request using `sendRequest` with `tabId: "8e398c37-5d24-46ad-9cad-66c3beb87f55"`.

## Success criteria
1. OAuth 2.0 Authorization Code is configured on the tab with the above settings.
2. The request has been sent and the status code + response body are reported back.

## Expected outcome
The request will likely return **401** even after OAuth config is applied — this is expected because no access token has been fetched yet (the user must click **"Get New Access Token"** manually in the Postman UI). Report this clearly to the user.
