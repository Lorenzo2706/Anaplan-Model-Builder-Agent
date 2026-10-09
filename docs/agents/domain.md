# Domain docs

Use a single-context layout for repository engineering: root `CONTEXT.md` and `docs/adr/`. This layout supplements the existing customer/wiki navigation rules.

Before codebase exploration, read CONTEXT.md when present and ADRs relevant to the change. If absent, proceed silently; domain-modeling creates them when terminology or decisions are resolved. No placeholder domain documents are required for setup.

Use the glossary's vocabulary in tickets and implementation proposals. Surface any conflict with an existing ADR explicitly. Keep customer-specific terminology and decisions within the customer's gitignored tree; root domain docs describe generic repository concepts only.
