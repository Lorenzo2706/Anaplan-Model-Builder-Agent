import json
import os
from dataclasses import replace
from pathlib import Path

import pytest

import fetch_model_data
import registry
from fetch_model_data import (
    Grid,
    GridTooLargeError,
    MAX_CELLS,
    NameMismatchError,
    build_arg_parser,
    build_digest,
    build_pages_param,
    check_grid_size,
    fetch_list_items,
    fetch_module,
    fetch_view_metadata,
    find_list_id_via_api,
    find_view_id_offline,
    find_view_id_via_api,
    main,
    narrow_cols,
    narrow_rows,
    parse_page_arg,
    parse_view_data,
    resolve_page_selection,
    row_stats,
    safe_print,
    select_sample_indices,
    verify_resolved_name,
    write_full_csv,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def sample_grid():
    return parse_view_data(load_fixture("view_data_sample.json"),
                           load_fixture("view_meta_sample.json"))


def test_parse_view_data_shape():
    grid = sample_grid()
    assert isinstance(grid, Grid)
    assert grid.col_labels == ["Jan 26", "Feb 26", "Mar 26"]
    assert grid.row_labels == [("Volume",), ("Price",), ("Revenue",), ("Discount",)]
    assert grid.cells[0] == ["100", "105", "110"]


def test_parse_view_data_row_dim_names_come_from_metadata():
    """The data payload has no row dimension names - they only exist in
    GET /views/{id}. A Grid built from the data payload alone would be
    unlabelled."""
    assert sample_grid().row_dim_names == ["Line Item"]


def test_parse_view_data_page_selection_zips_names_to_values():
    """`pages` in the data payload is a bare list of selected VALUES; the
    dimension NAMES come from the metadata payload, matched by position."""
    grid = sample_grid()
    assert grid.page_selection == {"Product": "Widget A", "Region": "EMEA"}
    assert grid.available_page_dims == ["Product", "Region"]
    assert grid.page_dim_ids == {"Product": "101000000007", "Region": "101000000019"}


def test_parse_view_data_normalizes_empty_string_to_none():
    """A blank cell and a zero cell are DIFFERENT facts when validating a
    formula. Anaplan sends blanks as "" and zeros as "0"; collapsing them would
    hide a real class of bug."""
    assert sample_grid().cells[3] == [None, "0", None]


def test_parse_view_data_handles_multi_coordinate_axes():
    """Coordinate tuples are length 1 only when a single dimension is on the
    axis. Two dimensions on rows produce 2-element tuples."""
    data = {
        "pages": [],
        "columnCoordinates": [["Jan 26", "Actual"], ["Jan 26", "Budget"]],
        "rows": [{"rowCoordinates": ["EMEA", "Volume"], "cells": ["1", "2"]}],
    }
    meta = {"viewName": "V", "viewId": "1",
            "columns": [{"name": "Time", "id": "a"}, {"name": "Version", "id": "b"}],
            "rows": [{"name": "Region", "id": "c"}, {"name": "Line Item", "id": "d"}],
            "pages": []}
    grid = parse_view_data(data, meta)
    assert grid.row_labels == [("EMEA", "Volume")]
    assert grid.col_labels == ["Jan 26 / Actual", "Jan 26 / Budget"]
    assert grid.row_dim_names == ["Region", "Line Item"]


def test_parse_view_data_normalizes_null_cell_to_none_too():
    """How Anaplan represents a genuinely blank cell is UNVERIFIED against the
    live API - every probed cell was a non-empty string, so "" is only an
    assumption, not an observation. This test builds an inline payload where a
    blank cell arrives as JSON null (the other plausible sentinel) instead of
    "", and proves parse_view_data normalizes it to None exactly like the ""
    case, while still keeping a real "0" distinct from either blank form."""
    data = {
        "pages": [],
        "columnCoordinates": [["Jan 26"], ["Feb 26"]],
        "rows": [{"rowCoordinates": ["Discount"], "cells": [None, "0"]}],
    }
    meta = {"viewName": "V", "viewId": "1",
            "columns": [{"name": "Time", "id": "a"}],
            "rows": [{"name": "Line Item", "id": "b"}],
            "pages": []}
    grid = parse_view_data(data, meta)
    assert grid.cells[0] == [None, "0"]


# resolve_raw_dir and its seven tests used to live here. The function is gone:
# the vault path for a model is ResolvedModel.default_out_dir now, derived from
# the customer's `folder` plus the model's `raw_dir`, and test_registry.py's
# TestDerivedUrlsAndPaths / TestResolveOutDir carry its assertions - raw_dir
# not name, customer-folder scoping, the "no <repo>/raw/models/ any more"
# regression guard, and the must-already-exist check.


# Row 2 is a SAVED view sharing the module's exact name with a different ID,
# listed BEFORE the default view. Without it, nothing would exercise the
# ID == Module ID preference and a naive first-match would pass.
VIEWS_CSV = """﻿,ID,Module ID,Code
⠀⠀⠀       ◼️ LOAD MODULES,102000000000,102000000000,
REV 01. Revenue Calc,102000000099,102000000025,
REV 01. Revenue Calc,102000000025,102000000025,
CA 02. Cost Allocation,102000000031,102000000031,
"""


def write_views_csv(tmp_path):
    p = tmp_path / "Views.csv"
    p.write_text(VIEWS_CSV, encoding="utf-8")
    return str(p)


def test_find_view_id_offline_prefers_default_view_over_same_named_saved_view(tmp_path):
    """A module's DEFAULT view has ID == Module ID. A saved view sharing the
    name must never win: its filtered/pivoted layout would silently return a
    different grid. The saved view is listed FIRST in the fixture so a naive
    first-match implementation fails this test."""
    assert find_view_id_offline(write_views_csv(tmp_path),
                                "REV 01. Revenue Calc") == "102000000025"


def test_find_view_id_offline_is_case_insensitive(tmp_path):
    assert find_view_id_offline(write_views_csv(tmp_path),
                                "rev 01. revenue calc") == "102000000025"


def test_find_view_id_offline_strips_section_header_padding(tmp_path):
    """Modules.csv/Views.csv contain section pseudo-rows padded with braille
    blanks and emoji. They must still be findable by their bare name."""
    assert find_view_id_offline(write_views_csv(tmp_path),
                                "LOAD MODULES") == "102000000000"


def test_find_view_id_offline_returns_none_when_absent(tmp_path):
    assert find_view_id_offline(write_views_csv(tmp_path), "Nope") is None


def test_find_view_id_offline_returns_none_when_file_missing(tmp_path):
    """Some models have no Views.csv at all - this must fall through, not crash."""
    assert find_view_id_offline(str(tmp_path / "Views.csv"), "Anything") is None


class FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, timeout=180):
        self.calls.append(url)
        return self.payload


