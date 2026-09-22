from utils.config import BASE_URL, USERNAME, PASSWORD
def test_navigate(page):
    page.goto(BASE_URL)
    print(page.url)
    print(page.title())
    page.reload()
    page.goto("https://testbook.com/")
    print(page.url)
    page.go_back()
    page.go_forward()
    