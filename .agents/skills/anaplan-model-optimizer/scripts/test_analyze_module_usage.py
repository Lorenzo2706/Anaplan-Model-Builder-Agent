import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from analyze_module_usage import detect_manual_marker


def test_detect_manual_marker_no_signal():
    result = detect_manual_marker("Some normal note about formatting.", "CALCULATION MODULES")
    assert result == {"flagged": False, "reasons": []}


def test_detect_manual_marker_notes_keyword():
    result = detect_manual_marker("To be deleted after Q4 close.", "")
    assert result["flagged"] is True
    assert any("delete" in r.lower() for r in result["reasons"])


def test_detect_manual_marker_notes_keyword_obsolete():
    result = detect_manual_marker("This module is obsolete, replaced by CA26.", "")
    assert result["flagged"] is True
    assert any("obsolete" in r.lower() for r in result["reasons"])


def test_detect_manual_marker_functional_area():
    result = detect_manual_marker("", "DELETE")
    assert result["flagged"] is True
    assert any("Functional Area" in r for r in result["reasons"])


def test_detect_manual_marker_both_sources():
    result = detect_manual_marker("Deprecated - remove in next cleanup.", "DELETE")
    assert result["flagged"] is True
    assert len(result["reasons"]) == 2


def test_detect_manual_marker_case_insensitive():
    result = detect_manual_marker("DELETE THIS", "delete")
    assert result["flagged"] is True


def test_detect_manual_marker_empty_inputs():
    result = detect_manual_marker(None, None)
    assert result == {"flagged": False, "reasons": []}


import csv as csv_module

from analyze_module_usage import load_modules_csv, analyze, to_markdown_modules


def _write_csv(path: Path, header: str, rows: list, delimiter: str = ","):
    path.write_text(header + "\n" + "\n".join(rows), encoding="utf-8-sig")


def _write_modules_csv(tmp_path: Path) -> Path:
    model_dir = tmp_path / "TestModel"
    model_dir.mkdir()
    header = ",Functional Area,Applies To,Time Scale,Time Range,Versions,Breakback,Users List,Cell Count,Populated Cell Count,Memory Used,Notes,Read Access Driver,Write Access Driver,Data Tags,Managed By,Referenced By,Used in Dashboards,Line Items"
    rows = [
        "CA01 Candidate,CALCULATION MODULES,,,,,,,,,,,,,,,,,",
        "CA02 Marked Candidate,CALCULATION MODULES,,,,,,,,,,To be deleted next release,,,,,,,",
        "IN01 Kept Referenced,INPUT MODULES,,,,,,,,,,Deprecated - kept for now,,,,,'CA03 Kept'.some line,,",
        "OU01 Active,OUTPUT MODULES,,,,,,,,,,,,,,,,,",
    ]
    _write_csv(model_dir / "Modules.csv", header, rows)
    (model_dir / "Imports.csv").write_text(";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data\n", encoding="utf-8-sig")
    return model_dir


def _write_workbook(path: Path, modules_usage_rows: list, extra_sheets: dict = None):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Modules Usage Count"
    ws.append(["Module", "Module ID", "Usage Count"])
    for row in modules_usage_rows:
        ws.append(row)
    for name, rows in (extra_sheets or {}).items():
        sheet = wb.create_sheet(name)
        for row in rows:
            sheet.append(row)
    wb.save(path)


def test_load_modules_csv_captures_notes_and_marker(tmp_path):
    model_dir = _write_modules_csv(tmp_path)
    modules = load_modules_csv(model_dir)
    assert modules["CA02 Marked Candidate"]["notes"] == "To be deleted next release"
    assert modules["CA02 Marked Candidate"]["manual_marker"]["flagged"] is True
    assert modules["CA01 Candidate"]["manual_marker"]["flagged"] is False


