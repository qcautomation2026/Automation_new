#get_by_lable

def test_locators(page):
    #register 
    page.goto("https://demowebshop.tricentis.com/")
    register_link = page.get_by_text("Register")
    register_link.click()
    page.get_by_label("Male").nth(0).check()
    page.get_by_label("First name:").fill("vighnesh")
    page.get_by_label("Last name:").fill("qc")
    page.get_by_label("Email:").fill("abc@12gmail.com")
    page.get_by_label("Password:").nth(0).fill("test@123")
    page.get_by_label("Confirm password:").fill("test@123")
    page.get_by_role("button", name="Register").click()
    