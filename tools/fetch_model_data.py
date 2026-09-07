"""
fetch_model_data.py
-------------------
Read real cell values out of a live Anaplan model, one module or list per call.

Read-only. Token-bounded: prints a compact digest and writes the full grid to a
caller-supplied --out-dir (never a default location).

NEVER write fetched cell values into wiki/, analyses/, or log.md. See CLAUDE.md.
"""
import argparse
import csv
import os
import re
import sys
import time
from dataclasses import dataclass, field, replace
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# `models` resolves every credential via `os.getenv(...)` at IMPORT TIME (see
# the module-level `getenv(...)` calls in models.py), so `.env` must already
# be loaded into os.environ before `import models` runs below. Normally that
# happens as a side effect of importing `scraper_ux` (via `scrape_model_data`),
# but this CLI must not eagerly `import scrape_model_data`/`scraper_ux` at
# module top - that drags in Selenium at import time, which is slow and a
# hard dependency this explicitly "no browser" tool must not require just to
# parse --help. So `load_dotenv()` is called here, directly, ourselves.
#
# DO NOT let an import-sorter (isort/ruff/etc.) move `import models` above
# this call. If it ever does, every value in models.MODELS silently reverts
# to None instead of raising - this is the exact 2026-08-14 incident where a
# live request went to ".../models/None/..." instead of failing loudly.
try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv is optional; --help must not require it.
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

import anaplan_session
import models


@dataclass
class Grid:
    """Engine-agnostic normalized grid. Everything downstream operates on this,
    never on the raw Anaplan payload, so wire-format changes are confined to
    parse_view_data(). Revision 1's wire-format guesses were all wrong and this
    boundary is why only one function had to change."""
    row_dim_names: list[str] = field(default_factory=list)
    row_labels: list[tuple[str, ...]] = field(default_factory=list)
    col_labels: list[str] = field(default_factory=list)
    cells: list[list[str | None]] = field(default_factory=list)
    page_selection: dict[str, str] = field(default_factory=dict)
    available_page_dims: list[str] = field(default_factory=list)
    page_dim_ids: dict[str, str] = field(default_factory=dict)

    @property
    def n_rows(self) -> int:
        return len(self.row_labels)

    @property
    def n_cols(self) -> int:
        return len(self.col_labels)


def _cell(raw):
    """Verified 2026-08-14 against live FSP 2.0 data: all 2,688 probed cells came
    back as JSON strings, 1,288 of them the empty string ""; null was never
    returned. Anaplan represents a genuinely BLANK cell as "", not null. This
    still defensively treats None and whitespace-only strings as blank -> None
    too, so downstream code has ONE blank sentinel and can still tell a blank
    from a "0"."""
    if raw is None:
        return None
    text = str(raw)
    return None if text.strip() == "" else text