def test_analyze_attaches_marker_and_flagged_but_kept(tmp_path):
    model_dir = _write_modules_csv(tmp_path)
    excel_path = tmp_path / "report.xlsx"
    _write_workbook(excel_path, [
        ["CA01 Candidate", "1", 0],
        ["CA02 Marked Candidate", "2", 0],
        ["IN01 Kept Referenced", "3", 0],
        ["OU01 Active", "4", 5],
    ])

    report, _line_item_exposure = analyze(excel_path, model_dir)
    by_name = {e["name"]: e for e in report["modules"]}

    assert by_name["OU01 Active"]["verdict"].startswith("ACTIVE")
    assert by_name["IN01 Kept Referenced"]["verdict"].startswith("KEEP")
    assert by_name["CA01 Candidate"]["verdict"].startswith("CANDIDATE")
    assert by_name["CA02 Marked Candidate"]["verdict"].startswith("CANDIDATE")

    # Marked candidate should sort before the unmarked candidate.
    candidate_names = [e["name"] for e in report["modules"] if e["verdict"].startswith("CANDIDATE")]
    assert candidate_names.index("CA02 Marked Candidate") < candidate_names.index("CA01 Candidate")

    # IN01 has a marker (Notes says "Deprecated") but was computed KEEP - contradiction case.
    assert by_name["IN01 Kept Referenced"]["flagged_but_kept"] is True
    assert by_name["CA02 Marked Candidate"]["flagged_but_kept"] is False  # it's a candidate, not a contradiction
    assert report["summary"]["flagged_but_kept"] == 1


def test_to_markdown_modules_renders_flagged_but_kept_section(tmp_path):
    model_dir = _write_modules_csv(tmp_path)
    excel_path = tmp_path / "report.xlsx"
    _write_workbook(excel_path, [
        ["CA01 Candidate", "1", 0],
        ["CA02 Marked Candidate", "2", 0],
        ["IN01 Kept Referenced", "3", 0],
        ["OU01 Active", "4", 5],
    ])
    report, _line_item_exposure = analyze(excel_path, model_dir)
    md = to_markdown_modules(report, "TestModel")
    assert "## Modules flagged for deletion but still active or kept" in md
    assert "IN01 Kept Referenced" in md.split("## Modules flagged for deletion but still active or kept")[1]


from analyze_module_usage import (
    load_line_items_csv,
    _parse_dotted_reference,
    load_import_line_item_matches,
)


def _write_line_items_csv(tmp_path: Path) -> Path:
    model_dir = tmp_path / "LiModel"
    model_dir.mkdir()
    header = ",Format,Formula,Summary,Applies To,Time Scale,Time Range,Versions,Style,Cell Count,Populated Cell Count,Memory Used,Calculation Complexity,Calculation Effort,Notes,Read Access Driver,Write Access Driver,Users List,Parent,Is Summary,Formula Scope,Code,Use Switchover,Breakback,Start of Section,Data Tags,Referenced By,Module Name"
    rows = [
        "Line A,,,,,,,,,,,,,,,,,,,,,,,,,,,CA01 Candidate",
        "Line B,,,,,,,,,,,,,,Remove this line item,,,,,,,,,,,,,CA01 Candidate",
        "Line C,,,,,,,,,,,,,,,,,,,,,,,,,,'Line A',IN01 Kept Referenced",
    ]
    _write_csv(model_dir / "Line Items.csv", header, rows)
    return model_dir


def test_load_line_items_csv(tmp_path):
    model_dir = _write_line_items_csv(tmp_path)
    items = load_line_items_csv(model_dir)
    assert items[("CA01 Candidate", "Line A")]["referenced_by"] == []
    assert items[("CA01 Candidate", "Line B")]["notes"] == "Remove this line item"
    assert items[("IN01 Kept Referenced", "Line C")]["referenced_by"] == ["Line A"]


@pytest.mark.parametrize("obj,expected", [
    ("Data Hub 2.0 / 'SYS 05. Time Settings'.Current Period", ("SYS 05. Time Settings", "Current Period")),
    ("'CA01 Candidate'.Line A", ("CA01 Candidate", "Line A")),
    ("SM 02. General Settings", None),  # whole-module target, no line item
    ("", None),
])
def test_parse_dotted_reference(obj, expected):
    assert _parse_dotted_reference(obj) == expected


def test_load_import_line_item_matches(tmp_path):
    model_dir = tmp_path / "ImportModel"
    model_dir.mkdir()
    header = ";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data"
    rows = [
        "Import A;Feed;'CA01 Candidate'.Line A;SAVED VIEW;SM 02. General Settings;MODULE;FALSE",
        "Import B;External File;FILE;IMPORT;'IN01 Kept Referenced'.Line C;MODULE;FALSE",
    ]
    (model_dir / "Imports.csv").write_text(header + "\n" + "\n".join(rows), encoding="utf-8-sig")

    known_pairs = {("CA01 Candidate", "Line A"), ("IN01 Kept Referenced", "Line C"), ("CA01 Candidate", "Line B")}
    matched = load_import_line_item_matches(model_dir, known_pairs)
    assert matched == {("CA01 Candidate", "Line A"), ("IN01 Kept Referenced", "Line C")}


