"""Offline tests for scrape_model_data's pure seams.

None of these touch Anaplan, a browser, or the developer's real .env: every
test here exercises string/dict logic only. That is deliberate — the failure
mode this module guards against is a *silent wrong-tenant export* (a KWS model
scraped against Stedin's shard, or into Stedin's folder), which is cheap to
assert here and expensive to notice live.
"""
import os

import pytest

import scrape_model_data as smd


class TestAppUrlForShard:
    def test_derives_url_from_shard_token(self):
        assert smd.app_url_for_shard("eu3") == "https://eu3.app.anaplan.com/"

    def test_derives_url_for_existing_stedin_shard(self):
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
        not quietly resolve to Stedin's shard."""
        with pytest.raises(ValueError):
            smd.app_url_for_shard("nonsense")
