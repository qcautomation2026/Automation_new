import pytest
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:3000/"
pytest.mark.asyncio
# async def test_api_post_on_comment():
#         async with async_playwright() as playwright:
#             api = await playwright.request.new_context(
#                 base_url=BASE_URL,
#                 extra_http_headers={"Accept": "application/json"},
#                 timeout=5000
#             )
#             resp = await api.post("posts",data={
#             "title": "NoteBOOK",
#             "views": 300
#             })
#             resp_json = await resp.json()
#             res_id = resp_json["id"]
#             #============================ post commet=============
#             resp_com = await api.post("comments",data={
#                 "text": "demo",
#                 "postId": res_id
#                 })
#             print(await resp.json())


# modify the title and views 

#-------------------------post-------------------------------     
            
            
            
# pytest.mark.asyncio
# async def test_api_post_on_put():
#     async with async_playwright() as playwright:
#             api = await playwright.request.new_context(
#                 base_url=BASE_URL,
#                 extra_http_headers={"Accept": "application/json"},
#                 timeout=5000
#             )
#             await api.put("posts/1",data={
#                 "views": 500
#             })
#-----------------------patch---------------------------

# async def test_api_post_on_patch():
#     async with async_playwright() as playwright:
#             api = await playwright.request.new_context(
#                 base_url=BASE_URL,
#                 extra_http_headers={"Accept": "application/json"},
#                 timeout=5000
#             )
#             await api.patch("posts/1",data={
#                 "views": 800,
#                 "title": "API Testing"
                
#             })

#-----------------------Delete and check Bad Request--------------------------- 

#@pytest.mark.asyncio
#using api fixture from conftest.py
async def test_api_patch(api):

            await api.delete("comments/1")

            res =  await api.get("comments/1")
            assert  res.status >= 400
            print(await res.json())