
#1st Sign in and registration test case using async and await

import pytest

#for Sign in
@pytest.mark.asyncio
async def test_login(async_page):
    await async_page.goto("https://agents.akbartravelsonline.com/b2bplus/login")
    await async_page.locator('#mat-input-1').fill("revamp2")
    await async_page.locator('#mat-input-2').fill("Rajan@1234*")
    await async_page.locator("//div[normalize-space()='Sign In']").click()





#for registration
@pytest.mark.asyncio
async def test_registor_(async_page):
    await async_page.goto("https://agents.akbartravelsonline.com/b2bplus/apisign-up")
    await async_page.locator('//input[@formcontrolname="Name"]').fill("abc")
    await async_page.locator('//input[@formcontrolname="EmailID"]').fill("abctest@gmail.com")
    await async_page.locator('//input[@formcontrolname="ContactNumber"]').fill("70349173870")
    #time
    await async_page.wait_for_timeout(10000)
    await async_page.locator("//span[text()='Submit']").click()
    ele = async_page.locator("p[text()='Get Ready For Integration! Our Team Will Contact You Shortly.' ]")