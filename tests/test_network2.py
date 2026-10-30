
#step 6 .Capture network traffic for performance analysis(har)

import asyncio
import pytest
from playwright.async_api import async_playwright
@pytest.mark.asyncio
async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            record_har_path= "network_traffic.har"
        )
        page = await context.new_page()
        async def log_res(response):
           req =  response.request
           timings = req.timing

           st =  timings.get("startTime" , 0)
           et = timings.get("endTime" , -1)

           if et >= 0:
                duration = et - st
                print(
                    f"status : {response.status}",
                    f"Time : {duration:.2f} ms ",
                    f"url : {req.url}"
                )

        page.on("response" ,
                lambda  response : asyncio.create_task(log_res(response)))
        await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)
        await context.close()
        await browser.close()