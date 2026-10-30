import pytest
from playwright.async_api import async_playwright
#@pytest.mark.asyncio
# async def test_step1():
#     async with async_playwright() as p:
#        browser =  await p.chromium.launch(headless=False,args=["--start-maximized"])
#        context = await browser.new_context(
#            record_har_path="network1_log.har"
#        ) # file har file
#        page =await context.new_page()
#        # setup
#        # page.on("",function)
#        # console msg
#        page.on("console", lambda msg: print(f"[{msg.type.upper()}]: console {msg.text}"))
#        # Js
#        page.on("pageerror",lambda err:print(f"[PAGE ERROR] {err}"))
#        # get res and
#        #req and resp
#        # why :-->rep data res
#        async def had_req(req):
#            post_data = req.post_data
#            data_str = f"Payload:{post_data} if post_data else "" "
#            print(f" req : {req.method} : {req.url} {req.post_data}")
#        page.on("request", had_req)
#        async def had_res(res):
#            content_type = res.headers.get("content_type","unknown")
#            print(f"res : {res.status} {content_type} {res.url}")

#        page.on("response" ,had_res)

#        # test
#        await page.goto("https://parabank.parasoft.com/parabank/index.htm")
#        await page.get_by_text("Register").click()
#        await page.wait_for_timeout(5000)
#        await context.close()
#        await page.close()

# @pytest.mark.asyncio
# async def test_main():
#    async with async_playwright() as p:
#        browser = await p.chromium.launch(headless=False)
#        page = await browser.new_page()
#        async def intercept(route):
#            request = route.request
#            url = request.url.lower()
#            resource_type = request.resource_type
#            if resource_type in ["image", "font"]:
#                print("BLOCKED RESOURCE:", url)
#                await route.abort()
#            elif "analytics" in url:
#                print("BLOCKED ANALYTICS:", url)
#                await route.abort()
#            else:
#                await route.continue_()


#        await page.route("**/*", intercept)
#        await page.goto("https://parabank.parasoft.com/parabank/index.htm")
#        await page.get_by_text("Register").click()
#        await page.wait_for_timeout(5000)
#        await page.close()

#--------------------------
@pytest.mark.asyncio
async def test_main():
   async with async_playwright() as p:
       browser = await p.chromium.launch(headless=False)
       page = await browser.new_page()
       async def req_(req):
           if "/api/" in req.url:
               print("url:" ,req.url )
               print("method:", req.method)
               print("headers:", req.all_headers)
               print("payload" , req.req_data)


       page.on("request", req_)

       async def res_(res):
           print("api  resp")
           print("url" ,res.url)
           print("status:",res.status_code)
           content_type = res.headers.get("content-type", "")
           # If the response is JSON, decode it automatically into a Python dictionary
           if "application/json" in content_type:
               try:
                   print("JSON:", await res.json())
               except Exception as error:
                   print("Could not read JSON:", error)

       page.on("response", res_)
       await page.goto("https://parabank.parasoft.com/parabank/index.htm")
       await page.get_by_text("Register").click()
       await page.wait_for_timeout(5000)
       await page.close()
       
#------------Network Interception----------------
       