import pytest
from playwright.async_api import expect

#mouse hover
@pytest.mark.asyncio
async def test_hover(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    ele = async_page.locator("(//a[contains(text(),'Computers')])[1]")
    await ele.hover()
    
    ele1= async_page.locator("(//a[contains(text(),'Desktops')])[1]")
    await expect(ele1).to_be_visible()
    await async_page.wait_for_timeout(5000)
    await ele1.click()
    print(await async_page.title())
    await async_page.wait_for_timeout(5000)
    
    