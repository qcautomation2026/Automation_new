import pytest

from playwright.async_api import expect

@pytest.mark.asyncio

async def test_multi_step_form(async_page):
    await async_page.goto("https://demoqa.com/automation-practice-form")
    fn  =  async_page.locator("//input[@id='firstName']")
    await fn.fill("abc")
    ln = async_page.locator("#lastName")
    await ln.fill("a")
    email = async_page.locator("#userEmail")
    await email.fill("abc@gmail.com")
    g = async_page.locator("#gender-radio-1")
    await g.click()
    ph = async_page.locator("#userNumber")
    await ph.fill("1234567899")
    # date = async_page.locator("#dateOfBirthInput")
    # await date.clear()
    # await date.click()
    # date_ = async_page.locator("//div[text()='9']")
    # await date_.click()
    # sub = async_page.locator("//div[@class='subjects-auto-complete__input-container css-19bb58m']")
    # await sub.fill("abc")

    assert await fn.input_value() == "abc"
    assert await ln.input_value() == "a"
    assert await email.input_value() == "abc@gmail.com"
    await expect(g).to_be_checked()
    assert await ph.input_value() == "1234567899"
    # assert await date.input_value() == "09 Oct 2026"
    # assert await sub.input_value() == "abc"
    await async_page.wait_for_timeout(5000)
    submit = async_page.locator("//button[@id='submit']")
    await submit.click()
    
    
    