#sort the lists
import pytest
@pytest.mark.asyncio
async def test_drop(async_page):
  await async_page.goto("https://www.amazon.in/")
  search_box= async_page.locator("#twotabsearchtextbox")
  await search_box.fill("books")
  
  await async_page.wait_for_timeout(2000)
  
  await search_box.press("ArrowDown")
  await search_box.press("ArrowDown")
  await search_box.press("ArrowDown")
  await search_box.press("Enter")
  
  await async_page.wait_for_timeout(2000)
