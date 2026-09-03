"""
scrape_model_data.py
---------------------
Merged Anaplan model-settings exporter. Default mode retrieves most files through
Anaplan HTTP APIs; the browser is used for login and the few grids that still
require the model-settings UI.

Why this exists
---------------
The pure-Selenium fallback drives the model-settings Dojo UI grid-by-grid (navigate
nested iframes → click nav/sub-tab → Export… → Run Export → wait for a CSV
download), 13 times per model. That is slow. This module pulls the same data
from Anaplan HTTP APIs instead:

  • **5 files via the REST API v2** (`/2/0/models/{id}/...`) as JSON over plain
    `requests` — Line Items (rich: formula/format/applies-to/summary/cell-count/
    referenced-by), Versions, Actions, Imports, Views.
  • **2 files via the Selenium model-settings UI export** — Modules and General
    Lists. The REST API returns these two too sparse to use (Modules: id+name
    only, so every stat/metadata column is blank; General Lists: no Top Level,
    Parent Hierarchy, or dependency-graph "Referenced in…" columns), and the
    classic core-webapp API can't drive them reliably (the client references
    open grids by view index and the UI export is an un-interceptable form
    download, so no dependable viewDefinition template exists — a wrong template
    silently exports the wrong grid). The Selenium export is byte-for-byte
    identical to Anaplan's own export, so these two core files are always correct.
  • **8 legacy grids via the classic core-webapp API** (`--full`) — Line Item
    Subsets, Time Ranges, Source Models, Roles + Roles Modules/Versions/Lists/
    Actions. These have no REST endpoint (they live in the classic core engine),
    but the engine's own HTTP protocol is driven directly — jsonrpc
    VIEW_REQUEST_SET → PROGRESS → servlet?taskType=export — via fetch() inside the
    core-webapp iframe. No UI clicking. See the _LEGACY_TEMPLATES block below for
    the mechanism. A legacy grid that fails this path falls back to
    this script's UI export path for that one grid.

Authentication
--------------
The REST API v2 calls are **fully head-less** — no browser involved. They
authenticate the documented Integration-API way:

    POST https://auth.anaplan.com/token/authenticate   (Authorization: Basic ...)
      -> tokenInfo.tokenValue
    GET  https://api.anaplan.com/2/0/...               (Authorization: AnaplanAuthToken ...)

History / why this changed (2026-08-14). An earlier version of this module tried
to authenticate the REST calls by lifting the logged-in browser's session
cookies into a `requests.Session` and calling the **app shard**
(`eu2a.app.anaplan.com/2/0/...`). That worked until ~2026-08-07 and then began
returning `401 {"status":{"code":401,"message":"Not Authenticated."}}` for every
endpoint. Diagnosed live 2026-08-14: the app shard now redirects `/2/0/` to the
global `us1a` endpoint, which accepts only Integration-API auth and rejects web
session cookies. Confirmed dead from *every* transport — same-origin in-page
fetch, `requests` + lifted cookies, `api.anaplan.com` + cookies, and plain
browser navigation all returned the identical 401 — and the Anaplan web client
never calls `/2/0/` itself, so there was no client header to replay. A prior note
in this file claimed Basic auth was disabled for the Integration API on this
tenant (FAILURE_BAD_CREDENTIAL, observed 2026-07-15); that is **not** true as of
2026-08-14 — the token exchange above succeeds and every endpoint returns 200.

The browser is therefore needed only for:
  • the Selenium model-settings UI export (Modules, General Lists), and
  • the classic core-webapp API calls for the 8 legacy grids (`--full`),
both of which are driven from a real authenticated session. Use `--rest-only`
to run the 5 REST files with no browser at all.

Modes
-----
  default     → 7 fast files (5 REST + Modules & General Lists via UI export).
  --full      → all 15 files (5 REST + Modules & General Lists via UI + 8
                classic-API). A legacy grid that fails the classic-API path
                falls back to this script's UI export path for that one grid,
                so coverage never regresses.
  --rest-only → just the 5 Integration-API files. No browser, no Selenium —
                the fastest way to refresh formulas/structure, and the isolated
                path to test when the REST pull misbehaves.

Column fidelity: the produced CSVs reuse the exact blueprint column layout (first
header cell blank, first data column = entity name). Modules, General Lists, and
the 8 legacy files are byte-for-byte the same grids the UI exports (verified equal
to the reference). Within the REST-derived Line Items.csv, a few columns the REST
API does not expose (Populated Cell Count, Memory Used, Calculation Complexity/
Effort, Read/Write Access Driver, Users List, Parent, Code, Data Tags) are left
blank. `wiki-data-ingestion` parses everything identically.

Usage
-----
    python tools/scrape_model_data.py modela --name "ModelA"             # 7 fast files
    python tools/scrape_model_data.py modela --name "ModelA" --full      # all 15 files
    python tools/scrape_model_data.py modela --name "ModelA" --ui-only   # pure UI fallback

As a library:

    from scrape_model_data import download_model_exports_api, download_model_exports_full
    download_model_exports_full("modela", out_dir=r"raw/models/ModelA")
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile
import time
from glob import glob

import requests
from selenium.webdriver.common.by import By

# import order matters: scraper_ux loads .env before models reads env-backed IDs.
import scraper_ux
import models

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The 8 legacy-engine grids that the REST API v2 does NOT expose. Default
# (REST-only) mode skips them and reports them as such; --full retrieves them
# over the classic core-webapp API. Listed so a default run never silently looks
# "complete" when these 8 blueprint grids are absent.
API_UNAVAILABLE = [
    "Line Item Subsets.csv", "Time Ranges.csv", "Source Models.csv",
    "Roles.csv", "Roles Modules.csv", "Roles Versions.csv",
    "Roles Lists.csv", "Roles Actions.csv",
]

# Two blueprint grids that the REST API v2 delivers UNUSABLY sparse and that
# cannot be pulled over the classic core-webapp API either (the client references
# open grids by view index, and the UI export is a form-submit download — neither
# exposes the grid's viewDefinition, so no reliable classic-API template exists;
# a wrong template silently exports the wrong grid, which is unacceptable for
# these core files). They are therefore ALWAYS produced via the proven Selenium
# model-settings UI export (byte-for-byte identical to Anaplan's own export),
# in both default and --full modes. Expressed as UI export
# (nav_label, subtab_label, filename) targets.
#   • Modules       — REST /modules returns id+name only, so every stat/metadata
#                     column (Applies To, Time Scale, Cell Count, Referenced By,
#                     …) came out blank.
#   • General Lists — REST /lists lacks Top Level, Parent Hierarchy, and the
#                     dependency-graph columns (Referenced in Applies To / as
#                     Format / in Formula), which only the classic engine computes.
UI_ONLY_TARGETS = [
    ("Modules", "Modules", "Modules.csv"),
    ("General lists", None, "General Lists.csv"),
]

EXPORT_TARGETS = [
    ("Modules", "Modules", "Modules.csv"),
    ("Modules", "Line Items", "Line Items.csv"),
    ("Line item subsets", None, "Line Item Subsets.csv"),
    ("General lists", None, "General Lists.csv"),
    ("Versions", None, "Versions.csv"),
    ("Time", "Time Ranges", "Time Ranges.csv"),
    ("Actions", "Actions", "Actions.csv"),
    ("Source models", None, "Source Models.csv"),
    ("Users", "Roles", "Roles.csv"),
    ("Users", "Roles -> Modules", "Roles Modules.csv"),
    ("Users", "Roles -> Versions", "Roles Versions.csv"),
    ("Users", "Roles -> Lists", "Roles Lists.csv"),
    ("Users", "Roles -> Actions", "Roles Actions.csv"),
]


# Anaplan app shards follow one uniform host pattern, so the URL is DERIVED
# rather than looked up — onboarding a customer on a new shard must not require
# a code edit. KNOWN_SHARDS is only a hint list for error messages (and, in
# Pass 2, the interactive wizard's menu); it is deliberately NOT a gate, so a
# shard Anaplan adds tomorrow works today.
KNOWN_SHARDS = ("eu1a", "eu2a", "eu3", "eu4", "us1a", "us2a", "ca1a", "ap1a")

_SHARD_RE = re.compile(r"^[a-z]{2}\d{1,2}[a-z]?$")


def app_url_for_shard(shard):
    """Return the app-shard base URL for `shard` (e.g. 'eu3').

    Raises ValueError on anything that is not a bare shard token. There is
    deliberately NO default: the previous `.get(env, ANAPLAN_URLS["eu2a"])`
    meant a typo'd or missing shard logged into whichever tenant the default
    named and exported the wrong model into the requested folder.
    """
    token = (shard or "").strip().lower()
    if not _SHARD_RE.match(token):
        raise ValueError(
            f"{shard!r} is not an Anaplan shard token (expected e.g. 'eu2a', "
            f"'eu3'; known: {', '.join(KNOWN_SHARDS)}). Pass the bare shard, "
            f"not a URL or hostname."
        )
    return f"https://{token}.app.anaplan.com/"


# ============================================================================
#  Selenium model-settings UI helpers
# ============================================================================

def enter_shell(browser, timeout=25):
    """default_content -> outer shell iframe. Left-nav lives here."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            browser.switch_to.default_content()
            outer = (browser.find_elements(By.CSS_SELECTOR, 'iframe[data-testid="shell-content"]')
                     or browser.find_elements(By.TAG_NAME, "iframe"))
            if not outer:
                time.sleep(0.5)
                continue
            browser.switch_to.frame(outer[0])
            body = browser.execute_script("return document.body ? document.body.innerText : ''") or ""
            if any(k in body for k in ("Modules", "General lists", "Versions")):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def enter_grid(browser, timeout=25):
    """default -> outer shell iframe -> inner grid iframe. Toolbar/tabs/dialog live here."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            browser.switch_to.default_content()
            outer = (browser.find_elements(By.CSS_SELECTOR, 'iframe[data-testid="shell-content"]')
                     or browser.find_elements(By.TAG_NAME, "iframe"))
            if not outer:
                time.sleep(0.5)
                continue
            browser.switch_to.frame(outer[0])
            inner = browser.find_elements(By.TAG_NAME, "iframe")
            if not inner:
                time.sleep(0.5)
                continue
            browser.switch_to.frame(inner[0])
            if browser.execute_script("return !!document.querySelector('.dijitButtonText');"):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def click_visible(browser, text, timeout=8, contains_all=None):
    """Click the first visible element whose normalized text matches."""
    end = time.time() + timeout
    if contains_all:
        xp = "//*[self::span or self::div or self::button or @role='tab' or @role='button' or self::a]"
    else:
        xp = (f"//span[normalize-space()='{text}'] | //*[@role='button'][normalize-space()='{text}'] "
              f"| //button[normalize-space()='{text}'] | //div[normalize-space()='{text}'] "
              f"| //*[@role='tab'][normalize-space()='{text}']")
    while time.time() < end:
        for el in browser.find_elements(By.XPATH, xp):
            try:
                if not el.is_displayed():
                    continue
                t = " ".join((el.text or "").split())
                if contains_all and not all(p in t for p in contains_all):
                    continue
                browser.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.1)
                try:
                    el.click()
                except Exception:
                    browser.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                continue
        time.sleep(0.3)
    return False


def _alnum(s):
    return "".join(ch for ch in (s or "").lower() if ch.isalnum())


def click_tab(browser, label, timeout=10):
    """Click a Dojo grid sub-tab by label."""
    want = _alnum(label)
    xp = ("//*[@role='tab'] | //*[contains(@class,'tabLabel')] "
          "| //*[contains(@class,'dijitTab')]")
    end = time.time() + timeout
    while time.time() < end:
        for el in browser.find_elements(By.XPATH, xp):
            try:
                if not el.is_displayed():
                    continue
                if _alnum(el.text) == want:
                    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    time.sleep(0.1)
                    try:
                        el.click()
                    except Exception:
                        browser.execute_script("arguments[0].click();", el)
                    return True
            except Exception:
                continue
        time.sleep(0.3)
    return False


def _export_one_target(browser, download_dir, nav_label, subtab_label, out_filename):
    """
    Navigate to one (nav_label, subtab_label) grid and export it to CSV.
    Returns {"ok": bool, "saved_path": str|None, "raw_name": str|None,
             "error": str|None}. Never raises.
    """
    result = {"ok": False, "saved_path": None, "raw_name": None, "error": None}
    tag = f"[{nav_label}" + (f" > {subtab_label}]" if subtab_label else "]")

    def fail(msg):
        result["error"] = msg
        print(f"  {tag} failed: {msg}")
        return result

    try:
        if not enter_shell(browser):
            return fail("no shell")
        if not click_visible(browser, nav_label, 10):
            return fail("nav not found")
        time.sleep(2)

        if not enter_grid(browser):
            return fail("no grid iframe")

        if subtab_label:
            if not click_tab(browser, subtab_label, 10):
                return fail("subtab not found")
            time.sleep(2)
            enter_grid(browser, 10)

        before = set(glob(os.path.join(download_dir, "*")))
        if not click_visible(browser, "Export...", 10):
            return fail("Export button not found")
        time.sleep(3)
        enter_grid(browser, 10)
        if not click_visible(browser, "Run Export", 10):
            return fail("Run Export not found")

        downloaded = scraper_ux._wait_for_download(download_dir, before, timeout=90)
        if not downloaded:
            return fail("no download")

        result["raw_name"] = os.path.basename(downloaded)
        result["saved_path"] = downloaded
        result["ok"] = True

        try:
            size = os.path.getsize(downloaded)
            print(f"  {tag} downloaded '{result['raw_name']}' ({size} bytes)")
        except OSError:
            print(f"  {tag} downloaded '{result['raw_name']}'")

        return result

    except Exception as e:
        return fail(f"unexpected error: {e}")


REQUIRED_ENTRY_KEYS = ("name", "raw_dir", "folder", "shard",
                       "customer_id", "workspace_id", "model_id")


def _resolve_model(model, name=None):
    """Resolve a models.MODELS shortcut key into a fully merged entry dict.

    Returns a dict (not the old 4-tuple) because an entry now carries the
    shard, the vault folder and the raw export folder in addition to the three
    GUIDs — seven fields, four of them opaque GUID strings, is exactly the
    shape where positional unpacking silently swaps a tenant.
    """
    configured = getattr(models, "MODELS", {})
    if model not in configured:
        raise ValueError(
            f"'{model}' is not a configured shortcut in models.MODELS "
            f"({sorted(configured)}). Raw model_id lookups need a workspace and "
            f"shard that cannot be safely inferred; add an entry to models.py "
            f"with folder, shard, raw_dir, customer_id, workspace_id and "
            f"model_id, then pass its key here."
        )

    entry = dict(configured[model])
    missing = [k for k in REQUIRED_ENTRY_KEYS if not entry.get(k)]
    if missing:
        raise ValueError(
            f"models.MODELS['{model}'] is missing {missing}. Every entry must "
            f"declare its own shard, folder and raw_dir — there is no global "
            f"default for any of them."
        )

    app_url_for_shard(entry["shard"])          # fail here, not mid-login
    entry["display_name"] = name or entry["name"]
    return entry


def settings_url(entry):
    """The model-settings URL for a resolved entry. Single definition: this
    string was previously duplicated in three functions, so every shard or
    path change had to be applied three times and kept in sync."""
    base = app_url_for_shard(entry["shard"]).rstrip("/")
    return (f"{base}/a/modeling/customers/{entry['customer_id']}"
            f"/workspaces/{entry['workspace_id']}/models/{entry['model_id']}"
            f"/model-settings")


def default_out_dir(entry, repo_root=REPO_ROOT):
    """Where this model's CSVs live in the vault. Derived from the entry's
    folder + raw_dir, NEVER from the display name: the two legitimately differ
    (a shortcut named 'UMD' exports into a folder called 'AAC')."""
    return os.path.join(repo_root, "customers", entry["folder"],
                        "raw", "models", entry["raw_dir"])


def resolve_out_dir(entry, out_dir=None, repo_root=REPO_ROOT):
    """Resolve the export destination.

    An explicit --out is created if absent (it is routinely a scratch dir).
    The derived vault path must already exist: creating it would mean a typo in
    raw_dir silently produces a second, wrong-named folder alongside the real
    one, and a run that reports success while the wiki still points at the old
    folder.
    """
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        return out_dir

    path = default_out_dir(entry, repo_root)
    if not os.path.isdir(path):
        raise ValueError(
            f"export folder {path!r} does not exist. Check "
            f"models.MODELS['...']['raw_dir'] ({entry['raw_dir']!r}) and "
            f"['folder'] ({entry['folder']!r}) against the vault, or pass "
            f"--out explicitly for a scratch export."
        )
    return path


def _build_config(shard):
    """Browser/login config for one shard. `shard` is REQUIRED and comes from
    the resolved model entry — never from a global env var."""
    use_sso = os.getenv("ANAPLAN_USE_SSO", "false").strip().lower() in ("1", "true", "yes")
    return {
        "main_url": app_url_for_shard(shard),
        "username": os.getenv("ANAPLAN_USERNAME", ""),
        "password": os.getenv("ANAPLAN_PASSWORD", ""),
        "use_basic_auth": not use_sso,
        "output_folder": tempfile.gettempdir(),
    }


def list_available_models(shard):
    """Log in to `shard` and fetch every model visible to this account,
    independent of models.MODELS. Used to bootstrap a customer's registry
    entry, so it must not require one."""
    config = _build_config(shard)
    download_dir = tempfile.mkdtemp(prefix="anaplan_list_models_")
    browser = None
    try:
        browser = scraper_ux._create_browser(download_dir)
        scraper_ux.login(browser, config)

        main_url = config["main_url"]
        data = scraper_ux.api_get(
            browser,
            f"{main_url}/a/springboard-platform-gateway-service/models?limit=50000&offset=0",
        )
        items = data.get("items", []) or []

        out = []
        for m in items:
            ws_guid = m.get("CurrentWorkspaceGuid") or m.get("WorkspaceGuid", "")
            customer = m.get("CustomerGuid") or m.get("TenantGuid", "")
            if not customer and ws_guid:
                try:
                    ws_resp = scraper_ux.api_get(browser, f"{main_url}/1/3/workspaces/{ws_guid}")
                    customer = ws_resp.get("workspace", {}).get("customerId", "")
                except Exception:
                    pass
            out.append({
                "model_name": m.get("ModelName"),
                "model_id": m.get("ModelGuid"),
                "workspace_name": m.get("CurrentWorkspaceName") or m.get("WorkspaceName") or "Unknown workspace",
                "workspace_id": ws_guid,
                "customer_id": customer,
            })
        out.sort(key=lambda m: (m["workspace_name"] or "", m["model_name"] or ""))
        return out
    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception:
                pass
        shutil.rmtree(download_dir, ignore_errors=True)


def download_model_exports(model, out_dir=None, headless_download_dir=None, name=None):
    """
    Pure-Selenium fallback: export all 13 model-settings grids through the UI.
    """
    entry = _resolve_model(model, name=name)
    model_id = entry["model_id"]
    model_name = entry["display_name"]

    out_dir = resolve_out_dir(entry, out_dir)

    download_dir = headless_download_dir or tempfile.mkdtemp(prefix="anaplan_scrape_")
    own_download_dir = headless_download_dir is None

    config = _build_config(entry["shard"])
    url = settings_url(entry)

    results = {}
    browser = None

    try:
        print(f"\n{'=' * 70}")
        print(f"  Anaplan pure-UI model export - {model_name}")
        print(f"{'=' * 70}")
        print(f"  Settings URL : {url}")
        print(f"  Output dir   : {out_dir}\n")

        browser = scraper_ux._create_browser(download_dir)
        browser.set_script_timeout(120)

        scraper_ux.login(browser, config)

        print("  Opening model-settings shell...")
        browser.get(url)

        if not enter_shell(browser, timeout=30):
            raise RuntimeError(
                "Could not enter the model-settings iframe after navigating "
                "to the settings URL; check the URL/credentials/model IDs."
            )

        for nav_label, subtab_label, out_filename in EXPORT_TARGETS:
            grid_result = _export_one_target(
                browser, download_dir, nav_label, subtab_label, out_filename
            )

            if grid_result["ok"]:
                dest_path = os.path.join(out_dir, out_filename)
                try:
                    if os.path.exists(dest_path):
                        os.remove(dest_path)
                    shutil.move(grid_result["saved_path"], dest_path)
                    grid_result["saved_path"] = dest_path
                except Exception as e:
                    grid_result["ok"] = False
                    grid_result["error"] = f"downloaded but failed to move file: {e}"
                    print(f"    could not move to {dest_path}: {e}")

            results[out_filename] = grid_result

    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception:
                pass
        if own_download_dir:
            shutil.rmtree(download_dir, ignore_errors=True)

    ok_count = sum(1 for r in results.values() if r["ok"])
    print(f"\n{'=' * 70}")
    print(f"  {ok_count}/{len(EXPORT_TARGETS)} exported")
    for out_filename, r in results.items():
        marker = "ok" if r["ok"] else "--"
        detail = r["saved_path"] if r["ok"] else r["error"]
        print(f"    {marker} {out_filename:<22} {detail}")
    print(f"{'=' * 70}\n")

    return results


# ══════════════════════════════════════════════════════════════════════════════
#  Integration API v2 session (token auth, no browser)
# ══════════════════════════════════════════════════════════════════════════════

# The Integration API is served from this global host. NOT the regional app shard
# (eu2a/us1a/...): the app shard redirects /2/0/ to the global endpoint, which
# rejects web-session cookies with 401. See the Authentication note at the top.
API_BASE = "https://api.anaplan.com"

AUTH_TOKEN_URL = "https://auth.anaplan.com/token/authenticate"


def _anaplan_token():
    """Exchange the .env credentials for an Integration-API bearer token.

    Returns the token string. Raises RuntimeError with the tenant's own
    statusMessage on failure, so a credential/permission problem is never
    mistaken for "the model has no data".
    """
    import base64

    user = os.getenv("ANAPLAN_USERNAME", "")
    pwd = os.getenv("ANAPLAN_PASSWORD", "")
    if not user or not pwd:
        raise RuntimeError(
            "ANAPLAN_USERNAME / ANAPLAN_PASSWORD missing from .env — required for "
            "the Integration API token exchange."
        )
    basic = base64.b64encode(f"{user}:{pwd}".encode("utf-8")).decode("ascii")
    try:
        r = requests.post(AUTH_TOKEN_URL,
                          headers={"Authorization": f"Basic {basic}"}, timeout=60)
    except Exception as e:
        raise RuntimeError(f"token endpoint unreachable: {e}") from e

    body = {}
    try:
        body = r.json()
    except Exception:
        pass
    token = ((body.get("tokenInfo") or {}).get("tokenValue")
             if isinstance(body, dict) else None)
    if not token:
        raise RuntimeError(
            f"Integration API token exchange failed (HTTP {r.status_code}, "
            f"statusMessage={body.get('statusMessage')!r}). Basic auth may be "
            f"disabled for the Integration API on this tenant, or the .env "
            f"credentials are wrong/expired. Do NOT retry blindly — repeated "
            f"failures can lock the account."
        )
    return token


def _api_session():
    """A requests.Session pre-authenticated for https://api.anaplan.com/2/0/.

    No browser required. The token is valid ~30 min, which comfortably covers a
    full export run.
    """
    sess = requests.Session()
    sess.headers.update({
        "Authorization": f"AnaplanAuthToken {_anaplan_token()}",
        "Accept": "application/json",
    })
    return sess


def _get(sess, url):
    """GET url and return parsed JSON.

    Raises RuntimeError on any non-200 / non-JSON response. This is deliberate:
    the previous version swallowed every failure into `{}`, so a 401 produced a
    valid-but-EMPTY CSV that silently overwrote good data while still reporting
    "ok" (this is exactly how the 2026-08-13 export lost 5 files). A failed pull
    must be loud.
    """
    try:
        r = sess.get(url, timeout=180)
    except Exception as e:
        raise RuntimeError(f"GET {url} failed: {e}") from e
    if r.status_code != 200:
        raise RuntimeError(f"GET {url} -> HTTP {r.status_code}: {r.text[:200]}")
    if "json" not in r.headers.get("Content-Type", ""):
        raise RuntimeError(
            f"GET {url} -> non-JSON response "
            f"(Content-Type={r.headers.get('Content-Type')!r}): {r.text[:200]}"
        )
    return r.json()


def _list_field(body):
    """Return the first list value in a dict body (the payload array), or []."""
    if not isinstance(body, dict):
        return []
    for v in body.values():
        if isinstance(v, list):
            return v
    return []


# ══════════════════════════════════════════════════════════════════════════════
#  Small formatting helpers
# ══════════════════════════════════════════════════════════════════════════════

def _names(seq):
    """Join a list of {"id","name"} (or plain strings) into 'a, b, c'."""
    out = []
    for x in seq or []:
        if isinstance(x, dict):
            out.append(str(x.get("name", "")))
        else:
            out.append(str(x))
    return ", ".join(n for n in out if n)


def _b(v):
    """Blueprint-style boolean text (Anaplan writes lowercase true/false)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    return "" if v is None else str(v)


