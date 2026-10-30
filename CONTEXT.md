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

### Agent tool server (Anaplan MCP)

**Intent tool**:
An MCP tool that takes model, module, view, list and item *names*, resolves them to IDs itself, and returns one answer, walking one path through the API dependency map. The agent never builds a URL or handles a raw ID.
_Avoid_: endpoint wrapper, API tool

**Verification read**:
A read of live cell or list values whose only purpose is to check a hypothesis, such as a proposed formula. It returns a sample with full coordinates and is never stored: values live in the server's RAM for the session and nowhere else.
_Avoid_: export, data pull, extract

**Bulk fallback**:
What a verification read switches to when the transactional read would exceed its cell cap: a large-volume read request whose pages are streamed, filtered as they arrive, stopped early once the sample is full, and always deleted afterwards. The agent doesn't choose it; the tool does.
_Avoid_: bulk export, large export

**Session cache**:
The server's in-RAM copy of a view already read in full during this session, kept only while the view fits under a size ceiling and is younger than the freshness limit. It is never written to disk and disappears when the server stops.
_Avoid_: data cache, local copy

**Grid position**:
A 1-based row or column number in a view's grid as Anaplan shows it, counted after page selection. A positional request always echoes each cell's coordinates so the caller can confirm the position meant what they thought.
_Avoid_: row index, line number
