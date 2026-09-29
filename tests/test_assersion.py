#type of assersions
#1- expected vs actual
# 2- expected vs actual with message


import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_google_search(async_page):
 await async_page.goto("https://demowebshop.tricentis.com/")
#  ele= async_page.locator(".topic-html-content-header")
#  expect(ele).to_be_visible()
#  print(await(ele.inner_text()))

 await expect(async_page).to_have_title("Demo Web Shop")
 options = async_page.locator("//li[@class='answer']")
 await expect(options).to_have_count(4)
 #await async_page.locator("(//li[@class='answer'])[1]").click()
 await options.nth(0).click()
 
   
 
 