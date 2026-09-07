"""
Anaplan NUX Scraper
-------------------
Run the script, log in, choose a model — done.

Output: Excel file with 5 sheets:
  - All Views
  - Actions Usage Report
  - Views Usage Report
  - Modules Usage Count
  - Actions <model name>

Requirements: pip install selenium openpyxl webdriver-manager python-dotenv
              Microsoft Edge (driver is downloaded automatically)

Configuration: copy .env.example to .env and fill in your own values.
"""

import csv
import getpass
import glob
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import time

from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.edge.service import Service as EdgeService

load_dotenv()

import models

try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    _WDM_AVAILABLE = True
except ImportError:
    _WDM_AVAILABLE = False

# Windows consoles/redirected output often default to cp1252, which can't
# encode the box-drawing/emoji characters printed throughout this script.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — Configuration via interactive prompts
# ══════════════════════════════════════════════════════════════════════════════

ANAPLAN_URLS = {
    "eu2a": "https://eu2a.app.anaplan.com/",
}

# springboard-definition-service (pages/boards) is a single global service,
# always hosted here regardless of which regional shard the model lives on.
SDS_HOST = "https://us1a.app.anaplan.com"

# ── User defaults, sourced from .env (see .env.example) ───────────────────────
# All personal/environment values live in .env, not here. Any value left unset
# in .env falls back to being prompted for interactively.
DEFAULTS = {
    "username":       os.getenv("ANAPLAN_USERNAME", ""),
    "environment":    os.getenv("ANAPLAN_ENVIRONMENT", "eu2a"),
    "use_sso":        os.getenv("ANAPLAN_USE_SSO", "false").strip().lower() in ("1", "true", "yes"),
    "output_folder":  os.getenv("ANAPLAN_OUTPUT_FOLDER", ""),
}
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Anaplan NUX Reports")


def _safe_filename(value: str, fallback: str = "model") -> str:
    """Return a Windows-safe filename fragment."""
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(value)).strip(" ._")
    return safe or fallback


def _safe_sheet_title(value: str, fallback: str = "Sheet") -> str:
    """Return an Excel-safe worksheet title."""
    safe = re.sub(r"[\[\]:*?/\\]", "_", str(value)).strip()
    return (safe or fallback)[:31]


def _separator(char="─", width=60):
    print(char * width)


def _header(title: str):
    _separator("═")
    print(f"  {title}")
    _separator("═")


def _ask(prompt: str, default: str = "") -> str:
    """Ask the user for input, with an optional default value."""
    if default:
        answer = input(f"{prompt} [{default}]: ").strip()
        return answer if answer else default
    return input(f"{prompt}: ").strip()


def _normalise_path(p: str) -> str:
    """Convert backslashes to forward slashes so Windows paths always work."""
    return p.replace("\\", "/")


def _ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "[Y/N, default=Y]" if default else "[Y/N, default=N]"
    answer = input(f"{prompt} {hint}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def _ask_choice(options: list[str], prompt: str = "Choose an option") -> int:
    """Display a numbered list and return the chosen index (0-based)."""
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    while True:
        try:
            choice = int(input(f"\n{prompt}: ")) - 1
            if 0 <= choice < len(options):
                return choice
        except ValueError:
            pass
        print("  Invalid choice, please try again.")


def _collect_config() -> dict:
    """
    Interactive wizard to collect all required configuration.
    Values in DEFAULTS are pre-filled so the user can just press Enter.
    Returns a dict with: main_url, username, password, use_basic_auth, output_folder.
    """
    _header("Anaplan NUX Scraper — Setup")
    print()
    print("This script logs into Anaplan and exports model data to Excel.")
    print("Answer the questions below. Press Enter to accept the default value.")
    print()

    # ── Environment ───────────────────────────────────────────────────────────
    _separator()
    print("STEP 1 of 4 — Anaplan environment")
    _separator()
    url_keys  = list(ANAPLAN_URLS.keys())
    url_vals  = list(ANAPLAN_URLS.values())
    default_env_idx = url_keys.index(DEFAULTS["environment"]) if DEFAULTS["environment"] in url_keys else 0
    print("\nWhich Anaplan environment do you use?")
    for i, (k, v) in enumerate(ANAPLAN_URLS.items()):
        marker = " ← default" if i == default_env_idx else ""
        print(f"  [{i+1}] {k}  →  {v}{marker}")
    while True:
        raw = input(f"\nChoose an option [default={default_env_idx+1}]: ").strip()
        if not raw:
            idx = default_env_idx
            break
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(url_keys):
                break
        except ValueError:
            pass
        print("  Invalid choice, please try again.")
    main_url = url_vals[idx]
    print(f"  ✓ Environment: {main_url}\n")

    # ── Credentials ───────────────────────────────────────────────────────────
    _separator()
    print("STEP 2 of 4 — Login credentials")
    _separator()
    username = _ask("\nAnaplan email address", default=DEFAULTS["username"])

    print(
        "\nDoes your organisation use SSO (Single Sign-On) to log into Anaplan?\n"
        "  Answer Y if you normally log in via Microsoft/Google/your company portal.\n"
        "  Answer N if you log in with just your Anaplan email and password."
    )
    use_sso = _ask_yes_no("Use SSO?", default=DEFAULTS["use_sso"])
    print(f"  ✓ SSO: {'yes' if use_sso else 'no'}\n")

    password = ""
    if not use_sso:
        env_password = os.getenv("ANAPLAN_PASSWORD", "")
        if env_password:
            password = env_password
            print("  ✓ Password loaded from .env")
        else:
            password = getpass.getpass("Anaplan password (hidden input): ")

    # ── Output folder ─────────────────────────────────────────────────────────
    _separator()
    print("STEP 3 of 4 — Output location")
    _separator()
    folder_default = _normalise_path(DEFAULTS["output_folder"]) if DEFAULTS["output_folder"] else DEFAULT_OUTPUT_FOLDER
    output_folder = _normalise_path(_ask(
        "\nFolder where the Excel file should be saved",
        default=folder_default,
    ))
    os.makedirs(output_folder, exist_ok=True)
    print(f"  ✓ Output folder: {output_folder}\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    _separator()
    print("STEP 4 of 4 — Confirm")
    _separator()
    print(f"\n  Environment : {main_url}")
    print(f"  User        : {username}")
    print(f"  SSO         : {'yes' if use_sso else 'no'}")
    print(f"  Save to     : {output_folder}")
    print()

    if not _ask_yes_no("Everything correct? The script will now open the browser."):
        print("\nCancelled. Restart the script to try again.")
        sys.exit(0)

    return {
        "main_url":       main_url,
        "username":       username,
        "password":       password,
        "use_basic_auth": not use_sso,
        "output_folder":  output_folder,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  Logging
# ══════════════════════════════════════════════════════════════════════════════

def setup_logging(output_folder: str, model_name: str, timestamp: str) -> str:
    safe_model_name = _safe_filename(model_name)
    log_file = os.path.join(output_folder, f"Anaplan NUX Report - {safe_model_name}_{timestamp}.log")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return log_file


# ══════════════════════════════════════════════════════════════════════════════
#  Helper functions
# ══════════════════════════════════════════════════════════════════════════════

def _nested(d: dict, *keys, default="") -> str:
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
        if d is None:
            return default
    return str(d) if not isinstance(d, dict) else default


def table_to_workbook(workbook: Workbook, table: list, name: str, index: int | None = 0):
    """Write `table` (list of rows, first row = header) as a styled Excel table.

    `index` controls where the sheet is inserted: 0 (default) prepends it — the
    original behaviour used for the five core sheets; pass index=None to append
    the sheet at the end of the workbook instead (used for the two extra sheets
    so the five originals keep their exact position and content).
    """
    sheet = workbook.create_sheet(_safe_sheet_title(name), index)
    for row in table:
        sheet.append(row)

    tbl = Table(
        displayName=re.sub(r"[^A-Za-z0-9_]", "_", name),
        ref=f"A1:{get_column_letter(sheet.max_column)}{sheet.max_row}",
    )
    tbl.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium11",
        showFirstColumn=False, showLastColumn=False,
        showRowStripes=True,   showColumnStripes=False,
    )
    sheet.add_table(tbl)

    for col_cells in sheet.columns:
        col_letter = get_column_letter(col_cells[0].column)
        col_width  = max(len(str(cell.value or "")) for cell in col_cells)
        if col_width > 0:
            sheet.column_dimensions[col_letter].width = min(col_width, 100)


def api_get(browser: webdriver.Remote, url: str) -> dict:
    browser.get(url)
    try:
        raw = browser.find_element(By.TAG_NAME, "pre").text
    except Exception:
        raw = browser.execute_script(
            "return document.body.innerText || document.body.textContent;"
        )
    return json.loads(raw)


# ══════════════════════════════════════════════════════════════════════════════
#  Login
# ══════════════════════════════════════════════════════════════════════════════

def _dismiss_cookie_banner(browser: webdriver.Remote):
    try:
        accept_btn = WebDriverWait(browser, 7).until(
            EC.presence_of_element_located((By.XPATH,
                "//button[normalize-space()='Accept' or "
                "normalize-space()='Accepteren' or "
                "normalize-space()='Accept All' or "
                "normalize-space()='Alles accepteren']"
            ))
        )
        browser.execute_script("arguments[0].click();", accept_btn)
        time.sleep(1)
        return
    except Exception:
        pass

    try:
        WebDriverWait(browser, 3).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '//iframe[@title="TrustArc Cookie Consent Manager"]')
            )
        )
        btn = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class,'acceptAllButton')]")
            )
        )
        browser.execute_script("arguments[0].click();", btn)
        browser.switch_to.default_content()
        time.sleep(1)
        return
    except Exception:
        browser.switch_to.default_content()

    try:
        browser.execute_script("""
            ['[class*="cookie"]','[class*="consent"]','[class*="gdpr"]',
             '[id*="cookie"]','[id*="consent"]','[class*="privacy"]']
            .forEach(function(s) {
                document.querySelectorAll(s).forEach(function(el) {
                    el.style.setProperty('display','none','important');
                });
            });
        """)
    except Exception:
        pass


