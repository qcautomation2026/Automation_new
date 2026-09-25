
#print the number of products and their names in the demowebshop website

def test_get_options(page):
    page.goto("https://demowebshop.tricentis.com/",wait_until='domcontentloaded')
    page.locator("(//a[contains(text(), 'Books')])[3]").click()
    products_locators = page.locator("//h2[@class='product-title']")

    
    print("num of books =", products_locators.count())  #num of products
    
    print("products list", products_locators.all_inner_texts())
    
    print("First Book is:", products_locators.nth(0).inner_text()) # print first Book name
    
    product_list = ["Computing and Internet", "Fiction", "Health Book", "Science"]
    
    for i in product_list:
        page.locator(f"//a[text()='{i}']/../..//input[@value='Add to cart']").click()
        