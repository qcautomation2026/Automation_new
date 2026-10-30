
import asyncio
import json

import pytest
from playwright.async_api import async_playwright
@pytest.mark.asyncio
async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # slow
        async def modify_req(route):
            print(route.request.url)
            req = route.request
            header = await req.all_headers()
            # custom herder
            header["x-test-client"] = "playwright-Async"
            # post with playload
            if req.method == "POST" and req.post_data:
                try:
                    payload =json.load(req.post_data)
                    if isinstance(payload, dict):
                        print(payload)
                        if "quantity" in payload:
                            payload["quantity"] = 5

                            update_playload = json.dumps(payload)
                            print(update_playload)
                            await route.continue_(
                                headers=header,
                                post_data=update_playload
                            )
                            return
                except json.JSONDecodeError:
                    print("req body not json")

            await route.continue_(headers=header)
                    # {"key" : "value }
        await page.route(
            "**/api/**",modify_req
        )
# api :-->
        await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)
        await browser.close()