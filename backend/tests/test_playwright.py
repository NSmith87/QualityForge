import os

import pytest

from qualityforge.graph import requirement_from_request, run_pipeline

pytestmark = pytest.mark.playwright


def test_generated_spec_is_playwright() -> None:
    requirement = requirement_from_request(
        title="Shopper can open the cart",
        text="As a shopper I can open the cart from https://example.com",
        requirement_id="QF-1",
    )
    run = run_pipeline(requirement)
    spec = run.tests[0].spec
    assert "from playwright.async_api import" in spec
    assert "page.goto" in spec
    assert "https://example.com" in spec
    assert run.results[0].diagnostics[0].startswith("dry-run:")


@pytest.mark.skipif(os.getenv("PLAYWRIGHT_LIVE") != "1", reason="PLAYWRIGHT_LIVE is not enabled")
def test_live_example_com_heading() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        assert page.get_by_role("heading", name="Example Domain").is_visible()
        browser.close()
