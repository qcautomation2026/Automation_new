# date picker

import pytest

from playwright.async_api import expect
@pytest.mark.asyncio

async def test_date_picker(async_page):
    await async_page.goto("https://jqueryui.com/datepicker/")
    frame = async_page.frame_locator(".demo-frame")
    date_input = frame.locator("#datepicker")
    await date_input.click()

    user_month = "December"
    user_year = "2026"
    user_day = "29"
    while True:
        cm =await frame.locator(".ui-datepicker-month").inner_text()
        cy = await frame.locator(".ui-datepicker-year").inner_text()
        if cm == user_month and cy == user_year:
            break

        next = frame.locator(".ui-datepicker-next")
        await next.click()
    await frame.get_by_text(user_day).click()
    await async_page.wait_for_timeout(5000)