import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_check_box(async_page):

    await async_page.goto( "https://testautomationpractice.blogspot.com/")
    radio_buttons= await async_page.locator("//label[text()='Gender:']/..//input[@class='form-check-input']").all()
    
    for radio in radio_buttons:
        await radio.click()
        expect(radio).to_be_checked()
        await async_page.wait_for_timeout(3000)