"""Offline tests for scrape_model_data's pure seams.

None of these touch Anaplan, a browser, or the developer's real .env: every
test here exercises string/dict logic only. That is deliberate — the failure
mode this module guards against is a *silent wrong-tenant export* (one
customer's model scraped against another customer's shard, or into another
customer's folder), which is cheap to assert here and expensive to notice
live.
"""
import json
import os

import pytest

import registry
import scrape_model_data as smd

# TestAppUrlForShard, TestResolveModel, TestSettingsUrl and TestOutDir used to
# live here. app_url_for_shard, _resolve_model, settings_url, default_out_dir
# and resolve_out_dir all moved into registry.py, and test_registry.py now
# covers them against a placeholder CUSTOMERS tree. What remains here is only
# what is genuinely scrape_model_data's own: the CLI, the core-webapp origin
# validator, and the export seams.

# Placeholder registry tree. The real one is gitignored and differs per
# machine, so a test that read it would pass or fail depending on whose clone
# ran it. `eu9z` is a deliberately unassigned-looking shard token.
FAKE_CUSTOMERS = {
    "customera": {
        "name": "CustomerA",
        "shard": "eu9z",
        "folder": "CustomerA",
        "customer_id": "C1",
        "models": {
            "modela": {
                "name": "ModelA",
                # Shortcut key and raw_dir deliberately differ: a shortcut is
                # an abbreviation the modeller types, raw_dir is the vault
                # folder name, and the two drift the moment a model is renamed.
                "raw_dir": "ModelA 2.0",
                "workspace_id": "W1",
                "model_id": "M1",
            },
        },
    },
}

FAKE_MODELS = registry.flatten(FAKE_CUSTOMERS)
SHORTCUT = "customera:modela"


class TestListModelsCli:
    def test_list_models_requires_shard(self, capsys):
        """--list-models has no registry entry to take a shard from, so it must
        demand one explicitly rather than defaulting to any tenant."""
        with pytest.raises(SystemExit) as exc:
            smd._main(["--list-models"])
        assert exc.value.code != 0
        assert "--shard" in capsys.readouterr().err

    def test_list_models_passes_shard_through(self, monkeypatch):
        seen = {}

        def fake_list(shard):
            seen["shard"] = shard
            return []

        monkeypatch.setattr(smd, "list_available_models", fake_list)
        with pytest.raises(SystemExit) as exc:
            smd._main(["--list-models", "--shard", "eu3"])
        assert exc.value.code == 0
        assert seen["shard"] == "eu3"

    def test_shard_without_list_models_is_rejected(self, capsys, monkeypatch):
        """--shard only means something for --list-models (which has no
        registry entry to infer one from). Passing it with a model shortcut
        must not be silently ignored — that's exactly the silent-divergence
        failure mode this branch exists to eliminate."""
        monkeypatch.setattr(smd.registry, "MODELS", FAKE_MODELS)
        with pytest.raises(SystemExit) as exc:
            smd._main([SHORTCUT, "--shard", "eu9", "--rest-only"])
        assert exc.value.code != 0
        assert "--shard" in capsys.readouterr().err

    def test_shard_without_list_models_rejected_before_any_work(self, monkeypatch):
        """The rejection above must happen before the model resolves or any
        network/browser call is attempted."""
        monkeypatch.setattr(smd.registry, "MODELS", FAKE_MODELS)
        monkeypatch.setattr(smd, "download_model_exports_api",
                            lambda *a, **k: pytest.fail("must not run"))
        monkeypatch.setattr(smd, "download_model_exports_full",
                            lambda *a, **k: pytest.fail("must not run"))
        monkeypatch.setattr(smd, "download_model_exports",
                            lambda *a, **k: pytest.fail("must not run"))
        with pytest.raises(SystemExit):
            smd._main([SHORTCUT, "--shard", "eu9"])


class TestReExportedRegistryNames:
    """`app_url_for_shard` and `resolve_out_dir` are re-exported off
    scrape_model_data so existing importers keep working after the definitions
    moved to registry.py. Assert they are the SAME objects, not copies that
    could drift."""

    def test_app_url_for_shard_is_the_registry_one(self):
        assert smd.app_url_for_shard is registry.app_url_for_shard

    def test_resolve_out_dir_is_the_registry_one(self):
        assert smd.resolve_out_dir is registry.resolve_out_dir


