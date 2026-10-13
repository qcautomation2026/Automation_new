#using keybord action to move the slider

import pytest

from playwright.async_api import expect
@pytest.mark.asyncio
#
async def test_slider(async_page):
    await async_page.goto("https://jqueryui.com/slider/#range")
    frame = async_page.frame_locator(".demo-frame")
    slider = frame.locator("#slider-range")
    min = slider.nth(0)
    max = slider.nth(1)
    await async_page.wait_for_timeout(5000)
    await min.click()
    await min.press("Home")
    for i in range(20):
        await min.press("ArrowRight")
        await async_page.wait_for_timeout(2000)
    await max.click()
    await max.press("End")
    for i in range(20):
        await min.press("ArrowLeft")
        await async_page.wait_for_timeout(2000)