from analyze_module_usage import load_excel, FIXED_SHEETS


def test_load_excel_reads_line_item_exposure_sheets(tmp_path):
    excel_path = tmp_path / "report.xlsx"
    _write_workbook(excel_path, [["OU01 Active", "1", 5]], extra_sheets={
        "Views Usage Report - Line Items": [
            ["Module/View name", "App name", "Page name", "View URL", "Page URL",
             "Module/View ID", "App ID", "Page ID", "UX Type", "Line Item"],
            ["OU01 Active", "App", "Page", "url", "url", "1", "a", "p", "GRID", "Revenue"],
            ["OU01 Active", "App", "Page", "url", "url", "1", "a", "p", "GRID", ""],
        ],
        "UI Filters": [
            ["Page", "Module", "Filter Column", "Value Filter Column", "Filter Rows", "Value Filter Rows"],
            ["Page", "OU01 Active", "Cost Center; Region", True, "", False],
        ],
        "Actions TestModel": [
            ["Source Label", "Source Object", "Source Type", "Target Object", "Target Type"],
        ],
    })

    ux_counts, action_usage, line_item_exposure = load_excel(excel_path)

    assert ("OU01 Active", "Revenue") in line_item_exposure
    assert ("OU01 Active", "Cost Center") in line_item_exposure
    assert ("OU01 Active", "Region") in line_item_exposure
    # Blank Line Item cell must not add a bogus ("OU01 Active", "") entry.
    assert ("OU01 Active", "") not in line_item_exposure


def test_fixed_sheets_includes_new_sheets():
    assert "Views Usage Report - Line Items" in FIXED_SHEETS
    assert "UI Filters" in FIXED_SHEETS


from analyze_module_usage import analyze_line_items, LI_CANDIDATE_VERDICT


def _fake_module_results():
    return [
        {"name": "CA01 Candidate", "functional_area": "CALCULATION MODULES", "verdict": "CANDIDATE FOR REVIEW - no NUX usage, no formula reference, no dashboard usage, no action usage found"},
        {"name": "IN01 Kept Referenced", "functional_area": "INPUT MODULES", "verdict": "KEEP - feeds other modules via formula"},
        {"name": "OU01 Active", "functional_area": "OUTPUT MODULES", "verdict": "ACTIVE - used in NUX pages/boards"},
    ]