def test_find_view_id_via_api_prefers_default_view():
    sess = FakeSession(load_fixture("views_list_sample.json"))
    got = find_view_id_via_api(sess, "https://api.anaplan.com", "M1",
                               "REV 01. Revenue Calc")
    assert got == "102000000025"


def test_find_view_id_via_api_raises_when_absent():
    sess = FakeSession(load_fixture("views_list_sample.json"))
    with pytest.raises(ValueError) as exc:
        find_view_id_via_api(sess, "https://api.anaplan.com", "M1", "Ghost Module")
    assert "Ghost Module" in str(exc.value)


def test_find_list_id_via_api():
    sess = FakeSession(load_fixture("lists_sample.json"))
    got = find_list_id_via_api(sess, "https://api.anaplan.com", "M1", "Afdeling")
    assert got == "101000000013"


def test_fetch_view_metadata_returns_the_metadata_payload():
    sess = FakeSession(load_fixture("view_meta_sample.json"))
    meta = fetch_view_metadata(sess, "https://api.anaplan.com", "M1", "102000000025")
    assert meta["viewName"] == "REV 01. Revenue Calc"
    assert sess.calls == [
        "https://api.anaplan.com/2/0/models/M1/views/102000000025"]


def test_verify_resolved_name_accepts_match():
    assert verify_resolved_name("REV 01. Revenue Calc", "REV 01. Revenue Calc") is None


