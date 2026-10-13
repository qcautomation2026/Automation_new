import os
import json

from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright


load_dotenv("/home/user/Documents/New_playwrite/.env")
auth_file = Path("/home/user/Documents/New_playwrite/tests/auth.loginsession.json")
SESSION_STORAGE_FILE = Path ("/home/user/Documents/New_playwrite/tests/auth.session_storage.json")
async def login():
    username = os.getenv("B2B_AGENT_USERNAME")
    password = os.getenv("B2B_AGENT_PASSWORD")
    if not username and not password:
        raise ValueError("un and pwd is missing env file")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        if auth_file.exists():
            await page.goto("https://agents.akbartravelsonline.com/b2bplus/flight")
            if "login" not in page.url:
                print("existing session still valid")
                await browser.close()
                return
        print("Logging in to geanrate a session")
        await page.goto("https://agents.akbartravelsonline.com/b2bplus/login")
        await page.locator("//input[@name='username']").fill(username)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_text(" Sign In ").click()

        await page.locator("//h1[text()='Search Flights']").wait_for(state="visible",timeout=30000)
        await page.wait_for_load_state("networkidle")
        await context.storage_state(path=str(auth_file))
        await page.wait_for_load_state("networkidle")

        # session explicitly
        session_data = await page.evaluate("()=>JSON.stringify(window.sessionStorage)")
        SESSION_STORAGE_FILE.write_text(session_data)
        print("new session is created")
        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(login())