def test_analyze_line_items_scoping_and_verdicts(tmp_path):
    model_dir = tmp_path / "LiScopeModel"
    model_dir.mkdir()
    header = ",Format,Formula,Summary,Applies To,Time Scale,Time Range,Versions,Style,Cell Count,Populated Cell Count,Memory Used,Calculation Complexity,Calculation Effort,Notes,Read Access Driver,Write Access Driver,Users List,Parent,Is Summary,Formula Scope,Code,Use Switchover,Breakback,Start of Section,Data Tags,Referenced By,Module Name"
    rows = [
        # In-scope module (OU01 Active is ACTIVE): one exposed, one candidate, one marked candidate.
        "Revenue,,,,,,,,,,,,,,,,,,,,,,,,,,,OU01 Active",
        "Unused Aux,,,,,,,,,,,,,,,,,,,,,,,,,,,OU01 Active",
        "Legacy Aux,,,,,,,,,,,,,,To be deleted,,,,,,,,,,,,,OU01 Active",
        # In-scope module (IN01 Kept Referenced is KEEP): one referenced-by, one imported.
        "Referenced Line,,,,,,,,,,,,,,,,,,,,,,,,,,'Revenue',IN01 Kept Referenced",
        "Imported Line,,,,,,,,,,,,,,,,,,,,,,,,,,,IN01 Kept Referenced",
        # Out-of-scope module (CA01 Candidate is CANDIDATE at module level) - must be excluded entirely.
        "Skipped Line,,,,,,,,,,,,,,,,,,,,,,,,,,,CA01 Candidate",
    ]
    _write_csv(model_dir / "Line Items.csv", header, rows)
    (model_dir / "Imports.csv").write_text(
        ";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data\n"
        "Import C;Feed;'IN01 Kept Referenced'.Imported Line;SAVED VIEW;SM 02;MODULE;FALSE\n",
        encoding="utf-8-sig",
    )

    line_item_exposure = {("OU01 Active", "Revenue")}
    li_report = analyze_line_items(model_dir, _fake_module_results(), line_item_exposure)

    by_key = {(e["module"], e["line_item"]): e for e in li_report["line_items"]}

    assert ("CA01 Candidate", "Skipped Line") not in by_key  # module was a Pass-1 candidate - excluded

    assert by_key[("OU01 Active", "Revenue")]["verdict"].startswith("ACTIVE")
    assert by_key[("OU01 Active", "Unused Aux")]["verdict"] == LI_CANDIDATE_VERDICT
    assert by_key[("OU01 Active", "Legacy Aux")]["verdict"] == LI_CANDIDATE_VERDICT
    assert by_key[("OU01 Active", "Legacy Aux")]["manual_marker"]["flagged"] is True

    assert by_key[("IN01 Kept Referenced", "Referenced Line")]["verdict"].startswith("KEEP - feeds")
    assert by_key[("IN01 Kept Referenced", "Imported Line")]["verdict"].startswith("KEEP - used as an import")

    # Marked candidate sorts before the unmarked candidate within the same module.
    ou01_candidates = li_report["by_module"]["OU01 Active"]["candidates"]
    names = [e["line_item"] for e in ou01_candidates]
    assert names.index("Legacy Aux") < names.index("Unused Aux")

    assert li_report["summary"]["candidates_for_review"] == 2
    assert li_report["summary"]["modules_with_candidates"] == 1


def test_analyze_line_items_inherits_module_delete_functional_area(tmp_path):
    model_dir = tmp_path / "LiInheritModel"
    model_dir.mkdir()
    header = ",Format,Formula,Summary,Applies To,Time Scale,Time Range,Versions,Style,Cell Count,Populated Cell Count,Memory Used,Calculation Complexity,Calculation Effort,Notes,Read Access Driver,Write Access Driver,Users List,Parent,Is Summary,Formula Scope,Code,Use Switchover,Breakback,Start of Section,Data Tags,Referenced By,Module Name"
    # "Some Line" is itself referenced by another line item, so its own
    # verdict resolves to KEEP (not the candidate verdict) - this is what
    # lets the inherited module-level DELETE marker register as a genuine
    # flagged-but-kept contradiction rather than being suppressed by the
    # "never true for a CANDIDATE verdict" rule.
    rows = ["Some Line,,,,,,,,,,,,,,,,,,,,,,,,,,'Formula Consumer',DL01 Tagged Delete"]
    _write_csv(model_dir / "Line Items.csv", header, rows)
    (model_dir / "Imports.csv").write_text(";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data\n", encoding="utf-8-sig")

    module_results = [
        {"name": "DL01 Tagged Delete", "functional_area": "DELETE", "verdict": "KEEP - feeds other modules via formula"},
    ]
    li_report = analyze_line_items(model_dir, module_results, set())

    entry = li_report["line_items"][0]
    assert entry["inherited_module_delete_flag"] is True
    assert entry["flagged_but_kept"] is True  # KEEP verdict + inherited DELETE marker = contradiction
    assert li_report["summary"]["flagged_but_kept"] == 1


from analyze_module_usage import to_markdown_line_items


def test_to_markdown_line_items_renders_candidates_and_flagged_but_kept():
    li_report = {
        "summary": {"total_line_items_checked": 3, "candidates_for_review": 1, "modules_with_candidates": 1, "flagged_but_kept": 1, "unresolved_view_names": 0},
        "unresolved_view_names": [],
        "by_module": {
            "OU01 Active": {
                "functional_area": "OUTPUT MODULES",
                "candidates": [{
                    "module": "OU01 Active", "line_item": "Legacy Aux", "functional_area": "OUTPUT MODULES",
                    "verdict": LI_CANDIDATE_VERDICT, "referenced_by": [],
                    "manual_marker": {"flagged": True, "reasons": ["Notes: 'delete'"]},
                    "inherited_module_delete_flag": False, "flagged_but_kept": False,
                }],
                "flagged_but_kept": [{
                    "module": "OU01 Active", "line_item": "Weird Kept", "functional_area": "OUTPUT MODULES",
                    "verdict": "KEEP - feeds other line items via formula", "referenced_by": ["x"],
                    "manual_marker": {"flagged": False, "reasons": []},
                    "inherited_module_delete_flag": True, "flagged_but_kept": True,
                }],
                "total": 3,
            },
        },
    }
    md = to_markdown_line_items(li_report)
    assert "## Line item candidates for review" in md
    assert "Legacy Aux" in md
    assert "## Line items flagged for deletion but still active or kept" in md
    assert "Weird Kept" in md
    assert "inherited module Functional Area=DELETE" in md