class TestCoreWebappOrigin:
    def test_accepts_an_anaplan_app_origin(self):
        assert smd.validate_core_origin("https://eu4.app.anaplan.com") == \
            "https://eu4.app.anaplan.com"

    @pytest.mark.parametrize("bad", [
        "", None, "http://eu4.app.anaplan.com",          # not https
        "https://eu4.app.anaplan.com.evil.test",         # suffix attack
        "https://evil.test", "https://app.anaplan.com",
        "https://eu4.app.anaplan.com\n",                 # trailing newline: $ would
                                                          # accept this, \Z must not
    ])
    def test_rejects_anything_else(self, bad):
        with pytest.raises(RuntimeError):
            smd.validate_core_origin(bad)

    def test_builds_jsonrpc_and_servlet_from_origin(self):
        jsonrpc, servlet = smd._core_webapp_urls("https://eu9.app.anaplan.com", "WS1")
        assert jsonrpc == "https://eu9.app.anaplan.com/core-webapp-WS1/anaplan/jsonrpc"
        assert servlet == ("https://eu9.app.anaplan.com/core-webapp-WS1/anaplan/"
                           "servlet?taskType=export")


class _FakeWebDriverException(Exception):
    """Stand-in for selenium.common.exceptions.WebDriverException /
    TimeoutException — the point of these tests is that it is NOT a
    RuntimeError subclass, so a handler that only catches RuntimeError would
    let it propagate."""


class TestPullLegacyViaApiOriginDiscovery:
    """Regression coverage for I2: before this fix, only RuntimeError was
    caught around core-webapp origin discovery in _pull_legacy_via_api. A real
    Selenium WebDriverException/TimeoutException (e.g. a detached frame or a
    script timeout) is not a RuntimeError, so it used to propagate out of
    download_model_exports_full entirely, aborting Phase 2b's UI fallback and
    Phase 3 (Modules + General Lists) for the whole --full run. The fix
    broadens the handler to `except Exception` and still records a per-grid
    error, letting the caller's fallback logic run."""

    def test_non_runtimeerror_from_execute_script_is_caught_per_grid(self, monkeypatch):
        monkeypatch.setattr(smd, "enter_grid", lambda browser, timeout=20: True)

        class FakeBrowser:
            def execute_script(self, script):
                raise _FakeWebDriverException("script timed out")

        results = {}
        smd._pull_legacy_via_api(FakeBrowser(), "M1", "W1", "/out", results)

        assert set(results) == set(smd._LEGACY_TEMPLATES)
        for fn, r in results.items():
            assert r["ok"] is False
            assert "script timed out" in r["error"]

    def test_runtimeerror_from_bad_origin_is_still_caught(self, monkeypatch):
        """The broadened `except Exception` must still catch the pre-existing
        RuntimeError case (a malformed origin from validate_core_origin, now
        reached via _core_webapp_urls) — not just the new exception types."""
        monkeypatch.setattr(smd, "enter_grid", lambda browser, timeout=20: True)

        class FakeBrowser:
            def execute_script(self, script):
                return "https://evil.test"

        results = {}
        smd._pull_legacy_via_api(FakeBrowser(), "M1", "W1", "/out", results)

        assert set(results) == set(smd._LEGACY_TEMPLATES)
        for fn, r in results.items():
            assert r["ok"] is False
            assert "does not look like an Anaplan app shard" in r["error"]

    def test_no_enter_grid_iframe_still_reports_all_grids(self, monkeypatch):
        monkeypatch.setattr(smd, "enter_grid", lambda browser, timeout=20: False)
        results = {}
        smd._pull_legacy_via_api(object(), "M1", "W1", "/out", results)
        assert set(results) == set(smd._LEGACY_TEMPLATES)
        for r in results.values():
            assert r["ok"] is False
            assert "core-webapp iframe" in r["error"]


