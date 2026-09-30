import pytest

async def handle_alert(dialog):
    print("alert type", dialog.type)
    print("alert type", dialog.message)
    await dialog.acept()

@pytest.mark.asyncio

async def test_alerst(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/login")
    #await async_page.on("dialog",lambda dialog:handle_alert(dialog))
    await async_page.locator("//input[@class= 'button-1 search-box-button'][@type='submit']").click()
    await async_page.locator("#small-searchterms").fill("abc")