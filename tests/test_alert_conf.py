import pytest


async def handle_confirm_alert(dialog):
    print("alert type:", dialog.type)
    print("alert message:", dialog.message)
    await dialog.dismiss()


@pytest.mark.asyncio
async def test_confirm_alert(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")

    # Register dialog handler BEFORE triggering the alert
    async_page.on("dialog", handle_confirm_alert)

    await async_page.locator("#confirmBtn").click()

