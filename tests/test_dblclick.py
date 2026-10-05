import pytest
from playwright.async_api import expect

#double click
@pytest.mark.asyncio
async def test_hover(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    button = async_page.get_by_text("Copy Text")
    await button.dblclick()
    ele =async_page.locator("#field2")
    print(await ele.input_value())