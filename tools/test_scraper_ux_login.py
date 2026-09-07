"""Browser-free tests for scraper_ux.login().

Anaplan's basic-auth flow has two shapes in the wild:

* legacy  — the email step lands on a chooser page carrying a
            "Log in with Anaplan" button (#prelogin-anaplan-basic), and the
            password form appears only after that button is clicked.
* current — the email step redirects straight to the regional identity host
            (iam-<region>.anaplan.com), whose form already carries #password
            and #btn-login. No chooser is ever rendered.

login() must handle both. These tests drive the real function against a fake
driver, so the real WebDriverWait/expected_conditions logic is exercised
without a browser.
"""
import types

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

import scraper_ux


class FakeElement:
    def __init__(self, el_id, displayed=True, enabled=True, on_click=None):
        self.id = el_id
        self.displayed = displayed
        self.enabled = enabled
        self.on_click = on_click
        self.keys = []
        self.clicks = 0

    def send_keys(self, text):
        self.keys.append(text)

    def click(self):
        self.clicks += 1
        if self.on_click:
            self.on_click()

    def is_displayed(self):
        return self.displayed

    def is_enabled(self):
        return self.enabled

    def get_attribute(self, _name):
        return None


class FakeDriver:
    """A driver whose find_element resolves against whichever page is current."""

    def __init__(self, pages, start):
        self.pages = pages
        self.current = start
        self.visited = []
        self.switch_to = types.SimpleNamespace(default_content=lambda: None)

    def goto(self, page):
        self.current = page

    def get(self, url):
        self.visited.append(url)

    def execute_script(self, *_a, **_kw):
        return None

    def find_element(self, _by, value):
        el = self.pages[self.current].get(value)
        if el is None:
            raise NoSuchElementException(f"no element {value!r} on page {self.current!r}")
        return el


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    """Shrink the real 15s waits and remove the real sleeps, so a wait that
    genuinely cannot succeed fails in well under a second."""

    class _FastWait(WebDriverWait):
        def __init__(self, driver, _timeout, *_a, **_kw):
            super().__init__(driver, 0.5, poll_frequency=0.01)

    monkeypatch.setattr(scraper_ux, "WebDriverWait", _FastWait)
    monkeypatch.setattr(scraper_ux, "time", types.SimpleNamespace(sleep=lambda *_a: None))


CONFIG = {
    "main_url": "https://eu3.app.anaplan.com/",
    "username": "user@example.com",
    "password": "s3cret",
    "use_basic_auth": True,
}


def _current_flow_driver():
    """Reproduces the observed live pages: the chooser is present but HIDDEN on
    the prelogin page, and absent entirely after the redirect."""
    iam = {
        "username": FakeElement("username"),
        "password": FakeElement("password"),
        "btn-login": FakeElement("btn-login"),
    }
    prelogin = {
        "email-prelogin": FakeElement("email-prelogin"),
        "prelogin-anaplan-basic": FakeElement("prelogin-anaplan-basic", displayed=False),
    }
    driver = FakeDriver({"prelogin": prelogin, "iam": iam}, "prelogin")
    prelogin["submit-prelogin"] = FakeElement(
        "submit-prelogin", on_click=lambda: driver.goto("iam")
    )
    return driver, prelogin, iam


def _legacy_flow_driver():
    password_page = {
        "password": FakeElement("password"),
        "btn-login": FakeElement("btn-login"),
    }
    prelogin = {"email-prelogin": FakeElement("email-prelogin")}
    chooser = {}
    driver = FakeDriver(
        {"prelogin": prelogin, "chooser": chooser, "password": password_page}, "prelogin"
    )
    prelogin["submit-prelogin"] = FakeElement(
        "submit-prelogin", on_click=lambda: driver.goto("chooser")
    )
    chooser["prelogin-anaplan-basic"] = FakeElement(
        "prelogin-anaplan-basic", on_click=lambda: driver.goto("password")
    )
    return driver, prelogin, chooser, password_page


class TestLoginCurrentFlow:
    """The flow Anaplan actually serves today: no chooser, straight to iam-<region>."""

    def test_types_password_and_submits_without_a_chooser(self):
        driver, prelogin, iam = _current_flow_driver()

        scraper_ux.login(driver, CONFIG)

        assert prelogin["email-prelogin"].keys == ["user@example.com"]
        assert prelogin["submit-prelogin"].clicks == 1
        assert iam["password"].keys == ["s3cret"], "password was never typed"
        assert iam["btn-login"].clicks == 1, "login was never submitted"

    def test_does_not_require_the_hidden_chooser(self):
        driver, prelogin, _iam = _current_flow_driver()

        scraper_ux.login(driver, CONFIG)

        assert prelogin["prelogin-anaplan-basic"].clicks == 0, (
            "a hidden chooser must never be clicked"
        )


class TestLoginLegacyFlow:
    """The older flow must keep working — the chooser is clicked when present."""

    def test_clicks_the_chooser_then_types_the_password(self):
        driver, _prelogin, chooser, password_page = _legacy_flow_driver()

        scraper_ux.login(driver, CONFIG)

        assert chooser["prelogin-anaplan-basic"].clicks == 1
        assert password_page["password"].keys == ["s3cret"]
        assert password_page["btn-login"].clicks == 1


class TestLoginSso:
    def test_sso_waits_for_the_human_and_never_types_a_password(self, monkeypatch):
        driver, prelogin, iam = _current_flow_driver()
        monkeypatch.setattr("builtins.input", lambda *_a: "")

        scraper_ux.login(driver, dict(CONFIG, use_basic_auth=False))

        assert iam["password"].keys == [], "SSO must not type the stored password"
        assert prelogin["email-prelogin"].keys == ["user@example.com"]