def _write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  Per-file builders (return (header, rows))
# ══════════════════════════════════════════════════════════════════════════════

# Column layout copied verbatim from the Selenium export so ingestion is identical.
LINE_ITEM_HEADER = [
    "", "Format", "Formula", "Summary", "Applies To", "Time Scale", "Time Range",
    "Versions", "Style", "Cell Count", "Populated Cell Count", "Memory Used",
    "Calculation Complexity", "Calculation Effort", "Notes", "Read Access Driver",
    "Write Access Driver", "Users List", "Parent", "Is Summary", "Formula Scope",
    "Code", "Use Switchover", "Breakback", "Start of Section", "Data Tags",
    "Referenced By", "Module Name",
]

def build_line_items(sess, base, model_id):
    body = _get(sess, f"{base}/2/0/models/{model_id}/lineItems?includeAll=true")
    items = _list_field(body)
    rows = []
    for li in items:
        ver = li.get("version") or {}
        rows.append([
            li.get("name", ""),
            li.get("format", ""),
            li.get("formula", ""),
            li.get("summary", ""),
            _names(li.get("appliesTo")),
            li.get("timeScale", ""),
            li.get("timeRange", ""),
            ver.get("name", "") if isinstance(ver, dict) else _b(ver),
            li.get("style", ""),
            _b(li.get("cellCount")),
            "", "", "", "",                      # populated/memory/complexity/effort — n/a
            li.get("notes", ""),
            "", "", "", "",                      # read/write driver, users list, parent — n/a
            _b(li.get("isSummary")),
            li.get("formulaScope", ""),
            "",                                  # code — n/a
            _b(li.get("useSwitchover")),
            _b(li.get("breakback")),
            _b(li.get("startOfSection")),
            "",                                  # data tags — n/a
            _names(li.get("referencedBy")),
            li.get("moduleName", ""),
        ])
    return LINE_ITEM_HEADER, rows


