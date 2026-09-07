"""Customer-first registry for the Anaplan scraper toolchain.

WHY THIS MODULE EXISTS, AND WHY THE DATA IS NOT IN IT

    The registry's *data* lives in `tools/models.py`, which is gitignored: it
    holds tenant GUIDs and customer folder names. Its *logic* lives here,
    which is tracked, because logic in a gitignored file cannot be tested by
    a tracked test, cannot be reviewed, and has to be re-copied by hand into
    every clone from models.py.example.

    So: models.py is one `CUSTOMERS` dict and nothing else. This module knows
    the shape and is the only thing that does.

WHY THE CUSTOMER IS THE UNIT

    The pre-Pass-2 registry was flat, one dict per model, each repeating its
    customer's shard, folder and tenant GUID. Repetition is how a customer's
    models drift apart: one entry gets a corrected shard and the others keep
    the stale one, which presents as a login into the wrong tenant. Here a
    customer declares those once and its models inherit them.

WHY KEYS ARE COMPOSITE ("customera:modela")

    Model names are not unique across customers - "Data Hub" is close to
    universal. Bare model keys would collide, and dict construction resolves a
    collision by silently keeping the last one, which is a wrong-tenant export
    with no error. `aliases()` still offers a bare key, but ONLY where it is
    unambiguous across every customer.

EVERYTHING HERE IS PURE

    flatten(), aliases() and check_not_legacy() take their input as a
    parameter and import nothing from `models`. That keeps them testable with
    placeholder data and lets this module load on a clone whose models.py has
    not been migrated yet.
"""
import copy
import re


# Required on every customer. No defaults: a missing shard or folder cannot be
# guessed, and guessing means operating on the wrong tenant (spec decision 4).
CUSTOMER_KEYS = ("name", "shard", "folder", "customer_id")

# Required on every model.
MODEL_KEYS = ("name", "raw_dir", "workspace_id", "model_id")

# Present on every flattened entry, defaulted when the author omits them.
# `engine` defaults to "unknown" rather than to either engine: a wrong engine
# label is a formula-correctness hazard, "unknown" is visibly wrong.
OPTIONAL_MODEL_KEYS = {"engine": "unknown", "workspace_label": "PRODUCTION"}

# Customer and model keys become halves of a "customer:model" composite, so
# neither may contain ':' or whitespace.
_KEY_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class LegacyRegistryError(Exception):
    """models.py is still the pre-Pass-2 flat shape.

    Its own class, not a ValueError, because it is the one error whose fix is
    "edit your gitignored file" rather than "fix the code" - callers print its
    message and exit rather than treating it as a bug.
    """


def _check_key(kind, key):
    if not isinstance(key, str) or not _KEY_RE.match(key):
        raise ValueError(
            f"{kind} key {key!r} is not usable: keys become halves of a "
            f"'customer:model' composite, so they must be non-empty and "
            f"contain only letters, digits, '_', '.' or '-'."
        )


def flatten(customers):
    """Expand a CUSTOMERS tree into fully merged per-model entries.

    Returns {"<customer_key>:<model_key>": entry}, where each entry carries
    every customer field, every model field, the two optional defaults, and
    `customer_key` / `model_key` / `shortcut` for error messages.

    A model may override an inherited customer field (a second workspace on a
    different shard is legal); the model's own value wins.
    """
    flat = {}
    for ckey, cust in (customers or {}).items():
        _check_key("customer", ckey)
        if not isinstance(cust, dict):
            raise ValueError(f"customer {ckey!r} is not a dict")

        missing = [k for k in CUSTOMER_KEYS if not cust.get(k)]
        if missing:
            raise ValueError(
                f"customer {ckey!r} is missing {missing}. Every customer must "
                f"declare its own name, shard, folder and customer_id - there "
                f"is no global default for any of them."
            )
        if "models" not in cust:
            raise ValueError(
                f"customer {ckey!r} has no 'models' key. Add "
                f"\"models\": {{}} even if none are configured yet."
            )

        inherited = {k: v for k, v in cust.items() if k != "models"}
        for mkey, model in (cust["models"] or {}).items():
            _check_key("model", mkey)
            if not isinstance(model, dict):
                raise ValueError(f"model {ckey}:{mkey!r} is not a dict")

            shortcut = f"{ckey}:{mkey}"
            missing = [k for k in MODEL_KEYS if not model.get(k)]
            if missing:
                raise ValueError(
                    f"model {shortcut!r} is missing {missing}. Every model "
                    f"must declare its own name, raw_dir, workspace_id and "
                    f"model_id."
                )

            entry = copy.deepcopy(inherited)
            entry.update(copy.deepcopy(model))
            for k, default in OPTIONAL_MODEL_KEYS.items():
                entry.setdefault(k, default)
            entry["customer_key"] = ckey
            entry["model_key"] = mkey
            entry["shortcut"] = shortcut
            flat[shortcut] = entry
    return flat


def aliases(flat):
    """Bare model key -> composite key, for keys unique across all customers.

    A model key used by two customers gets NO alias. Resolving a colliding
    bare key to whichever customer happened to be first is precisely the
    wrong-tenant failure composite keys exist to prevent.
    """
    seen = {}
    for shortcut, entry in flat.items():
        seen.setdefault(entry["model_key"], []).append(shortcut)
    return {mkey: shortcuts[0]
            for mkey, shortcuts in seen.items()
            if len(shortcuts) == 1}


def check_not_legacy(models_module):
    """Raise LegacyRegistryError if `models_module` is the pre-Pass-2 shape.

    models.py is gitignored, so no commit can migrate a user's copy. Refusing
    loudly with the migration instructions is the only way the change reaches
    them - a `.get("CUSTOMERS", ...)` fallback would instead present as an
    empty registry and "unknown shortcut" for every model.
    """
    if getattr(models_module, "CUSTOMERS", None) is not None:
        return
    if getattr(models_module, "MODELS", None):
        raise LegacyRegistryError(
            "tools/models.py still uses the pre-Pass-2 flat MODELS dict. The "
            "registry is now a customer-first CUSTOMERS tree: each customer "
            "declares name/shard/folder/customer_id once and nests its models "
            "under a 'models' key, so per-model repetition of the shard and "
            "tenant GUID is gone. Copy the shape from tools/models.py.example "
            "and move each model's workspace_id/model_id under its customer. "
            "models.py is gitignored, so this migration cannot be done for "
            "you by a commit."
        )
