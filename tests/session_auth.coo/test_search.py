import pytest
@pytest.mark.asyncio
async def test_serach_(authenticated_page):
    await authenticated_page.goto("https://agents.akbartravelsonline.com/b2bplus/flight")
    assert "login" not in await authenticated_page.current_url
    header =  authenticated_page.locator("//h1[text()='Search Flights']")
    await   header.wait_for_load(state = "visible",timeout=5000)
    assert await header.is_visible()