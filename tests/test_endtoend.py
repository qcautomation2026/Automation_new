import pytest

from playwright.async_api import expect

@pytest.mark.asyncio

async def test_endtoend(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    #_________________________________________________---
    #    Items
    #-----------------------------------------------------
    item = "Books"
    locator_item = async_page.locator(f"(//a[contains(text(),'{item}')])[3]")
    await expect(locator_item).to_be_visible()
    await locator_item.click()
    # ---------------------------------------------
    #   collect all products
    #------------------------------------------------
    products = ["Computing and Internet","Fiction","Health Book"]
    for i in products:
        book = async_page.locator(f"//a[text()='{i}']/../..//input[@value='Add to cart']")
        await expect(book).to_be_visible()
        await book.click()
        await async_page.wait_for_timeout(2000)

    ############===-----------------------------
    # click on the add to cart
    # --------------------------------------------------

    add_to_cart = async_page.locator("//span[text()='Shopping cart']")
    await expect(add_to_cart).to_be_visible()
    await add_to_cart.click()

    terms_cond = async_page.locator("//input[@id='termsofservice']")
    await expect(terms_cond).to_be_visible()
    await terms_cond.click()

    check_out = async_page.locator("//button[@id='checkout']")
    await expect(check_out).to_be_visible()
    await check_out.click()
# reg = async_page.locator("//input[@value='Register']")
    # await expect(reg).to_be_visible()
    # await reg.click()
    #===================================================
    # = Reg
    #===================================================
    #
    # Female = async_page.get_by_text("Female")
    # await expect(Female).to_be_visible()
    # await Female.click()
    # await async_page.get_by_label("First name:").fill("abc")
    # await async_page.get_by_label("Last name:").fill("a")
    # await async_page.get_by_label("Email:").fill("abcnew1234@gmail.com")
    # await async_page.get_by_label("Password:").nth(0).fill("123456789")
    # await async_page.get_by_label("Confirm password:").fill("123456789")
    # await async_page.locator("#register-button").click()
    # try:
    #     async_page.get_by_text("Log out")
    # except Exception as e:
    #     print("user not reg")
# =================================================================#
    # login
# ====================================================================
    await async_page.locator("#Email").fill("abcnew1234@gmail.com")
    await async_page.locator("#Password").fill("123456789")
    await async_page.locator("//input[@value='Log in']").click()
    try:
        async_page.get_by_text("Log out")
    except Exception as e:
        print("user not login")
    #=====================================================
  #  order
    #=========================================================
    add_to_cart = async_page.locator("//span[text()='Shopping cart']")
    await expect(add_to_cart).to_be_visible()
    await add_to_cart.click()

    terms_cond = async_page.locator("//input[@id='termsofservice']")
    await expect(terms_cond).to_be_visible()
    await terms_cond.click()

    check_out = async_page.locator("//button[@id='checkout']")
    await expect(check_out).to_be_visible()
    await check_out.click()
# await async_page.locator("#BillingNewAddress_Company").fill("Demo")
    # await async_page.locator("#BillingNewAddress_CountryId").select_option(label = "India")
    # await async_page.locator("#BillingNewAddress_City").fill("Mysore")
    # await async_page.locator("#BillingNewAddress_Address1").fill("Srinagar")
    # await async_page.locator("#BillingNewAddress_Address2").fill("Srinagar")
    # await async_page.locator("#BillingNewAddress_ZipPostalCode").fill("5056256")
    # await async_page.locator("#BillingNewAddress_PhoneNumber").fill("123456789")
    # await async_page.locator("#BillingNewAddress_FaxNumber").fill("12345")
    await async_page.locator("(//input[@title='Continue'])[1]").click()
    await async_page.wait_for_timeout(5000)
    await async_page.locator("#PickUpInStore").click()
    await async_page.locator("(//input[@title='Continue'])[2]").click()
    await async_page.wait_for_timeout(5000)
    await async_page.locator("#paymentmethod_0").click()
    await async_page.locator("(//input[@value='Continue'])[4]").click()
    await async_page.wait_for_timeout(2000)
    await async_page.locator("(//input[@value='Continue'])[5]").click()
    #//table[@class='cart-total']//tr/td
    order_deatils = await async_page.locator("//table[@class='cart-total']//tr/td").all()
    for i in order_deatils:
        print(await i.inner_text())
    await async_page.wait_for_timeout(2000)
    await async_page.locator("(//input[@value='Confirm'])").click()