def test_verify_resolved_name_tolerates_whitespace_and_case():
    assert verify_resolved_name(" REV 01. Revenue Calc ", "rev 01. revenue calc") is None


def test_verify_resolved_name_rejects_mismatch():
    """The guard against silently validating a formula against the WRONG grid."""
    with pytest.raises(NameMismatchError) as exc:
        verify_resolved_name("REV 01. Revenue Calc", "CA 02. Cost Allocation")
    assert "REV 01. Revenue Calc" in str(exc.value)
    assert "CA 02. Cost Allocation" in str(exc.value)


def test_parse_page_arg_basic():
    assert parse_page_arg("Product:Widget A,Region:EMEA") == {
        "Product": "Widget A", "Region": "EMEA"}


def test_parse_page_arg_value_may_contain_colon_and_spaces():
    assert parse_page_arg("Account:1000: Revenue") == {"Account": "1000: Revenue"}


def test_parse_page_arg_empty_returns_empty_dict():
    assert parse_page_arg("") == {}
    assert parse_page_arg(None) == {}


def test_parse_page_arg_rejects_missing_colon():
    with pytest.raises(ValueError) as exc:
        parse_page_arg("Product")
    assert "Dimension:Item" in str(exc.value)


class FakeItemsSession:
    """Returns list items for /lists/{id}/items - note the `listItems` key."""

    def __init__(self):
        self.calls = []

    def get(self, url, timeout=180):
        self.calls.append(url)
        return {"listItems": [
            {"id": "214000000001", "name": "Widget A"},
            {"id": "214000000002", "name": "Widget B"},
        ]}


def test_resolve_page_selection_maps_names_to_ids():
    """The API rejects name-based pages= with 400 Malformed page parameters.
    Both sides must become numeric IDs."""
    meta = load_fixture("view_meta_sample.json")
    got = resolve_page_selection(FakeItemsSession(), "https://api.anaplan.com",
                                 "M1", meta, {"Product": "Widget B"})
    assert got == {"101000000007": "214000000002"}


def test_resolve_page_selection_unknown_dimension_lists_available():
    meta = load_fixture("view_meta_sample.json")
    with pytest.raises(ValueError) as exc:
        resolve_page_selection(FakeItemsSession(), "https://api.anaplan.com",
                               "M1", meta, {"Ghost": "X"})
    assert "Ghost" in str(exc.value) and "Product" in str(exc.value)


def test_resolve_page_selection_unknown_item_lists_available():
    meta = load_fixture("view_meta_sample.json")
    with pytest.raises(ValueError) as exc:
        resolve_page_selection(FakeItemsSession(), "https://api.anaplan.com",
                               "M1", meta, {"Product": "Nonexistent"})
    assert "Nonexistent" in str(exc.value) and "Widget A" in str(exc.value)


def test_build_pages_param_uses_ids_and_is_deterministic():
    """Sorted so identical requests produce byte-identical URLs, which keeps
    runs reproducible."""
    a = build_pages_param({"101000000019": "9", "101000000007": "1"})
    b = build_pages_param({"101000000007": "1", "101000000019": "9"})
    assert a == b == "101000000007:1,101000000019:9"


def test_build_pages_param_empty_is_empty_string():
    assert build_pages_param({}) == ""


def test_narrow_rows_selects_named_line_items():
    got = narrow_rows(sample_grid(), ["Volume", "Revenue"])
    assert got.row_labels == [("Volume",), ("Revenue",)]
    assert got.cells == [["100", "105", "110"], ["250", "262.5", "302.5"]]


def test_narrow_rows_is_case_insensitive():
    assert narrow_rows(sample_grid(), ["volume"]).row_labels == [("Volume",)]


def test_narrow_rows_preserves_source_order():
    """Output follows GRID order, not argument order, so the digest layout is
    stable regardless of how the caller listed the line items."""
    got = narrow_rows(sample_grid(), ["Revenue", "Volume"])
    assert got.row_labels == [("Volume",), ("Revenue",)]


