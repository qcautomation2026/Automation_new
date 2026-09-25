#list the links on the akbartravels website and click on first, last and 2nd link

def test_links(page):
    page.goto("https://www.akbartravels.com/in",wait_until='domcontentloaded')
    links = page.locator("a")
    
    for i in links.all():
        print("links", i.get_attribute("href"),flush=True)  # print all links on the page
        
        
    links.last.click()# click on last link
    links.first.click()  # click on first link
    links.nth(1).click()  # click on 2nd link    