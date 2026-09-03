"""Offline tests for scrape_model_data's pure seams.

None of these touch Anaplan, a browser, or the developer's real .env: every
test here exercises string/dict logic only. That is deliberate — the failure
mode this module guards against is a *silent wrong-tenant export* (one
customer's model scraped against another customer's shard, or into another
customer's folder), which is cheap to assert here and expensive to notice
live.
"""
import os

import pytest

import scrape_model_data as smd


class TestAppUrlForShard:
    def test_derives_url_from_shard_token(self):
        assert smd.app_url_for_shard("eu3") == "https://eu3.app.anaplan.com/"

    def test_derives_url_for_a_second_known_shard(self):
        assert smd.app_url_for_shard("eu2a") == "https://eu2a.app.anaplan.com/"

    def test_normalises_case_and_whitespace(self):
        assert smd.app_url_for_shard("  EU3 ") == "https://eu3.app.anaplan.com/"

    @pytest.mark.parametrize("bad", ["", None, "eu2a.app.anaplan.com",
                                     "https://eu3.app.anaplan.com/", "prod",
                                     "eu3/../evil", "eu 3"])
    def test_rejects_anything_that_is_not_a_shard_token(self, bad):
        with pytest.raises(ValueError) as exc:
            smd.app_url_for_shard(bad)
        assert repr(bad) in str(exc.value) or "shard" in str(exc.value).lower()

    def test_never_falls_back_to_eu2a(self):
        """The 2026-09 regression this exists to prevent: an unknown shard must
        not quietly resolve to some default shard."""
        with pytest.raises(ValueError):
            smd.app_url_for_shard("nonsense")


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
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        with pytest.raises(SystemExit) as exc:
            smd._main(["a", "--shard", "eu9", "--rest-only"])
        assert exc.value.code != 0
        assert "--shard" in capsys.readouterr().err

    def test_shard_without_list_models_rejected_before_any_work(self, monkeypatch):
        """The rejection above must happen before the model resolves or any
        network/browser call is attempted."""
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        monkeypatch.setattr(smd, "download_model_exports_api",
                            lambda *a, **k: pytest.fail("must not run"))
        monkeypatch.setattr(smd, "download_model_exports_full",
                            lambda *a, **k: pytest.fail("must not run"))
        monkeypatch.setattr(smd, "download_model_exports",
                            lambda *a, **k: pytest.fail("must not run"))
        with pytest.raises(SystemExit):
            smd._main(["a", "--shard", "eu9"])


FAKE_ENTRY = {
    "name": "ModelA", "raw_dir": "ModelA 2.0", "folder": "CustomerA",
    "shard": "eu3", "customer_id": "C1", "workspace_id": "W1", "model_id": "M1",
}


class TestResolveModel:
    def test_returns_merged_entry_with_all_required_keys(self, monkeypatch):
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        entry = smd._resolve_model("a")
        for key in smd.REQUIRED_ENTRY_KEYS:
            assert entry[key], f"{key} missing from resolved entry"
        assert entry["shard"] == "eu3"

    def test_name_override_sets_display_name_only(self, monkeypatch):
        """--name is cosmetic: it must NOT change raw_dir, which selects the
        output folder."""
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        entry = smd._resolve_model("a", name="Something Else")
        assert entry["display_name"] == "Something Else"
        assert entry["raw_dir"] == "ModelA 2.0"

    @pytest.mark.parametrize("missing", ["raw_dir", "folder", "shard",
                                         "customer_id", "workspace_id", "model_id"])
    def test_missing_key_raises_naming_it(self, monkeypatch, missing):
        broken = dict(FAKE_ENTRY)
        del broken[missing]
        monkeypatch.setattr(smd.models, "MODELS", {"a": broken})
        with pytest.raises(ValueError) as exc:
            smd._resolve_model("a")
        assert missing in str(exc.value)

    def test_bad_shard_in_entry_raises(self, monkeypatch):
        broken = dict(FAKE_ENTRY, shard="https://eu3.app.anaplan.com/")
        monkeypatch.setattr(smd.models, "MODELS", {"a": broken})
        with pytest.raises(ValueError):
            smd._resolve_model("a")

    def test_unknown_shortcut_lists_valid_ones(self, monkeypatch):
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        with pytest.raises(ValueError) as exc:
            smd._resolve_model("nope")
        assert "'a'" in str(exc.value) or "a" in str(exc.value)


class TestSettingsUrl:
    def test_built_from_entry_shard_and_guids(self):
        assert smd.settings_url(FAKE_ENTRY) == (
            "https://eu3.app.anaplan.com/a/modeling/customers/C1/workspaces/W1"
            "/models/M1/model-settings"
        )


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


