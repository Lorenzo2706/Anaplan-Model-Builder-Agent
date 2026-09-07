"""Offline tests for the customer-first registry.

Nothing here touches Anaplan, a browser, or the developer's real models.py.
Every test builds its own placeholder CUSTOMERS tree, because the real one is
gitignored and differs per machine — a test that read it would pass or fail
depending on whose clone ran it.

The failure mode these guard against is a silent WRONG-TENANT operation: one
customer's model resolved against another customer's shard, folder or tenant
GUID. That is cheap to assert here and expensive to notice live.

ONE DOCUMENTED EXCEPTION to "placeholder data only"

    TestModuleLevelLoad::test_every_entry_has_the_full_merged_shape and
    ::test_import_did_not_read_dotenv read the developer's real, gitignored
    models.py. That is deliberate: they assert the *shape* of whatever the
    local file happens to be and never a value, so they pass on any
    correctly-migrated clone, fail on an unmigrated one, and pass trivially on
    a fresh clone whose models.py is empty. No customer string can enter this
    file through them.
"""
import pytest

import registry


CUSTOMERS = {
    "customera": {
        "name": "CustomerA",
        "shard": "eu9z",
        "folder": "CustomerA",
        "customer_id": "CUST-A",
        "models": {
            "modela": {
                "name": "ModelA",
                "raw_dir": "ModelA 2.0",
                "workspace_id": "WS-A1",
                "model_id": "MODEL-A1",
                "engine": "Polaris",
                "workspace_label": "DEV",
            },
            "datahub": {
                "name": "Data Hub",
                "raw_dir": "Data Hub",
                "workspace_id": "WS-A2",
                "model_id": "MODEL-A2",
                "engine": "Classic",
            },
        },
    },
    "customerb": {
        "name": "CustomerB",
        "shard": "us9z",
        "folder": "CustomerB",
        "customer_id": "CUST-B",
        "models": {
            # Same model key as CustomerA's, deliberately: "datahub" is a
            # near-universal model name and the collision is the normal case,
            # not an edge case.
            "datahub": {
                "name": "Data Hub",
                "raw_dir": "Data Hub",
                "workspace_id": "WS-B1",
                "model_id": "MODEL-B1",
                "engine": "Classic",
            },
        },
    },
}


