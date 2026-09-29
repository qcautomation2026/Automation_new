import pytest
@pytest.mark.asyncio
async def test_drop(async_page):
  await async_page.goto("https://www.amazon.in/")
  drop_down= async_page.locator("#searchDropdownBox")
    
    #slect index
  await drop_down.select_option(index=5)

#selct vy value

  await drop_down.select_option(value="search-alias=baby")
  
  #select by label
  await drop_down.select_option(label="Electronics")