def test_to_markdown_line_items_handles_no_candidates():
    li_report = {
        "summary": {"total_line_items_checked": 1, "candidates_for_review": 0, "modules_with_candidates": 0, "flagged_but_kept": 0, "unresolved_view_names": 0},
        "unresolved_view_names": [],
        "by_module": {"OU01 Active": {"functional_area": "OUTPUT MODULES", "candidates": [], "flagged_but_kept": [], "total": 1}},
    }
    md = to_markdown_line_items(li_report)
    assert "None found." in md
    assert "Data quality: unresolved view/module names" not in md


def test_analyze_line_items_no_unresolved_view_names_when_all_match(tmp_path):
    """line_item_exposure only references module names that exist in
    module_results - unresolved_view_names must be empty and the markdown
    data-quality section must not render."""
    model_dir = tmp_path / "LiResolvedModel"
    model_dir.mkdir()
    header = ",Format,Formula,Summary,Applies To,Time Scale,Time Range,Versions,Style,Cell Count,Populated Cell Count,Memory Used,Calculation Complexity,Calculation Effort,Notes,Read Access Driver,Write Access Driver,Users List,Parent,Is Summary,Formula Scope,Code,Use Switchover,Breakback,Start of Section,Data Tags,Referenced By,Module Name"
    rows = ["Revenue,,,,,,,,,,,,,,,,,,,,,,,,,,,OU01 Active"]
    _write_csv(model_dir / "Line Items.csv", header, rows)
    (model_dir / "Imports.csv").write_text(
        ";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data\n",
        encoding="utf-8-sig",
    )

    line_item_exposure = {("OU01 Active", "Revenue")}
    li_report = analyze_line_items(model_dir, _fake_module_results(), line_item_exposure)

    assert li_report["unresolved_view_names"] == []
    assert li_report["summary"]["unresolved_view_names"] == 0

    md = to_markdown_line_items(li_report)
    assert "Data quality: unresolved view/module names" not in md


def test_analyze_line_items_flags_unresolved_view_names(tmp_path):
    """line_item_exposure references a Module/View name absent from
    module_results (e.g. a view renamed since the last scrape) -
    unresolved_view_names must capture it, and the markdown data-quality
    section must render with that name as a bullet."""
    model_dir = tmp_path / "LiUnresolvedModel"
    model_dir.mkdir()
    header = ",Format,Formula,Summary,Applies To,Time Scale,Time Range,Versions,Style,Cell Count,Populated Cell Count,Memory Used,Calculation Complexity,Calculation Effort,Notes,Read Access Driver,Write Access Driver,Users List,Parent,Is Summary,Formula Scope,Code,Use Switchover,Breakback,Start of Section,Data Tags,Referenced By,Module Name"
    rows = ["Revenue,,,,,,,,,,,,,,,,,,,,,,,,,,,OU01 Active"]
    _write_csv(model_dir / "Line Items.csv", header, rows)
    (model_dir / "Imports.csv").write_text(
        ";Source Label;Source Object;Source Type;Target Object;Target Type;Production Data\n",
        encoding="utf-8-sig",
    )

    # "OU01 Renamed View" does not match any name in _fake_module_results().
    line_item_exposure = {("OU01 Active", "Revenue"), ("OU01 Renamed View", "Some Line")}
    li_report = analyze_line_items(model_dir, _fake_module_results(), line_item_exposure)

    assert li_report["unresolved_view_names"] == ["OU01 Renamed View"]
    assert li_report["summary"]["unresolved_view_names"] == 1

    md = to_markdown_line_items(li_report)
    assert "## Data quality: unresolved view/module names" in md
    assert "- OU01 Renamed View" in md
