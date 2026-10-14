from playwright.async_api import expect
import pytest
@pytest.mark.asyncio
async def test_filter(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    await async_page.pause()
    login = async_page.get_by_role("link",name="Log in")
    await login.click()
    msg = async_page.get_by_text("Welcome, Please Sign In!")
    await expect(msg).to_be_visible()