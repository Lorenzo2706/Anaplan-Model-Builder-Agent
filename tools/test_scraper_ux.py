"""Tests for scraper_ux's model-metadata transport.

The /2/0 metadata calls (views, modules, line items, actions) must go over the
token-authenticated Integration API on the customer's own API host, never
through the browser session on the app shard: that transport died around
2026-08-07 (401 on eu2a, 503 on eu3 - observed live on an eu3 tenant 2026-10-15).
"""
import pytest

import registry
import scraper_ux


FAKE_CUSTOMERS = {
    "eucust": {"name": "EU Cust", "shard": "eu3", "api_region": "eu3",
               "folder": "EU Cust", "customer_id": "c" * 32,
               "models": {"m": {"name": "M", "raw_dir": "M",
                                "workspace_id": "w" * 32,
                                "model_id": "AAAA1111"}}},
    "glob": {"name": "Glob", "shard": "eu2a", "folder": "Glob",
             "customer_id": "d" * 32,
             "models": {"m": {"name": "M", "raw_dir": "M",
                              "workspace_id": "x" * 32,
                              "model_id": "BBBB2222"}}},
}


@pytest.fixture
def fake_registry(monkeypatch):
    monkeypatch.setattr(registry, "CUSTOMERS", FAKE_CUSTOMERS)
    monkeypatch.setattr(registry, "MODELS", registry.flatten(FAKE_CUSTOMERS))


def test_rest_hosts_use_customer_api_region(fake_registry):
    assert scraper_ux._rest_hosts("eucust", "AAAA1111") == (
        "https://eu3.api.anaplan.com",
        "https://eu3.auth.anaplan.com/token/authenticate",
    )


def test_rest_hosts_default_to_global_pair(fake_registry):
    assert scraper_ux._rest_hosts("glob", "BBBB2222") == (
        registry.GLOBAL_API_BASE, registry.GLOBAL_AUTH_URL,
    )


def test_rest_hosts_for_model_browsed_outside_registry(fake_registry):
    # A model picked via "Browse all models" has no registry entry; it still
    # inherits its customer's realm rather than falling back to global.
    assert scraper_ux._rest_hosts("eucust", "NOTINREG")[0] == \
        "https://eu3.api.anaplan.com"


class _FakeResponse:
    def __init__(self, body):
        self.status_code = 200
        self.headers = {"Content-Type": "application/json"}
        self._body = body
        self.text = ""

    def json(self):
        return self._body


class _FakeSession:
    """Stands in for scrape_model_data._api_session(); records every GET."""
    BODIES = {
        "views": {"views": [{"name": "V", "id": "1", "moduleId": "10"}]},
        "modules": {"modules": [{"name": "Mod", "id": "10"}]},
        "lineItems": {"items": [{"name": "LI", "id": "100", "moduleId": "10"}]},
        "processes": {"processes": [{"name": "P", "id": "118"}]},
        "imports": {"imports": []},
        "exports": {"exports": []},
        "actions": {"actions": []},
    }

    def __init__(self):
        self.urls = []

    def get(self, url, timeout=None):
        self.urls.append(url)
        return _FakeResponse(self.BODIES[url.rsplit("/", 1)[1]])


def test_metadata_goes_to_api_host_not_browser():
    sess = _FakeSession()
    meta = scraper_ux._fetch_model_metadata(
        sess, "https://eu3.api.anaplan.com", "AAAA1111")

    assert sess.urls, "no metadata call went through the token session"
    assert all(u.startswith("https://eu3.api.anaplan.com/2/0/models/AAAA1111/")
               for u in sess.urls), sess.urls
    assert meta["views"] == [{"name": "V", "id": "1", "moduleId": "10"}]
    assert meta["modules"] == [{"name": "Mod", "id": "10"}]
    assert meta["line_items"] == [{"name": "LI", "id": "100", "moduleId": "10"}]
    assert meta["actions"]["processes"] == [{"name": "P", "id": "118"}]


def test_sds_is_served_on_the_customers_own_app_shard():
    # The springboard-definition-service (NUX pages/boards) was hardcoded to
    # us1a, which 401s an eu3 browser session (an eu3 tenant, 2026-10-15).
    assert scraper_ux._sds_base("https://eu3.app.anaplan.com/") == \
        "https://eu3.app.anaplan.com/a/springboard-definition-service"


# ── Board payload shapes ─────────────────────────────────────────────────────
# Synthetic ids/names, shaped like the SDS /boards/<guid> payload observed live
# on 2026-10-15: `rows` is empty and `widgets` is a dict keyed by widget guid
# whose values ARE the widget definitions (no "widgetDefinition" wrapper).

