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

import pytest
from playwright.async_api import expect

from logger_config import logger

@pytest.mark.asyncio
async def test_logfile(async_page):
    logger.info("============== Test Started ==============")
    
    # 1. Capture browser console messages
    async_page.on(
        "console", 
        lambda msg: logger.error(
            "BROWSER CONSOLE [%s]: %s",
            msg.type.upper(),
            msg.text
        )
    )
    
    # 2. Capture JavaScript errors
    async_page.on(
        "pageerror", 
        lambda error: logger.error("JAVASCRIPT ERROR: %s", error)
    )
    
    # 3. Capture failed network requests
    async_page.on(
        "requestfailed",
        lambda req: logger.error("REQUEST FAILED [%s]: %s", req.url, req.failure)
    )
    
    # 4. Capture HTTP error responses (status >= 400)
    async_page.on(
        "response",
        lambda response: logger.warning(
            "HTTP ERROR: %s | Status: %s",
            response.url,
            response.status
        ) if response.status >= 400 else None
    )

    # Navigate to application
    await async_page.goto("https://demowebshop.tricentis.com/")
    logger.info("Opened browser and navigated to https://demowebshop.tricentis.com/")
    
    # Click Login Link
    login = async_page.get_by_text("Log in")
    await login.click()
    logger.info("Clicked on the login link")
    
    # Enter Credentials
    email_id = async_page.locator("#Email")
    await email_id.fill("trivenikmb@gmail.com")
    
    pwd = async_page.locator("#Password")
    await pwd.fill("123456789")
    logger.info("Entered username and password")
    
    # Click Login Button (Corrected locator value)
    login_button = async_page.locator("input.login-button") # or "//input[@value='Log in']"
    await login_button.click()
    logger.info("Clicked on the login button")
    
    # Validate Login via Logout element (Corrected locator using class or text)
    log_out = async_page.locator(".ico-logout")
    try:
        await expect(log_out).to_be_visible(timeout=5000)
        logger.info("Login successful - Logout is visible")
    except Exception as e:
        logger.error("Login failed or logout link not visible: %s", str(e))
        raise