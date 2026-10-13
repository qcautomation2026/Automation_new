import pytest

from playwright.async_api import async_playwright, expect

@pytest.mark.asynci

async def test_api_data_validation(async_page):
    Base_url = "https://parabank.parasoft.com/parabank"
    end_point = "register.htm"
    username = "vavachi"
    password = "abc@123"
    await async_page.goto(Base_url+"/"+end_point)

    await async_page.locator("#customer\\.firstName").fill("vavachi")
    await async_page.locator("#customer\\.lastName").fill("K")
    await async_page.locator("#customer\\.address\\.street").fill(
        "100 Test Street"
    )
    await async_page.locator("#customer\\.address\\.city").fill(
        "Bengaluru"
    )
    await async_page.locator("#customer\\.address\\.state").fill(
        "Karnataka"
    )
    await async_page.locator("#customer\\.address\\.zipCode").fill(
        "560001"
    )
    await async_page.locator("#customer\\.phoneNumber").fill(
        "9876543210"
    )
    await async_page.locator("#customer\\.ssn").fill("123456789")
    await async_page.locator("#customer\\.username").fill(username)
    await async_page.locator("#customer\\.password").fill(password)
    await async_page.locator("#repeatedPassword").fill(password)

    await async_page.locator("input[value='Register']").click()

    # Verify registration result
    await expect(
        async_page.locator("#rightPanel")
    ).to_contain_text("successfully", ignore_case=True)

    print("Customer registered:", username)