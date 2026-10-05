import pytest
from playwright.async_api import expect

#double click
@pytest.mark.asyncio
async def test_hover(async_page):
    await async_page.goto("https://demo.guru99.com/test/drag_drop.html")
    se =  async_page.locator("(//a[@class='button button-orange'])[5]")
    te = async_page.locator("(//li[@class='placeholder'])[1]")
    
    await se.drag_to(te)
    await async_page.wait_for_timeout(5000)
    