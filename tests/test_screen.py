from playwright.async_api import expect
import pytest
from pathlib import Path

PHOTO_DIR = Path("photos")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

@pytest.mark.asyncio
async def test_sc(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    products = async_page.locator(".product-title")
    simple_comp = products.filter(has_text="Simple Computer")
    await simple_comp.first.click()
    ele = async_page.locator("//h1[@itemprop='name']")
    await expect(ele).to_be_visible()
    await async_page.screenshot(path=str(PHOTO_DIR / "Simple Computer.png"),full_page=True)
    