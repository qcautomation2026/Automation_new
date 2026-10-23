import pytest
from playwright.async_api import async_playwright, expect
@pytest.mark.asyncio
async def test_ui_api():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://demowebshop.tricentis.com/login")
        print(await page.title())
        api = await p.request.new_context(
            base_url="https://demowebshop.tricentis.com/",
            extra_http_headers={"Accept": "application/json"}
        )
        resp = await api.get("login")
        print(await resp.text())