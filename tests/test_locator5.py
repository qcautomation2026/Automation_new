#locate the title of the demowebshop website

from playwright.sync_api import sync_playwright, expect
def test_title(page):
    page.goto("https://demowebshop.tricentis.com/")
    title = page.get_by_title("Speed | Tricentis")
    expect(title).to_be_visible()