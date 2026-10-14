from playwright.async_api import expect
import pytest
@pytest.mark.asyncio



async def test_filter(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    reg_or_log=(async_page.get_by_role("link",name="Register").or_(async_page.get_by_role("link",name = "Log in")))
    ele = await reg_or_log.all_text_contents()
    print(ele)