def build_versions(sess, base, model_id):
    body = _get(sess, f"{base}/2/0/models/{model_id}/versions")
    vers = _list_field(body)
    header = ["", "Current", "Actual", "Switchover", "Formula",
              "Edit From", "Edit To", "Notes"]
    rows = []
    for v in vers:
        ef = v.get("editFrom") or {}
        et = v.get("editTo") or {}
        rows.append([
            v.get("name", ""),
            _b(v.get("isCurrent")),
            _b(v.get("isActual")),
            "",                                  # Switchover — n/a
            "",                                  # Formula — n/a
            ef.get("periodText", "") if isinstance(ef, dict) else "",
            et.get("periodText", "") if isinstance(et, dict) else "",
            "",                                  # Notes — n/a
        ])
    return header, rows


def build_actions(sess, base, model_id):
    """Combined action inventory (processes/imports/exports/actions), name+type.
    The rich blueprint columns (durations, used-in-processes/dashboards) are not
    in the API."""
    header = ["", "Type"]
    rows = []
    for atype in ("processes", "imports", "exports", "actions"):
        body = _get(sess, f"{base}/2/0/models/{model_id}/{atype}")
        for a in _list_field(body):
            rows.append([a.get("name", ""), atype])
    return header, rows


def build_imports(sess, base, model_id):
    body = _get(sess, f"{base}/2/0/models/{model_id}/imports")
    imports = _list_field(body)
    files_body = _get(sess, f"{base}/2/0/models/{model_id}/files")
    files = {f.get("id"): f.get("name", "") for f in _list_field(files_body)}
    header = ["", "Import Type", "Source (file/view id)", "Source File Name"]
    rows = []
    for imp in imports:
        ds = imp.get("importDataSourceId", "")
        rows.append([
            imp.get("name", ""),
            imp.get("importType", ""),
            ds,
            files.get(ds, ""),
        ])
    return header, rows


