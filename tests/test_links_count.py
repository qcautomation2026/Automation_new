def test_count_the_links(page):
    page.goto("https://www.amazon.in/" ,wait_until="domcontentloaded")
    links_locator = page.locator("//a")
    links_locator.first.wait_for(state="attached")
    links = links_locator.all()
    print(len(links))
    print(len(links))
    print(type(links))
    for i in links:
        print(i.text_content(),flush =True)
        print("*"* 50)
        for i in links:
            print(i.get_attribute("href"),flush=True)

# def test_count_the_link(page):
#     page.goto("https://demowebshop.tricentis.com/")
#     links_locator = page.locator("//a")
#     #wait until atleast one link is visible in the page

#     links = links_locator.all()   
#     print(len(links)) # how many links are present in the page

#     print(type(links))

#     for i in links:
#         print(i.text_content(), flush =True) # text of the link
#     print("*"*50)
#     for i in links:
#         print(i.get_attribute("href"), flush =True) #href attribute of the link
