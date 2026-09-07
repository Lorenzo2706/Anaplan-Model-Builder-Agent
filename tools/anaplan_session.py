"""
anaplan_session.py
------------------
Read-only authenticated access to the Anaplan Integration API v2.

AUTHENTICATION
--------------
Token auth, no browser. `scrape_model_data._api_session()` exchanges the .env
credentials for an Integration-API bearer token and returns a pre-authenticated
requests.Session for https://api.anaplan.com/2/0/. We reuse it rather than
reimplementing the exchange.

Do NOT call the regional app shard (eu2a.app.anaplan.com) for /2/0/ endpoints:
it redirects to the global endpoint, which rejects web-session cookies with 401.
That transport died around 2026-08-07. The allowlist below enforces the correct
host so a copy-pasted app-shard URL fails loudly instead of returning 401s.

READ-ONLY BY CONSTRUCTION
-------------------------
This module exposes exactly one HTTP verb: AnaplanSession.get(). There is
deliberately NO post/put/patch/delete wrapper, and every URL is checked against
an allowlist. Four of the five shortcuts in models.py resolve to production
workspaces; adding a write path here must be a deliberate, reviewed act
rather than a one-line accident.
"""
import json
import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class AnaplanError(Exception):
    """Base for every failure this module reports. Never returns {} on error —
    an empty result and a failed call must stay distinguishable."""


class AnaplanAuthError(AnaplanError):
    """Session rejected (401/403). Caller may retry once with a fresh token."""


class AnaplanTooLargeError(AnaplanError):
    """The requested grid exceeds what Anaplan will return. Carries the view's
    page dimensions so the caller can tell the agent what to narrow by."""

    def __init__(self, message, page_dimensions=None):
        super().__init__(message)
        self.page_dimensions = list(page_dimensions or [])


class AnaplanTimeoutError(AnaplanError):
    """The request timed out. Distinct from 'the grid is empty'."""


class AnaplanURLNotAllowedError(AnaplanError):
    """URL is not on the read-only allowlist."""


class AnaplanEmptyGridError(AnaplanError):
    """The grid exists but has zero populated cells. A legitimate model state
    (common in sparse Polaris models), NOT an error condition to hide."""


# The Integration API is served ONLY from this global host. Pinned, not a
# pattern: an app-shard URL must fail the allowlist, not merely 401 later.
API_HOST = "https://api.anaplan.com"

_HOST = re.escape(API_HOST)
_MODEL = r"[A-Za-z0-9]+"

_ALLOWED_URL_PATTERNS = (
    re.compile(rf"^{_HOST}/2/0/models/{_MODEL}/views/\d+/data(\?.*)?$"),
    re.compile(rf"^{_HOST}/2/0/models/{_MODEL}/views/\d+(\?.*)?$"),
    re.compile(rf"^{_HOST}/2/0/models/{_MODEL}/views(\?.*)?$"),
    re.compile(rf"^{_HOST}/2/0/models/{_MODEL}/lists(\?.*)?$"),
    re.compile(rf"^{_HOST}/2/0/models/{_MODEL}/lists/\d+/items(\?.*)?$"),
)

# Verbatim oversize markers. Deliberately NARROW: the 400s actually observed on
# 2026-08-14 were "Mandatory query parameter 'format' is missing" and "Malformed
# pages parameter", neither of which is an oversize condition. Telling the agent
# to narrow when the real fix is a query parameter wastes a whole retry cycle.
_TOO_LARGE_MARKERS = ("too large", "exceeds", "too many cells", "size limit")


def is_url_allowed(url: str) -> bool:
    """True only for read endpoints this tool is permitted to call."""
    return any(p.match(url or "") for p in _ALLOWED_URL_PATTERNS)


def _looks_too_large(body_text: str) -> bool:
    low = (body_text or "").lower()
    return any(m in low for m in _TOO_LARGE_MARKERS)


def classify_response(status_code, content_type, body_text, url=""):
    """Return None if the response is a usable JSON 200; otherwise raise the
    most specific typed error. Deliberately NOT modelled on the older
    scrape_model_data._get(), which returned {} for every failure and so made an
    expired session indistinguishable from an empty module."""
    where = f" for {url}" if url else ""

    if status_code in (401, 403):
        raise AnaplanAuthError(f"Anaplan rejected the session ({status_code}){where}")
    if status_code == 400 and _looks_too_large(body_text):
        raise AnaplanTooLargeError(f"Anaplan refused the grid as too large{where}: "
                                   f"{(body_text or '')[:300]}")
    if status_code != 200:
        raise AnaplanError(f"Anaplan returned HTTP {status_code}{where}: "
                           f"{(body_text or '')[:300]}")
    if "json" not in (content_type or "").lower():
        raise AnaplanError(
            f"Expected JSON but got Content-Type {content_type!r}{where} — this "
            f"usually means the session expired and Anaplan served a login "
            f"page: {(body_text or '')[:200]}"
        )
    # Content-Type is not enough: a 200 with an undecodable body was observed
    # live on 2026-08-14. Decode here so the caller only ever sees AnaplanError.
    try:
        json.loads(body_text)
    except (TypeError, ValueError) as e:
        raise AnaplanError(
            f"Anaplan returned HTTP 200 with Content-Type {content_type!r}{where} "
            f"but the body could not be decoded as JSON ({e}). Body starts: "
            f"{(body_text or '')[:200]!r}"
        ) from e
    return None


class AnaplanSession:
    """Authenticated read-only HTTP. `get` is the ONLY verb by design."""

    def __init__(self, base_url, requests_session):
        self.base_url = base_url.rstrip("/")
        self._sess = requests_session
        self._refreshed = False

    def _refresh(self):
        """Swap in a session carrying a fresh Integration-API token."""
        import scrape_model_data
        self._sess = scrape_model_data._api_session()

    def get(self, url, timeout=180):
        """GET an allowlisted URL and return parsed JSON. Raises a typed
        AnaplanError subclass on any failure - never returns {}."""
        if not is_url_allowed(url):
            raise AnaplanURLNotAllowedError(
                f"Refusing to call {url!r}: not on the read-only allowlist. "
                f"This tool may only read views, view metadata, lists, and list "
                f"items, and only on {API_HOST}."
            )
        try:
            resp = self._sess.get(url, timeout=timeout)
        except requests.Timeout as e:
            raise AnaplanTimeoutError(f"Timed out after {timeout}s calling {url}") from e
        except requests.RequestException as e:
            raise AnaplanError(f"Network failure calling {url}: {e}") from e

        try:
            classify_response(resp.status_code, resp.headers.get("Content-Type", ""),
                              resp.text, url=url)
        except AnaplanAuthError:
            if self._refreshed:
                raise
            self._refreshed = True
            self._refresh()
            return self.get(url, timeout=timeout)

        return resp.json()

    def close(self):
        try:
            self._sess.close()
        except Exception:
            pass


def open_session():
    """Return an AnaplanSession backed by a fresh Integration-API token.

    No cache and no browser: the token exchange takes about a second, so
    caching would add a credential-equivalent file on disk for no real gain.
    """
    import scrape_model_data
    return AnaplanSession(scrape_model_data.API_BASE, scrape_model_data._api_session())