def build_views(sess, base, model_id):
    body = _get(sess, f"{base}/2/0/models/{model_id}/views")
    views = _list_field(body)
    header = ["", "ID", "Module ID", "Code"]
    rows = [[v.get("name", ""), v.get("id", ""), v.get("moduleId", ""), v.get("code", "")]
            for v in views]
    return header, rows


# ══════════════════════════════════════════════════════════════════════════════
#  Public API
# ══════════════════════════════════════════════════════════════════════════════

def _pull_api_files(sess, base, model_id, out_dir, results):
    """Write the 5 genuinely-REST-covered CSVs into out_dir, recording status in
    `results`. Modules.csv and General Lists.csv are NOT here — the REST API
    delivers them too sparse to use, so they are produced via the Selenium UI
    export (see UI_ONLY_TARGETS / _export_targets_via_ui)."""
    def emit(filename, builder):
        path = os.path.join(out_dir, filename)
        try:
            header, rows = builder()
        except Exception as e:
            # Do NOT write anything: leave any existing file for this name intact
            # rather than replacing good data with an empty CSV.
            results[filename] = {"ok": False, "rows": None, "path": None, "error": str(e)}
            print(f"  [API] ERR {filename:22} {e}")
            print(f"  [API]     -> {filename} left untouched (not overwritten)")
            return

        # Defense in depth: a 0-row pull is legitimate for a genuinely empty grid,
        # but must never silently clobber a file that already has content.
        if not rows and os.path.exists(path) and os.path.getsize(path) > 200:
            results[filename] = {
                "ok": False, "rows": 0, "path": None,
                "error": ("pulled 0 rows but existing file is non-empty — refusing "
                          "to overwrite; re-run or verify the model really is empty"),
            }
            print(f"  [API] ERR {filename:22} 0 rows vs non-empty existing file "
                  f"-> left untouched")
            return

        _write_csv(path, header, rows)
        results[filename] = {"ok": True, "rows": len(rows), "path": path, "error": None}
        print(f"  [API] ok  {filename:22} {len(rows):>5} rows")

    emit("Line Items.csv", lambda: build_line_items(sess, base, model_id))
    emit("Versions.csv",   lambda: build_versions(sess, base, model_id))
    emit("Actions.csv",    lambda: build_actions(sess, base, model_id))
    emit("Imports.csv",    lambda: build_imports(sess, base, model_id))
    emit("Views.csv",      lambda: build_views(sess, base, model_id))


