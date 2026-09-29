#navigate google type mobile in search, clear, again serch books and enter

import pytest
from playwright.async_api import Page, expect

from conftest import async_page

# @pytest.mark.asyncio
# async def test_google_search(async_page):
#     await async_page.goto("https://www.google.com")
#     await expect(async_page).to_have_title("Google")
#     await async_page.locator("textarea[name='q']").type("mobile")
#     await async_page.locator("textarea[name='q']").clear()
#     await async_page.locator("textarea[name='q']").fill("books")
#     await async_page.locator("textarea[name='q']").press("Enter")
#     await expect(async_page).to_have_title("books - Google Search")


@pytest.mark.asyncio
async def test_google_search(async_page):
 await async_page.goto("https://demowebshop.tricentis.com/")
 ele = async_page.locator("#pollanswers-1")
 print(ele.inner_text())
 #print(await async_page.locator("#pollanswers-1").inner_text())
 ele1= async_page.get_by_text("$25 Virtual Gift Card")
 print(ele1.get_attribute("href"))

#text_content() --> DOM
#Inner_text() --> UI (text)
#input value --> input field
#get_attribute() --> attribute value