"""Offline tests for the wizard's customer selection.

No browser, no login, no Anaplan. Prompts are driven by monkeypatching
builtins.input, which is what the anaplan-model-optimizer skill does with a
piped printf - so these tests exercise the same path the skill depends on.

The contract under test is the PROMPT ORDER as much as the values: the skill
feeds answers positionally, so an inserted or reordered question silently
lands an answer on the wrong prompt.
"""
import builtins

import pytest

import registry
import scraper_ux


TREE = {
    "customera": {
        "name": "CustomerA", "shard": "eu9z", "folder": "CustomerA",
        "customer_id": "CUST-A",
        "models": {
            "modela": {"name": "ModelA", "raw_dir": "ModelA 2.0",
                       "workspace_id": "WS-A1", "model_id": "MODEL-A1"},
        },
    },
    "customerb": {
        "name": "CustomerB", "shard": "us9z", "folder": "CustomerB",
        "customer_id": "CUST-B",
        "models": {
            "modelb": {"name": "ModelB", "raw_dir": "ModelB Prod",
                       "workspace_id": "WS-B1", "model_id": "MODEL-B1"},
            "datahub": {"name": "Data Hub", "raw_dir": "Data Hub",
                        "workspace_id": "WS-B2", "model_id": "MODEL-B2"},
        },
    },
}


@pytest.fixture
def registered(monkeypatch):
    flat = registry.flatten(TREE)
    monkeypatch.setattr(registry, "CUSTOMERS", TREE)
    monkeypatch.setattr(registry, "MODELS", flat)
    monkeypatch.setattr(registry, "ALIASES", registry.aliases(flat))
    return flat


@pytest.fixture
def answers(monkeypatch):
    """Feed input() from a list, and record the prompts it was asked."""
    def _install(values):
        queue = list(values)
        asked = []

        def fake_input(prompt=""):
            asked.append(prompt)
            return queue.pop(0) if queue else ""

        monkeypatch.setattr(builtins, "input", fake_input)
        monkeypatch.setattr(scraper_ux.getpass, "getpass",
                            lambda *a, **k: "pw")
        return asked
    return _install


class TestCustomerPrompt:
    def test_choosing_a_customer_sets_its_shard_url(self, registered, answers,
                                                    monkeypatch, tmp_path):
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        answers(["2", "", "", str(tmp_path), ""])   # customer 2 = customerb
        config = scraper_ux._collect_config()
        assert config["main_url"] == "https://us9z.app.anaplan.com/"
        assert config["customer_key"] == "customerb"
        assert config["folder"] == "CustomerB"

    def test_customer_menu_is_sorted_and_shows_every_customer(self, registered,
                                                              answers, monkeypatch,
                                                              tmp_path, capsys):
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        answers(["1", "", "", str(tmp_path), ""])
        scraper_ux._collect_config()
        out = capsys.readouterr().out
        assert out.index("customera") < out.index("customerb")

    def test_prompt_count_is_unchanged_at_four_steps_plus_confirm(
            self, registered, answers, monkeypatch, tmp_path):
        """anaplan-model-optimizer feeds this wizard positionally with
        printf. If the number of prompts changes, its recipe silently lands
        an answer on the wrong question - so the count is a contract."""
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        asked = answers(["1", "", "", str(tmp_path), ""])
        scraper_ux._collect_config()
        assert len(asked) == 5

    def test_no_shard_question_is_asked(self, registered, answers, monkeypatch,
                                        tmp_path, capsys):
        """The shard is a property of the customer. Asking a modeller which
        shard their tenant is on asks them to know what the registry records.

        The assertion is scoped to the prompts themselves (the `asked` list)
        rather than all of stdout: the customer menu legitimately *displays*
        each customer's shard as a read-only label the modeller reads (it is
        what makes a mis-selected customer visible before the browser opens),
        but no input() prompt may ask for it. "environment" is checked against
        all of stdout too, since the replacement genuinely eliminates that
        question rather than merely relabelling it.
        """
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        asked = answers(["1", "", "", str(tmp_path), ""])
        scraper_ux._collect_config()
        out = capsys.readouterr().out.lower()
        assert not any("shard" in p.lower() or "environment" in p.lower()
                       for p in asked)
        assert "environment" not in out

    def test_anaplan_urls_constant_is_gone(self):
        """It hardcoded one shard and silently defaulted unknown shards to it -
        the exact fallback spec decision 4 removed everywhere else."""
        assert not hasattr(scraper_ux, "ANAPLAN_URLS")