BASIC_AUTH_CHOOSER_ID = "prelogin-anaplan-basic"
PASSWORD_FIELD_ID = "password"


def _await_basic_auth_password_form(browser, timeout=30):
    """Get from the email step to the password form under either Anaplan flow.

    Legacy: the email step lands on a chooser page carrying a "Log in with
    Anaplan" button, and the password form appears only once it is clicked.
    Current: the email step redirects straight to the regional identity host
    (iam-<region>.anaplan.com), whose form already carries #password — the
    chooser is never rendered, and on the prelogin page it exists only as a
    hidden element that can never become clickable.

    So wait for whichever of the two arrives first and act accordingly, rather
    than requiring the chooser and timing out when Anaplan skips it.
    """
    def _whichever_arrives(drv):
        # Check the password field first: on the legacy chooser page it is
        # absent, so this can only match once the password form is really up.
        for el_id in (PASSWORD_FIELD_ID, BASIC_AUTH_CHOOSER_ID):
            try:
                el = drv.find_element(By.ID, el_id)
                if el.is_displayed():
                    return (el_id, el)
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        return False

    which, element = WebDriverWait(browser, timeout).until(_whichever_arrives)

    if which == BASIC_AUTH_CHOOSER_ID:
        element.click()
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.ID, PASSWORD_FIELD_ID))
        )


def login(browser: webdriver.Remote, config: dict):
    print("\n  → Opening browser and logging into Anaplan...")
    browser.get(config["main_url"])
    _dismiss_cookie_banner(browser)
    browser.switch_to.default_content()

    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.ID, "email-prelogin"))
    ).send_keys(config["username"])
    WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.ID, "submit-prelogin"))
    ).click()

    if config.get("use_basic_auth"):
        # Non-SSO: reach the password form, whichever shape Anaplan serves.
        _await_basic_auth_password_form(browser)

        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, PASSWORD_FIELD_ID))
        ).send_keys(config["password"])
        time.sleep(1)
        WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.ID, "btn-login"))
        ).click()
    else:
        print("  Complete the SSO login in the browser, then return here.")
        input("  Press Enter once Anaplan has loaded: ")

    time.sleep(6)
    print("  ✓ Logged in.\n")


# ══════════════════════════════════════════════════════════════════════════════
#  Model selection
# ══════════════════════════════════════════════════════════════════════════════

def _select_model(browser: webdriver.Remote, config: dict) -> tuple[str, str, str, str]:
    """
    Offers configured shortcuts from models.py first, falling back to the
    live API browser if none are configured or the user wants to browse.
    Returns (model_id, model_name, workspace_guid, customer_id).
    """
    configured_models = getattr(models, "MODELS", {})
    shortcuts = {
        key: m for key, m in configured_models.items()
        if m.get("customer_id") and m.get("workspace_id") and m.get("model_id")
    }
    if not shortcuts:
        return _choose_model_from_api(browser, config)

    _separator()
    print("MODEL SELECTION")
    _separator()
    keys = list(shortcuts.keys())
    for i, key in enumerate(keys, 1):
        print(f"  [{i}] {shortcuts[key].get('name', key)}")
    print(f"  [{len(keys) + 1}] Browse all models…")

    while True:
        entry = input("\nChoose an option: ").strip()
        try:
            idx = int(entry) - 1
            if 0 <= idx < len(keys):
                m = shortcuts[keys[idx]]
                model_name = m.get("name", keys[idx])
                print(f"\n  ✓ Selected: {model_name}")
                return m["model_id"], model_name, m["workspace_id"], m["customer_id"]
            if idx == len(keys):
                return _choose_model_from_api(browser, config)
        except ValueError:
            pass
        print("  Invalid choice, please try again.")


