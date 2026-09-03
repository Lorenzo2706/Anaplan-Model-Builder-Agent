"""Offline tests for scrape_model_data's pure seams.

None of these touch Anaplan, a browser, or the developer's real .env: every
test here exercises string/dict logic only. That is deliberate — the failure
mode this module guards against is a *silent wrong-tenant export* (one
customer's model scraped against another customer's shard, or into another
customer's folder), which is cheap to assert here and expensive to notice
live.
"""
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
