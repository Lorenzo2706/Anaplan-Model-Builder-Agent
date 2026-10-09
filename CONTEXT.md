# Anaplan model-data tooling

The scripts under `tools/` that read a live Anaplan model's structure and data into the vault for one customer at a time. This glossary covers how those scripts reach Anaplan; customer-specific terms stay in each customer's gitignored tree.

## Language

### Reaching Anaplan

**Integration API session**:
Authenticated, browser-free access to Anaplan's documented Integration API on the global API host. It carries the REST-derived export files and live cell/list reads.
_Avoid_: REST session, API cookie session

**Browser login**:
A logged-in Anaplan web session driven through a real browser. It's needed for the model-settings UI exports, the classic-engine grids, and model listing. It is always separate from the Integration API session, and neither is ever converted into the other.
_Avoid_: SSO session, UI auth

**Mixed run**:
An export whose files come partly from the Integration API session and partly from the browser login. It succeeds only if both halves succeed.
_Avoid_: hybrid export

### Authentication

**Auth mode**:
How a customer's Integration API session is authenticated. It's declared once per customer and inherited by every model under that customer; a model never overrides it.
_Avoid_: auth type, login method

**Default auth**:
The auth mode a customer has when it declares none: the username/password token exchange.
_Avoid_: legacy auth, Basic profile

**OAuth mode**:
An opt-in auth mode in which a stored, long-lived refresh token is exchanged for short-lived access tokens. It never falls back to default auth.
_Avoid_: token auth, Bearer auth

**Auth profile**:
The name that scopes one customer's OAuth secrets, so one customer can never pick up another customer's credentials.
_Avoid_: credential set, tenant key

**Visibility probe**:
A read-only check of which workspaces and models an authenticated identity can see, run before any model endpoint is called. It separates "can't authenticate" from "authenticated but can't see the model".
_Avoid_: smoke test, connectivity check