class TestDownloadModelExportsApiRestOnlySeam:
    """Browser-free seam test for the download_model_exports_api entry point
    (the branch's central claim — output folder derived from the registry
    entry — was previously only tested at the resolve_out_dir helper level,
    never through the real CLI/library entry point, which is why C3's stale
    docs went unnoticed). Monkeypatches only the network/browser seams
    (_api_session, _pull_api_files) plus registry.REPO_ROOT (so the derived
    path lands under tmp_path instead of the real repo), and drives everything
    else — resolve_shortcut, ResolvedModel.default_out_dir, resolve_out_dir's
    own existence check — for real."""

    def _repo_root_under(self, monkeypatch, tmp_path, entry):
        """Point registry.REPO_ROOT at tmp_path and create the vault folder the
        entry derives, so resolve_out_dir's existence check runs for real
        against a throwaway tree instead of the developer's vault."""
        monkeypatch.setattr(registry, "REPO_ROOT", str(tmp_path))
        path = os.path.join(str(tmp_path), "customers", entry["folder"],
                            "raw", "models", entry["raw_dir"])
        os.makedirs(path, exist_ok=True)
        return path

    def test_out_dir_comes_from_entry_and_name_does_not_move_it(self, tmp_path, monkeypatch):
        monkeypatch.setattr(smd.registry, "MODELS", FAKE_MODELS)
        self._repo_root_under(monkeypatch, tmp_path, FAKE_MODELS[SHORTCUT])
        monkeypatch.setattr(smd, "_api_session", lambda: object())

        pull_calls = []

        def fake_pull(sess, base, model_id, out_dir, results):
            pull_calls.append((model_id, out_dir))
            results["Line Items.csv"] = {"ok": True, "rows": 3, "path": None, "error": None}

        monkeypatch.setattr(smd, "_pull_api_files", fake_pull)

        results = smd.download_model_exports_api(
            SHORTCUT, name="A Totally Different Display Name", rest_only=True)

        expected_dir = os.path.join(str(tmp_path), "customers", "CustomerA",
                                    "raw", "models", "ModelA 2.0")
        assert len(pull_calls) == 1
        seen_model_id, seen_out_dir = pull_calls[0]
        assert seen_model_id == "M1"
        assert os.path.normpath(seen_out_dir) == os.path.normpath(expected_dir)
        assert results["Line Items.csv"]["ok"] is True

    def test_bad_shard_aborts_before_any_session_or_file(self, tmp_path, monkeypatch):
        broken = registry.flatten(
            {"customera": dict(FAKE_CUSTOMERS["customera"], shard="not-a-shard")})
        monkeypatch.setattr(smd.registry, "MODELS", broken)
        self._repo_root_under(monkeypatch, tmp_path, broken[SHORTCUT])

        called = {"session": False, "pull": False}
        monkeypatch.setattr(
            smd, "_api_session",
            lambda: called.__setitem__("session", True) or object())
        monkeypatch.setattr(
            smd, "_pull_api_files",
            lambda *a, **k: called.__setitem__("pull", True))

        with pytest.raises(ValueError):
            smd.download_model_exports_api(SHORTCUT, rest_only=True)

        assert called == {"session": False, "pull": False}
        assert list(tmp_path.rglob("*.csv")) == []


class TestListModelsStdoutIsPureJson:
    """`--list-models` exists to be machine-read: `... > models.json` must yield
    a file that parses. The browser/login helpers underneath it print progress
    with print(), i.e. to stdout, so without care that chatter lands in the
    redirected file and corrupts the payload."""

    def _fake_lookup(self, shard):
        # Mirrors the real helpers: _create_browser and login both print
        # progress banners to stdout before any JSON is produced.
        print("  → Trying Selenium Manager...")
        print("  ✓ Edge driver ready (Selenium Manager).")
        print("  → Opening browser and logging into Anaplan...")
        print("  ✓ Logged in.")
        return [{
            "model_name": "ModelA 2.0",
            "model_id": "M1",
            "workspace_name": "WS",
            "workspace_id": "W1",
            "customer_id": "C1",
        }]

    def test_stdout_parses_as_json(self, monkeypatch, capsys):
        monkeypatch.setattr(smd, "list_available_models", self._fake_lookup)

        with pytest.raises(SystemExit) as exc:
            smd._main(["--list-models", "--shard", "eu3"])
        assert exc.value.code == 0

        out = capsys.readouterr()
        parsed = json.loads(out.out)          # must not raise
        assert parsed[0]["model_id"] == "M1"

    def test_progress_chatter_goes_to_stderr(self, monkeypatch, capsys):
        monkeypatch.setattr(smd, "list_available_models", self._fake_lookup)

        with pytest.raises(SystemExit):
            smd._main(["--list-models", "--shard", "eu3"])

        out = capsys.readouterr()
        assert "Logged in" in out.err, "progress must stay visible on stderr"
        assert "Logged in" not in out.out, "progress must not pollute the JSON"


