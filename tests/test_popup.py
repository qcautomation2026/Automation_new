# import pytest
# from playwright.async_api import expect


# @pytest.mark.asyncio
# async def test_frm(async_page):
#     await async_page.goto("https://demo.guru99.com/test/guru99home/")
#     await async_page.wait_for_timeout(3000)
#     frame =async_page.frame.locator("#a077aa5e")
    
#     img= frame.locator("img[src='Jmeter720.png']")
#     await expect(img).to_be_visible()
#     await img.click()
    
    
#     email= async_page.get_by_placeholder("Enter Email")
#     await expect(email).to_be_visible()
#     await email.fill("vighnes@gmail.com")
#     print(await email.input_value())

import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_frm(async_page):
    await async_page.goto("https://demo.guru99.com/test/guru99home/", wait_until="load")
    
    frame = async_page.frame_locator("#a077aa5e")
    
    img =  frame.locator("//img[@src='Jmeter720.png']")
    await expect(img).to_be_visible()
    await img.click()

    email =  async_page.get_by_placeholder("Enter Email")
    await expect(email).to_be_visible()
    await email.fill("abc@gmail.com")
    print(await email.input_value())    