MOD_A, MOD_B, MOD_C, MOD_D = "102000000001", "102000000002", "102000000003", "102000000004"
LI_A1, LI_A2, LI_B1, LI_C1, LI_D1 = ("385000000001", "385000000002",
                                     "385000000003", "385000000004", "385000000005")

LINE_ITEMS_BY_MODULE = {
    MOD_A: [{"id": LI_A1, "name": "A one"}, {"id": LI_A2, "name": "A two"}],
    MOD_B: [{"id": LI_B1, "name": "B one"}],
    MOD_C: [{"id": LI_C1, "name": "C one"}],
    MOD_D: [{"id": LI_D1, "name": "D one"}],
}


def _grid(guid, module_id, shows):
    return {
        "type": "TABLE", "widgetGuid": guid, "dataSourceId": "g-" + guid,
        "widgetActions": [],
        "widgetDataSources": [{
            "widgetGuid": guid, "dataSourceId": "g-" + guid, "subEntityId": "",
            "dataSourceType": "MULTI_AXIS_DESCRIPTION",
            "axisDescriptionQuery": {"regions": {"SINGLE": {
                "moduleId": module_id,
                "rows": {"dimensions": [{"id": "20000000012", "shows": shows}],
                         "filters": {"rootNode": {"type": "BRANCH", "operator": "AND",
                                                  "nodes": [{"type": "LEAF", "rule": {
                                                      "selectedItems": [shows[0]]}}]}}},
                "columns": {"dimensions": []},
            }}},
        }],
    }


NEW_SHAPE_BOARD = {
    "pageGuid": "p1", "rows": [],
    "widgets": {
        "w-text": {"type": "TEXT", "widgetActions": [], "widgetDataSources": []},
        "w-grid": _grid("w-grid", MOD_A, [LI_A2]),
        "w-field": {"type": "FIELD", "widgetActions": [], "widgetDataSources": [],
                    "fields": [{"moduleId": MOD_B, "lineItemId": LI_B1, "label": "x"}]},
        "w-card": {"type": "CARD", "widgetActions": [], "dataSourceId": MOD_C,
                   "widgetDataSources": [{"dataSourceId": MOD_C, "subEntityId": LI_C1,
                                          "dataSourceType": "LINE_ITEM",
                                          "axisDescriptionQuery": None}]},
        "w-action": {"type": "ACTION", "widgetActions": [], "widgetDataSources": [],
                     "actions": '[{"id":"118000000001","name":"P","type":"PROCESS"}]',
                     "actionButtons": [{"id": "118000000001", "type": "PROCESS"}]},
    },
}

LEGACY_SHAPE_BOARD = {
    "rows": [{"columns": [{"widgets": [{"widgetDefinition": _grid("w-old", MOD_D, [LI_D1])}]}]}],
}


def _index():
    return scraper_ux._module_line_item_index(LINE_ITEMS_BY_MODULE)


def test_page_widget_defs_reads_guid_keyed_unwrapped_widgets():
    types = [w["type"] for w in scraper_ux._page_widget_defs(NEW_SHAPE_BOARD)]
    assert sorted(types) == ["ACTION", "CARD", "FIELD", "TABLE", "TEXT"]


def test_page_widget_defs_still_reads_legacy_rows_with_wrapper():
    defs = scraper_ux._page_widget_defs(LEGACY_SHAPE_BOARD)
    assert [w["widgetGuid"] for w in defs] == ["w-old"]


def test_page_action_ids_from_new_shape_action_widget():
    assert scraper_ux._page_action_ids(NEW_SHAPE_BOARD, "BOARD") == {"118000000001"}


def test_page_module_ids_cover_grid_field_and_card():
    mod_ids, mod_id2name = _index()
    assert scraper_ux._page_module_ids(NEW_SHAPE_BOARD, mod_ids, mod_id2name) == \
        [MOD_A, MOD_B, MOD_C]


def test_page_view_ids_fall_back_to_widget_modules_when_page_data_sources_empty():
    views = {m: {"name": "View " + m, "module": m} for m in (MOD_A, MOD_B, MOD_C, MOD_D)}
    mod_ids, mod_id2name = _index()
    page_data = {"pageDataSources": []}
    assert scraper_ux._page_view_ids(page_data, NEW_SHAPE_BOARD, views,
                                     mod_ids, mod_id2name) == [MOD_A, MOD_B, MOD_C]