def _export_targets_via_ui(browser, settings_url, download_dir, out_dir,
                           targets, results, max_tries=3):
    """Export a list of (nav_label, subtab_label, filename) grids via the proven
    Selenium model-settings UI export, moving each download into out_dir. Retries
    up to max_tries, re-opening the model-settings shell each attempt. Records
    per-file status in `results`. Never raises.

    This is the reliable path for grids that neither the REST API nor the classic
    core-webapp API can deliver correctly (see UI_ONLY_TARGETS). It is also reused
    as the per-grid fallback for legacy grids that fail the classic-API path.
    """
    import shutil
    pending = list(targets)
    for attempt in range(1, max_tries + 1):
        if not pending:
            break
        browser.get(settings_url)
        if not enter_shell(browser, timeout=30):
            print(f"  [UI]  -- attempt {attempt}: could not open model-settings shell")
            continue
        still_pending = []
        for nav_label, subtab_label, fn in pending:
            gr = _export_one_target(browser, download_dir, nav_label, subtab_label, fn)
            if gr["ok"] and gr.get("saved_path"):
                dest = os.path.join(out_dir, fn)
                try:
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.move(gr["saved_path"], dest)
                    results[fn] = {"ok": True, "rows": None, "path": dest, "error": None}
                    print(f"  [UI]  ok  {fn:22} (Selenium export)")
                except Exception as e:
                    results[fn] = {"ok": False, "rows": None, "path": None,
                                   "error": f"downloaded but move failed: {e}"}
                    still_pending.append((nav_label, subtab_label, fn))
            else:
                results[fn] = {"ok": False, "rows": None, "path": None,
                               "error": gr.get("error")}
                still_pending.append((nav_label, subtab_label, fn))
        pending = still_pending


def _print_summary(model_name, results, mode):
    produced = sum(1 for r in results.values() if r["ok"])
    print(f"\n{'=' * 70}")
    print(f"  {model_name} — {mode}: {produced} files produced")
    for fn, r in results.items():
        mark = "ok " if r["ok"] else "-- "
        detail = (f"{r['rows']} rows" if r["ok"] and r["rows"] is not None
                  else (r["error"] or ""))
        print(f"    {mark}{fn:24} {detail}")
    print(f"{'=' * 70}\n")


def download_model_exports_api(model, out_dir=None, name=None, rest_only=False):
    """Log in once (browser), then export the fast subset of model files:
      • 5 files over the REST API v2 (plain HTTP) — Line Items, Versions,
        Actions, Imports, Views.
      • Modules + General Lists via the Selenium model-settings UI export, because
        the REST API delivers those two too sparse to use (see UI_ONLY_TARGETS).
    The 8 legacy grids in API_UNAVAILABLE are reported as not produced here
    (use --full for those).

    Returns dict keyed by output filename -> {"ok", "rows", "path", "error"}.
    """
    entry = _resolve_model(model, name=name)
    model_id = entry["model_id"]
    model_name = entry["display_name"]
    out_dir = resolve_out_dir(entry, out_dir)
    config = _build_config(entry["shard"])

    url = settings_url(entry)

    print(f"\n{'=' * 70}")
    print(f"  Anaplan API model export — {model_name}")
    print(f"{'=' * 70}")
    print(f"  Output dir : {out_dir}")
    print(f"  (5 files over the Integration API — no browser"
          f"{'' if rest_only else '; Modules + General Lists via UI export'})\n")

    results = {}

    # ── Phase 1: REST pull over the Integration API (token auth, no browser) ───
    sess = _api_session()
    _pull_api_files(sess, API_BASE, model_id, out_dir, results)

    if rest_only:
        _print_summary(model_name, results, "REST-only mode")
        return results

    # ── Phase 2: Modules + General Lists via the proven Selenium UI export ─────
    download_dir = tempfile.mkdtemp(prefix="anaplan_api_login_")
    browser = None
    try:
        browser = scraper_ux._create_browser(download_dir)
        browser.set_script_timeout(120)
        scraper_ux.login(browser, config)

        print(f"\n  → Exporting {len(UI_ONLY_TARGETS)} grid(s) via the model-"
              f"settings UI (REST too sparse): "
              f"{', '.join(fn for _n, _s, fn in UI_ONLY_TARGETS)}")
        _export_targets_via_ui(browser, url, download_dir, out_dir,
                               UI_ONLY_TARGETS, results)
    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception:
                pass
        import shutil
        shutil.rmtree(download_dir, ignore_errors=True)

    for fn in API_UNAVAILABLE:
        results[fn] = {"ok": False, "rows": None, "path": None,
                       "error": "not in REST API v2 — run --full (classic core-webapp API)"}
    _print_summary(model_name, results, "API + UI mode")
    return results


