import pytest
from playwright.async_api import async_playwright
from playwright.sync_api import expect


@pytest.mark.asyncio
async def test_trace():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )
        try:
            page = await context.new_page()
            await page.goto("https://parabank.parasoft.com/parabank/register.htm")
            username = "1213ran1dom123"
            password = "abc@123"

            await page.locator(
                'input[name="customer.firstName"]'
            ).fill("abc")

            await page.locator(
                'input[name="customer.lastName"]'
            ).fill("a")

            await page.locator(
                'input[name="customer.address.street"]'
            ).fill("10 Test Street")

            await page.locator(
                'input[name="customer.address.city"]'
            ).fill("Bengaluru")

            await page.locator(
                'input[name="customer.address.state"]'
            ).fill("Karnataka")

            await page.locator(
                'input[name="customer.address.zipCode"]'
            ).fill("560001")

            await page.locator(
                'input[name="customer.phoneNumber"]'
            ).fill("9876543210")

            await page.locator(
                'input[name="customer.ssn"]'
            ).fill("123456789")

            await page.locator(
                'input[name="customer.username"]'
            ).fill(username)

            await page.locator(
                'input[name="customer.password"]'
            ).fill(password)

            await page.locator(
                'input[name="repeatedPassword"]'
            ).fill(password)

            # STEP 3: Submit registration
            await page.locator(
                'input[value="Register"]'
            ).click()

            # STEP 4: Validate registration result
            await expect(
                page.locator("#rightPanel")
            ).to_contain_text("Welcome")

            print("UI registration successful:", username)

           
        except Exception as e:
            print(f"error is {e}")
        finally:
            await context.tracing.stop(
                path="D:/AI/Python_playwright/tracing/trace1.zip"
            )
            await context.close()