class TestLineItemHeaderAndRowsStayAligned:
    """`Brought-Forward` was missing from LINE_ITEM_HEADER.

    Anaplan's Line Items UI export is not one layout: some tenants emit three
    memory/statistics columns and no Brought-Forward, others emit
    Brought-Forward and none of the three. The split is per TENANT, not per
    engine (Classic and Polaris models sit on both sides of it), so the header
    has to be the union or the vault ends up with two incompatible schemas.

    The REST payload does carry `broughtForward`, so unlike the three
    statistics columns this one is real data that was being dropped on the
    floor. The three statistics columns are asserted to stay blank so that a
    future "fill these in" change has to face the fact that REST does not
    return them.

    The alignment assertion is the important one: build_line_items appends a
    positional list, so inserting a column into the header without inserting a
    value shifts every column after it and silently mislabels the CSV.
    """

    ITEM = {
        "name": "Some Line Item",
        "format": "NUMBER",
        "formula": "1 + 1",
        "summary": "Sum",
        "appliesTo": [{"id": "1", "name": "Region"}],
        "timeScale": "Month",
        "timeRange": "Model Calendar",
        "version": {"id": "v1", "name": "Actual"},
        "style": "Normal",
        "cellCount": 42,
        "notes": "a note",
        "isSummary": False,
        "formulaScope": "All Versions",
        "useSwitchover": True,
        "breakback": False,
        "broughtForward": True,
        "startOfSection": False,
        "referencedBy": [{"id": "9", "name": "Other Module"}],
        "moduleName": "MOD 01",
    }

    def _build(self, monkeypatch, item):
        monkeypatch.setattr(smd, "_get", lambda sess, url: {"items": [item]})
        return smd.build_line_items(object(), "https://api.example", "MODEL")

    def test_header_places_brought_forward_where_the_ui_export_does(self):
        h = smd.LINE_ITEM_HEADER
        assert "Brought-Forward" in h, "REST returns broughtForward; do not drop it"
        assert h[h.index("Breakback") + 1] == "Brought-Forward"
        assert h[h.index("Brought-Forward") + 1] == "Start of Section"

    def test_every_row_is_exactly_as_wide_as_the_header(self, monkeypatch):
        header, rows = self._build(monkeypatch, self.ITEM)
        assert rows, "fixture should produce one row"
        for row in rows:
            assert len(row) == len(header), (
                "row/header width drift mislabels every column after the gap"
            )

    def test_brought_forward_value_is_lowercase_blueprint_boolean(self, monkeypatch):
        header, rows = self._build(monkeypatch, self.ITEM)
        cell = dict(zip(header, rows[0]))
        # Anaplan's own UI export writes lowercase true/false, and _b matches it.
        assert cell["Brought-Forward"] == "true"
        assert cell["Breakback"] == "false"
        assert cell["Start of Section"] == "false"

    def test_missing_brought_forward_is_blank_not_an_exception(self, monkeypatch):
        """A tenant/API version that omits the key must not blow up the export
        — a partial CSV is worse than a blank column."""
        item = {k: v for k, v in self.ITEM.items() if k != "broughtForward"}
        header, rows = self._build(monkeypatch, item)
        cell = dict(zip(header, rows[0]))
        assert cell["Brought-Forward"] == ""
        assert cell["Module Name"] == "MOD 01", "columns after the gap must not shift"

    def test_statistics_columns_stay_blank_because_rest_omits_them(self, monkeypatch):
        header, rows = self._build(monkeypatch, self.ITEM)
        cell = dict(zip(header, rows[0]))
        for col in ("Populated Cell Count", "Memory Used", "Calculation Complexity"):
            assert cell[col] == "", f"{col} is not in the REST payload"