def test_page_view_ids_do_not_double_count_a_module_already_in_page_data_sources():
    views = {MOD_A: {"name": "A", "module": MOD_A},
             "999": {"name": "A saved view", "module": MOD_A},
             MOD_B: {"name": "B", "module": MOD_B},
             MOD_C: {"name": "C", "module": MOD_C}}
    mod_ids, mod_id2name = _index()
    page_data = {"pageDataSources": [{"dataSourceId": "999"}]}
    assert scraper_ux._page_view_ids(page_data, NEW_SHAPE_BOARD, views,
                                     mod_ids, mod_id2name) == ["999", MOD_B, MOD_C]


def _page(content):
    return {"name": "Page", "guid": "p1", "app_name": "App", "app_guid": "a1",
            "page_url": "u", "content": content}


def test_line_items_sheet_shows_only_displayed_line_items_on_new_shape():
    views = {m: {"name": "View " + m, "module": m} for m in (MOD_A, MOD_B, MOD_C)}
    modules = {m: {"name": "Mod " + m} for m in (MOD_A, MOD_B, MOD_C)}
    table = scraper_ux._build_views_line_items_table(
        [_page(NEW_SHAPE_BOARD)], views, modules, LINE_ITEMS_BY_MODULE, "m", [])
    got = {(r[5], r[8], r[9]) for r in table[1:]}
    assert got == {(MOD_A, "Grid", "A two"), (MOD_B, "Field", "B one"),
                   (MOD_C, "KPI", "C one")}


def test_ui_filters_sheet_reads_new_shape_grids():
    modules = {MOD_A: {"name": "Mod A"}}
    names = {LI_A1: "A one", LI_A2: "A two"}
    table = scraper_ux._build_ui_filters_table([_page(NEW_SHAPE_BOARD)], modules, names)
    assert table[1:] == [["Page", "Mod A", "", False, "A two", True]]


# The Actions-detail sheet. The Modeling UI has no Export button on the
# Imports grid, so its Source/Target columns come from the classic
# core-webapp export of that grid (CSV text, first header cell blank, CRLF
# rows - as the servlet returned it live on an eu3 tenant 2026-10-15) and are
# merged onto the REST action list, which still supplies every non-import row.
IMPORTS_GRID_CSV = (
    ",Source Label,Source Object,Source Type,Target Object,Target Type,Production Data\r\n"
    "Load Mod X,Other Model / 'SRC'.'SV 1',Other Model / 'SRC'.'SV 1 full',SAVED VIEW,Mod X,MODULE,false\r\n"
    "Load List Y,y.csv,y.csv,FILE,List Y,LIST,true\r\n"
)

REST_ACTIONS = [
    {"__atype": "imports", "name": "Load Mod X", "importType": "MODULE_DATA",
     "importDataSourceId": ""},
    {"__atype": "imports", "name": "Load List Y", "importType": "HIERARCHY_DATA",
     "importDataSourceId": "113000000001"},
    {"__atype": "exports", "name": "Export Z"},
    {"__atype": "processes", "name": "Run all"},
]


def test_actions_detail_fills_import_rows_from_imports_grid():
    table = scraper_ux._build_actions_detail(REST_ACTIONS, IMPORTS_GRID_CSV)
    rows = {r[0]: r for r in table[1:]}
    assert rows["Load Mod X"] == [
        "Load Mod X", "imports", "Other Model / 'SRC'.'SV 1'",
        "Other Model / 'SRC'.'SV 1 full'", "SAVED VIEW", "Mod X", "MODULE", "false"]
    assert rows["Load List Y"] == [
        "Load List Y", "imports", "y.csv", "y.csv", "FILE", "List Y", "LIST", "true"]


def test_actions_detail_keeps_non_import_rows_from_rest():
    table = scraper_ux._build_actions_detail(REST_ACTIONS, IMPORTS_GRID_CSV)
    assert table[0] == scraper_ux._build_actions_detail_fallback([])[0]
    assert [r[0] for r in table[1:]] == ["Load Mod X", "Load List Y", "Export Z", "Run all"]
    rows = {r[0]: r for r in table[1:]}
    assert rows["Export Z"] == ["Export Z", "exports", "", "", "SAVED VIEW", "", "FILE", ""]
    assert rows["Run all"] == ["Run all", "processes", "", "", "", "", "", ""]


def test_actions_detail_without_grid_is_the_rest_fallback():
    assert (scraper_ux._build_actions_detail(REST_ACTIONS, None)
            == scraper_ux._build_actions_detail_fallback(REST_ACTIONS))