class TestFlatten:
    def test_keys_are_customer_scoped_composites(self):
        flat = registry.flatten(CUSTOMERS)
        assert set(flat) == {"customera:modela", "customera:datahub",
                             "customerb:datahub"}

    def test_customer_fields_are_inherited_into_every_model(self):
        flat = registry.flatten(CUSTOMERS)
        entry = flat["customera:modela"]
        assert entry["shard"] == "eu9z"
        assert entry["folder"] == "CustomerA"
        assert entry["customer_id"] == "CUST-A"

    def test_colliding_model_keys_stay_separate_entries(self):
        """The whole point of composite keys. Two customers with a 'datahub'
        must not collapse into one entry, whichever is defined last."""
        flat = registry.flatten(CUSTOMERS)
        assert flat["customera:datahub"]["model_id"] == "MODEL-A2"
        assert flat["customerb:datahub"]["model_id"] == "MODEL-B1"
        assert flat["customera:datahub"]["shard"] == "eu9z"
        assert flat["customerb:datahub"]["shard"] == "us9z"

    def test_entry_carries_its_own_provenance(self):
        flat = registry.flatten(CUSTOMERS)
        entry = flat["customerb:datahub"]
        assert entry["customer_key"] == "customerb"
        assert entry["model_key"] == "datahub"
        assert entry["shortcut"] == "customerb:datahub"

    def test_model_may_override_an_inherited_customer_field(self):
        """A model in a second workspace on a different shard is legal. The
        model's own value wins; it does not silently lose to the customer's."""
        tree = {"customera": dict(CUSTOMERS["customera"],
                                  models={"odd": {"name": "Odd",
                                                  "raw_dir": "Odd",
                                                  "workspace_id": "WS",
                                                  "model_id": "M",
                                                  "shard": "ap9z"}})}
        assert registry.flatten(tree)["customera:odd"]["shard"] == "ap9z"

    def test_flatten_does_not_mutate_the_input_tree(self):
        """flatten() is called at import time by registry.py and again by
        tests; mutating the source would make the second call see the first
        call's inherited fields as if they had been authored."""
        import copy
        before = copy.deepcopy(CUSTOMERS)
        registry.flatten(CUSTOMERS)
        assert CUSTOMERS == before

    def test_optional_keys_default_rather_than_raise(self):
        flat = registry.flatten(CUSTOMERS)
        assert flat["customera:datahub"]["workspace_label"] == "PRODUCTION"
        assert flat["customera:modela"]["workspace_label"] == "DEV"

    def test_engine_defaults_to_unknown_not_to_a_guess(self):
        tree = {"customera": dict(CUSTOMERS["customera"],
                                  models={"noeng": {"name": "NoEng",
                                                    "raw_dir": "NoEng",
                                                    "workspace_id": "WS",
                                                    "model_id": "M"}})}
        assert registry.flatten(tree)["customera:noeng"]["engine"] == "unknown"

    @pytest.mark.parametrize("dropped", registry.CUSTOMER_KEYS)
    def test_missing_customer_field_raises_and_names_it(self, dropped):
        cust = {k: v for k, v in CUSTOMERS["customera"].items() if k != dropped}
        with pytest.raises(ValueError) as exc:
            registry.flatten({"customera": cust})
        assert dropped in str(exc.value)
        assert "customera" in str(exc.value)

    @pytest.mark.parametrize("dropped", registry.MODEL_KEYS)
    def test_missing_model_field_raises_and_names_it(self, dropped):
        model = {k: v for k, v in CUSTOMERS["customera"]["models"]["modela"].items()
                 if k != dropped}
        tree = {"customera": dict(CUSTOMERS["customera"], models={"modela": model})}
        with pytest.raises(ValueError) as exc:
            registry.flatten(tree)
        assert dropped in str(exc.value)
        assert "customera:modela" in str(exc.value)

    def test_customer_with_no_models_key_raises(self):
        cust = {k: v for k, v in CUSTOMERS["customera"].items() if k != "models"}
        with pytest.raises(ValueError) as exc:
            registry.flatten({"customera": cust})
        assert "models" in str(exc.value)

    def test_empty_tree_is_empty_not_an_error(self):
        """A fresh clone has no customers configured yet. --list-models must
        still run, so this is a legal state, not a misconfiguration."""
        assert registry.flatten({}) == {}

    @pytest.mark.parametrize("bad_key", ["cust:omera", "customer a", "", "CustomerA:"])
    def test_rejects_customer_keys_that_break_composite_parsing(self, bad_key):
        """A ':' or whitespace in a customer key makes 'a:b' ambiguous to
        parse, so it is rejected at flatten time rather than mis-parsed later."""
        with pytest.raises(ValueError):
            registry.flatten({bad_key: CUSTOMERS["customera"]})


class TestAliases:
    def test_unique_model_key_gets_a_bare_alias(self):
        flat = registry.flatten(CUSTOMERS)
        assert registry.aliases(flat)["modela"] == "customera:modela"

    def test_colliding_model_key_gets_no_alias(self):
        """'datahub' exists under both customers, so a bare 'datahub' has no
        safe meaning and must NOT resolve to whichever came first."""
        flat = registry.flatten(CUSTOMERS)
        assert "datahub" not in registry.aliases(flat)

    def test_composite_keys_are_never_themselves_aliases(self):
        flat = registry.flatten(CUSTOMERS)
        assert all(":" not in a for a in registry.aliases(flat))


class TestCheckNotLegacy:
    def test_flat_models_module_raises_with_migration_instructions(self):
        """models.py is gitignored, so a commit cannot migrate it. The only way
        to tell the user their file is the old shape is to refuse loudly and
        say exactly what to change."""
        class OldModels:
            MODELS = {"modela": {"name": "ModelA", "shard": "eu9z"}}

        with pytest.raises(registry.LegacyRegistryError) as exc:
            registry.check_not_legacy(OldModels)
        msg = str(exc.value)
        assert "CUSTOMERS" in msg
        assert "models.py.example" in msg

    def test_customers_module_passes(self):
        class NewModels:
            CUSTOMERS = CUSTOMERS

        registry.check_not_legacy(NewModels)   # must not raise

    def test_module_with_both_prefers_customers_and_does_not_raise(self):
        """Mid-migration a user may leave the old dict in place. CUSTOMERS
        present means they have migrated; the stale MODELS is ignored, not an
        error, so the migration can be done in one edit without a broken
        intermediate state."""
        class Both:
            CUSTOMERS = CUSTOMERS
            MODELS = {"modela": {}}

        registry.check_not_legacy(Both)

    def test_empty_module_passes(self):
        """A fresh clone with no models.py content is legal — see
        test_empty_tree_is_empty_not_an_error."""
        class Empty:
            pass

        registry.check_not_legacy(Empty)


