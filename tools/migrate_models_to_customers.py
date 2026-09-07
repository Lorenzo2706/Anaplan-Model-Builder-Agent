"""Print a CUSTOMERS block equivalent to a legacy flat models.MODELS.

READ-ONLY. Prints to stdout; never writes models.py. models.py is gitignored,
so a bad in-place transform is unrecoverable - review the output, then paste.

    python tools/migrate_models_to_customers.py > customers-block.py

Customer keys are derived from each entry's `folder`, lowercased with
non-alphanumerics collapsed to '_'. Engine and workspace_label are NOT
inferable from the old shape and are emitted as TODO comments: fill them from
customers/registry.md.
"""
import os
import pprint
import re
import sys

# os.path.dirname(os.path.abspath(__file__)), not __file__.rsplit("/", 1):
# on Windows __file__ carries backslashes, so a rsplit on "/" does not split
# and the whole file path lands on sys.path, making `import models` fail.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# This script reads the LEGACY models.py, which resolves every GUID through
# os.getenv() at import time - the exact 2026-08-14 "models/None" mechanism
# this migration exists to remove. So .env has to be in os.environ BEFORE
# `import models` below, or every workspace_id/model_id/customer_id comes out
# None and the emitted CUSTOMERS block has to be filled in by hand, defeating
# the point of the script. DO NOT let an import-sorter move `import models`
# above this call. This is the last tool that needs the dance: once the user
# has pasted the block, models.py holds literals and nothing reads the
# environment to build the registry again.
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        print("python-dotenv is not installed, so .env cannot be read. Every "
              "GUID in the output will be empty. Install it and re-run: "
              "pip install python-dotenv", file=sys.stderr)
        return False

load_dotenv()

import models  # noqa: E402

CUSTOMER_FIELDS = ("shard", "folder", "customer_id")
MODEL_FIELDS = ("name", "raw_dir", "workspace_id", "model_id")


def customer_key(folder):
    return re.sub(r"[^a-z0-9]+", "_", (folder or "").lower()).strip("_")


def main():
    flat = getattr(models, "MODELS", None)
    if not flat:
        print("models.MODELS is empty or absent - nothing to migrate.",
              file=sys.stderr)
        return 1

    tree = {}
    for shortcut, entry in flat.items():
        folder = entry.get("folder")
        if not folder:
            print(f"SKIPPED {shortcut!r}: no 'folder' key, so its customer "
                  f"cannot be determined. Add it by hand.", file=sys.stderr)
            continue
        ckey = customer_key(folder)
        cust = tree.setdefault(ckey, {"name": folder, "models": {}})
        for field in CUSTOMER_FIELDS:
            value = entry.get(field)
            if value and cust.setdefault(field, value) != value:
                print(f"CONFLICT on {ckey}.{field}: {cust[field]!r} vs "
                      f"{value!r} (from {shortcut!r}). Kept the first; check "
                      f"which is right.", file=sys.stderr)
        cust["models"][shortcut] = {f: entry.get(f, "") for f in MODEL_FIELDS}

    print("# Review before pasting into tools/models.py.")
    print("# TODO: add \"engine\": \"Classic\" | \"Polaris\" and, where it")
    print("# applies, \"workspace_label\": \"DEV\" to each model. Neither is")
    print("# inferable from the old shape; customers/registry.md has both.")
    print("CUSTOMERS = " + pprint.pformat(tree, width=88, sort_dicts=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