def _choose_model_from_api(browser: webdriver.Remote, config: dict) -> tuple[str, str, str, str]:
    """
    Fetches all available models and lets the user choose one.
    Returns (model_id, model_name, workspace_guid, customer_id).
    """
    main_url = config["main_url"]
    print("  → Fetching available models...")

    all_models = api_get(
        browser,
        f"{main_url}/a/springboard-platform-gateway-service/models?limit=50000&offset=0",
    )["items"]

    if not all_models:
        print("\nNo models found. Check your credentials and try again.")
        sys.exit(1)

    # Group by workspace for readability
    workspaces: dict[str, list] = {}
    for m in all_models:
        ws = m.get("CurrentWorkspaceName") or m.get("WorkspaceName") or "Unknown workspace"
        workspaces.setdefault(ws, []).append(m)

    _separator()
    print(f"MODEL SELECTION — {len(all_models)} model(s) found")
    _separator()

    flat_models = []
    counter = 1
    for ws_name, models in sorted(workspaces.items()):
        print(f"\n  📁 {ws_name}")
        for m in sorted(models, key=lambda x: x["ModelName"]):
            print(f"     [{counter:3}] {m['ModelName']}")
            flat_models.append(m)
            counter += 1

    print()
    while True:
        entry = input("Type the number of the model you want to scrape: ").strip()
        try:
            idx = int(entry) - 1
            if 0 <= idx < len(flat_models):
                model = flat_models[idx]
                break
        except ValueError:
            pass
        print("  Invalid choice, please try again.")

    model_id   = model["ModelGuid"]
    model_name = model["ModelName"]
    ws_guid    = model.get("CurrentWorkspaceGuid") or model.get("WorkspaceGuid", "")
    customer   = model.get("CustomerGuid") or model.get("TenantGuid", "")

    if not customer:
        try:
            ws_resp  = api_get(browser, f"{main_url}/1/3/workspaces/{ws_guid}")
            customer = ws_resp.get("workspace", {}).get("customerId", "")
        except Exception as e:
            print(f"  ! Could not resolve customer ID for workspace {ws_guid}: {e}")

    print(f"\n  ✓ Selected: {model_name}")
    print(f"    Model ID  : {model_id}")
    print(f"    Workspace : {ws_guid}")
    print()

    return model_id, model_name, ws_guid, customer


# ══════════════════════════════════════════════════════════════════════════════
#  Download helpers
# ══════════════════════════════════════════════════════════════════════════════

def _wait_for_download(download_dir: str, before_files: set, timeout: int = 60) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        current   = set(glob.glob(os.path.join(download_dir, "*")))
        new_files = current - before_files
        complete  = [f for f in new_files if not f.endswith((".crdownload", ".tmp", ".part"))]
        if complete:
            time.sleep(0.5)
            return max(complete, key=os.path.getmtime)
        time.sleep(0.5)
    return None


def _parse_downloaded_file(filepath: str) -> tuple[list, list]:
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".xlsx", ".xls"):
        from openpyxl import load_workbook as _lw
        wb = _lw(filepath, read_only=True, data_only=True)
        ws = wb.active
        all_rows = [list(r) for r in ws.iter_rows(values_only=True)]
        wb.close()
        if not all_rows:
            return [], []
        return [str(h) if h is not None else "" for h in all_rows[0]], all_rows[1:]
    else:
        with open(filepath, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            all_rows = list(reader)
        if not all_rows:
            return [], []
        return all_rows[0], all_rows[1:]


def _click_export_button(browser: webdriver.Remote, timeout: int = 15) -> bool:
    selectors = [
        "//button[normalize-space()='Export']",
        "//a[normalize-space()='Export']",
        "//button[contains(normalize-space(.), 'Export')]",
        "//*[@role='button'][contains(normalize-space(.), 'Export')]",
        "//button[@aria-label='Export']",
        "//button[@title='Export']",
        "//*[@data-action='export']",
        "//*[@data-testid='export-button']",
    ]
    for sel in selectors:
        try:
            btn = WebDriverWait(browser, timeout).until(
                EC.element_to_be_clickable((By.XPATH, sel))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.3)
            browser.execute_script("arguments[0].click();", btn)
            return True
        except Exception:
            continue
    return False


def _confirm_export_dialog(browser: webdriver.Remote):
    try:
        btn = WebDriverWait(browser, 6).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[normalize-space()='OK' or "
                "normalize-space()='Download' or "
                "normalize-space()='Export' or "
                "normalize-space()='CSV' or "
                "normalize-space()='Bevestigen']"
            ))
        )
        browser.execute_script("arguments[0].click();", btn)
        time.sleep(1)
    except Exception:
        pass


def _try_modeling_section_export(
    browser: webdriver.Remote,
    model_new_url: str,
    section: str,
    download_dir: str,
    extra_wait: int = 5,
    download_timeout: int = 60,
) -> tuple[list, list]:
    url_candidates = [
        f"{model_new_url}/model-settings/{section}",
        f"{model_new_url}/{section}",
        f"{model_new_url}/settings/{section}",
        f"{model_new_url}/model-settings",
    ]

    before_files = set(glob.glob(os.path.join(download_dir, "*")))
    page_loaded  = False

    for url in url_candidates:
        try:
            browser.get(url)
            WebDriverWait(browser, 8).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH,
                        "//button[contains(normalize-space(.), 'Export')]")),
                    EC.presence_of_element_located((By.TAG_NAME, "table")),
                    EC.presence_of_element_located((By.XPATH,
                        "//*[contains(@class,'ag-root')]")),
                    EC.presence_of_element_located((By.XPATH,
                        "//*[contains(@class,'virtualized')]")),
                )
            )
            page_loaded = True
            break
        except Exception:
            continue

    if not page_loaded:
        return [], []

    time.sleep(min(extra_wait, 4))

    if not _click_export_button(browser, timeout=8):
        return [], []

    _confirm_export_dialog(browser)

    downloaded = _wait_for_download(download_dir, before_files, timeout=download_timeout)
    if not downloaded:
        return [], []

    try:
        return _parse_downloaded_file(downloaded)
    except Exception:
        return [], []


# ══════════════════════════════════════════════════════════════════════════════
#  Actions detail builders
# ══════════════════════════════════════════════════════════════════════════════

