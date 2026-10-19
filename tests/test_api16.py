import pytest
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:3000/"
@pytest.mark.asyncio
async def test_api():
    async with async_playwright() as playwright:
        api = await playwright.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Accept": "application/json"},
            timeout=5000
        )
        #http://localhost:3000/posts
        resp =  await api.get("posts")
        assert resp.status == 200 
        print(await resp.text())
        print("*" * 30)
        print(await resp.json())