def test_narrow_rows_empty_list_is_a_noop():
    assert narrow_rows(sample_grid(), []).n_rows == 4


def test_narrow_rows_unknown_name_raises_and_lists_available():
    with pytest.raises(ValueError) as exc:
        narrow_rows(sample_grid(), ["Ghost"])
    assert "Ghost" in str(exc.value)
    assert "Volume" in str(exc.value)


def test_narrow_cols_explicit_list():
    got = narrow_cols(sample_grid(), "Jan 26,Mar 26")
    assert got.col_labels == ["Jan 26", "Mar 26"]
    assert got.cells[0] == ["100", "110"]


def test_narrow_cols_range_is_inclusive():
    got = narrow_cols(sample_grid(), "Jan 26:Feb 26")
    assert got.col_labels == ["Jan 26", "Feb 26"]
    assert got.cells[2] == ["250", "262.5"]


def test_narrow_cols_range_rejects_reversed_bounds():
    with pytest.raises(ValueError) as exc:
        narrow_cols(sample_grid(), "Mar 26:Jan 26")
    assert "after" in str(exc.value).lower()


def test_narrow_cols_unknown_label_raises():
    with pytest.raises(ValueError) as exc:
        narrow_cols(sample_grid(), "Jun 99")
    assert "Jun 99" in str(exc.value)


def test_narrow_cols_empty_is_a_noop():
    assert narrow_cols(sample_grid(), "").n_cols == 3


def test_narrow_rows_does_not_alias_row_lists_with_source():
    """Later code holds a reference to the unnarrowed grid alongside the
    narrowed one. If narrow_rows's returned Grid shares its inner row lists
    with the source (e.g. `cells=[grid.cells[i] for i in keep]`, which copies
    the outer list but reuses each inner row object), mutating a cell in the
    narrowed grid silently corrupts the same cell in the original."""
    grid = sample_grid()
    original_value = grid.cells[0][1]
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.cells[0][1] = "MUTATED"
    assert grid.cells[0][1] == original_value


def test_narrow_cols_does_not_alias_row_lists_with_source():
    """Same aliasing guarantee as narrow_rows, pinned here too so it cannot
    silently regress in whichever of the two a future edit touches."""
    grid = sample_grid()
    original_value = grid.cells[0][0]
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.cells[0][0] = "MUTATED"
    assert grid.cells[0][0] == original_value


def test_narrow_rows_does_not_alias_col_labels_with_source():
    """narrow_rows never rebuilds col_labels itself (only narrow_cols narrows
    columns), so dataclasses.replace() would otherwise carry over the SAME
    list object from the source grid. Appending to the narrowed grid's
    col_labels must not resize the original's."""
    grid = sample_grid()
    original_cols = list(grid.col_labels)
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.col_labels.append("Apr 26")
    assert grid.col_labels == original_cols


def test_narrow_rows_does_not_alias_page_selection_with_source():
    """page_selection is a passthrough dict untouched by narrow_rows's own
    logic. Writing through the narrowed grid's copy must not leak into the
    source grid that later code still holds a reference to."""
    grid = sample_grid()
    original_selection = dict(grid.page_selection)
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.page_selection["Product"] = "MUTATED"
    assert grid.page_selection == original_selection


def test_narrow_rows_does_not_alias_available_page_dims_with_source():
    """available_page_dims is a passthrough list. Appending to the narrowed
    grid's copy must not affect the source grid's list."""
    grid = sample_grid()
    original_dims = list(grid.available_page_dims)
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.available_page_dims.append("MUTATED")
    assert grid.available_page_dims == original_dims


def test_narrow_rows_does_not_alias_page_dim_ids_with_source():
    """page_dim_ids is a passthrough dict, same aliasing risk as
    page_selection."""
    grid = sample_grid()
    original_ids = dict(grid.page_dim_ids)
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.page_dim_ids["Product"] = "MUTATED"
    assert grid.page_dim_ids == original_ids