_TGT_TYPE_MAP = {
    "MODULE_DATA":      "MODULE",
    "VERSIONS":         "VERSIONS",
    "LIST_ACCESS_DATA": "LIST",
    "USERS":            "USERS",
    "ROLE_ACCESS_DATA": "ROLES",
}


def _build_actions_detail_fallback(all_actions_raw: list) -> list:
    table = [[
        "Action Name", "Action Type",
        "Source", "Source Object", "Source Type",
        "Target Object", "Target Type",
        "Production Data",
    ]]
    for action in all_actions_raw:
        atype    = action.get("__atype", "")
        name     = action.get("name", "")
        imp_type = action.get("importType", "")
        ds_id    = action.get("importDataSourceId", "")

        if atype == "imports":
            src_type = "FILE" if ds_id else ("-" if imp_type == "VERSIONS" else "SAVED VIEW")
            tgt_type = _TGT_TYPE_MAP.get(imp_type, imp_type)
        elif atype == "exports":
            src_type = "SAVED VIEW"
            tgt_type = "FILE"
        else:
            src_type = tgt_type = ""

        table.append([name, atype, "", "", src_type, "", tgt_type, ""])
    return table


def _build_actions_detail_from_download(headers: list, rows: list) -> list:
    def _find(row_dict, *candidates):
        for c in candidates:
            v = row_dict.get(c)
            if v not in (None, ""):
                return str(v)
        return ""

    table = [[
        "Action Name", "Action Type",
        "Source", "Source Object", "Source Type",
        "Target Object", "Target Type",
        "Production Data",
    ]]
    for row_list in rows:
        if not any(v for v in row_list):
            continue
        row = dict(zip(headers, row_list))
        table.append([
            _find(row, "Name", "Action Name", "Naam", "Actienaam"),
            _find(row, "Type", "Action Type", "Type actie"),
            _find(row, "Source", "Bron", "Source Model", "Bronmodel"),
            _find(row, "Source Object", "Bronobject", "Source View", "Bronweergave"),
            _find(row, "Source Type", "Brontype", "Import Type", "Importtype"),
            _find(row, "Target", "Target Object", "Doelobject", "Target Module"),
            _find(row, "Target Type", "Doeltype"),
            _find(row, "Production Data", "Productiedata", "Production"),
        ])
    return table


# ══════════════════════════════════════════════════════════════════════════════
#  Line-item & UI-filter builders (two extra sheets)
# ══════════════════════════════════════════════════════════════════════════════

def _iter_filter_leaves(filter_obj):
    """Yield every LEAF node inside an axis-filter tree.

    Grid filters live in axisDescriptionQuery.regions.SINGLE.<axis>.filters as a
    nested BRANCH/LEAF tree: {"rootNode": {"type": "BRANCH", "nodes": [...],
    "operator": "AND"}}. A LEAF carries a "rule" with "selectedItems" (a
    coordinate of member/line-item ids), "operator" and "values".
    """
    if not isinstance(filter_obj, dict):
        return
    stack = [filter_obj]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        if node.get("type") == "LEAF":
            yield node
            continue
        # BRANCH (or the {"rootNode": {...}} wrapper) — descend
        if "rootNode" in node:
            stack.append(node["rootNode"])
        for child in node.get("nodes", []) or []:
            stack.append(child)


def _grid_widgets_of_page(page_content: dict) -> list:
    """Flatten a board/grid-page's widgets into a single list.

    BOARD pages nest widgets under rows->columns->widgets; GRID-PAGE pages carry
    a flat "widgets" list. Returns widget dicts (each with a widgetDefinition).
    """
    if not isinstance(page_content, dict):
        return []
    widgets = list(page_content.get("widgets", []) or [])
    for row in page_content.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        for col in row.get("columns", []) or []:
            if isinstance(col, dict):
                widgets += col.get("widgets", []) or []
    return widgets


# Anaplan reserves this fixed entity id for the "Line Items" dimension. When
# line items are placed on a grid axis, they appear as a dimension with this id
# whose `shows`/`hides` arrays subset which line items are actually displayed.
_LINE_ITEMS_DIM_ID = "20000000012"


def _axis_dimensions(axis_obj):
    """Yield the dimension dicts of an axis object ({"dimensions": [...]})."""
    if isinstance(axis_obj, dict):
        for d in axis_obj.get("dimensions", []) or []:
            if isinstance(d, dict):
                yield d


def _iter_region_axis_objs(adq):
    """Yield (module_id, columns_axis_obj, rows_axis_obj) per data region of a grid.

    An "axis object" is the dict that carries this region's ``dimensions`` and
    ``filters`` for one axis. Handles the two payload shapes seen in the view
    edit-mode config:

      A. axisDescriptionQuery.regions.<key> = {moduleId, columns:{…}, rows:{…}}
         — a single grid with its axes inlined on the region (plain grid).
      B. axisDescriptionQuery.regions = [ {moduleId, columnAxisKey, rowAxisKey}, … ]
         with the axis objects living under
         axisDescriptionQuery.{columnAxis,rowAxis}.childAxes.<key>
         — split/synced grids and COMBINED grids that share child axes across
         regions (each nested grid is one region, keyed to its own child axes).

    Only the row and column axes are returned (the grid the user sees); page /
    off-axis context dimensions are intentionally excluded. This is the single
    source of truth for "which axes belong to which region", shared by both the
    line-items builder (reads each axis's dimensions) and the UI-filters builder
    (reads each axis's filters), so both stay consistent across grid shapes.
    """
    if not isinstance(adq, dict):
        return
    regions = adq.get("regions", {})
    if isinstance(regions, list):
        col_children = (adq.get("columnAxis", {}) or {}).get("childAxes", {}) or {}
        row_children = (adq.get("rowAxis", {}) or {}).get("childAxes", {}) or {}
        for region in regions:
            if not isinstance(region, dict):
                continue
            cols = col_children.get(region.get("columnAxisKey"), {}) or {}
            rows = row_children.get(region.get("rowAxisKey"), {}) or {}
            yield region.get("moduleId", ""), cols, rows
    elif isinstance(regions, dict):
        for region in regions.values():
            if not isinstance(region, dict):
                continue
            yield (region.get("moduleId", ""),
                   region.get("columns") or {},
                   region.get("rows") or {})


def _iter_region_axes(adq):
    """Yield (module_id, [row/column dimension dicts]) per data region of a grid.

    Thin wrapper over :func:`_iter_region_axis_objs` that flattens each region's
    column + row axis objects down to their dimension dicts (the input the
    line-items resolver expects). Combined/split grids and plain grids are both
    handled transparently via the shared helper.
    """
    for module_id, cols, rows in _iter_region_axis_objs(adq):
        dims = list(_axis_dimensions(cols)) + list(_axis_dimensions(rows))
        yield module_id, dims


