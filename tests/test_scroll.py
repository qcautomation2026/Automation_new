#Scrolling the windows



import pytest

from playwright.async_api import expect
@pytest.mark.asyncio
#fully scrolling the page to the footer and checking if it is visible
async def test_scroll(async_page):
    #await async_page.goto("https://demowebshop.tricentis.com/")
    # footer = async_page.locator(".footer")
    
    # await footer.scroll_into_view_if_needed()
    
    # await async_page.wait_for_timeout(5000)
    # await expect(footer).to_be_visible()
    #--------------------------------------
    
    #scrolling specific amount of pixels down the page and checking if the footer is visible
   
    # await async_page.mouse.wheel(0, 500)
    # await async_page.wait_for_timeout(5000)
    # await async_page.evaluate("window.scrollBy(0, 500)")
    
    #--------------
    #infinite scrolling down the page until the footer is visible
    
    await async_page.goto("https://www.playwrightautomation.com/infinite-scroll.html")
    loading = async_page.get_by_text("Loading more books…").first
    end_of_catalog = async_page.locator("#end-of-catalog")

    scroll = async_page.locator("#scroll-sentinel")

    while True:
        await scroll.scroll_into_view_if_needed()
        print("scroll again")
        await async_page.wait_for_timeout(5000)
        #expect(end_of_catalog).to_be_visible() # stop
        if await end_of_catalog.is_visible():
            print("scroll till end")
            break
    
    