def test_narrow_rows_does_not_alias_row_dim_names_with_source():
    """row_dim_names is a passthrough list, same aliasing risk as
    available_page_dims."""
    grid = sample_grid()
    original_names = list(grid.row_dim_names)
    narrowed = narrow_rows(grid, ["Volume"])
    narrowed.row_dim_names.append("MUTATED")
    assert grid.row_dim_names == original_names


def test_narrow_cols_does_not_alias_row_labels_container_with_source():
    """narrow_cols never rebuilds row_labels itself (only narrow_rows narrows
    rows), so dataclasses.replace() would otherwise carry over the SAME outer
    list object from the source grid. The individual tuple elements are
    immutable and safe to share, but the list container itself must be
    distinct: appending to the narrowed grid's row_labels must not resize the
    original's."""
    grid = sample_grid()
    original_rows = list(grid.row_labels)
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.row_labels.append(("MUTATED",))
    assert grid.row_labels == original_rows


def test_narrow_cols_does_not_alias_page_selection_with_source():
    """Same passthrough-dict aliasing guarantee as narrow_rows, pinned
    independently for narrow_cols."""
    grid = sample_grid()
    original_selection = dict(grid.page_selection)
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.page_selection["Product"] = "MUTATED"
    assert grid.page_selection == original_selection


def test_narrow_cols_does_not_alias_available_page_dims_with_source():
    """Same passthrough-list aliasing guarantee as narrow_rows, pinned
    independently for narrow_cols."""
    grid = sample_grid()
    original_dims = list(grid.available_page_dims)
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.available_page_dims.append("MUTATED")
    assert grid.available_page_dims == original_dims


def test_narrow_cols_does_not_alias_page_dim_ids_with_source():
    """Same passthrough-dict aliasing guarantee as narrow_rows, pinned
    independently for narrow_cols."""
    grid = sample_grid()
    original_ids = dict(grid.page_dim_ids)
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.page_dim_ids["Product"] = "MUTATED"
    assert grid.page_dim_ids == original_ids


def test_narrow_cols_does_not_alias_row_dim_names_with_source():
    """Same passthrough-list aliasing guarantee as narrow_rows, pinned
    independently for narrow_cols."""
    grid = sample_grid()
    original_names = list(grid.row_dim_names)
    narrowed = narrow_cols(grid, "Jan 26")
    narrowed.row_dim_names.append("MUTATED")
    assert grid.row_dim_names == original_names


def test_sample_indices_returns_all_when_grid_is_small():
    assert select_sample_indices(3, 10) == [0, 1, 2]


def test_sample_indices_includes_first_and_last():
    got = select_sample_indices(48, 3)
    assert got[0] == 0 and got[-1] == 47


def test_sample_indices_are_evenly_spaced_and_deterministic():
    assert select_sample_indices(48, 3) == [0, 24, 47]
    assert select_sample_indices(48, 3) == [0, 24, 47]


def test_sample_indices_single_sample_takes_first():
    assert select_sample_indices(48, 1) == [0]


def test_sample_indices_never_duplicates():
    got = select_sample_indices(4, 10)
    assert got == sorted(set(got))


def test_sample_indices_empty_grid():
    assert select_sample_indices(0, 5) == []


def test_row_stats_distinguishes_blank_from_zero():
    """A blank cell and a zero cell are different facts when validating a
    formula. Collapsing them would hide real bugs."""
    stats = row_stats([None, "0", "5", None, "10"])
    assert stats["blank"] == 2
    assert stats["zero"] == 1
    assert stats["min"] == 0.0
    assert stats["max"] == 10.0
    assert stats["numeric"] == 3


def test_row_stats_all_blank():
    stats = row_stats([None, None])
    assert stats["blank"] == 2 and stats["min"] is None and stats["max"] is None


def test_row_stats_ignores_non_numeric_text():
    stats = row_stats(["abc", "5"])
    assert stats["numeric"] == 1 and stats["max"] == 5.0