def parse_view_data(data_payload: dict, meta_payload: dict) -> Grid:
    """Convert an Anaplan view-data response into a Grid.

    THE ONLY function in this codebase that knows Anaplan's wire format.

    Takes TWO payloads because one is not enough:
      data_payload = GET /2/0/models/{m}/views/{v}/data?format=v1
        -> {"pages": [selected values], "columnCoordinates": [[...]],
            "rows": [{"rowCoordinates": [...], "cells": [...]}]}
      meta_payload = GET /2/0/models/{m}/views/{v}
        -> {"viewName", "columns": [{name,id}], "rows": [{name,id}],
            "pages": [{name,id}]}

    `pages` in the data payload is a bare list of SELECTED VALUES with no
    dimension names; the names live in the metadata payload and are matched by
    POSITION. Verified 2026-08-14.
    """
    rows = data_payload.get("rows") or []
    col_coords = data_payload.get("columnCoordinates") or []
    page_values = data_payload.get("pages") or []
    page_dims = meta_payload.get("pages") or []

    # Zip page dimension names to their selected values by position.
    page_selection, page_dim_ids = {}, {}
    for i, dim in enumerate(page_dims):
        name = dim.get("name")
        if not name:
            continue
        page_selection[name] = (page_values[i] if i < len(page_values) else "")
        page_dim_ids[name] = str(dim.get("id") or "")

    return Grid(
        row_dim_names=[d.get("name", "") for d in (meta_payload.get("rows") or [])],
        row_labels=[tuple(r.get("rowCoordinates") or []) for r in rows],
        col_labels=[" / ".join(c) for c in col_coords],
        cells=[[_cell(c) for c in (r.get("cells") or [])] for r in rows],
        page_selection=page_selection,
        available_page_dims=[d["name"] for d in page_dims if d.get("name")],
        page_dim_ids=page_dim_ids,
    )


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_raw_dir(shortcut, models_map, repo_root=REPO_ROOT):
    """Map a registry shortcut to its vault CSV folder.

    `<repo>/customers/<folder>/raw/models/<raw_dir>`.

    Both keys are required and neither is derivable:

    - `raw_dir`, because shortcut keys are abbreviations the modeller types and
      drift from the folder name as soon as a model is renamed.
    - `folder`, because two customers may legitimately hold a model with the
      same `raw_dir` ("Data Hub" is a near-universal name), so an unscoped path
      would read one customer's CSVs while reporting the other's.

    Defaulting either one picks a customer at random, so both raise instead.
    """
    if shortcut not in models_map:
        raise ValueError(
            f"'{shortcut}' is not a configured shortcut. Available: "
            f"{sorted(models_map)}"
        )
    entry = models_map[shortcut]
    missing = [k for k in ("raw_dir", "folder") if not entry.get(k)]
    if missing:
        raise ValueError(
            f"registry entry '{shortcut}' is missing {missing}. Add the vault "
            f"folder name(s) for this model, e.g. \"folder\": \"CustomerA\", "
            f"\"raw_dir\": \"ModelA 2.0\"."
        )
    path = os.path.join(repo_root, "customers", entry["folder"],
                        "raw", "models", entry["raw_dir"])
    if not os.path.isdir(path):
        raise ValueError(
            f"raw_dir {entry['raw_dir']!r} for shortcut '{shortcut}' does not "
            f"exist at {path}. Check 'folder' and 'raw_dir' in the registry "
            f"against the vault. Note the vault moved to "
            f"customers/<folder>/raw/models/ — there is no <repo>/raw/models/ "
            f"any more."
        )
    return path


class NameMismatchError(Exception):
    """The grid Anaplan returned is not the one that was asked for. Raised
    instead of returning data, because validating a formula against the wrong
    grid produces a confident wrong answer."""


# Anaplan pads section-header rows with braille-blank (U+2800), non-breaking
# space, and block emoji. Strip them before comparing names.
_PADDING = re.compile(r"[⠀ \s◼️▪⬛]+")


def _norm_name(value):
    return _PADDING.sub(" ", (value or "")).strip().casefold()


