import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_check_box(async_page):

    # Open the website
    await async_page.goto( "https://testautomationpractice.blogspot.com/")

    # Locate the Sunday checkbox
    check_box = async_page.locator("#sunday")
    
    await expect(check_box).not_to_be_checked()
    # Check the checkbox
    await check_box.check()

    # Verify that it is checked
    await expect(check_box).to_be_checked()
    await async_page.wait_for_timeout(3000)
   

    print("Sunday checkbox is checked")