def test_write_full_csv_writes_labels_and_values(tmp_path):
    path = write_full_csv(sample_grid(), str(tmp_path), "ModelA 2.0",
                          "REV 01. Revenue Calc", "20260813T142530")
    text = Path(path).read_text(encoding="utf-8-sig")
    assert "Jan 26" in text and "Volume" in text and "100" in text
    assert Path(path).parent == tmp_path


def test_write_full_csv_filename_is_safe(tmp_path):
    path = write_full_csv(sample_grid(), str(tmp_path), "ModelA 2.0",
                          'Bad/Name:With*Chars', "20260813T142530")
    assert Path(path).exists()
    for ch in '/\\:*?"<>|':
        assert ch not in Path(path).name


def test_write_full_csv_handles_non_ascii_labels(tmp_path):
    """Live row coordinates include values like 'Financien' with a diaeresis."""
    grid = replace(sample_grid(), row_labels=[("Financi\u00ebn",)] * 4)
    path = write_full_csv(grid, str(tmp_path), "ModelA 2.0", "M", "20260813T142530")
    assert "Financi\u00ebn" in Path(path).read_text(encoding="utf-8-sig")


DIGEST_META = {"model_name": "ModelA 2.0", "object_name": "REV 01. Revenue Calc",
               "view_id": "102000000025", "workspace_label": "DEV",
               "engine": "Polaris"}


def test_build_digest_contains_shape_and_sample():
    digest = build_digest(sample_grid(), DIGEST_META, sample_n=3,
                          full_path="C:/scratch/x.csv")
    assert "REV 01. Revenue Calc" in digest
    assert "4 rows x 3 cols" in digest
    assert "Jan 26" in digest
    assert "Volume" in digest
    assert "Product=Widget A" in digest
    assert "C:/scratch/x.csv" in digest


def test_build_digest_reports_truncation_explicitly():
    """Never let a sampled digest read as if it showed everything."""
    digest = build_digest(sample_grid(), DIGEST_META, sample_n=2, full_path="x.csv")
    assert "2 of 4" in digest


def test_safe_print_survives_unencodable_console(monkeypatch):
    """On a cp1252 console, printing 'Financien' with a diaeresis raises
    UnicodeEncodeError - losing the result AFTER the data was already fetched."""
    def boom(*a, **k):
        raise UnicodeEncodeError("charmap", "x", 0, 1, "unmappable")
    monkeypatch.setattr("builtins.print", boom)
    safe_print("Financi\u00ebn")  # must not raise


def test_out_dir_is_required():
    """The tool must never pick a fallback location for client data."""
    parser = build_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["module", SHORTCUT, "REV 01. Revenue Calc"])


def test_parses_module_command_with_all_narrowing():
    args = build_arg_parser().parse_args([
        "module", SHORTCUT, "REV 01. Revenue Calc", "--out-dir", "/scratch",
        "--page", "Product:Widget A", "--line-items", "Volume,Price",
        "--periods", "Jan 26:Mar 26", "--sample", "5",
    ])
    assert args.command == "module"
    assert args.shortcut == SHORTCUT
    assert args.name == "REV 01. Revenue Calc"
    assert args.out_dir == "/scratch"
    assert args.page == "Product:Widget A"
    assert args.line_items == "Volume,Price"
    assert args.periods == "Jan 26:Mar 26"
    assert args.sample == 5


def test_parses_list_command():
    args = build_arg_parser().parse_args(
        ["list", "modelb", "Afdeling", "--out-dir", "/scratch"])
    assert args.command == "list" and args.name == "Afdeling"


def test_sample_defaults_to_ten():
    args = build_arg_parser().parse_args(
        ["module", SHORTCUT, "M", "--out-dir", "/scratch"])
    assert args.sample == 10


def test_check_grid_size_allows_small_grid():
    assert check_grid_size(sample_grid()) is None


def test_check_grid_size_refuses_oversized_and_names_page_dims():
    """Refuse rather than truncate: a silently biased slice is worse than an
    error, because the agent cannot tell it was truncated."""
    with pytest.raises(GridTooLargeError) as exc:
        check_grid_size(sample_grid(), max_cells=2)
    assert "Product" in str(exc.value) and "Region" in str(exc.value)
    assert "--page" in str(exc.value)