def find_view_id_offline(views_csv_path, module_name):
    """Look up a module's DEFAULT view ID in an ingested Views.csv.

    Returns None when the file is absent (some models have no Views.csv) or
    the module is not listed (another model's Views.csv covers 125 rows
    against 141 live views) - the caller then falls back to the live API.

    A module's default view has ID == Module ID. Scans ALL matching rows before
    settling, because a saved view with the same name may appear first and its
    filtered/pivoted layout would silently return a different grid.
    """
    if not os.path.isfile(views_csv_path):
        return None
    want = _norm_name(module_name)
    fallback = None
    with open(views_csv_path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            name = row.get("") or ""
            if _norm_name(name) != want:
                continue
            view_id = (row.get("ID") or "").strip()
            module_id = (row.get("Module ID") or "").strip()
            if view_id and view_id == module_id:
                return view_id
            fallback = fallback or view_id or None
    return fallback


def find_view_id_via_api(session, base, model_id, module_name):
    """Resolve a module name to its default view ID over the live API.

    Required, not optional: some models have no Views.csv at all, and another
    model's CSV is 16 views short of the live model."""
    body = session.get(f"{base}/2/0/models/{model_id}/views")
    views = body.get("views") or []
    want = _norm_name(module_name)
    fallback = None
    for v in views:
        if _norm_name(v.get("name")) != want:
            continue
        vid, mid = str(v.get("id") or ""), str(v.get("moduleId") or "")
        if vid and vid == mid:
            return vid
        fallback = fallback or vid or None
    if fallback:
        return fallback
    raise ValueError(
        f"No view named {module_name!r} exists in model {model_id}. "
        f"{len(views)} views are available; check the module name spelling."
    )


def find_list_id_via_api(session, base, model_id, list_name):
    """Resolve a list name to its ID over the live API.

    Always the API: General Lists.csv has no ID column, so no offline source
    for list IDs exists anywhere in the vault."""
    body = session.get(f"{base}/2/0/models/{model_id}/lists")
    lists = body.get("lists") or []
    want = _norm_name(list_name)
    for item in lists:
        if _norm_name(item.get("name")) == want:
            return str(item.get("id") or "")
    raise ValueError(
        f"No list named {list_name!r} exists in model {model_id}. "
        f"{len(lists)} lists are available; check the spelling."
    )


def fetch_view_metadata(session, base, model_id, view_id):
    """GET /views/{id} - the ONLY source of viewName, row/column dimension
    names, and page dimension names+ids. The data payload has none of them."""
    return session.get(f"{base}/2/0/models/{model_id}/views/{view_id}")


# Refuse rather than truncate above this size. A truncated grid the agent
# believes is complete is the worst outcome for formula validation.
MAX_CELLS = 50_000

# Engine per model, from CLAUDE.md. Surfaced in the digest because Classic
# and Polaris differ on sparsity and aggregation, which changes how blanks
# read.
#
# TEMPORARY. Both of the dicts below encode one customer's model layout in a
# tracked, public file, which is exactly what the customer-first registry
# exists to stop. Task 7 of the Pass 2 plan deletes both and reads `engine`
# and `workspace_label` off the resolved registry entry instead. Until then
# they are placeholder-keyed, so no real shortcut or raw_dir can ever match
# either dict: `engine` falls through to "unknown" for every real model, and
# `_DEV_SHORTCUTS` can never contain a real shortcut, so `workspace_label`
# will read "PRODUCTION" even for a model that is genuinely DEV. The "unknown"
# engine fails loud; the workspace mislabel fails quiet, but this tool is
# read-only diagnostics, so it is accepted until Task 7 restores both
# mappings from the registry.
_ENGINE_BY_RAW_DIR = {
    "ModelA 2.0": "Polaris",
    "ModelB Prod": "Classic",
}

# Only `modela` sits in a DEV workspace; the rest are production. Placeholder
# key only -- see the TEMPORARY note above.
_DEV_SHORTCUTS = {"modela"}


class GridTooLargeError(Exception):
    """The grid exceeds MAX_CELLS. Carries actionable narrowing advice."""


def check_grid_size(grid, max_cells=MAX_CELLS):
    total = grid.n_rows * grid.n_cols
    if total <= max_cells:
        return None
    dims = ", ".join(grid.available_page_dims) or "(none reported)"
    raise GridTooLargeError(
        f"Grid is {grid.n_rows} x {grid.n_cols} = {total} cells, over the "
        f"{max_cells} limit. Refusing to truncate. Narrow it with --page "
        f"(available page dimensions: {dims}), or restrict --periods."
    )


def fetch_module(session, base, model_id, view_id, meta_payload, pages):
    """Fetch a view's cell data. `format=v1` is MANDATORY - without it the API
    returns 400 'Mandatory query parameter format is missing'."""
    url = f"{base}/2/0/models/{model_id}/views/{view_id}/data?format=v1"
    if pages:
        url = f"{url}&pages={quote(pages, safe=':,')}"
    return parse_view_data(session.get(url), meta_payload)


def fetch_list_items(session, base, model_id, list_id):
    """Render list items as a Grid so digest/CSV/narrowing code is shared.

    The response key is `listItems`, NOT `items` (verified 2026-08-14)."""
    body = session.get(f"{base}/2/0/models/{model_id}/lists/{list_id}/items")
    items = body.get("listItems") or []
    cols = ["id", "code", "parent"]
    return Grid(
        row_dim_names=["Item"],
        row_labels=[(str(i.get("name", "")),) for i in items],
        col_labels=cols,
        cells=[[_fmt(i.get(c)) or None for c in cols] for i in items],
    )


def verify_resolved_name(requested, returned):
    """Confirm Anaplan returned the grid we asked for. Raises rather than
    returning data on mismatch - a stale offline ID must never silently
    resolve to a different module."""
    if _norm_name(requested) != _norm_name(returned):
        raise NameMismatchError(
            f"Asked Anaplan for {requested!r} but it returned {returned!r}. "
            f"The cached ID is probably stale - re-scrape this model's CSVs. "
            f"Refusing to return data that would be attributed to the wrong grid."
        )
    return None


def parse_page_arg(spec):
    """Parse --page "Product:Widget A,Region:EMEA" into {dimName: itemName}.

    Splits each comma segment on its FIRST colon only, so item names that
    themselves contain a colon (e.g. "1000: Revenue") survive intact."""
    out = {}
    for segment in (spec or "").split(","):
        segment = segment.strip()
        if not segment:
            continue
        if ":" not in segment:
            raise ValueError(
                f"--page segment {segment!r} is malformed. Use Dimension:Item, "
                f'e.g. --page "Product:Widget A,Region:EMEA".'
            )
        dim, item = segment.split(":", 1)
        out[dim.strip()] = item.strip()
    return out


def resolve_page_selection(session, base, model_id, meta_payload, wanted):
    """Translate {dimensionName: itemName} into {dimensionId: itemId}.

    The API rejects name-based page selection outright:
        pages=OPEX/CAPEX:CAPEX          -> 400 Malformed page parameters
        pages=214000000002              -> 400 Malformed pages parameter
        pages=101000000007:214000000002 -> 200   <-- the only accepted form
    Dimension ids come from the view metadata; item ids need one
    /lists/{dimId}/items call per selected dimension.
    """
    dims = {d.get("name"): str(d.get("id") or "")
            for d in (meta_payload.get("pages") or []) if d.get("name")}
    resolved = {}
    for dim_name, item_name in (wanted or {}).items():
        dim_id = next((i for n, i in dims.items()
                       if _norm_name(n) == _norm_name(dim_name)), None)
        if not dim_id:
            raise ValueError(
                f"{dim_name!r} is not a page dimension of this view. "
                f"Available: {sorted(dims)}"
            )
        body = session.get(f"{base}/2/0/models/{model_id}/lists/{dim_id}/items")
        # Verified 2026-08-14: the key is `listItems`, NOT `items`.
        items = body.get("listItems") or []
        item_id = next((str(it.get("id")) for it in items
                        if _norm_name(it.get("name")) == _norm_name(item_name)), None)
        if not item_id:
            names = sorted(str(it.get("name")) for it in items)
            raise ValueError(
                f"{item_name!r} is not an item of page dimension {dim_name!r}. "
                f"Available: {names[:40]}{' ...' if len(names) > 40 else ''}"
            )
        resolved[dim_id] = item_id
    return resolved


def build_pages_param(resolved):
    """Render {dimensionId: itemId} as the API's pages= value. Sorted by
    dimension id so the same request always produces the same URL."""
    return ",".join(f"{d}:{resolved[d]}" for d in sorted(resolved or {}))


def _detached_passthrough_fields(grid):
    """Copy every Grid field that neither narrow_rows nor narrow_cols rebuilds
    itself (row_dim_names, page_selection, available_page_dims, page_dim_ids).

    dataclasses.replace() only replaces the fields it is explicitly given;
    every other field is carried over BY REFERENCE to the new instance. Later
    stages keep a live reference to the un-narrowed grid, so a narrowed grid
    that still points at the same list/dict objects would let an in-place
    mutation on one grid (e.g. `narrowed.page_selection["X"] = "Y"`) silently
    corrupt the other. Returning fresh containers here is what makes the
    narrowed grid fully independent of its source."""
    return {
        "row_dim_names": list(grid.row_dim_names),
        "page_selection": dict(grid.page_selection),
        "available_page_dims": list(grid.available_page_dims),
        "page_dim_ids": dict(grid.page_dim_ids),
    }


def narrow_rows(grid, line_items):
    """Keep only rows whose label tuple contains one of `line_items`.

    Matches ANY component of the tuple, because a row label may combine a line
    item with a list item. Output preserves the grid's own row order so the
    digest layout is stable."""
    if not line_items:
        return grid
    wanted = {_norm_name(n) for n in line_items}
    keep = [i for i, labels in enumerate(grid.row_labels)
            if any(_norm_name(part) in wanted for part in labels)]
    matched = {_norm_name(part) for i in keep for part in grid.row_labels[i]}
    missing = sorted(n for n in line_items if _norm_name(n) not in matched)
    if missing:
        available = sorted({part for labels in grid.row_labels for part in labels})
        raise ValueError(
            f"Line item(s) {missing} are not rows in this grid. Available rows: "
            f"{available[:40]}{' ...' if len(available) > 40 else ''}"
        )
    return replace(
        grid,
        row_labels=[grid.row_labels[i] for i in keep],
        cells=[list(grid.cells[i]) for i in keep],
        col_labels=list(grid.col_labels),
        **_detached_passthrough_fields(grid),
    )


def narrow_cols(grid, periods_spec):
    """Keep only the named columns.

    Two forms, both matching the labels exactly as Anaplan returns them:
      "Jan 26,Mar 26"   explicit list
      "Jan 26:Mar 26"   inclusive range by position
    Label-based on purpose: no calendar parsing, so it works whatever format
    the periods come back in.
    """
    spec = (periods_spec or "").strip()
    if not spec:
        return grid

    index = {_norm_name(c): i for i, c in enumerate(grid.col_labels)}

    def locate(label):
        key = _norm_name(label)
        if key not in index:
            raise ValueError(
                f"Period {label!r} is not a column in this grid. Available: "
                f"{grid.col_labels}"
            )
        return index[key]

    if ":" in spec:
        start_label, end_label = spec.split(":", 1)
        start, end = locate(start_label.strip()), locate(end_label.strip())
        if start > end:
            raise ValueError(
                f"Period range start {start_label.strip()!r} comes after end "
                f"{end_label.strip()!r} in this grid's column order."
            )
        keep = list(range(start, end + 1))
    else:
        keep = [locate(part.strip()) for part in spec.split(",") if part.strip()]

    return replace(
        grid,
        col_labels=[grid.col_labels[i] for i in keep],
        cells=[[row[i] for i in keep] for row in grid.cells],
        row_labels=list(grid.row_labels),
        **_detached_passthrough_fields(grid),
    )


_UNSAFE_FILENAME = re.compile(r'[/\\:*?"<>|]+')


def safe_print(text):
    """Print text that may contain characters the console can't encode.

    Live Anaplan row labels include values like 'Financien' (with a diaeresis).
    On Windows the default console encoding is cp1252, and printing such text
    raises UnicodeEncodeError - which would throw away the digest AFTER the
    data had already been fetched from a live model. That is the worst place
    to fail, so this degrades the unprintable characters instead of losing the
    result.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        enc = (getattr(sys.stdout, "encoding", None) or "ascii")
        sys.stdout.write(text.encode(enc, "replace").decode(enc, "replace") + "\n")


def select_sample_indices(n_rows, sample_n):
    """Evenly spaced row indices, always including the first and last row.

    Deterministic on purpose - the same fetch must produce the same sample on
    every run, so a validation can be re-checked and reproduced.

    Dedup invariant: once n_rows <= 0 and sample_n >= n_rows are handled above,
    sample_n is strictly between 2 and n_rows - 1, so step = (n_rows-1) /
    (sample_n-1) is strictly greater than 1. Two indices i < j then have real
    positions i*step < j*step differing by more than 1, and since round() never
    moves a value by more than 0.5, their rounded results cannot collide. The
    `sorted({...})` below therefore never drops an index in practice for this
    function's own call sites - it is a belt-and-braces guard, not a silent
    truncation path.
    """
    if n_rows <= 0:
        return []
    if sample_n >= n_rows:
        return list(range(n_rows))
    if sample_n <= 1:
        return [0]
    step = (n_rows - 1) / (sample_n - 1)
    return sorted({int(round(i * step)) for i in range(sample_n)})


def row_stats(cells_row):
    """Per-row fill and range stats.

    Blank and zero are counted SEPARATELY: 'no value here' and 'the value is
    zero' are different facts when validating a formula, and collapsing them
    would hide a real class of bug. Non-numeric text is ignored rather than
    raising, since a row may legitimately mix labels and numbers.
    """
    blank = zero = numeric = 0
    lo = hi = None
    for raw in cells_row:
        if raw is None or str(raw).strip() == "":
            blank += 1
            continue
        try:
            val = float(str(raw).replace(",", ""))
        except ValueError:
            continue
        numeric += 1
        if val == 0:
            zero += 1
        lo = val if lo is None else min(lo, val)
        hi = val if hi is None else max(hi, val)
    return {"blank": blank, "zero": zero, "min": lo, "max": hi, "numeric": numeric}


def write_full_csv(grid, out_dir, model_name, object_name, timestamp):
    """Write the complete grid to out_dir and return the path.

    out_dir is ALWAYS caller-supplied (the agent's session scratchpad), never a
    default location inside this repo: the repo lives under OneDrive sync and
    fetched cells are real client values. See CLAUDE.md and the module
    docstring above.
    """
    os.makedirs(out_dir, exist_ok=True)
    stem = _UNSAFE_FILENAME.sub("-", f"{model_name}-{object_name}-{timestamp}")
    path = os.path.join(out_dir, f"{stem}.csv")
    header = list(grid.row_dim_names or ["Row"]) + list(grid.col_labels)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for labels, row in zip(grid.row_labels, grid.cells):
            writer.writerow(list(labels) + ["" if c is None else c for c in row])
    return path


def _fmt(value):
    return "" if value is None else str(value)


def build_digest(grid, meta, sample_n, full_path):
    """Compact, token-bounded stdout summary of a fetched grid.

    Carries real labelled values so a formula can actually be checked, and
    always states how much of the grid was sampled so a partial view can never
    be mistaken for a complete one.
    """
    populated = sum(1 for row in grid.cells for c in row
                    if c is not None and str(c).strip() != "")
    total = grid.n_rows * grid.n_cols
    pages = " | ".join(f"{d}={grid.page_selection[d]}"
                       for d in sorted(grid.page_selection)) or "(none)"
    indices = select_sample_indices(grid.n_rows, sample_n)

    lines = [
        f"OBJECT : {meta.get('object_name', '')}  (view {meta.get('view_id', '')})",
        f"MODEL  : {meta.get('model_name', '')}  [{meta.get('workspace_label', '')}]"
        f"  engine={meta.get('engine', 'unknown')}",
        f"PAGES  : {pages}",
        f"GRID   : {grid.n_rows} rows x {grid.n_cols} cols "
        f"({total} cells, {populated} populated, {total - populated} blank)",
        f"COLS   : {' | '.join(grid.col_labels)}",
        f"SAMPLE : {len(indices)} of {grid.n_rows} rows "
        f"(deterministic: evenly spaced, first and last always included)",
    ]

    label_width = max((len(" / ".join(grid.row_labels[i])) for i in indices),
                      default=0)
    for i in indices:
        label = " / ".join(grid.row_labels[i]).ljust(label_width)
        values = " | ".join(_fmt(c) for c in grid.cells[i])
        lines.append(f"  {label} | {values}")

    lines.append("STATS  : per sampled row")
    for i in indices:
        s = row_stats(grid.cells[i])
        label = " / ".join(grid.row_labels[i]).ljust(label_width)
        lines.append(
            f"  {label} | blank={s['blank']} zero={s['zero']} "
            f"numeric={s['numeric']} min={_fmt(s['min'])} max={_fmt(s['max'])}"
        )

    if grid.available_page_dims:
        lines.append(f"NARROW : page dims available -> "
                     f"{', '.join(grid.available_page_dims)}")
    lines.append(f"FULL   : {full_path}")
    lines.append("NOTE   : values above are live model data. Quote them in chat "
                 "if useful, but never write them into wiki/, analyses/, or log.md.")
    return "\n".join(lines)


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="fetch_model_data.py",
        description="Read-only: fetch live Anaplan cell data for one module or "
                    "list. Prints a token-bounded digest; writes the full grid "
                    "to --out-dir.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (("module", "Fetch a module's default view"),
                            ("list", "Fetch a list's items")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("shortcut", help="models.py shortcut, e.g. fsp")
        p.add_argument("name", help="Module or list name, exactly as in Anaplan")
        p.add_argument("--out-dir", required=True,
                       help="REQUIRED. Directory for the full CSV - pass your "
                            "session scratchpad. Never a path inside the repo.")
        p.add_argument("--sample", type=int, default=10,
                       help="Rows to show in the digest (default 10)")
        if name == "module":
            p.add_argument("--page", default="",
                           help='Server-side narrowing, e.g. "Product:Widget A,Region:EMEA"')
            p.add_argument("--line-items", default="",
                           help='Rows to keep, e.g. "Volume,Price"')
            p.add_argument("--periods", default="",
                           help='Columns to keep: "Jan 26,Mar 26" or "Jan 26:Mar 26"')
    return parser


def _is_inside_repo(path, repo_root=REPO_ROOT):
    """True if `path` is the repo root itself or anything under it.

    Deliberately NOT `os.path.abspath(path).startswith(os.path.abspath(repo_root))`:
    that raw-string check has two bugs on Windows, the platform this actually
    runs on. First, `os.path.abspath()` does not normalize case, so a
    repo-inside path that merely differs in drive-letter or segment casing
    (routine with copy-pasted Windows/OneDrive paths) fails the `startswith`
    and slips PAST the guard - the exact failure this guard exists to
    prevent. Second, a raw prefix match is wrong the other way too: a sibling
    directory that merely shares a string prefix with the repo root (e.g.
    "...\\Anaplan LLM wiki-backup" next to "...\\Anaplan LLM wiki") would be
    incorrectly REJECTED. Normalizing case and comparing on a path-component
    boundary via `os.path.commonpath` fixes both directions.
    """
    target = os.path.normcase(os.path.abspath(path))
    root = os.path.normcase(os.path.abspath(repo_root))
    if target == root:
        return True
    try:
        common = os.path.commonpath([target, root])
    except ValueError:
        # Different drives on Windows (e.g. D:\... vs C:\...) - never inside.
        return False
    return common == root


def main(argv=None):
    args = build_arg_parser().parse_args(argv)

    if _is_inside_repo(args.out_dir):
        print(f"ERROR: --out-dir {args.out_dir!r} is inside the repository. "
              f"This repo is under OneDrive sync and must never hold client "
              f"cell data. Pass your session scratchpad instead.", file=sys.stderr)
        return 2

    try:
        entry = models.MODELS[args.shortcut]
    except KeyError:
        print(f"ERROR: unknown shortcut {args.shortcut!r}. Available: "
              f"{sorted(models.MODELS)}", file=sys.stderr)
        return 2

    model_id = entry["model_id"]
    raw_dir_name = entry.get("raw_dir", "")
    meta = {
        "model_name": raw_dir_name or entry.get("name", args.shortcut),
        "object_name": args.name,
        "engine": _ENGINE_BY_RAW_DIR.get(raw_dir_name, "unknown"),
        "workspace_label": "DEV" if args.shortcut in _DEV_SHORTCUTS else "PRODUCTION",
        "view_id": "",
    }

    # open_session()'s only job is the credential/token exchange: it calls
    # scrape_model_data._api_session() -> _anaplan_token(), and every raise
    # site in that path (missing ANAPLAN_USERNAME/PASSWORD, unreachable token
    # endpoint, failed token exchange) is a plain RuntimeError - never an
    # anaplan_session.AnaplanError, which open_session() has no way to raise
    # since it never touches AnaplanSession.get(). The catch is narrowed to
    # exactly RuntimeError (verified by reading both call sites, not assumed)
    # so that an ImportError/ModuleNotFoundError from the `import
    # scrape_model_data` this function performs at call time - a broken
    # dependency, a typo, anything unrelated to credentials - propagates
    # instead of being confidently misreported as an auth failure. This call
    # is deliberately OUTSIDE the try/finally below: if it raises, no session
    # was ever created, so there is nothing for `finally: session.close()` to
    # leak and no risk of `finally` referencing an unbound `session` name.
    try:
        session = anaplan_session.open_session()
    except RuntimeError as e:
        print(f"ERROR (auth): {e}\nToken refresh failed. Check .env credentials.",
              file=sys.stderr)
        return 5

    base = session.base_url
    try:
        if args.command == "module":
            view_id = None
            try:
                raw_dir = resolve_raw_dir(args.shortcut, models.MODELS)
                view_id = find_view_id_offline(
                    os.path.join(raw_dir, "Views.csv"), args.name)
            except ValueError as e:
                print(f"  (offline lookup unavailable: {e})", file=sys.stderr)
            if not view_id:
                print("  (resolving view ID via API)", file=sys.stderr)
                view_id = find_view_id_via_api(session, base, model_id, args.name)
            meta["view_id"] = view_id

            view_meta = fetch_view_metadata(session, base, model_id, view_id)
            # Guard against a stale offline ID resolving to a different module.
            verify_resolved_name(args.name, view_meta.get("viewName", ""))

            pages = build_pages_param(resolve_page_selection(
                session, base, model_id, view_meta, parse_page_arg(args.page)))
            grid = fetch_module(session, base, model_id, view_id, view_meta, pages)
            check_grid_size(grid)
            grid = narrow_rows(grid, [s.strip() for s in args.line_items.split(",")
                                      if s.strip()])
            grid = narrow_cols(grid, args.periods)
        else:
            list_id = find_list_id_via_api(session, base, model_id, args.name)
            meta["view_id"] = list_id
            grid = fetch_list_items(session, base, model_id, list_id)
            check_grid_size(grid)

        if grid.n_rows == 0:
            safe_print(f"EMPTY: {args.name!r} resolved successfully "
                       f"(id {meta['view_id']}) but the grid has no rows. This is "
                       f"a real model state, not an error - do NOT read it as "
                       f"'the formula produces nothing'.")
            return 0

        timestamp = time.strftime("%Y%m%dT%H%M%S")
        full_path = write_full_csv(grid, args.out_dir, meta["model_name"],
                                   args.name, timestamp)
        safe_print(build_digest(grid, meta, args.sample, full_path))
        return 0

    except anaplan_session.AnaplanTooLargeError as e:
        print(f"ERROR (too large): {e}\nNarrow with --page and retry.",
              file=sys.stderr)
        return 3
    except GridTooLargeError as e:
        print(f"ERROR (too large): {e}", file=sys.stderr)
        return 3
    except NameMismatchError as e:
        print(f"ERROR (wrong grid): {e}", file=sys.stderr)
        return 4
    except anaplan_session.AnaplanAuthError as e:
        print(f"ERROR (auth): {e}\nToken refresh failed. Check .env credentials.",
              file=sys.stderr)
        return 5
    except anaplan_session.AnaplanTimeoutError as e:
        print(f"ERROR (timeout): {e}\nThis is a timeout, NOT an empty grid.",
              file=sys.stderr)
        return 6
    except (anaplan_session.AnaplanError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())