class TestAppUrlForShard:
    def test_derives_url_from_shard_token(self):
        assert registry.app_url_for_shard("eu9z") == "https://eu9z.app.anaplan.com/"

    def test_normalises_case_and_whitespace(self):
        assert registry.app_url_for_shard("  EU9Z ") == "https://eu9z.app.anaplan.com/"

    @pytest.mark.parametrize("bad", ["", None, "eu9z.app.anaplan.com",
                                     "https://eu9z.app.anaplan.com/", "prod",
                                     "eu9z/../evil", "eu 9"])
    def test_rejects_anything_that_is_not_a_shard_token(self, bad):
        with pytest.raises(ValueError):
            registry.app_url_for_shard(bad)

    def test_never_falls_back_to_a_default_shard(self):
        """The regression this exists to prevent: an unknown shard must not
        quietly resolve to some default, which logs into the wrong tenant and
        exports the wrong model into the requested folder."""
        with pytest.raises(ValueError):
            registry.app_url_for_shard("nonsense")


class TestResolve:
    def test_resolves_a_composite_key(self):
        r = registry.resolve("customera:modela", registry.flatten(CUSTOMERS))
        assert r.model_id == "MODEL-A1"
        assert r.customer_key == "customera"

    def test_resolves_an_unambiguous_bare_key(self):
        r = registry.resolve("modela", registry.flatten(CUSTOMERS))
        assert r.shortcut == "customera:modela"

    def test_ambiguous_bare_key_raises_and_lists_the_candidates(self):
        with pytest.raises(ValueError) as exc:
            registry.resolve("datahub", registry.flatten(CUSTOMERS))
        msg = str(exc.value)
        assert "customera:datahub" in msg and "customerb:datahub" in msg

    def test_customer_argument_disambiguates_a_colliding_bare_key(self):
        r = registry.resolve("datahub", registry.flatten(CUSTOMERS),
                             customer="customerb")
        assert r.model_id == "MODEL-B1"

    def test_customer_argument_conflicting_with_a_composite_key_raises(self):
        """`--customer customera modelb:...` is a contradiction, not a
        precedence question. Silently honouring one of the two is how a
        deliberate --customer gate gets bypassed."""
        with pytest.raises(ValueError) as exc:
            registry.resolve("customera:modela", registry.flatten(CUSTOMERS),
                             customer="customerb")
        assert "customera" in str(exc.value) and "customerb" in str(exc.value)

    def test_unknown_key_lists_available_shortcuts(self):
        with pytest.raises(ValueError) as exc:
            registry.resolve("nope", registry.flatten(CUSTOMERS))
        assert "customera:modela" in str(exc.value)

    def test_unknown_customer_lists_available_customers(self):
        with pytest.raises(ValueError) as exc:
            registry.resolve("modela", registry.flatten(CUSTOMERS),
                             customer="nosuch")
        assert "customera" in str(exc.value)

    def test_display_name_defaults_to_the_model_name(self):
        r = registry.resolve("customera:modela", registry.flatten(CUSTOMERS))
        assert r.display_name == "ModelA"

    def test_display_name_override_does_not_touch_anything_else(self):
        """--name is display-only (spec decision 6). It must not reach the
        output folder: raw_dir does that."""
        r = registry.resolve("customera:modela", registry.flatten(CUSTOMERS),
                             name="Whatever")
        assert r.display_name == "Whatever"
        assert r.raw_dir == "ModelA 2.0"

    def test_resolved_model_is_immutable(self):
        r = registry.resolve("customera:modela", registry.flatten(CUSTOMERS))
        with pytest.raises(Exception):
            r.shard = "us9z"

    def test_bad_shard_fails_at_resolve_not_mid_login(self):
        tree = {"customera": dict(CUSTOMERS["customera"], shard="not-a-shard")}
        with pytest.raises(ValueError):
            registry.resolve("customera:modela", registry.flatten(tree))


