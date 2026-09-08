---
name: wiki-lint
description: >
  Run a full sanity check on any markdown-based wiki and fix what's safe to fix automatically.
  Trigger this skill whenever the user asks to: lint the wiki, run a wiki health check, check for
  orphan pages, find broken links, check wiki consistency, audit the wiki, or do a wiki cleanup.
  Also trigger when the user says "sanity check" in the context of a documentation or notes system.
  Works on any wiki that has index files and markdown pages — Obsidian vaults, AGENTS.md-driven
  knowledge bases, plain markdown wikis, etc.
---

# Wiki Lint

A generic sanity-check and auto-fix pass for any markdown wiki. The goal is to keep the wiki navigable and trustworthy by catching the problems that accumulate silently over time: pages that exist but aren't indexed, links that point nowhere, stats that drifted out of date, and facts that contradict each other across pages.

## Step 0 — Orient yourself

Before running any checks, understand the wiki's structure. Look for, in order:

1. **AGENTS.md or README.md** at the vault root — this is the richest source of structural conventions (index file names, log file name, link syntax, folder layout).
2. **A master index file** (`index.md` at the root, or whatever the conventions say). Read it to understand the top-level sections and where sub-indexes live.
3. **Sub-index files** — follow every sub-index link from the master index and read those too. They define what's "officially catalogued" in each section.

You're building a mental model of: *what does this wiki claim to contain?* You'll compare this against what's actually on disk.

If the wiki has no index files and no conventions file, fall back to treating every `.md` file as a candidate page and every `[[link]]` as a reference to check.

## Step 1 — Scan the filesystem

**Multi-domain scope:** this vault has four domain trees as of 2026-08-31 — `anaplan/`, each `customers/<Name>/`, and `other-topics/`. Run the full lint procedure (orphans, broken links, stale stats, contradictions) independently against each domain's own `index.md`/`log.md`/wiki pages — do not cross-check links between domains as if they shared one namespace, except to confirm a cross-domain `[[wiki link]]` (e.g. a customer model page linking to a shared `anaplan/wiki/functions/` page) actually resolves.

List all markdown files (`.md`) under the wiki root. Exclude any paths the conventions say are non-wiki (e.g., raw source documents, immutable imports, auto-generated files). The result is the **ground truth set** of pages that exist.

```bash
find <wiki-root> -name "*.md" | sort
```

Also note any non-markdown files (`.html`, `.pdf`, scripts) that live in wiki directories — they may need to be acknowledged in the index or are orphaned artifacts.

## Step 2 — Run the five standard checks

Work through each check systematically. Collect all findings before fixing anything.

### Check A — Orphan pages

**Definition:** A `.md` file exists on disk but is not referenced in any index and has no inbound `[[wiki links]]` from other pages.

How to find them:
- Build the set of all files on disk.
- Build the set of all files that appear in an index OR are the target of a `[[link]]` anywhere in the wiki.
- The difference is orphans.

Not every unlisted file is a problem — some wikis intentionally have scratch files or appendix pages. Use judgment: if a file has meaningful content and a clear topic, it should probably be indexed. If it's a stub or empty, flag it for deletion.

### Check B — Broken internal links

**Definition:** A `[[wiki link]]` or relative markdown link points to a file that doesn't exist on disk.

Scan every wiki page for internal links and verify the target exists. Common causes: a page was renamed, a planned page was never written, a copy-paste error introduced a typo.

For each broken link, note: source page, broken target, and (if obvious) what the correct target should be.

### Check C — Stale counts and stats

**Definition:** A number stated in an index page (e.g., "22 concept pages", "3 models", "27 sources") doesn't match the actual count on disk.

Look for explicit count claims in index files and master index stats lines. Recount the actual items and compare. This includes:
- "N pages" claims
- "N sources" claims  
- Module/item counts in model or catalog pages
- Any `updated: YYYY-MM-DD` frontmatter date that's older than the page was last meaningfully edited (use your judgment here — don't flag trivially)

### Check D — Contradictions

**Definition:** The same fact is stated differently in two or more pages.

This requires domain judgment. Look for:
- A property stated in both a detail page and an index/overview page with different values (e.g., module count, engine type, item count)
- A date or version number that differs between a source page and the model page it describes
- Status flags (e.g., "deprecated", "new", "Classic vs Polaris") that contradict each other

When you find a contradiction, identify which source is authoritative (usually the most recently updated page, or the most specific one) and flag the others as stale.

### Check E — Undocumented companion files

**Definition:** Files that clearly belong to a catalogued page but aren't mentioned anywhere (e.g., `-detailed.md` variants, `.html` analysis artifacts, images, supplementary CSVs).

Scan for filename patterns like `<page>-detailed.md`, `<page>.html`, `<page>-v2.md`. If the parent page doesn't mention them, add a note so future readers know they exist.

## Step 3 — Fix what's safe to fix

Fix automatically (no user confirmation needed):
- **Register orphan pages** in the appropriate index file, with a one-line description. Don't invent content — derive the description from the page's frontmatter or first heading.
- **Correct stale counts** in index stats lines when the correct value is unambiguous.
- **Correct wrong facts** when one source is clearly authoritative (e.g., a detailed source page says Classic but the summary index says Polaris — fix the summary).
- **Update `updated:` frontmatter dates** on pages you just edited.
- **Add notes about undocumented companion files** to the relevant index.

Do NOT fix automatically (flag for user):
- Broken links where the correct target is ambiguous.
- Contradictions where it's unclear which source is authoritative.
- Orphan pages that might be intentional drafts or should be deleted.
- Any structural change (renaming files, moving pages, deleting content).

## Step 4 — Append to the log

If the wiki has a log file (usually `log.md` at the root), append a lint entry. Use the wiki's existing log format. A minimal entry looks like:

```markdown
## [YYYY-MM-DD] lint | Wiki sanity check
Issues found and fixed:
1. <summary of fix 1>
2. <summary of fix 2>
...
Issues flagged for manual review:
- <broken link in page X — target unclear>
```

If there's no log file, skip this step (don't create one — the wiki may not use one).

## Step 5 — Report findings

Give the user a concise summary organized by severity:

**🔴 Data-accuracy bugs (fixed)** — facts that were wrong and have been corrected.

**🟡 Structural issues (fixed)** — orphan pages registered, stale stats updated, undocumented files noted.

**⚪ Flagged for manual review** — broken links with ambiguous targets, deletion candidates, structural decisions you didn't want to make unilaterally.

**✅ No issues found** — call out any section that came back clean so the user knows it was checked.

End with: "No contradictions found" or list the contradictions and their resolution.

---

## Tips for different wiki shapes

**Obsidian vaults with `[[wiki links]]`:** The `[[target]]` syntax may omit the `.md` extension and may be relative or use the page title. Resolve links by matching the target string against file basenames (case-insensitive where the OS is case-insensitive).

**Wikis with a AGENTS.md:** AGENTS.md describes the intended structure — use it as the spec. Pages that AGENTS.md says should exist but don't are missing pages, not just gaps.

**Wikis without any index:** Run checks A–E using grep-based link analysis. Every page is reachable if at least one other page links to it OR it's at the top level of a section folder.

**Large wikis (100+ pages):** Prioritize: fix the master index first, then model/section indexes, then individual pages. Don't try to be exhaustive on the first pass — flag patterns and fix the most impactful issues.