def _shown_line_item_names(dims, module_li_ids: set, id_to_name: dict):
    """Resolve which line items a grid actually displays, given its axis dims.

    `module_li_ids` / `id_to_name` describe the module's full line item set (ids
    and id→name, in natural module order). Returns an ordered list of displayed
    line item names, or ``None`` when line items are NOT explicitly subset on any
    axis — in which case the caller shows the module's full list (Anaplan
    semantics: an empty `shows`/`hides` on the Line Items dimension = show all).
    """
    for d in dims:
        shows = [str(x) for x in (d.get("shows") or [])]
        hides = [str(x) for x in (d.get("hides") or [])]
        # Identify the Line Items dimension by its reserved id, or (defensively,
        # for models that ever key it differently) by its shows/hides pointing at
        # ids that are line items of this module.
        is_li_dim = str(d.get("id", "")) == _LINE_ITEMS_DIM_ID
        if not is_li_dim and not ((set(shows) & module_li_ids) or (set(hides) & module_li_ids)):
            continue
        if shows:
            ordered = [id_to_name[sid] for sid in shows if sid in id_to_name]
            if ordered:
                return ordered
            # shows present but none resolve to this module's line items → treat
            # as unrestricted rather than silently dropping the whole view.
            return None
        if hides:
            hidden = set(hides)
            return [nm for sid, nm in id_to_name.items() if sid not in hidden]
        # Line Items dimension on an axis, but no explicit subset → all shown.
        return None
    return None


def _module_line_item_index(line_items_by_module: dict):
    """Return (mod_ids, mod_id2name): per module, its line item id-set and an
    ordered {id: name} map, in natural module order."""
    mod_ids: dict = {}
    mod_id2name: dict = {}
    for mid, items in line_items_by_module.items():
        ordered = {}
        for li in items:
            ordered[str(li.get("id", ""))] = li.get("name", "")
        mod_id2name[str(mid)] = ordered
        mod_ids[str(mid)] = set(ordered.keys())
    return mod_ids, mod_id2name


# Widget types that never display line items — skipped by the line-items sheet.
_NON_DATA_WIDGET_TYPES = {"TEXT", "ACTION", "IMAGE"}


def _widget_ux_type(wdef: dict):
    """Classify a widget into the UX object the user sees, or None if it shows no
    line items. Distinguishes a plain grid from a combined grid (a grid whose axis
    query spans more than one data region)."""
    t = str(wdef.get("type", "")).upper()
    if t in _NON_DATA_WIDGET_TYPES:
        return None
    if t == "FIELD":
        return "Field"
    if t == "CARD":
        return "KPI"
    if t.endswith("CHART"):
        return "Chart"
    if t == "TABLE":
        region_count = 0
        for wds in wdef.get("widgetDataSources", []) or []:
            if not isinstance(wds, dict):
                continue
            regions = (wds.get("axisDescriptionQuery") or {}).get("regions")
            if isinstance(regions, dict):
                region_count += sum(1 for r in regions.values() if isinstance(r, dict))
            elif isinstance(regions, list):
                region_count += sum(1 for r in regions if isinstance(r, dict))
        return "Combined grid" if region_count > 1 else "Grid"
    # Unknown but data-bearing widget: treat generically (still surface its LIs).
    return "Other"


def _widget_module_line_items(wdef: dict, mod_ids: dict, mod_id2name: dict):
    """Yield (module_id, [line item names]) for the line items a single widget
    actually displays. Handles every UX object:

      * FIELD — the explicit `fields[]` list (each a selected module+line item;
        can be several); the widget's `axisDescriptionQuery` is empty.
      * grids / combined grids / charts — line items placed on the row/column
        axes of `axisDescriptionQuery`, with `shows`/`hides` subsetting applied
        (via `_iter_region_axes` / `_shown_line_item_names`); charts and combined
        grids carry the same axis-query shape as a grid.
      * KPI (CARD) and other single-value widgets with no axis query — the one
        selected line item carried on the data source as `subEntityId`.
    """
    wtype = str(wdef.get("type", "")).upper()
    if wtype == "FIELD":
        by_mod: dict = {}
        order: list = []
        for f in wdef.get("fields", []) or []:
            if not isinstance(f, dict):
                continue
            m = str(f.get("moduleId", ""))
            nm = mod_id2name.get(m, {}).get(str(f.get("lineItemId", "")), "")
            if m not in by_mod:
                by_mod[m] = []
                order.append(m)
            if nm and nm not in by_mod[m]:
                by_mod[m].append(nm)
        for m in order:
            yield m, by_mod[m]
        return

    for wds in wdef.get("widgetDataSources", []) or []:
        if not isinstance(wds, dict):
            continue
        adq = wds.get("axisDescriptionQuery") or {}
        regions = adq.get("regions")
        has_regions = (
            (isinstance(regions, dict) and any(isinstance(r, dict) for r in regions.values()))
            or (isinstance(regions, list) and any(isinstance(r, dict) for r in regions))
        )
        if has_regions:
            for module_id, dims in _iter_region_axes(adq):
                module_id = str(module_id)
                id2name = mod_id2name.get(module_id, {})
                shown = _shown_line_item_names(dims, mod_ids.get(module_id, set()), id2name)
                names = list(id2name.values()) if shown is None else shown
                yield module_id, names
        else:
            # No axis query (KPI/Card, single-field field): the widget's one
            # selected line item rides on the data source as subEntityId.
            module_id = str(wds.get("dataSourceId", ""))
            nm = mod_id2name.get(module_id, {}).get(str(wds.get("subEntityId", "")), "")
            if nm:
                yield module_id, [nm]


