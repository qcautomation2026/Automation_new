import pytest
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:3000/"
pytest.mark.asyncio
# async def test_api_post():
#         async with async_playwright() as playwright:
#             api = await playwright.request.new_context(
#                 base_url=BASE_URL,
#                 extra_http_headers={"Accept": "application/json"},
#                 timeout=5000
#             )
#             resp = await api.post("posts",
#                            data={
#                                 "title": "Java and python",
#                                 "views": 500
#                                 })
#             assert resp.status == 201
#             resp_json = resp.json()
#             print(await resp.json())
#             print(await resp.text())

# async def test_api_get_comment():
#         async with async_playwright() as playwright:
#             api = await playwright.request.new_context(
#                 base_url=BASE_URL,
#                 extra_http_headers={"Accept": "application/json"},
#                 timeout=5000
#             )
#             resp = await api.get("comments/1")
#             print(await resp.json())

# 
async def test_api_get_profile():
        async with async_playwright() as playwright:
            api = await playwright.request.new_context(
                base_url=BASE_URL,
                extra_http_headers={"Accept": "application/json"},
                timeout=5000
            )
            resp = await api.get("profile")
            print(await resp.json())