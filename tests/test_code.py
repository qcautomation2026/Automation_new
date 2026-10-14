import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://demowebshop.tricentis.com/")
    await page.get_by_role("link", name="Register").click()
    await page.goto("https://demowebshop.tricentis.com/register")
    await expect(page.get_by_role("heading", name="Register")).to_be_visible()
    await page.get_by_role("link", name="Log in").click()
    await page.goto("https://demowebshop.tricentis.com/login")
    await expect(page.get_by_role("heading", name="Welcome, Please Sign In!")).to_be_visible()
    await page.locator("#small-searchterms").click()
    await page.locator("#small-searchterms").fill("books")
    await page.locator("#small-searchterms").click()
    await page.locator("#small-searchterms").press("Enter")
    await page.goto("https://demowebshop.tricentis.com/search?q=books")
    await expect(page.get_by_text("No products were found that")).to_be_visible()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())