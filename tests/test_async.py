import pytest

@pytest.mark.asyncio
async def test_async(async_page):
    await async_page.goto("https://demo.guru99.com/test/simple_context_menu.html")
    double_click = async_page.locator("//button[text()='Double-Click Me To See Alert']")
    await double_click.dblclick()
    