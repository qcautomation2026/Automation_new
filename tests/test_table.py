def test_count_links(page):
    page.goto("https://www.w3schools.com/html/html_tables.asp")
    table_count=page.locator("//table").count() #how many tables are there in the page
    print(table_count,flush=True)
    