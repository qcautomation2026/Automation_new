import pytest

from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio

async def test_restore_session(async_page):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="session.json")
        page = await context.new_page()
        await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)