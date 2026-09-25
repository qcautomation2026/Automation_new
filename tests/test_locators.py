#action using get_by_label, get_by_role and fill the input fields and click on register and login button in demowebshop website

def test_locators(page):
   
    #register 
    page.goto("https://demowebshop.tricentis.com/")
    page.get_by_role("link", name="Register").click()
    page.get_by_role("radio", name="Male", exact=True).click()
    page.get_by_role("textbox", name="First name:").fill("vighnesh")
    page.get_by_role("textbox", name="Last name:").fill("qc")
    page.get_by_role("textbox", name="Email").fill("test@gamil.com")
    page.get_by_role("textbox", name="Confirm password:").fill("test@123")
    page.get_by_role("button", name="Register").click()
    page.wait_for_timeout(2000)
    
    #login
    page.get_by_role("link", name="Log in").click()
    page.get_by_role("textbox", name="Email").fill("test@gamil.com")
    page.get_by_role("textbox", name="Password").fill("test@123")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_timeout(2000)