def _build_views_line_items_table(collected_pages: list, views: dict,
                                  modules: dict, line_items_by_module: dict,
                                  model_new_url: str, views_table: list) -> list:
    """One row per (widget occurrence, line item actually displayed by it).

    Widget-driven: walks every board widget (grid, combined grid, field, KPI,
    chart) and emits the line items that widget genuinely shows — the grid's
    `shows`/`hides` subset, the field's selected `fields[]`, the KPI's single
    `subEntityId`, the chart's axis line items — never the module's full list
    unless the widget truly displays all of it. A "UX Type" column records which
    kind of object surfaced each line item, so e.g. a KPI and a chart that both
    show the same line item appear as two distinguishable rows.

    Columns match the "Views Usage Report" (Module/View name, App/Page, URLs and
    IDs) so the two sheets line up, with "UX Type" + "Line Item" appended. Any
    view present in the Views Usage Report but not covered by a parsed widget
    (e.g. a view on a non-board page with no edit-mode payload) is preserved with
    its full line item list and a blank UX Type, so nothing regresses.
    """
    header = ["Module/View name", "App name", "Page name", "View URL",
              "Page URL", "Module/View ID", "App ID", "Page ID",
              "UX Type", "Line Item"]
    out = [header]
    mod_ids, mod_id2name = _module_line_item_index(line_items_by_module)
    # module -> a view id (view id == module id in most tenants); used for the
    # Module/View name + View URL columns of a widget row.
    mod2view: dict = {}
    for vid, v in views.items():
        mod2view.setdefault(str(v.get("module", "")), vid)

    covered: set = set()  # (page_guid, module_id) emitted from a real widget

    for page in collected_pages:
        for widget in _grid_widgets_of_page(page.get("content", {})):
            if not isinstance(widget, dict):
                continue
            wdef = widget.get("widgetDefinition", {}) or {}
            ux_type = _widget_ux_type(wdef)
            if ux_type is None:
                continue
            for module_id, names in _widget_module_line_items(wdef, mod_ids, mod_id2name):
                module_id = str(module_id)
                if not module_id:
                    continue
                covered.add((page["guid"], module_id))
                view_id = mod2view.get(module_id, module_id)
                view_name = ((views.get(view_id, {}) or {}).get("name")
                             or (modules.get(module_id, {}) or {}).get("name")
                             or module_id)
                base = [view_name, page["app_name"], page["name"],
                        f"{model_new_url}/tabs/{view_id}", page["page_url"],
                        view_id, page["app_guid"], page["guid"], ux_type]
                if names:
                    for nm in names:
                        out.append(base + [nm])
                else:
                    out.append(base + [""])

    # Fallback: views in the report with no parsed widget (non-board pages).
    for row in (views_table[1:] if views_table else []):
        view_id = row[5] if len(row) > 5 else ""
        page_guid = row[7] if len(row) > 7 else ""
        module_id = str(views.get(view_id, {}).get("module", ""))
        if (page_guid, module_id) in covered:
            continue
        covered.add((page_guid, module_id))
        names = [li.get("name", "") for li in line_items_by_module.get(module_id, [])]
        base = list(row[:8]) + [""]
        if names:
            for nm in names:
                out.append(base + [nm])
        else:
            out.append(base + [""])
    return out


def _build_ui_filters_table(collected_pages: list, modules: dict,
                            line_item_name_by_id: dict) -> list:
    """One row per (page, module) grid, reporting its row/column line-item filters.

    `collected_pages` is a list of (page_name, page_content) gathered while
    scraping each board; page_content is flattened to its widget list here. For
    every TABLE widget we walk its data regions via `_iter_region_axis_objs`
    (which resolves both plain single grids AND combined/split grids — the latter
    keep each nested grid's axes under columnAxis/rowAxis.childAxes), read each
    region's column/row `filters`, resolve every filter leaf's selectedItems
    against `line_item_name_by_id` (only the entry that is a real line item
    resolves), and aggregate per (page, module). A combined grid therefore
    contributes one filter row per nested grid. The two "Value Filter …" columns
    are booleans flagging whether that axis has a resolved line-item filter.
    """
    header = ["Page", "Module", "Filter Column", "Value Filter Column",
              "Filter Rows", "Value Filter Rows"]
    # (page, module) -> {"col": [line item names], "row": [line item names]}
    agg: dict = {}
    order: list = []

    for page in collected_pages:
        page_name = page["name"]
        page_content = page["content"]
        for widget in _grid_widgets_of_page(page_content):
            if not isinstance(widget, dict):
                continue
            wdef = widget.get("widgetDefinition", {}) or {}
            if wdef.get("type") != "TABLE":
                continue
            for wds in wdef.get("widgetDataSources", []) or []:
                if not isinstance(wds, dict):
                    continue
                adq = wds.get("axisDescriptionQuery")
                if not isinstance(adq, dict):
                    continue
                # One (module, columns-axis, rows-axis) triple per data region.
                # Plain grids expose a single region ({"SINGLE": {...}}); combined
                # and split grids expose a list of regions whose axes live under
                # columnAxis/rowAxis.childAxes — `_iter_region_axis_objs` resolves
                # both, so a combined grid yields one entry per nested grid here.
                for module_id, cols, rows in _iter_region_axis_objs(adq):
                    module_name = modules.get(module_id, {}).get("name", "") or module_id
                    key = (page_name, module_name)
                    if key not in agg:
                        agg[key] = {"col": [], "row": []}
                        order.append(key)
                    slot = agg[key]
                    for axis_obj, bucket in ((cols, "col"), (rows, "row")):
                        axis_filters = (axis_obj or {}).get("filters", {})
                        for leaf in _iter_filter_leaves(axis_filters):
                            rule = leaf.get("rule", {}) or {}
                            for sid in rule.get("selectedItems", []) or []:
                                name = line_item_name_by_id.get(str(sid))
                                if name and name not in slot[bucket]:
                                    slot[bucket].append(name)

    out = [header]
    for key in order:
        page_name, module_name = key
        col = agg[key]["col"]
        row = agg[key]["row"]
        out.append([
            page_name,
            module_name,
            "; ".join(col),
            bool(col),
            "; ".join(row),
            bool(row),
        ])
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  Scrapen
# ══════════════════════════════════════════════════════════════════════════════