class TestOutDir:
    def test_default_is_customer_scoped(self):
        got = smd.default_out_dir(FAKE_ENTRY, repo_root="/repo")
        assert got == os.path.join("/repo", "customers", "CustomerA",
                                   "raw", "models", "ModelA 2.0")

    def test_default_must_already_exist(self, tmp_path):
        """A typo'd raw_dir must error, not silently create a stray sibling
        folder that then looks like a successful export."""
        with pytest.raises(ValueError) as exc:
            smd.resolve_out_dir(FAKE_ENTRY, out_dir=None, repo_root=str(tmp_path))
        assert "ModelA 2.0" in str(exc.value)

    def test_default_used_when_it_exists(self, tmp_path):
        target = tmp_path / "customers" / "CustomerA" / "raw" / "models" / "ModelA 2.0"
        target.mkdir(parents=True)
        got = smd.resolve_out_dir(FAKE_ENTRY, out_dir=None, repo_root=str(tmp_path))
        assert os.path.normpath(got) == os.path.normpath(str(target))

    def test_explicit_out_dir_is_created(self, tmp_path):
        scratch = tmp_path / "scratch" / "probe"
        got = smd.resolve_out_dir(FAKE_ENTRY, out_dir=str(scratch),
                                  repo_root=str(tmp_path))
        assert os.path.isdir(got)

    def test_missing_folder_error_names_the_shortcut(self, tmp_path, monkeypatch):
        """The ValueError used to print the literal models.MODELS['...'], which
        can't be searched for in models.py. Once an entry has gone through
        _resolve_model it carries the actual shortcut key, and the error
        should name it."""
        monkeypatch.setattr(smd.models, "MODELS", {"my-shortcut": dict(FAKE_ENTRY)})
        entry = smd._resolve_model("my-shortcut")
        with pytest.raises(ValueError) as exc:
            smd.resolve_out_dir(entry, out_dir=None, repo_root=str(tmp_path))
        assert "my-shortcut" in str(exc.value)

    def test_missing_folder_error_tolerates_entry_without_shortcut(self, tmp_path):
        """resolve_out_dir is also called directly in tests/library use with a
        plain dict that never went through _resolve_model — must not KeyError
        just because 'shortcut' is absent."""
        with pytest.raises(ValueError):
            smd.resolve_out_dir(FAKE_ENTRY, out_dir=None, repo_root=str(tmp_path))

    def test_name_override_does_not_change_out_dir(self, tmp_path, monkeypatch):
        target = tmp_path / "customers" / "CustomerA" / "raw" / "models" / "ModelA 2.0"
        target.mkdir(parents=True)
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        entry = smd._resolve_model("a", name="Wrong Folder Name")
        got = smd.resolve_out_dir(entry, out_dir=None, repo_root=str(tmp_path))
        assert os.path.normpath(got) == os.path.normpath(str(target))


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
    (_api_session, _pull_api_files) plus default_out_dir (so the derived path
    lands under tmp_path instead of the real repo), and drives everything else
    — _resolve_model, resolve_out_dir's own existence check — for real."""

    def _patch_default_out_dir_under(self, monkeypatch, tmp_path):
        def fake_default_out_dir(entry, repo_root=None):
            path = os.path.join(str(tmp_path), "customers", entry["folder"],
                                "raw", "models", entry["raw_dir"])
            os.makedirs(path, exist_ok=True)
            return path
        monkeypatch.setattr(smd, "default_out_dir", fake_default_out_dir)

    def test_out_dir_comes_from_entry_and_name_does_not_move_it(self, tmp_path, monkeypatch):
        self._patch_default_out_dir_under(monkeypatch, tmp_path)
        monkeypatch.setattr(smd.models, "MODELS", {"a": dict(FAKE_ENTRY)})
        monkeypatch.setattr(smd, "_api_session", lambda: object())

        pull_calls = []

        def fake_pull(sess, base, model_id, out_dir, results):
            pull_calls.append((model_id, out_dir))
            results["Line Items.csv"] = {"ok": True, "rows": 3, "path": None, "error": None}

        monkeypatch.setattr(smd, "_pull_api_files", fake_pull)

        results = smd.download_model_exports_api(
            "a", name="A Totally Different Display Name", rest_only=True)

        expected_dir = os.path.join(str(tmp_path), "customers", "CustomerA",
                                    "raw", "models", "ModelA 2.0")
        assert len(pull_calls) == 1
        seen_model_id, seen_out_dir = pull_calls[0]
        assert seen_model_id == "M1"
        assert os.path.normpath(seen_out_dir) == os.path.normpath(expected_dir)
        assert results["Line Items.csv"]["ok"] is True

    def test_bad_shard_aborts_before_any_session_or_file(self, tmp_path, monkeypatch):
        self._patch_default_out_dir_under(monkeypatch, tmp_path)
        broken = dict(FAKE_ENTRY, shard="not-a-shard")
        monkeypatch.setattr(smd.models, "MODELS", {"a": broken})

        called = {"session": False, "pull": False}
        monkeypatch.setattr(
            smd, "_api_session",
            lambda: called.__setitem__("session", True) or object())
        monkeypatch.setattr(
            smd, "_pull_api_files",
            lambda *a, **k: called.__setitem__("pull", True))

        with pytest.raises(ValueError):
            smd.download_model_exports_api("a", rest_only=True)

        assert called == {"session": False, "pull": False}
        assert list(tmp_path.rglob("*.csv")) == []
