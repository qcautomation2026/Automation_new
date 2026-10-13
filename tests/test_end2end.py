
import pytest

from playwright.async_api import expect

@pytest.mark.asyncio

async def test_multi_page(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    #_________________________________________________---
    #    Items
    #-----------------------------------------------------
    item = "Books"
    locator_item = async_page.locator(f"(//a[contains(text(),'{item}')])[3]")
    await expect(locator_item).to_be_visible()
    await locator_item.click()
    # validate :-- books
    books_page = async_page.locator("//h1[text()='Books']")
    try:
        expect(books_page).to_be_visible()
        print("user naviagte to Books page")
    except Exception as e:
        print("user not naviagte to Books page")

    # ---------------------------------------------
    #   collect all products
    #------------------------------------------------
    products = ["Computing and Internet","Fiction","Health Book"]
    for i in products:
        book = async_page.locator(f"//a[text()='{i}']/../..//input[@value='Add to cart']")
        await expect(book).to_be_visible()
        await book.click()
        await async_page.wait_for_timeout(2000)
    count_of_cart = await async_page.locator("//span[text()='(3)']").inner_text()
    try:
        assert count_of_cart == len(products)
        print(count_of_cart , "add to cart")
    except Exception as e:
        print(products , "not add to cart")
    await async_page.wait_for_timeout(2000)

    ############===-----------------------------
    # click on the add to cart
    # --------------------------------------------------

    add_to_cart = async_page.locator("//span[text()='Shopping cart']")
    await expect(add_to_cart).to_be_visible()
    await add_to_cart.click()

    product_in_cart = await async_page.locator("//td[@class='product']/a").all_text_contents()
    try:
        assert product_in_cart == products
        print(add_to_cart , "add to cart")
    except Exception as e:
        print(add_to_cart, "not in add to cart")