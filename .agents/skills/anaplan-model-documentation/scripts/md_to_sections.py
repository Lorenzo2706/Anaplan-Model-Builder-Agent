"""
Convert a sequence of research-agent markdown deliverables into a single
ordered JSON tree of typed content blocks, ready for build_docx.js.

Why this exists: research agents each pick their own markdown heading depth
(#, ##, ###) independently, and those choices are NOT consistent with each
other or with the model documentation's canonical outline numbering. Trusting
raw markdown heading depth produces a document with headings jumping around
at random. Instead, this script derives each heading's TRUE level from its
own numbering prefix (e.g. "2.1.1 Load" -> level 3, because it has 3
dot-separated segments), which is reliable because every agent is instructed
(see references/section-specs.md) to always prefix its headings with the
exact outline number from the canonical structure. Unnumbered headings
(model-specific names like "Loads (inferred)" or "Calculation flow") nest
one level deeper than whatever numbered/Appendix heading most recently
preceded them.

Usage:
    python md_to_sections.py <output.json> <file1.md> [<file2.md> ...]

Files are concatenated in the order given on the command line - that order
IS the document order, so pass them in canonical chapter sequence (e.g.
sec1_intro.md, sec2_dataflows.md, sec3_lists.md, ...).
"""
import re
import sys
import json


def clean_inline(text):
    text = text.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    return text.strip()


NUMBERED_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")
APPENDIX_RE = re.compile(r"^Appendix\s+[A-Z0-9]", re.IGNORECASE)


def heading_level(text):
    """Return the absolute outline level for a heading's text, or None if
    the text carries no explicit numbering (caller must nest it relative to
    the last numbered heading)."""
    m = NUMBERED_RE.match(text)
    if m:
        return len(m.group(1).split("."))
    if APPENDIX_RE.match(text):
        return 1
    return None


def parse_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        # A separator line ("|---|---|") is pipes/dashes/colons/space only -
        # but so is a genuinely blank header row ("|  |  |"), which is NOT a
        # separator and must not be swallowed here, or the table ends up
        # with zero real header cells further down.
        if re.match(r"^\|?[\s:\-]+\|[\s:\-|]*$", line) and "-" in line:
            continue
        cells = [clean_inline(c) for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    headers = rows[0] if rows else []
    body = rows[1:] if len(rows) > 1 else []
    if not headers or all(not h.strip() for h in headers):
        # No real column labels survived parsing - this "table" is either a
        # stray pipe-only line or a fully blank header row (both observed in
        # real research-agent output). Building a docx table with zero
        # populated columns produces a <w:tblGrid/> with no <w:gridCol>,
        # which is invalid OOXML - Word refuses to open the WHOLE document
        # over one bad table like that, not just skip it. Drop the block
        # entirely rather than emit something structurally broken.
        return None
    return {"type": "table", "headers": headers, "rows": body}


def parse_blocks(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "":
            i += 1
            continue
        if stripped.startswith(">"):
            kind_m = re.match(r"^>\s*\[!(\w+)\]", stripped)
            kind = kind_m.group(1).lower() if kind_m else "note"
            buf = []
            first = re.sub(r"^>\s*\[![\w]+\]\s*", "", stripped).strip()
            if first:
                buf.append(first)
            i += 1
            while i < n and lines[i].strip().startswith(">"):
                t = lines[i].strip().lstrip(">").strip()
                if t:
                    buf.append(t)
                i += 1
            blocks.append({"type": "callout", "kind": kind, "text": clean_inline(" ".join(buf))})
            continue
        if stripped.startswith("|"):
            tbl_lines = []
            while i < n and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i])
                i += 1
            tbl = parse_table(tbl_lines)
            if tbl is not None:
                blocks.append(tbl)
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(clean_inline(re.sub(r"^[-*]\s+", "", lines[i].strip())))
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue
        if stripped.startswith("[PLACEHOLDER"):
            buf = [stripped]
            i += 1
            while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(("#", "|", ">", "-", "*")):
                buf.append(lines[i].strip())
                i += 1
            blocks.append({"type": "placeholder", "text": clean_inline(" ".join(buf))})
            continue
        buf = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(("#", "|", ">", "- ", "* ")):
            buf.append(lines[i])
            i += 1
        blocks.append({"type": "para", "text": clean_inline(" ".join(x.strip() for x in buf))})
    return blocks


def unescape_html_entities(text):
    """Research-agent output has been observed coming back HTML-escaped
    (&gt; instead of >, &amp; instead of &) - likely an artifact of the
    message-passing layer between the agent and the orchestrator, not
    something the agent itself controls. Unescape on the RAW text before
    any structural parsing, not just on packaged block text: a callout
    marker of "&gt; [!note]" or a table row of "&gt;|foo|bar|" would
    otherwise fail the ">"/"|" prefix checks below and silently fall
    through to being treated as a plain paragraph instead of a callout or
    table row."""
    return (
        text.replace("&amp;", "&")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = unescape_html_entities(text)
    lines = text.split("\n")
    sections = []
    current = None
    buf = []

    def flush():
        if current is not None:
            sections.append({"heading": clean_inline(current), "blocks": parse_blocks(buf)})

    for line in lines:
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            flush()
            current = m.group(1)
            buf = []
        else:
            buf.append(line)
    flush()
    return sections


def assign_levels(sections):
    last_numbered_level = 1  # sensible default if the very first heading is unnumbered
    for sec in sections:
        lvl = heading_level(sec["heading"])
        if lvl is not None:
            sec["target_level"] = min(lvl, 4)
            last_numbered_level = lvl
        else:
            sec["target_level"] = min(last_numbered_level + 1, 4)
    return sections


def main():
    if len(sys.argv) < 3:
        print("Usage: python md_to_sections.py <output.json> <file1.md> [<file2.md> ...]")
        sys.exit(1)
    out_path = sys.argv[1]
    md_files = sys.argv[2:]

    all_sections = []
    for path in md_files:
        all_sections.extend(parse_file(path))

    assign_levels(all_sections)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_sections, f, ensure_ascii=False, indent=2)

    print(f"Sections: {len(all_sections)} -> {out_path}")
    for s in all_sections:
        print(f"  L{s['target_level']}  {s['heading']}  ({len(s['blocks'])} blocks)")


if __name__ == "__main__":
    main()