# The 8 legacy-engine-only grids, expressed as EXPORT_TARGETS
# (nav_label, subtab_label, filename). These cannot be pulled from the REST API
# (proven: served only by the classic core-webapp jsonrpc/servlet). --full mode
# drives them over that classic API directly (no UI clicking) — see below.
_LEGACY_TARGETS = [t for t in EXPORT_TARGETS if t[2] in set(API_UNAVAILABLE)]


# ══════════════════════════════════════════════════════════════════════════════
#  Legacy-grid export over the classic core-webapp API (jsonrpc + servlet)
# ══════════════════════════════════════════════════════════════════════════════
#
# The 8 legacy grids live in the classic core engine (core-webapp-<ws> on the eu4
# shard). There is no REST endpoint, but the engine's own HTTP protocol can be
# driven directly — no Dojo UI clicking — once a browser session exists:
#
#   1. POST .../anaplan/jsonrpc  {requestType:"VIEW_REQUEST_SET", viewRequests:[
#        {viewIndex:-1, viewGuid:<new>, viewDefinition:<grid template>, ...}],
#        activeViewIndices:[], modelDefinitionSerialNumber:<n>, clientSessionId:<s>}
#      → returns the opened view's `viewIndex`.
#   2. POST .../anaplan/jsonrpc  {requestType:"PROGRESS", activeViewIndices:[viewIndex]}
#      → returns a `taskId`.
#   3. POST .../anaplan/servlet?taskType=export (multipart: taskId, entityId=<grid>,
#        viewDefinition, fileType=CSV, ...) → streams the grid CSV (text/csv).
#
# A MINIMAL VIEW_REQUEST_SET (empty carried view-state) is sufficient — proven
# live against all 8 grids. `entityId` (= the grid name, i.e. the filename minus
# ".csv") is the primary driver; `viewDefinition` is the model-INDEPENDENT
# template below (system identifiers `_SYSTEM_AXIS_IDENTIFIER.*` / `_2000000xxx_`
# / `_4000xxxxx_` only — no per-model data), captured once and reused for any
# model. `modelDefinitionSerialNumber` + `clientSessionId` ARE per-session and
# are scraped from the client's own first jsonrpc call at run time.
#
# The fetch() calls run inside the eu4 core-webapp iframe (via execute_async_
# script) so the browser session cookies + origin are supplied automatically.

_LEGACY_TEMPLATES = json.loads(r'''
{
  "Time Ranges.csv": {"entityId": "Time Ranges", "viewDefinition": {"name": "Time Ranges", "type": "MODEL_DEFINITION", "rowAxisSpecification": {"axisDefinitionIdentifier": "_20000000068_", "axisDefinition": null}, "columnAxisSpecification": {"axisDefinitionIdentifier": "_20000000069_", "axisDefinition": null}, "pageAxisSpecifications": [], "useDefaultPageOrder": true, "columnSizes": {"customRowLabelWidthsByDimension": [], "defaultColumnWidth": 150, "rowLabelWidth": 0, "customWidthsByStyle": [], "customWidthsByLineItem": []}, "pageContext": "SINGLE"}},
  "Line Item Subsets.csv": {"entityId": "Line Item Subsets", "viewDefinition": {"name": "Line Item Subsets", "type": "MODEL_DEFINITION", "rowAxisSpecification": {"axisDefinitionIdentifier": "_20000000041_", "axisDefinition": null}, "columnAxisSpecification": {"axisDefinitionIdentifier": "_20000000042_", "axisDefinition": null}, "pageAxisSpecifications": [], "useDefaultPageOrder": true, "columnSizes": {"customRowLabelWidthsByDimension": [], "defaultColumnWidth": 150, "rowLabelWidth": 0, "customWidthsByStyle": [], "customWidthsByLineItem": []}, "pageContext": "SINGLE"}},
  "Source Models.csv": {"entityId": "Source Models", "viewDefinition": {"name": "Source Models", "type": "MODEL_DEFINITION", "rowAxisSpecification": {"axisDefinitionIdentifier": "_20000000064_", "axisDefinition": null}, "columnAxisSpecification": {"axisDefinitionIdentifier": "_20000000065_", "axisDefinition": null}, "pageAxisSpecifications": [], "useDefaultPageOrder": true, "columnSizes": {"customRowLabelWidthsByDimension": [], "defaultColumnWidth": 75, "rowLabelWidth": 400, "customWidthsByStyle": [], "customWidthsByLineItem": []}, "pageContext": "SINGLE"}},
  "Roles.csv": {"entityId": "Roles", "viewDefinition": {"name": "Roles", "type": "MODEL_DEFINITION", "columnSizes": {"defaultColumnWidth": 150, "customRowLabelWidthsByDimension": [], "customWidthsByLineItem": [], "customWidthsByStyle": []}, "rows": "_SYSTEM_AXIS_IDENTIFIER.FULL_ACCESS_WITH_CUSTOM_MODEL_ROLE", "columns": "_SYSTEM_AXIS_IDENTIFIER.MODEL_ROLE_PROPERTY", "pages": []}},
  "Roles Modules.csv": {"entityId": "Roles Modules", "viewDefinition": {"name": "Roles Modules", "type": "MODEL_DEFINITION", "staticContextIdentifiers": ["_4000001000_"], "columnSizes": {"defaultColumnWidth": 150, "customRowLabelWidthsByDimension": [], "customWidthsByLineItem": [], "customWidthsByStyle": []}, "rows": "_SYSTEM_AXIS_IDENTIFIER.MODULE_ALL", "columns": "_SYSTEM_AXIS_IDENTIFIER.MODEL_ROLE", "pages": []}},
  "Roles Versions.csv": {"entityId": "Roles Versions", "viewDefinition": {"name": "Roles Versions", "type": "MODEL_DEFINITION", "staticContextIdentifiers": ["_4000001000_"], "columnSizes": {"defaultColumnWidth": 150, "customRowLabelWidthsByDimension": [], "customWidthsByLineItem": [], "customWidthsByStyle": []}, "rows": "_SYSTEM_AXIS_IDENTIFIER.VERSION_ALL", "columns": "_SYSTEM_AXIS_IDENTIFIER.MODEL_ROLE", "pages": []}},
  "Roles Lists.csv": {"entityId": "Roles Lists", "viewDefinition": {"name": "Roles Lists", "type": "MODEL_DEFINITION", "staticContextIdentifiers": ["_4000001001_"], "columnSizes": {"defaultColumnWidth": 150, "customRowLabelWidthsByDimension": [], "customWidthsByLineItem": [], "customWidthsByStyle": []}, "rows": "_SYSTEM_AXIS_IDENTIFIER.HIERARCHY_NOUSER", "columns": "_SYSTEM_AXIS_IDENTIFIER.MODEL_ROLE", "pages": []}},
  "Roles Actions.csv": {"entityId": "Roles Actions", "viewDefinition": {"name": "Roles Actions", "type": "MODEL_DEFINITION", "staticContextIdentifiers": ["_4000001002_"], "columnSizes": {"defaultColumnWidth": 150, "customRowLabelWidthsByDimension": [], "customWidthsByLineItem": [], "customWidthsByStyle": []}, "rows": "_SYSTEM_AXIS_IDENTIFIER.ACTION_WITH_HEADING", "columns": "_SYSTEM_AXIS_IDENTIFIER.MODEL_ROLE", "pages": []}}
}
''')

