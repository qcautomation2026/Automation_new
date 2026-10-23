# parabank :--> create on user
# create one account
# random
import random
import string
from multiprocessing import context

import pytest
from playwright.async_api import async_playwright, expect


def user_name():
    un = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return un
def email_id():
    email = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{email}@gmail.com"

def phone_num():
    ph_num = "".join(random.choices(string.digits, k=10))
    return ph_num
def ssnno():
    ssn_num = "".join(random.choices(string.digits, k=10))
    return ssn_num

#ui and api
@pytest.mark.asyncio
async def test_ui_api():

    Base_url = "https://parabank.parasoft.com/parabank/"
    Api_url = f"{Base_url}/services/bank/"
    ph = phone_num()
    ssn = ssnno()
    un = user_name()
    pwd = "123456789"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"{Base_url}register.htm")
        await page.locator("//input[@id='customer.firstName']").fill("abc")
        await page.locator("//input[@id='customer.lastName']").fill("a")
        await page.locator("//input[@id='customer.address.street']").fill("abc")
        await page.locator("//input[@id='customer.address.city']").fill("abc")
        await page.locator("//input[@id='customer.address.state']").fill("abc")
        await page.locator("//input[@id='customer.address.zipCode']").fill("123456")
        await page.locator("//input[@id='customer.phoneNumber']").fill(ph)
        await page.locator("//input[@id='customer.ssn']").fill(ssn)
        await page.locator("//input[@id='customer.username']").fill(un)
        await page.locator("//input[@id='customer.password']").fill(pwd)
        await page.locator("//input[@id='repeatedPassword']").fill(pwd)
        await page.locator("//input[@value='Register']").click()
        print("user_name is = " ,un)
        print("pwd = " ,pwd)
        msg = page.get_by_text("Your account was created successfully. You are now logged in.")
        await expect(msg).to_be_visible()
        # await page.get_by_text("Open New Account").click()
        # await page.locator("#type").wait_for()
        # await page.locator("#type").select_option("0")
        # await page.get_by_role("button", name="Open New Account").click()
        # await page.get_by_text("Account Opened!", exact=False).wait_for(timeout=15000)
        # account_id = (await page.locator("#newAccountId").inner_text()).strip()
        # print("STEP 3 PASS: Account opened:", account_id)
        # msg = page.get_by_text("Your account was created successfully. You are now logged in.")
        # await expect(msg).to_be_visible()
        # await page.get_by_text("Open New Account").click()
        # await page.locator("#type").wait_for()
        # await page.locator("#type").select_option("0")
        # await page.get_by_role("button", name="Open New Account").click()
        # await page.get_by_text("Account Opened!", exact=False).wait_for(timeout=15000)
        # account_id = (await page.locator("#newAccountId").inner_text()).strip()
        # print("STEP 3 PASS: Account opened:", account_id)
        api = await p.request.new_context(
            base_url=Api_url,
            extra_http_headers={"Accept": "application/json"}
        )
        res = await api.get(f"login/{un}/{pwd}")
        assert  res.status == 200
        user_info = await res.json()
        user_id = user_info["id"]
        print(user_id) #28862
        print("*******************")
        print(f"user_name is = {un} and pwd is {pwd} user_id id {user_id}" )