class RecordingSession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, timeout=180):
        self.calls.append(url)
        return self.payload


def test_fetch_module_always_sends_format_v1():
    """Without format=v1 the API returns 400 'Mandatory query parameter
    format is missing'."""
    sess = RecordingSession(load_fixture("view_data_sample.json"))
    fetch_module(sess, "https://api.anaplan.com", "M1", "102000000025",
                 load_fixture("view_meta_sample.json"), "")
    assert "format=v1" in sess.calls[0]


def test_fetch_module_appends_pages_after_format():
    sess = RecordingSession(load_fixture("view_data_sample.json"))
    fetch_module(sess, "https://api.anaplan.com", "M1", "102000000025",
                 load_fixture("view_meta_sample.json"), "101000000007:214000000002")
    assert "format=v1" in sess.calls[0]
    assert "pages=101000000007:214000000002" in sess.calls[0]


def test_fetch_list_items_reads_listItems_key():
    """The API returns `listItems`; reading `items` would yield an empty grid
    for every list and be reported as the legitimate EMPTY: state."""
    sess = RecordingSession({"listItems": [
        {"id": "1", "name": "Alpha", "code": "A", "parent": "Top"},
        {"id": "2", "name": "Beta", "code": None, "parent": None},
    ]})
    grid = fetch_list_items(sess, "https://api.anaplan.com", "M1", "101000000012")
    assert grid.n_rows == 2
    assert grid.row_labels == [("Alpha",), ("Beta",)]


# --- main()'s --out-dir repo guard -----------------------------------------
#
# Regression coverage for a review finding: the guard used to be
# `os.path.abspath(args.out_dir).startswith(os.path.abspath(REPO_ROOT))`,
# which is broken on Windows two ways - (1) abspath() does not normalize
# case, so a repo-inside path differing only in casing slipped past the
# guard entirely, and (2) a raw string prefix match incorrectly rejects a
# sibling directory that merely shares a prefix with the repo root. These
# tests drive the guard through main() itself (not a helper in isolation),
# so a future refactor that reorders the guard is caught, and assert on the
# real exit code (2) main() returns.

# Placeholder registry, flattened through the real registry.flatten() so its
# shape can never drift from what resolve_shortcut() actually consumes.
FAKE_CUSTOMERS_FOR_MAIN = {
    "customera": {
        "name": "CustomerA",
        "shard": "eu9z",
        "folder": "CustomerA",
        "customer_id": "C1",
        "models": {
            "modela": {"name": "ModelA", "raw_dir": "ModelA 2.0",
                       "workspace_id": "W1", "model_id": "M1"},
        },
    },
}

FAKE_MODELS_FOR_MAIN = registry.flatten(FAKE_CUSTOMERS_FOR_MAIN)
SHORTCUT = "customera:modela"


class _OpenSessionCalled(Exception):
    """Raised by a stubbed anaplan_session.open_session() to prove main()
    reached the session-open step for a given --out-dir - i.e. the repo-path
    guard did NOT reject it. Not a RuntimeError, so it propagates straight
    out of main() instead of being caught by the auth except clause."""


@pytest.fixture(autouse=True)
def _stub_session_for_guard_tests(request, monkeypatch):
    """Every out-dir-guard test in this module stubs open_session() and
    registry.MODELS UNCONDITIONALLY - including the tests that expect the
    guard to REJECT the path. If the guard under test is broken (e.g. a
    regression reintroducing the old raw startswith() comparison), a
    "rejects" case can silently fall through past the guard; without this
    stub that fallthrough would reach the real anaplan_session.open_session()
    and make a live authenticated call to Anaplan using whatever .env
    credentials happen to be present. Stubbing unconditionally means a broken
    guard fails the test loudly (wrong return value / unexpected exception)
    instead of ever reaching the network."""
    if "out_dir_guard" not in request.node.name:
        return
    monkeypatch.setattr(fetch_model_data.registry, "MODELS", FAKE_MODELS_FOR_MAIN)

    def boom():
        raise _OpenSessionCalled()

    monkeypatch.setattr(fetch_model_data.anaplan_session, "open_session", boom)


