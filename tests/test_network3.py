#1. Measuring page performance metrics
import asyncio
import pytest
from playwright.async_api import async_playwright
@pytest.mark.asyncio


async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        response = await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)
        assert response is not None
        assert response.status < 400
        metrics = await page.evaluate("""() => {
            const timing = performance.getEntriesByType(
                'navigation'
            )[0];

            return {
                domContentLoaded:
                    timing.domContentLoadedEventEnd -
                    timing.startTime,
                loadEvent:
                    timing.loadEventEnd - timing.startTime,
                responseTime:
                    timing.responseEnd - timing.requestStart,
                resourceCount:
                performance.getEntriesByType('resource').length
            };
        }""")

        print("http status" , response.status)
        print(metrics)