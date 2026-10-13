#Auth.jason save 

import pytest

from playwright.async_api import expect

@pytest.mark.asyncio

async def test_auth_form(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    await async_page.get_by_text("Log in").click()
    await async_page.locator("#Email").fill("abcnew1234@gmail.com")
    await async_page.locator("#Password").fill("123456789")
    await async_page.wait_for_timeout(3000)
    await async_page.locator("//input[@value='Log in']").click()
    try:
        async_page.get_by_text("Log out")
    except Exception as e:
        print("user not login")
    #auth.josn
    await async_page.context.storage_state(
        path="auth.json"
    )