class TestFilteredModelMenu:
    def test_menu_lists_only_the_chosen_customers_models(self, registered):
        shown = scraper_ux._models_for_customer("customerb")
        assert set(shown) == {"customerb:modelb", "customerb:datahub"}

    def test_menu_excludes_other_customers_models(self, registered):
        assert "customera:modela" not in scraper_ux._models_for_customer("customerb")

    def test_unknown_customer_yields_nothing_rather_than_everything(self, registered):
        """Failing open here would offer one customer's models under another's
        login - a wrong-tenant scrape that looks like a successful one."""
        assert scraper_ux._models_for_customer("nosuch") == {}

    def test_empty_registry_for_customer_warns_before_falling_through_to_the_api(
            self, registered, monkeypatch, capsys):
        """After filtering, _select_model can fall through to
        _choose_model_from_api - which lists every workspace the account can
        see, i.e. potentially another customer's models. That must never
        happen silently: the user just answered "I am scraping customerc",
        and the listing about to appear is account-wide, not filtered to
        them. Stubbed at the _choose_model_from_api seam so this never
        reaches a browser, a login, or the network.
        """
        monkeypatch.setattr(scraper_ux, "_choose_model_from_api",
                            lambda browser, config: ("SENTINEL", "n", "w", "c"))
        config = {"customer_key": "customerc"}

        result = scraper_ux._select_model(None, config)

        out = capsys.readouterr().out
        assert "customerc" in out
        assert "not filtered" in out.lower() or "account-wide" in out.lower()
        assert result == ("SENTINEL", "n", "w", "c")


class TestNuxOutputLocation:
    def test_default_output_folder_is_the_customers_UI_folder(
            self, registered, answers, monkeypatch, tmp_path):
        import os
        monkeypatch.setattr(registry, "REPO_ROOT", str(tmp_path))
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        monkeypatch.delenv("ANAPLAN_OUTPUT_FOLDER", raising=False)
        answers(["2", "", "", "", ""])            # customerb, accept defaults
        config = scraper_ux._collect_config()
        parts = os.path.normpath(config["output_folder"]).split(os.sep)
        assert parts[-3:] == ["customers", "CustomerB", "UI"]

    def test_default_is_per_customer_not_one_shared_folder(
            self, registered, answers, monkeypatch, tmp_path):
        """Two customers' NUX reports must not pile into one directory: the
        filenames carry only the model name, and model names collide across
        customers ('Data Hub')."""
        monkeypatch.setattr(registry, "REPO_ROOT", str(tmp_path))
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        monkeypatch.delenv("ANAPLAN_OUTPUT_FOLDER", raising=False)
        answers(["1", "", "", "", ""])
        a = scraper_ux._collect_config()["output_folder"]
        answers(["2", "", "", "", ""])
        b = scraper_ux._collect_config()["output_folder"]
        assert a != b

    def test_explicit_answer_still_overrides_the_default(
            self, registered, answers, monkeypatch, tmp_path):
        """A scratch run outside the vault must stay possible - it is how a
        first scrape gets diffed before promotion (spec decision 17)."""
        import os
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        answers(["1", "", "", str(tmp_path / "scratch"), ""])
        config = scraper_ux._collect_config()
        # Compared via os.path.normpath, not raw string equality: _ask()
        # always runs the answer through _normalise_path (backslash ->
        # forward slash), which on Windows makes str(tmp_path / "scratch")
        # (backslash-separated) never literally equal the returned value even
        # though it names the same directory. normpath makes the comparison
        # separator-agnostic without weakening what is actually asserted -
        # that the explicit answer, not the customer default, won.
        assert os.path.normpath(config["output_folder"]) == os.path.normpath(str(tmp_path / "scratch"))

    def test_the_folder_is_created(self, registered, answers, monkeypatch, tmp_path):
        import os
        monkeypatch.setattr(registry, "REPO_ROOT", str(tmp_path))
        monkeypatch.setenv("ANAPLAN_USERNAME", "u@example.com")
        monkeypatch.setenv("ANAPLAN_PASSWORD", "pw")
        monkeypatch.delenv("ANAPLAN_OUTPUT_FOLDER", raising=False)
        answers(["1", "", "", "", ""])
        assert os.path.isdir(scraper_ux._collect_config()["output_folder"])
