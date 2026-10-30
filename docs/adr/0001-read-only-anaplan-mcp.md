# 0001 — The Anaplan MCP is read-only and stores no model data

- Status: accepted
- Date: 2026-10-23

## Context

We're designing an MCP server so the agent can call Anaplan on the spot while helping build models. The Integration API also exposes writes (cell writes, list item add/update/delete), state changes (set current period, switchover, close, wake) and destructive calls (bulk delete models). The same server reaches production workspaces. `tools/anaplan_session.py` is already read-only by construction for the same reason.

The data use case is verification: the agent proposes a formula and checks it against a few real cells. It never needs to persist a dataset.

## Decision

1. v1 exposes read endpoints only, plus POST/DELETE calls that don't change the model: model status, dimension item lookup, and the large-volume read request lifecycle (start, poll, page, delete the request).
2. No fetched model value is written to disk, memory files or the vault. Values live in the server process's RAM for the session (see *Session cache* in CONTEXT.md) and reach the agent only as a filtered sample.
3. The one permitted local write is `register_model`, which adds a model to `tools/models.py` and `customers/registry.md` together. That's vault configuration, not model data.

## Consequences

- The dependency map (`docs/mcp/anaplan-api-map.html`) still draws the write endpoints, dashed, so the excluded surface stays visible.
- Adding any write tool later means a new ADR and a separate, opt-in tool group, never a widened allowlist.
- Unlike `fetch_model_data.py`, verification reads produce no full-CSV file.
