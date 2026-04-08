from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright, Browser, Page, Playwright

BRIDGE_DIR = Path(__file__).resolve().parent.parent / "bridge"
INDEX_HTML = BRIDGE_DIR / "index.html"

if not INDEX_HTML.exists():
    raise RuntimeError(
        f"Bridge assets not found at {BRIDGE_DIR}. "
        "Ensure bundle.js and index.html are in the excanim/bridge/ directory."
    )

# Shared Playwright instance
_pw: Playwright | None = None
_browser: Browser | None = None
_page: Page | None = None


def get_browser() -> Browser:
    """Get or create a shared headless Chromium browser. Auto-installs chromium if missing."""
    global _pw, _browser
    if _browser is not None:
        return _browser
    _pw = sync_playwright().start()
    try:
        _browser = _pw.chromium.launch(headless=True)
    except Exception:
        import subprocess, sys
        print("Chromium not found — installing...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        _browser = _pw.chromium.launch(headless=True)
    return _browser


def _get_page() -> Page:
    """Get or create the Excalidraw bridge page."""
    global _page
    if _page is not None:
        return _page
    browser = get_browser()
    _page = browser.new_page()
    _page.goto(f"file://{INDEX_HTML}")
    _page.wait_for_function("window.bridgeReady === true", timeout=30000)
    return _page


def elements_to_svg(elements: list[dict], app_state: dict | None = None) -> str:
    page = _get_page()
    default_state = app_state or {
        "exportWithDarkMode": False,
        "exportBackground": True,
        "viewBackgroundColor": "#ffffff",
    }
    return page.evaluate(
        """async ({elements, appState}) => {
            return await window.renderToSvg(elements, appState, {});
        }""",
        {"elements": elements, "appState": default_state},
    )


def batch_elements_to_svg(
    frames: list[list[dict]], app_state: dict | None = None
) -> list[str]:
    page = _get_page()
    default_state = app_state or {
        "exportWithDarkMode": False,
        "exportBackground": True,
        "viewBackgroundColor": "#ffffff",
    }
    return page.evaluate(
        """async ({frames, appState}) => {
            const results = [];
            for (const elements of frames) {
                const svg = await window.renderToSvg(elements, appState, {});
                results.push(svg);
            }
            return results;
        }""",
        {"frames": frames, "appState": default_state},
    )
