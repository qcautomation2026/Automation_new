#locate the image using alt text and search box using placeholder in amazon website

from playwright.sync_api import sync_playwright, expect
def test_placeholder(page):
    page.goto("https://www.amazon.in/")
    image= page.get_by_alt_text("Art Supplies")
    expect(image).to_be_visible()
    page.get_by_placeholder("Search Amazon.in").fill("laptop")
    page.wait_for_timeout(8000)
    page.keyboard.press("Enter")
    