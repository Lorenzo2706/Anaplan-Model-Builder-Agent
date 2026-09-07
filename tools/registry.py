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
import dataclasses
import os
import re
from dataclasses import dataclass


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


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Anaplan app shards follow one uniform host pattern, so the URL is DERIVED
# rather than looked up - onboarding a customer on a new shard must not
# require a code edit. KNOWN_SHARDS is only a hint list for error messages and
# for the wizard's menu; it is deliberately NOT a gate, so a shard Anaplan adds
# tomorrow works today.
KNOWN_SHARDS = ("eu1a", "eu2a", "eu3", "eu4", "us1a", "us2a", "ca1a", "ap1a")

_SHARD_RE = re.compile(r"^[a-z]{2}\d{1,2}[a-z]?$")


def app_url_for_shard(shard):
    """Return the app-shard base URL for `shard` (e.g. 'eu3').

    Raises ValueError on anything that is not a bare shard token. There is
    deliberately NO default: the pre-Pass-1 `.get(env, ANAPLAN_URLS[<one
    shard>])` meant a typo'd or missing shard logged into whichever tenant the
    default named and exported the wrong model into the requested folder.
    """
    token = (shard or "").strip().lower()
    if not _SHARD_RE.match(token):
        raise ValueError(
            f"{shard!r} is not an Anaplan shard token (expected e.g. 'eu2a', "
            f"'eu3'; known: {', '.join(KNOWN_SHARDS)}). Pass the bare shard, "
            f"not a URL or hostname."
        )
    return f"https://{token}.app.anaplan.com/"


@dataclass(frozen=True)
class ResolvedModel:
    """One fully resolved model: customer fields merged with model fields.

    Frozen because it is passed through six call sites across three modules
    and read on both sides of a browser login. Seven of its fields are opaque
    strings, four of them GUIDs, so an accidental mutation mid-flow would be
    invisible - it would present as a successful export of the wrong model.
    """
    shortcut: str
    customer_key: str
    model_key: str
    name: str
    display_name: str
    raw_dir: str
    folder: str
    shard: str
    customer_id: str
    workspace_id: str
    model_id: str
    engine: str = "unknown"
    workspace_label: str = "PRODUCTION"

    @property
    def app_url(self):
        return app_url_for_shard(self.shard)

    @property
    def settings_url(self):
        """The model-settings URL. Single definition: this string was once
        duplicated in three functions, so every shard or path change had to be
        applied three times and kept in sync."""
        base = self.app_url.rstrip("/")
        return (f"{base}/a/modeling/customers/{self.customer_id}"
                f"/workspaces/{self.workspace_id}/models/{self.model_id}"
                f"/model-settings")

    @property
    def default_out_dir(self):
        """Where this model's CSVs live in the vault. Derived from folder +
        raw_dir, NEVER from the display name: the two legitimately differ (a
        shortcut named 'modela' exports into a folder called 'ModelA 2.0')."""
        return os.path.join(REPO_ROOT, "customers", self.folder,
                            "raw", "models", self.raw_dir)

    @property
    def nux_out_dir(self):
        """Where this customer's NUX Excel reports land (spec decision 12).
        A peer of raw/, not inside it: raw/ is immutable source material and
        a NUX report is generated output."""
        return os.path.join(REPO_ROOT, "customers", self.folder, "UI")


_RESOLVED_FIELDS = tuple(f.name for f in dataclasses.fields(ResolvedModel))


def resolve(key, flat, customer=None, name=None):
    """Resolve `key` against a flattened registry into a ResolvedModel.

    `key` is either a composite "customer:model" or a bare model key. A bare
    key resolves only when it is unique across every customer (see aliases());
    otherwise this raises and lists the candidates, because picking one is a
    wrong-tenant operation.

    `customer` disambiguates a bare key. Combining it with a composite key
    that names a DIFFERENT customer is a contradiction and raises - silently
    honouring one of the two is how a deliberate --customer gate is bypassed.

    `name` overrides display_name only. It never reaches the output folder.
    """
    if not key:
        raise ValueError("no model key given")

    if ":" in key:
        ckey, _, mkey = key.partition(":")
        if customer and customer != ckey:
            raise ValueError(
                f"--customer {customer!r} contradicts the customer in "
                f"{key!r} ({ckey!r}). Pass one or the other, not both."
            )
        shortcut = key
    elif customer:
        known = sorted({e["customer_key"] for e in flat.values()})
        if customer not in known:
            raise ValueError(
                f"{customer!r} is not a configured customer. Available: "
                f"{known}"
            )
        shortcut = f"{customer}:{key}"
    else:
        alias = aliases(flat).get(key)
        if alias is None:
            candidates = sorted(s for s, e in flat.items()
                                if e["model_key"] == key)
            if candidates:
                raise ValueError(
                    f"{key!r} is ambiguous - {len(candidates)} customers "
                    f"configure a model with that key: {candidates}. Pass the "
                    f"composite key, or --customer."
                )
            raise ValueError(
                f"'{key}' is not a configured shortcut. Available: "
                f"{sorted(flat)}. Raw model_id lookups need a workspace, a "
                f"shard and a customer folder that cannot be safely inferred; "
                f"add the model to CUSTOMERS in models.py first."
            )
        shortcut = alias

    if shortcut not in flat:
        raise ValueError(
            f"'{shortcut}' is not a configured shortcut. Available: "
            f"{sorted(flat)}."
        )

    entry = flat[shortcut]
    app_url_for_shard(entry["shard"])          # fail here, not mid-login
    fields = {k: entry[k] for k in _RESOLVED_FIELDS if k in entry}
    fields["display_name"] = name or entry["name"]
    return ResolvedModel(**fields)


def resolve_out_dir(resolved, out_dir=None):
    """Resolve the export destination for a ResolvedModel.

    An explicit --out is created if absent (it is routinely a scratch dir).
    The derived vault path must ALREADY exist: creating it would mean a typo in
    raw_dir silently produces a second, wrong-named folder alongside the real
    one, and a run that reports success while the wiki still points at the old
    folder.
    """
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        return out_dir

    path = resolved.default_out_dir
    if not os.path.isdir(path):
        raise ValueError(
            f"export folder {path!r} does not exist. Check "
            f"{resolved.shortcut!r}'s 'raw_dir' ({resolved.raw_dir!r}) and "
            f"'folder' ({resolved.folder!r}) against the vault, or pass --out "
            f"explicitly for a scratch export."
        )
    return path
