"""Offline tests for the customer-first registry.

Nothing here touches Anaplan, a browser, or the developer's real models.py.
Every test builds its own placeholder CUSTOMERS tree, because the real one is
gitignored and differs per machine — a test that read it would pass or fail
depending on whose clone ran it.

The failure mode these guard against is a silent WRONG-TENANT operation: one
customer's model resolved against another customer's shard, folder or tenant
GUID. That is cheap to assert here and expensive to notice live.
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
