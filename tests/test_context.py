from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context1 = browser.new_context()
    page1 = context1.new_page()

    
    context2 = browser.new_context()
    page2 = context2.new_page()

    # User A
    page1.goto("https://google.com")
    print("User A:", page1.title())

    # User B
    page2.goto("https://google.com")
    print("User B:", page2.title())

    browser.close()