def test_out_dir_guard_rejects_path_inside_repo(capsys):
    out_dir = os.path.join(fetch_model_data.REPO_ROOT, "raw", "models")
    rc = main(["module", SHORTCUT, "X", "--out-dir", out_dir])
    assert rc == 2
    assert "inside the repository" in capsys.readouterr().err


def test_out_dir_guard_rejects_repo_root_itself(capsys):
    rc = main(["module", SHORTCUT, "X", "--out-dir", fetch_model_data.REPO_ROOT])
    assert rc == 2
    assert "inside the repository" in capsys.readouterr().err


def test_out_dir_guard_rejects_differently_cased_path_inside_repo(capsys):
    """The actual reported bug: os.path.abspath() does not normalize case on
    Windows, so a repo-inside path differing only in drive-letter/segment
    casing (routine with copy-pasted Windows/OneDrive paths) used to slip
    past a raw str.startswith(abspath) comparison. Client data would then be
    written into a OneDrive-synced repo - the exact failure the guard exists
    to prevent."""
    out_dir = os.path.join(fetch_model_data.REPO_ROOT, "raw", "models").upper()
    rc = main(["module", SHORTCUT, "X", "--out-dir", out_dir])
    assert rc == 2
    assert "inside the repository" in capsys.readouterr().err


def test_out_dir_guard_allows_sibling_directory_sharing_prefix():
    """A sibling directory like '...-backup' shares a string PREFIX with the
    repo root but is not inside it on a path-component boundary - must not
    be rejected."""
    sibling = fetch_model_data.REPO_ROOT + "-backup"
    with pytest.raises(_OpenSessionCalled):
        main(["module", SHORTCUT, "X", "--out-dir", sibling])


def test_out_dir_guard_allows_genuinely_outside_path(tmp_path):
    with pytest.raises(_OpenSessionCalled):
        main(["module", SHORTCUT, "X", "--out-dir", str(tmp_path)])


class TestEngineComesFromTheRegistry:
    """The engine label drives Classic-vs-Polaris formula reasoning
    downstream, so a wrong one is a correctness hazard, not a cosmetic bug. It
    used to come from a folder-name -> engine dict hardcoded in this tracked
    file, which was one customer's layout and silently wrong for every other
    customer."""

    TREE = {
        "customera": {
            "name": "CustomerA", "shard": "eu9z", "folder": "CustomerA",
            "customer_id": "CUST-A",
            "models": {
                "polaris": {"name": "P", "raw_dir": "P", "workspace_id": "W",
                            "model_id": "M1", "engine": "Polaris",
                            "workspace_label": "DEV"},
                "classic": {"name": "C", "raw_dir": "C", "workspace_id": "W",
                            "model_id": "M2", "engine": "Classic"},
                "silent": {"name": "S", "raw_dir": "S", "workspace_id": "W",
                           "model_id": "M3"},
            },
        },
    }

    def _resolve(self, key):
        import registry
        return registry.resolve(key, registry.flatten(self.TREE))

    def test_engine_is_read_from_the_entry(self):
        assert self._resolve("customera:polaris").engine == "Polaris"
        assert self._resolve("customera:classic").engine == "Classic"

    def test_unmarked_model_reports_unknown_not_a_guessed_engine(self):
        assert self._resolve("customera:silent").engine == "unknown"

    def test_workspace_label_is_read_from_the_entry(self):
        assert self._resolve("customera:polaris").workspace_label == "DEV"

    def test_workspace_label_defaults_to_production(self):
        assert self._resolve("customera:classic").workspace_label == "PRODUCTION"

    def test_the_hardcoded_dicts_are_gone(self):
        """Guard against reintroduction. Either constant coming back means one
        customer's layout is back in a tracked public file."""
        import fetch_model_data
        assert not hasattr(fetch_model_data, "_ENGINE_BY_RAW_DIR")
        assert not hasattr(fetch_model_data, "_DEV_SHORTCUTS")