def _progress(current: int, total: int, label: str = ""):
    pct   = int(current / total * 100) if total else 0
    bar   = "█" * (pct // 5) + "░" * (20 - pct // 5)
    print(f"\r  [{bar}] {pct:3}%  {current}/{total}  {label:<40}", end="", flush=True)


def scrape(browser: webdriver.Remote, config: dict, model_id: str, model_name: str,
           ws_guid: str, customer: str, download_dir: str):

    main_url  = config["main_url"].rstrip("/")
    out_dir   = config["output_folder"]
    sds_url   = f"{SDS_HOST}/a/springboard-definition-service"

    if not customer:
        raise RuntimeError("Missing customer ID for selected model; cannot fetch NUX pages.")
    if not ws_guid:
        raise RuntimeError("Missing workspace ID for selected model; cannot open Modeling UI exports.")

    model_api_url   = f"{main_url}/2/0/models/{model_id}"
    model_pages_url = f"{sds_url}/customer/{customer}/model/{model_id}/pages"
    model_new_url   = (
        f"{main_url}/a/modeling/customers/{customer}"
        f"/workspaces/{ws_guid}/models/{model_id}"
    )

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    setup_logging(out_dir, model_name, timestamp)
    logging.info(f"Model: {model_name}  |  ID: {model_id}")

    workbook    = Workbook()
    blank_sheet = workbook.active

    # ── All Views ──────────────────────────────────────────────────────────────
    print("\n  → Step 1/5: Fetching views...")
    raw_views = api_get(browser, f"{model_api_url}/views")["views"]
    table = [["Name", "ID", "Module ID"]]
    for v in raw_views:
        table.append([v["name"], v["id"], v["moduleId"]])
    table_to_workbook(workbook, table, "All Views")
    workbook.remove(blank_sheet)
    views = {v["id"]: {"name": v["name"], "module": v["moduleId"]} for v in raw_views}
    print(f"  ✓ {len(raw_views)} views found.")

    # ── Modules ────────────────────────────────────────────────────────────────
    print("  → Step 2/5: Fetching modules...")
    raw_modules = api_get(browser, f"{model_api_url}/modules")["modules"]
    modules = {m["id"]: {"name": m["name"], "count": 0} for m in raw_modules}
    print(f"  ✓ {len(raw_modules)} modules found.")

    # ── Line items (for the two extra sheets) ───────────────────────────────────
    # Official Anaplan API: one record per line item, tagged with its module.
    try:
        raw_line_items = api_get(browser, f"{model_api_url}/lineItems").get("items", [])
    except Exception as e:
        logging.warning("Could not fetch line items: %s", e)
        raw_line_items = []
    line_items_by_module: dict = {}
    line_item_name_by_id: dict = {}
    for li in raw_line_items:
        line_items_by_module.setdefault(str(li.get("moduleId", "")), []).append(li)
        line_item_name_by_id[str(li.get("id", ""))] = li.get("name", "")
    print(f"  ✓ {len(raw_line_items)} line items found.")

    # Board contents stashed here (additive) so the two extra sheets can be built
    # after the loop without re-fetching or disturbing the five core sheets.
    collected_pages: list = []

    # ── Pages ─────────────────────────────────────────────────────────────────
    print("  → Step 3/5: Processing pages, actions and views...")
    pages = api_get(browser, model_pages_url)["items"]

    # ── Action definitions ─────────────────────────────────────────────────────
    actions_dict: dict = {}
    all_actions_raw: list = []
    for atype in ["processes", "imports", "exports", "actions"]:
        resp = api_get(browser, f"{model_api_url}/{atype}")
        for action in resp.get(atype, []):
            actions_dict[action["id"]] = {"name": action["name"], "type": atype}
            all_actions_raw.append({"__atype": atype, **action})

    # ── Actions Usage Report ───────────────────────────────────────────────────
    actions_table = [[
        "Action name", "Action type", "App name", "Page name",
        "Page URL", "Action ID", "App ID", "Page ID",
    ]]

    views_table = [[
        "Module/View name", "App name", "Page name",
        "View URL", "Page URL", "Module/View ID", "App ID", "Page ID",
    ]]

    for i, page in enumerate(pages):
        page_name = page.get("name", "<unnamed page>")
        page_guid = page.get("guid", "")
        page_type = page.get("pageType", "")
        app_guid = page.get("appGuid", "")
        app_name = page.get("appName", "")
        page_url = f"{main_url}/a/apps/app/{app_guid}/boards/{page_guid}"
        _progress(i + 1, len(pages), page_name[:40])

        # Actions per pagina
        if page_type in ("BOARD", "GRID-PAGE"):
            try:
                page_content = api_get(
                    browser, f"{sds_url}/{page_type.lower()}s/{page_guid}"
                )
            except Exception as e:
                logging.warning(
                    "Could not fetch page content for %s (%s): %s",
                    page_name, page_guid, e,
                )
                page_content = {}

            # Stash for the two extra sheets (built after the loop). Additive —
            # does not affect the existing action/view extraction below. Full page
            # metadata is carried so the line-items sheet can be built widget-driven
            # (one row per widget × displayed line item) without re-fetching.
            collected_pages.append({
                "name":     page_name,
                "guid":     page_guid,
                "app_name": app_name,
                "app_guid": app_guid,
                "page_url": page_url,
                "content":  page_content,
            })

            page_actions: set = set()
            if page_type == "BOARD":
                widgets = []
                for row in page_content.get("rows", []):
                    for col in row.get("columns", []):
                        widgets += col.get("widgets", [])
            else:
                widgets = page_content.get("widgets", [])
                for action in page_content.get("actions", []):
                    if not isinstance(action, dict):
                        continue
                    action_id = action.get("actionId")
                    if action_id:
                        page_actions.add(action_id)

            for widget in widgets:
                if not isinstance(widget, dict):
                    continue
                wdef = widget.get("widgetDefinition", {})
                for a in wdef.get("widgetActions", []):
                    if not isinstance(a, dict):
                        continue
                    action_id = a.get("actionId")
                    if action_id:
                        page_actions.add(action_id)
                if wdef.get("type") == "ACTION":
                    try:
                        widget_actions = json.loads(wdef.get("actions") or "[]")
                    except json.JSONDecodeError as e:
                        logging.warning(
                            "Could not parse action widget JSON on %s (%s): %s",
                            page_name, page_guid, e,
                        )
                        widget_actions = []
                    if not isinstance(widget_actions, list):
                        widget_actions = []
                    for a in widget_actions:
                        if not isinstance(a, dict):
                            continue
                        action_id = a.get("id")
                        if action_id:
                            page_actions.add(action_id)

            for aid in page_actions:
                if aid not in actions_dict:
                    continue
                actions_table.append([
                    actions_dict[aid]["name"],
                    actions_dict[aid]["type"],
                    app_name,
                    page_name,
                    page_url,
                    aid,
                    app_guid,
                    page_guid,
                ])

        # Views per pagina
        try:
            page_data = api_get(
                browser, f"{model_pages_url}/{page_guid}?moduleUsage=true"
            )
        except Exception as e:
            logging.warning(
                "Could not fetch module usage for %s (%s): %s",
                page_name, page_guid, e,
            )
            page_data = {}

        data_sources = set()
        for card in page_data.get("pageDataSources", []):
            if not isinstance(card, dict):
                continue
            data_source_id = card.get("dataSourceId")
            if data_source_id:
                data_sources.add(data_source_id)
        for ds_id in data_sources:
            if ds_id not in views:
                continue
            views_table.append([
                views[ds_id]["name"],
                app_name,
                page_name,
                f"{model_new_url}/tabs/{ds_id}",
                page_url,
                ds_id,
                app_guid,
                page_guid,
            ])
            module_id = views[ds_id]["module"]
            if module_id in modules:
                modules[module_id]["count"] += 1
            else:
                logging.warning(
                    "View %s (%s) references missing module ID %s",
                    views[ds_id]["name"], ds_id, module_id,
                )

    print()  # newline after progress bar
    table_to_workbook(workbook, actions_table, "Actions Usage Report")
    table_to_workbook(workbook, views_table,   "Views Usage Report")

    # ── Modules Usage Count ────────────────────────────────────────────────────
    modules_table = [["Name", "ID", "Count"]]
    for mid, mdata in modules.items():
        modules_table.append([mdata["name"], mid, mdata["count"]])
    table_to_workbook(workbook, modules_table, "Modules Usage Count")

    # ── Actions detail via Modeling UI Export ──────────────────────────────────
    print("  → Step 4/5: Downloading actions detail via Modeling UI...")
    sheet_label     = _safe_sheet_title(f"Actions {model_name}", fallback="Actions")
    act_detail_table = None

    for section in ("imports", "actions"):
        headers, rows = _try_modeling_section_export(
            browser, model_new_url, section, download_dir, extra_wait=4, download_timeout=20,
        )
        if headers and rows:
            act_detail_table = _build_actions_detail_from_download(headers, rows)
            break

    if act_detail_table is None:
        logging.warning("UI export failed. Falling back to REST API data.")
        act_detail_table = _build_actions_detail_fallback(all_actions_raw)

    table_to_workbook(workbook, act_detail_table, sheet_label)

    # ── Two extra sheets (appended at the end; five core sheets untouched) ──────
    # a. "Views Usage Report - Line Items": one row per (widget, line item the
    #    widget actually displays), across every UX object — grid, combined grid,
    #    field, KPI, chart — read from the board edit-mode payload. A "UX Type"
    #    column records which kind of object surfaced each line item.
    views_li_table = _build_views_line_items_table(
        collected_pages, views, modules, line_items_by_module,
        model_new_url, views_table,
    )
    table_to_workbook(workbook, views_li_table,
                      "Views Usage Report - Line Items", index=None)

    # b. "UI Filters": per (page, module) grid, the line items used as row/column
    #    filters plus a boolean flag for each axis.
    ui_filters_table = _build_ui_filters_table(
        collected_pages, modules, line_item_name_by_id,
    )
    table_to_workbook(workbook, ui_filters_table, "UI Filters", index=None)

    # ── Save ───────────────────────────────────────────────────────────────────
    print("  → Step 5/5: Saving Excel file...")
    safe_model_name = _safe_filename(model_name)
    excel_path = os.path.join(out_dir, f"Anaplan NUX Report - {safe_model_name}_{timestamp}.xlsx")
    workbook.save(excel_path)

    _separator("═")
    print(f"\n  ✅ DONE!\n")
    print(f"  File saved to:\n  {excel_path}")
    print(f"\n  Summary:")
    print(f"    • {len(raw_views)} views")
    print(f"    • {len(actions_table) - 1} action links on pages")
    print(f"    • {len(views_table) - 1} view links on pages")
    print(f"    • {len(raw_modules)} modules")
    print(f"    • {len(views_li_table) - 1} view × line-item rows")
    print(f"    • {len(ui_filters_table) - 1} page × module filter rows")
    _separator("═")


# ══════════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════════

def _get_edge_version() -> str:
    """Read the installed Edge version from the Windows registry."""
    try:
        import winreg
        for key_path in (
            r"SOFTWARE\Microsoft\Edge\BLBeacon",
            r"SOFTWARE\WOW6432Node\Microsoft\Edge\BLBeacon",
        ):
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
            except Exception:
                continue
    except Exception:
        pass
    return ""


def _create_browser(download_dir: str) -> webdriver.Remote:
    """
    Start Edge with the correct WebDriver.

    Strategy (in order):
    1. msedgedriver.exe in the same folder as this script
    2. Selenium Manager (bundled with Selenium 4.6+)
    3. webdriver-manager (needs internet on first run)
    """
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {
        "download.default_directory":   download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade":   True,
        "safebrowsing.enabled":         True,
    })

    # Strategy 1: driver next to this script
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    local_driver = os.path.join(script_dir, "msedgedriver.exe")
    if os.path.isfile(local_driver):
        print(f"  → Using local driver: {local_driver}")
        try:
            service = EdgeService(executable_path=local_driver)
            browser = webdriver.Edge(service=service, options=options)
            print("  ✓ Edge driver ready.\n")
            return browser
        except Exception as e:
            print(f"  ! Local driver failed: {e}")

    # Strategy 2: Selenium Manager
    print("  → Trying Selenium Manager...")
    try:
        browser = webdriver.Edge(options=options)
        print("  ✓ Edge driver ready (Selenium Manager).\n")
        return browser
    except Exception as e:
        print(f"  ! Selenium Manager failed: {e}")

    # Strategy 3: webdriver-manager (needs internet)
    if _WDM_AVAILABLE:
        print("  → Trying webdriver-manager (needs internet)...")
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
            browser = webdriver.Edge(service=service, options=options)
            print("  ✓ Edge driver ready (webdriver-manager).\n")
            return browser
        except Exception as e:
            print(f"  ! webdriver-manager failed: {e}")

    raise RuntimeError(
        f"No working msedgedriver found.\n"
        f"Place msedgedriver.exe (matching your Edge version) in:\n  {script_dir}\n"
        f"Download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
    )


