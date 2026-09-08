---
name: project-setup
description: >
  Bootstrap a freshly cloned copy of this Anaplan LLM wiki template into a working
  vault, AND onboard additional customers into an already-set-up vault — the same
  idempotent operation, auto-detected by current state. Trigger whenever the user
  says "run first-time setup", "set up this vault", "bootstrap this repo", "initial
  setup", "onboard this repo", "add a customer", "add a new client", "I'm starting
  work for <name>" — or whenever you notice `customers/registry.md` doesn't exist
  yet, which signals an unbootstrapped clone. Handles: creating the vault's empty
  domain skeleton (`anaplan/`, `customers/`, `other-topics/`), creating/extending
  `customers/registry.md` with customer + model + engine rows, and reporting which
  of the eight project skills (all ship with the repo) are present under
  `.agents/skills/`. Always check current state first so re-running is a safe no-op.
---

# Project Setup — Bootstrap and Customer Onboarding

This skill turns a freshly cloned copy of this repo into a working vault, and
later extends that same vault with additional customers — both are the same
idempotent flow, differing only in how much of the skeleton already exists. It
replaces the old `first-setup` skill, which handled only the first case.

---

## Phase 0 — Detect current state

Before changing anything, check:

1. Does `anaplan/` exist with its standard subfolders (`raw/docs`, `raw/assets`,
   `wiki/concepts`, `wiki/functions`, `wiki/patterns`, `wiki/sources`)?
2. Does `customers/registry.md` exist?
3. Which customer folders already exist under `customers/`?
4. Does `other-topics/` exist?
5. Which skill folders exist under `.agents/skills/`?

**If (1) and (2) are both true**, this vault has already been bootstrapped — you
are in **onboard-a-customer** mode (Phase 2 only; skip Phase 1).

**If (1) or (2) is false**, this is a fresh clone — you are in **first-run**
mode (Phase 1, then Phase 2 for the first customer(s)).

---

## Phase 1 — Build the shared skeleton (first-run only)

Create whichever of the following don't already exist. Empty is fine — Codex
populates them over time as content is ingested:

- `anaplan/raw/docs/`, `anaplan/raw/assets/`
- `anaplan/wiki/concepts/`, `anaplan/wiki/functions/`, `anaplan/wiki/patterns/`, `anaplan/wiki/sources/`
- `other-topics/`
- `Clippings/`

Guardrails:
- **Never touch a directory that already exists** — creating it again is a
  no-op, but don't delete or clear anything inside it.
- **Don't create `customers/registry.md` here** — Phase 2 owns it.
- **Don't create `anaplan/index.md` or `anaplan/log.md`** — these are generated
  organically on first ingest, not pre-seeded, per `AGENTS.md`.

If `anaplan/` ships already populated (it does, in this template — it's
git-tracked and carries the accumulated generic Anaplan knowledge base), this
phase is normally a no-op on a fresh clone; just confirm nothing is missing.

---

## Phase 2 — Onboard customer(s)

Ask: **"How many customers do you want to set up this vault for — just one
(or working internally for a single organization), or several?"**

**If one customer:**
1. Ask for that customer's name (this becomes the `customers/<Name>/` folder
   name and the registry key — use it verbatim, matching however the user
   writes it).
2. Create the skeleton: `customers/<Name>/raw/{models,docs,assets}/`,
   `customers/<Name>/wiki/{models,sources}/`, `customers/<Name>/logs/`,
   `customers/<Name>/analyses/`. Note `logs/` is a peer of `raw/`, not
   nested inside it.
3. Ask whether they already know their first model(s) and engine(s)
   (Classic/Polaris). If yes, add a row per model to `customers/registry.md`
   (create the file with its header + table if it doesn't exist yet). If not,
   still create the customer skeleton and leave the registry without model
   rows for now — `wiki-data-ingestion` adds them on first CSV ingest.
4. Create `customers/<Name>/index.md` following the pattern in `AGENTS.md`'s
   Layers section (a domain index listing Models/Sources/Analyses/Raw
   sections, empty placeholders where nothing's ingested yet) and an empty
   `customers/<Name>/log.md`.

**If several customers:** repeat the 4 steps above once per customer, in a
loop, asking for each name before moving to the next.

**If the vault was already bootstrapped (onboard-a-customer mode):** skip the
"how many" question — the user is clearly asking to add exactly one more.
Just run steps 1–4 above for the new customer, then also touch the root
`index.md` router: add one line under its `## Customers` heading pointing
at the new customer's index — never add it anywhere else in that file, and
never link past the customer's own index straight to one of its models.
This keeps the cascade (root → customer index → model sub-index → page)
intact as customers are added — per `AGENTS.md`'s Cascade principle.

Guardrail: **never overwrite an existing `customers/<Name>/` tree.** If the
name the user gives already has a folder, tell them and ask whether they mean
to add more models to that existing customer (→ that's just `wiki-data-ingestion`,
not this skill) or whether they mean a different, similarly-named customer.

---

## Phase 3 — Verify skills

Report which of `anaplan-formula-agent`, `anaplan-module-mapping`,
`anaplan-model-optimizer`, `anaplan-model-documentation`,
`circular-reference-prevention`, `wiki-lint`, `wiki-data-ingestion`, and
`project-setup` (this skill) are present under `.agents/skills/` — they all
ship with the repo, so normally all 8 are.

---

## Phase 4 — Summary

End with a structured summary, always:

```
## Project setup complete

**Mode:** [first-run | onboard-customer]
**Shared skeleton:** [N directories created: <list> | already complete]
**Customers set up this run:** [<Name> (folder + skeleton created, N model rows added to registry) | ...]
**Registry:** customers/registry.md [created | extended with N new row(s)]
**Skills present:** anaplan-formula-agent [✓/✗], anaplan-module-mapping [✓/✗], anaplan-model-optimizer [✓/✗], anaplan-model-documentation [✓/✗], circular-reference-prevention [✓/✗], wiki-lint [✓/✗], wiki-data-ingestion [✓/✗], project-setup [✓/✗]

**Follow-ups for the user:**
- [e.g. "add model/engine rows for <Customer> once the first CSV export lands"]
```

If nothing is outstanding, say so explicitly: "Vault is fully set up — ready
for your first ingest."