class TestDerivedUrlsAndPaths:
    def _resolved(self):
        return registry.resolve("customerb:datahub", registry.flatten(CUSTOMERS))

    def test_app_url_comes_from_the_customers_shard(self):
        assert self._resolved().app_url == "https://us9z.app.anaplan.com/"

    def test_settings_url_is_built_from_all_three_guids(self):
        assert self._resolved().settings_url == (
            "https://us9z.app.anaplan.com/a/modeling/customers/CUST-B"
            "/workspaces/WS-B1/models/MODEL-B1/model-settings"
        )

    def test_default_out_dir_is_folder_plus_raw_dir(self):
        parts = registry.os.path.normpath(self._resolved().default_out_dir).split(registry.os.sep)
        assert parts[-4:] == ["CustomerB", "raw", "models", "Data Hub"]

    def test_default_out_dir_ignores_the_display_name(self):
        r = registry.resolve("customera:modela", registry.flatten(CUSTOMERS),
                             name="Whatever")
        assert "Whatever" not in r.default_out_dir
        assert r.default_out_dir.endswith("ModelA 2.0")

    def test_default_out_dir_never_uses_the_pre_restructure_root(self):
        """The vault has no <repo>/raw/models/ any more - every model's CSVs
        live under customers/<folder>/raw/models/. Regression guard carried
        over from fetch_model_data.resolve_raw_dir's tests when that function
        was replaced by ResolvedModel.default_out_dir."""
        parts = registry.os.path.normpath(
            self._resolved().default_out_dir).split(registry.os.sep)
        assert parts[-5] == "customers"

    def test_nux_out_dir_is_the_customers_UI_folder(self):
        parts = registry.os.path.normpath(self._resolved().nux_out_dir).split(registry.os.sep)
        assert parts[-2:] == ["CustomerB", "UI"]


class TestResolveOutDir:
    def test_explicit_out_dir_is_created_if_absent(self, tmp_path):
        target = tmp_path / "scratch" / "deeper"
        got = registry.resolve_out_dir(
            registry.resolve("customera:modela", registry.flatten(CUSTOMERS)),
            out_dir=str(target))
        assert got == str(target)
        assert target.is_dir()

    def test_derived_vault_path_must_already_exist(self, tmp_path):
        """Creating it would mean a typo in raw_dir silently produces a second,
        wrong-named folder beside the real one, and a run that reports success
        while the wiki still points at the old folder."""
        flat = registry.flatten(CUSTOMERS)
        r = registry.resolve("customera:modela", flat)
        r = registry.dataclasses.replace(r, folder=str(tmp_path / "nope"))
        with pytest.raises(ValueError) as exc:
            registry.resolve_out_dir(r)
        assert "ModelA 2.0" in str(exc.value)


class TestModuleLevelLoad:
    def test_models_module_is_loaded_into_MODELS(self):
        """registry.MODELS is what every consumer reads. It must be a
        flattened registry, not the raw tree."""
        assert isinstance(registry.MODELS, dict)
        assert all(":" in k for k in registry.MODELS)

    def test_every_entry_has_the_full_merged_shape(self):
        for shortcut, entry in registry.MODELS.items():
            for key in registry.CUSTOMER_KEYS + registry.MODEL_KEYS:
                assert entry.get(key), f"{shortcut} is missing {key}"

    def test_resolve_shortcut_binds_to_MODELS(self, monkeypatch):
        monkeypatch.setattr(registry, "MODELS", registry.flatten(CUSTOMERS))
        assert registry.resolve_shortcut("customera:modela").model_id == "MODEL-A1"

    def test_import_did_not_read_dotenv(self):
        """The 2026-08-14 'models/None' incident: models.py resolved every
        GUID via os.getenv() at import time, so any consumer that imported it
        before load_dotenv() got None for every id. The fix is structural -
        models.py holds literals now and reads no environment at all - so this
        asserts the absence of the mechanism, which is what replaces
        test_env_import_order.py."""
        import inspect
        import models
        src = inspect.getsource(models)
        assert "getenv" not in src, (
            "models.py must hold literal values. Reading the environment at "
            "import time is what caused the models/None incident; the "
            "import-order guard that used to catch it is gone because the "
            "mechanism is supposed to be gone."
        )
        assert "dotenv" not in src

    def test_customer_keys_are_sorted(self, monkeypatch):
        monkeypatch.setattr(registry, "CUSTOMERS", CUSTOMERS)
        assert registry.customer_keys() == ["customera", "customerb"]