def main():
    # 1. Collect configuration via wizard
    config = _collect_config()

    download_dir = tempfile.mkdtemp(prefix="anaplan_dl_")

    # 2. Start browser
    print("\n  → Starting Edge browser...")
    try:
        browser = _create_browser(download_dir)
    except Exception as e:
        print(f"\n  ERROR: Could not start Edge browser.\n  {e}")
        print(
            "\n  Make sure Microsoft Edge is installed and that the Edge WebDriver\n"
            "  version matches your Edge version.\n"
            "  Run:  pip install webdriver-manager\n"
            "  to let the script manage this automatically."
        )
        shutil.rmtree(download_dir, ignore_errors=True)
        sys.exit(1)

    browser.set_script_timeout(120)

    try:
        # 3. Login
        login(browser, config)

        # 4. Model selection
        model_id, model_name, ws_guid, customer = _select_model(browser, config)

        # 5. Confirm before scraping
        if not _ask_yes_no(f"Ready to scrape '{model_name}'. Continue?"):
            print("Cancelled.")
            return

        # 6. Scrape
        scrape(browser, config, model_id, model_name, ws_guid, customer, download_dir)

        # 7. Scrape another model?
        while _ask_yes_no("\nWould you like to scrape another model?"):
            model_id, model_name, ws_guid, customer = _select_model(browser, config)
            if _ask_yes_no(f"Scrape '{model_name}'?"):
                scrape(browser, config, model_id, model_name, ws_guid, customer, download_dir)

    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    finally:
        browser.quit()
        shutil.rmtree(download_dir, ignore_errors=True)

    print("\nBrowser closed. Goodbye!")


if __name__ == "__main__":
    main()
