# import pytest
# from playwright.async_api import expect
# from urllib3 import request

# from logger_config import logger

# @pytest.mark.asyncio
# async def test_logfile(async_page):
#     logger.info("==============Test Started ==============")
#     # br / js/n/w / http req
#     #browser console msg
#     # 1. Capture browser console messages
#     async_page.on(
#         "console",
#         lambda msg: logger.error(
#             "BROWSER CONSOLE [%s]: %s",
#             msg.type.upper(),
#             msg.text
#         )
#     )

#     # js
#     async_page.on("pageerror",lambda error:logger.error("JAVASCRIPT ERROR [%s]:%s",error))
#     # n/w
#     async_page.on("requestfailed",
#                   lambda request:logger.error("REQUEST FAILED [%s]:%s",
#                 request.url,request.failure))
#     # 4. Capture HTTP error responses
#     async_page.on(
#         "response",
#         lambda response: logger.warning(
#             "HTTP ERROR: %s | Status: %s",
#             response.url,
#             response.status
#         ) if response.status >= 400 else None
#     )


#     await async_page.goto("https://demowebshop.tricentis.com/")
#     logger.info("open the browser naviagte to https://demowebshop.tricentis.com/")
#     login = async_page.get_by_text("Log in")
#     await login.click()
#     logger.info("click on the login link ")
#     email_id = async_page.locator("#Email")
#     await email_id.fill("trivenikmb@gmail.com")
#     pwd = async_page.locator("#Password")
#     await pwd.fill("123456789")
#     logger.info("entee the un and pwd ")
#     login_button = async_page.locator("//input[@value='Log in1234']")
#     await login_button.click()
#     logger.info("click on the login button ")
#     log_out = async_page.locator("#Log out11324")
#     try:
#         await expect(log_out).to_be_visible()
#         logger.info("logout is visible")
#     except Exception as e:
#         logger.error("logoin failed")

import asyncio

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_main():

    logger.info("========== TEST EXECUTION STARTED ==========")

    try:
        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=False)

            page = await browser.new_page()

            # 1. Capture browser console messages
            page.on(
                "console",
                lambda msg: logger.error(
                    "BROWSER CONSOLE [%s]: %s",
                    msg.type.upper(),
                    msg.text
                )
            )

            # 2. Capture JavaScript errors
            page.on(
                "pageerror",
                lambda error: logger.error(
                    "JAVASCRIPT ERROR: %s", error
                )
            )

            # 3. Capture failed network requests
            page.on(
                "requestfailed",
                lambda request: logger.error(
                    "REQUEST FAILED: %s | Error: %s",
                    request.url,
                    request.failure
                )
            )

            # 4. Capture HTTP error responses
            page.on(
                "response",
                lambda response: logger.warning(
                    "HTTP ERROR: %s | Status: %s",
                    response.url,
                    response.status
                ) if response.status >= 400 else None
            )

            logger.info("Launching browser: Chromium")

            # Navigate to application
            logger.info("Opening Demo Web Shop")
            await page.goto(
                "https://demowebshop.tricentis.com/",
                wait_until="domcontentloaded"
            )

            logger.info("Page title: %s", await page.title())

            # Search for a book
            search_box = page.get_by_role(
                "textbox", name="Search store"
            )

            await search_box.fill("book")
            await page.get_by_role(
                "button", name="Search"
            ).click()

            logger.info("Search executed successfully")

            # Wait for search results to appear
            await page.locator(
                ".product-item"
            ).first.wait_for(state="visible")

            logger.info("Search results are visible")

            logger.info("TEST RESULT: PASSED")

            await browser.close()
            logger.info("Browser closed successfully")

    except Exception:
        logger.exception("TEST RESULT: FAILED")

    finally:
        logger.info("========== TEST EXECUTION FINISHED ==========")