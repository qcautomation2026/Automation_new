import pytest
@pytest.mark.asyncio
async def test_drop(async_page):
  await async_page.goto("https://www.amazon.in/")
  search_box= async_page.locator("#twotabsearchtextbox")
  await search_box.fill("books")
  
  #dynamic drop down
  lists= async_page.locator("//div[@class='s-suggestion s-suggestion-ellipsis-direction']")
  
  #list all suggesion
  await lists.first.wait_for()
  
  #print the no of lists
  count=await lists.count()
  print("Total lists: ", count)
  
  #print lists using with index
  
  for i in range(count):
      text= await lists.nth(i).inner_text()  
      print(f"{i} : {text}")
      
  await async_page.get_by_text("helf for home").click()  
  await async_page.wait_for_timeout(2000)