# JS run inside the eu4 iframe: VIEW_REQUEST_SET -> PROGRESS -> servlet, returning
# {vrs_status, viewIndex, taskId, servlet_status, ct, csv} (csv = full text).
_LEGACY_CHAIN_JS = r"""
const p = arguments[0], done = arguments[1];
const rand = () => { let s=''; for(let i=0;i<26;i++) s+='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'[Math.floor(Math.random()*62)]; return s; };
const guid = () => 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'.replace(/X/g, () => '0123456789ABCDEF'[Math.floor(Math.random()*16)]);
const vrs = {
  modelId:p.model_id, modelDefinitionSerialNumber:p.mdsn, requestType:'VIEW_REQUEST_SET', workspaceId:p.ws,
  submissions:[], viewRequests:[{
    workspaceId:p.ws,
    dataPageRequests:[{startRow:0,startColumn:0,rowCount:-1,columnCount:-1}],
    rowLabelPageRequests:[{start:0,count:-1}], columnLabelPageRequests:[{start:0,count:-1}],
    cellSelectorLabelsRequired:false, pageSelectorLabelsRequired:false,
    serialNumbers:{breakbackHeldCellsSerialNumber:'-1',columnAxisSerialNumber:'-1',dataSerialNumber:'-1',pageInfoSerialNumber:'-1',rowAxisSerialNumber:'-1',viewDefinitionSerialNumber:'-1'},
    viewIndex:-1, viewGuid:guid(), containerEntityLongId:-1, state:{}, modelId:p.model_id, viewDefinition:p.vd
  }], systemActions:[], fetchAllModelSummaries:false, clientSessionId:p.csid, activeViewIndices:[], txid:rand(), includeDetailsInErrorInfo:true
};
const out = {};
fetch(p.jsonrpc,{method:'POST',credentials:'include',headers:{'Content-Type':'application/json'},body:JSON.stringify(vrs)})
 .then(r=>r.text().then(t=>{ out.vrs_status=r.status; let vi=null; try{vi=JSON.parse(t).result.viewRequestResults[0].viewIndex;}catch(e){out.vrs=t.slice(0,300);} out.viewIndex=vi;
   if(vi===null){ done(out); return; }
   const prog={workspaceId:p.ws,requestType:'PROGRESS',modelId:p.model_id,activeViewIndices:[vi],txid:rand(),includeDetailsInErrorInfo:true};
   return fetch(p.jsonrpc,{method:'POST',credentials:'include',headers:{'Content-Type':'application/json'},body:JSON.stringify(prog)})
    .then(r2=>r2.text().then(t2=>{ let tid=null; try{tid=JSON.parse(t2).taskId;}catch(e){} out.taskId=tid; if(!tid){out.prog=t2.slice(0,300); done(out); return;}
      const fd=new FormData();
      const f={taskType:'export',context:JSON.stringify({workspaceId:p.ws,modelId:p.model_id,modelName:null}),
        taskId:tid,entityId:p.entityId,moduleId:'',exportLayout:'GRID_CURRENT_PAGE',fileType:'CSV',formattingEnabled:'false',
        omitSummaries:'false',useFormatSettings:'false',omitEmptyRows:'false',withBOM:'false',filter0LineItemEntityLongId:'-1',
        filter1LineItemEntityLongId:'-1',listDimensionColumnSelection:'{}',listFormattedCellPropertySelection:'{}',
        includeRowLabelHeaders:'false',sharingOption:'0',entityLongIdOfShare:'',viewDefinition:JSON.stringify(p.vd)};
      for(const k in f) fd.append(k,f[k]);
      return fetch(p.servlet,{method:'POST',credentials:'include',body:fd})
       .then(r3=>r3.text().then(t3=>{ out.servlet_status=r3.status; out.ct=r3.headers.get('content-type'); out.csv=t3; done(out); }));
    }));
 })).catch(e=>{ out.error=String(e); done(out); });
"""

# Hook that records the client's own jsonrpc request bodies, so we can scrape the
# per-session modelDefinitionSerialNumber + clientSessionId from a VIEW_REQUEST_SET.
_SESSION_HOOK_JS = r"""
window.__cap = window.__cap || [];
if (!window.__hooked) {
  window.__hooked = true;
  const S = XMLHttpRequest.prototype.send, O = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(m,u){ this.__u=u; return O.apply(this,arguments); };
  XMLHttpRequest.prototype.send = function(b){ if(this.__u && this.__u.indexOf('jsonrpc')>=0 && b) window.__cap.push(String(b)); return S.apply(this,arguments); };
}
return 'ok';
"""


def _capture_session_params(browser):
    """Inside the eu4 grid iframe, install the jsonrpc hook and nudge the client
    into issuing a VIEW_REQUEST_SET (by re-opening a nav item), then scrape the
    per-session modelDefinitionSerialNumber + clientSessionId. Returns (mdsn,
    csid) or (None, None)."""
    browser.execute_script(_SESSION_HOOK_JS)
    # Nudge the classic client to emit a VIEW_REQUEST_SET we can read.
    enter_shell(browser)
    for nudge in ("Versions", "General lists", "Modules"):
        if click_visible(browser, nudge, 6):
            break
    time.sleep(2)
    enter_grid(browser, 12)
    for b in browser.execute_script("return window.__cap || [];"):
        try:
            j = json.loads(b)
        except Exception:
            continue
        if j.get("requestType") == "VIEW_REQUEST_SET":
            return j.get("modelDefinitionSerialNumber"), j.get("clientSessionId")
    return None, None


def _pull_legacy_via_api(browser, base, model_id, ws, out_dir, results):
    """Export the 8 legacy grids over the classic core-webapp API (jsonrpc +
    servlet), driven by fetch() inside the eu4 iframe — no UI navigation. The
    browser must already be on the model-settings page (shell entered)."""
    jsonrpc = f"https://eu4.app.anaplan.com/core-webapp-{ws}/anaplan/jsonrpc"
    servlet = f"https://eu4.app.anaplan.com/core-webapp-{ws}/anaplan/servlet?taskType=export"

    if not enter_grid(browser, 20):
        for fn in _LEGACY_TEMPLATES:
            results[fn] = {"ok": False, "rows": None, "path": None,
                           "error": "could not enter core-webapp iframe"}
        return
    mdsn, csid = _capture_session_params(browser)
    if mdsn is None or csid is None:
        for fn in _LEGACY_TEMPLATES:
            results[fn] = {"ok": False, "rows": None, "path": None,
                           "error": "could not capture session params (mdsn/csid)"}
        return

    enter_grid(browser, 12)  # ensure we're in the eu4 iframe for fetch()
    for fn, tpl in _LEGACY_TEMPLATES.items():
        params = {"model_id": model_id, "ws": ws, "mdsn": mdsn, "csid": csid,
                  "jsonrpc": jsonrpc, "servlet": servlet,
                  "vd": tpl["viewDefinition"], "entityId": tpl["entityId"]}
        try:
            res = browser.execute_async_script(_LEGACY_CHAIN_JS, params)
        except Exception as e:
            results[fn] = {"ok": False, "rows": None, "path": None, "error": f"chain exec error: {e}"}
            print(f"  [CLS] ERR {fn:22} {e}")
            continue
        csv_text = res.get("csv")
        ok = (res.get("servlet_status") == 200 and "csv" in str(res.get("ct")) and csv_text)
        if ok:
            path = os.path.join(out_dir, fn)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_text)
            n = csv_text.count("\n")
            results[fn] = {"ok": True, "rows": n, "path": path, "error": None}
            print(f"  [CLS] ok  {fn:22} {n:>5} lines")
        else:
            err = (res.get("error") or f"vrs={res.get('vrs_status')} "
                   f"servlet={res.get('servlet_status')} ct={res.get('ct')}")
            results[fn] = {"ok": False, "rows": None, "path": None, "error": err}
            print(f"  [CLS] ERR {fn:22} {err}")


