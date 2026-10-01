#multiple windows
import pytest
from playwright.async_api import expect

@pytest.mark.asyncio
async def test_frm(async_page):
   await async_page.goto("https://demowebshop.tricentis.com/")
   
   # --------------------------Facebook
   async with async_page.expect_popup() as popup_info:
       facebook = async_page.get_by_text("Facebook")
       await expect(facebook).to_be_visible()
       await facebook.click()
   facebook_page = await popup_info.value
   await facebook_page.wait_for_load_state()
   print(facebook_page.url)
   print(facebook_page.title)
   email = facebook_page.locator("(//input[@name='email'])[2]")
   await expect(email).to_be_visible()
   await email.fill("abc@gmail.com")
   print(await email.input_value())
   
   # come back to demo webshop
   await async_page.bring_to_front()
   
   # ------ event google
   async with async_page.expect_popup() as popup_info:
       google = async_page.get_by_text("Google+")
       await expect(google).to_be_visible()
       await google.click()
   google_page = await popup_info.value
   await google_page.locator("//input[@name='q']").fill("Books")
    