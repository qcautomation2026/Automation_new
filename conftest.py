# from playwright.async_api import async_playwright
# import pytest_asyncio

# @pytest_asyncio.fixture
# async def async_page():
#    async with async_playwright() as p:
#        browser = await p.chromium.launch(headless=False)
#        page = await browser.new_page()
#        yield page # act as a generator operator
#        await browser.close()

import asyncio
import pytest
from pathlib import Path

import pytest_asyncio
from playwright.async_api import async_playwright

from tests.auth.login_setup import login
AUTH_FILE = Path("/home/user/Documents/New_playwrite/tests/auth.loginsession.json")
SESSION_STORAGE_FILE = Path("/home/user/Documents/New_playwrite/tests/auth.session_storage.json")

def pytest_sessionstart(session):
    """Pytest hook running globally BEFORE any test execution begins."""
    print("\n--- Running Global Authentication Setup ---")
    asyncio.run(login())

@pytest.fixture
async def authenticated_page():
    """Fully async fixture providing an authenticated Playwright page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Build context arguments with storage state if available
        context_args = {}
        if AUTH_FILE.exists():
            context_args["storage_state"] = str(AUTH_FILE)

        context = await browser.new_context(**context_args)

        # Re-inject sessionStorage tokens into the browser context
        if SESSION_STORAGE_FILE.exists():
            session_data = SESSION_STORAGE_FILE.read_text()
            await context.add_init_script(f"""
                const data = {session_data};
                for (const [key, val] of Object.entries(data)) {{
                    window.sessionStorage.setItem(key, val);
                }}
            """)

        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()

@pytest_asyncio.fixture
async def async_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page
        await browser.close()
       

#
# @pytest.fixture(scope="session")
# def api_request(playwright: Playwright):
#
#     api = playwright.request.new_context(
#         base_url="https://parabank.parasoft.com",
#         extra_http_headers={
#             "Accept": "application/json"
#         }
#     )
#
#     yield api
#
#     api.dispose()