def download_model_exports_full(model, out_dir=None, name=None):
    """Full 15-file export in ONE browser login:
      • Phase 1 — the 5 REST-API files over the Integration API (token auth,
        no browser involved).
      • Phase 2 — the 8 legacy grids over the classic core-webapp API
        (jsonrpc VIEW_REQUEST_SET → PROGRESS → servlet), driven by fetch()
        inside the eu4 iframe. No Dojo UI navigation.
      • Phase 3 — Modules and General Lists via the Selenium model-settings UI
        export (the REST API delivers them too sparse; see UI_ONLY_TARGETS).
    Any legacy grid that fails the classic-API path falls back to the
    local UI export path for that one grid, so coverage never regresses.
    """
    entry = _resolve_model(model, name=name)
    model_id = entry["model_id"]
    model_name = entry["display_name"]
    workspace_id = entry["workspace_id"]
    out_dir = resolve_out_dir(entry, out_dir)
    config = _build_config(entry["shard"])
    base = config["main_url"].rstrip("/")
    url = settings_url(entry)

    print(f"\n{'=' * 70}")
    print(f"  Anaplan FULL model export (API-driven) — {model_name}")
    print(f"{'=' * 70}")
    print(f"  Output dir : {out_dir}")
    print(f"  REST API for 5 files; classic core-webapp API for "
          f"{len(_LEGACY_TEMPLATES)} legacy files; UI export for "
          f"{len(UI_ONLY_TARGETS)} (Modules, General Lists).\n")

    download_dir = tempfile.mkdtemp(prefix="anaplan_full_")
    browser = None
    results = {}
    try:
        # ── Phase 1: REST pull over the Integration API (token auth, no browser)
        sess = _api_session()
        _pull_api_files(sess, API_BASE, model_id, out_dir, results)

        browser = scraper_ux._create_browser(download_dir)
        browser.set_script_timeout(120)
        scraper_ux.login(browser, config)

        # ── Phase 2: legacy grids over the classic core-webapp API (no UI) ──────
        print(f"\n  → Exporting {len(_LEGACY_TEMPLATES)} legacy grids over the "
              f"classic core-webapp API...")
        browser.get(url)
        if not enter_shell(browser, timeout=30):
            for fn in _LEGACY_TEMPLATES:
                results[fn] = {"ok": False, "rows": None, "path": None,
                               "error": "could not open model-settings shell"}
        else:
            _pull_legacy_via_api(browser, base, model_id, workspace_id, out_dir, results)

        # ── Phase 2b: UI-export fallback for any legacy grid the API missed ─────
        failed = [t for t in _LEGACY_TARGETS
                  if not results.get(t[2], {}).get("ok")]
        if failed:
            print(f"\n  → UI-export fallback for {len(failed)} legacy grid(s): "
                  f"{', '.join(fn for _n, _s, fn in failed)}")
            _export_targets_via_ui(browser, url, download_dir, out_dir,
                                   failed, results)

        # ── Phase 3: Modules + General Lists via the proven Selenium UI export ──
        print(f"\n  → Exporting {len(UI_ONLY_TARGETS)} grid(s) via the model-"
              f"settings UI (REST too sparse): "
              f"{', '.join(fn for _n, _s, fn in UI_ONLY_TARGETS)}")
        _export_targets_via_ui(browser, url, download_dir, out_dir,
                               UI_ONLY_TARGETS, results)
    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception:
                pass
        import shutil
        shutil.rmtree(download_dir, ignore_errors=True)

    _print_summary(model_name, results, "FULL mode (API-driven)")
    return results


# ══════════════════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════════════════

def _main(argv=None):
    p = argparse.ArgumentParser(
        description="API-driven Anaplan model export. Default mode produces 7 "
                    "fast files: 5 over the REST API v2 (HTTP) plus Modules and "
                    "General Lists via the Selenium model-settings UI export (the "
                    "REST API delivers those two too sparse to use). --full "
                    "additionally exports the 8 legacy-engine files (Line Item "
                    "Subsets, Time Ranges, Source Models, Roles×5) over the "
                    "classic core-webapp API — a complete 15-file export in one "
                    "browser login. Use --ui-only for the original full "
                    "Selenium UI export path.")
    p.add_argument(
        "model",
        nargs="?",
        default=None,
        help="Shortcut key from models.MODELS (e.g. 'modela'). Omit when using --list-models.",
    )
    p.add_argument("--name", default=None,
                   help="Display name for console output only. It does NOT select "
                        "the output folder — that comes from the entry's folder + "
                        "raw_dir (or --out).")
    p.add_argument("--out", default=None, help="Output directory for the CSV files.")
    p.add_argument("--full", action="store_true",
                   help="Also export the 8 legacy-engine files over the classic "
                        "core-webapp API (complete 15-file export). Omit for the "
                        "7-file fast subset.")
    p.add_argument("--ui-only", action="store_true",
                   help="Run the original pure-Selenium 13-grid exporter from this merged script.")
    p.add_argument("--rest-only", action="store_true",
                   help="Export ONLY the 5 Integration-API files (Line Items, "
                        "Versions, Actions, Imports, Views). No browser at all.")
    p.add_argument("--list-models", action="store_true",
                   help="Log in, fetch every model visible to this account, print JSON, and exit.")
    p.add_argument("--shard", default=None,
                   help="Anaplan shard to log into for --list-models (e.g. eu3). "
                        "Required with --list-models, which has no registry entry "
                        "to read a shard from.")
    args = p.parse_args(argv)

    if args.list_models:
        if not args.shard:
            p.error("--list-models requires --shard (e.g. --shard eu3): there is "
                    "no registry entry to infer the shard from")
        print(json.dumps(list_available_models(args.shard), indent=2))
        sys.exit(0)

    if not args.model:
        p.error("model is required unless --list-models is passed")

    if args.ui_only:
        results = download_model_exports(args.model, out_dir=args.out, name=args.name)
        produced = sum(1 for r in results.values() if r["ok"])
        sys.exit(0 if produced == len(EXPORT_TARGETS) else 1)

    if args.full:
        results = download_model_exports_full(args.model, out_dir=args.out, name=args.name)
        expected = None
    else:
        results = download_model_exports_api(args.model, out_dir=args.out,
                                             name=args.name, rest_only=args.rest_only)
        expected = 5 if args.rest_only else None

    produced = sum(1 for r in results.values() if r["ok"])
    if expected is not None:
        # --rest-only has a known target count, so a partial pull is a failure —
        # never exit 0 on a half-empty export.
        sys.exit(0 if produced == expected else 1)
    sys.exit(0 if produced else 1)


if __name__ == "__main__":
    _main()
