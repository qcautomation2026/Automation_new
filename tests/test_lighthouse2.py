
import json
import subprocess
from pathlib import Path
from tabnanny import check

import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_sanity_dom_check():
    url = "https://parabank.parasoft.com/parabank/register.htm"
    async with (async_playwright() as p):
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        title =await page.title()
        print("title is not missing") if bool(title.strip()) else print("title is missing") #  bool("") False bool("sddd") true
        check.is_true(bool(title.strip()),"title is missing")

        # alt :-->
        missing_alt = await page.locator("img:not([alt])").count()
        print(missing_alt)
        check.equal(missing_alt,0,f"{missing_alt} num of img missing alt attribute")

        main_count = await page.locator("main").count()
        print(main_count)
        check.equal(main_count, 0, f"{main_count} main landlandmarks missing")