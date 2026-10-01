
import pytest

from playwright.async_api import expect
@pytest.mark.asyncio

async def test_frm(async_page):
   await async_page.goto("https://the-internet.herokuapp.com/upload")
   file_input = async_page.locator("#file-upload")
   await file_input.set_input_files("/home/user/Downloads/download.jpeg")
   await async_page.locator("#file-submit").click()
   await async_page.wait_for_timeout(5000)
   msg = async_page.get_by_text("File Uploaded!")
   await expect(msg).to_be_visible()