import json

import pytest
from playwright.async_api import async_playwright
import pytest_asyncio

#-------------Getting the account details for a customer using the API----------------
# @pytest.mark.asyncio
# async def test_get_acc(api):
#     res  = await api.get("customers/12212/accounts",
#                   headers={"Accept": "application/json"}, )
#     print(await res.json())
#     body = await res.text()
#     print(body)
#     assert res.status == 200
#     accounts = json.loads(body)
#     for acc in accounts:
#         print("account id:" ,acc.get("id",acc.get("customerId")))
#         print("account type:",acc.get("type"))
#         print("balance:",acc.get("balance"))

#---------------Create a new account for a customer using the API----------------      
# @pytest.mark.asyncio
# async def test_create_acc(api):
#     cust_id = 12212
#     from_acc_id = 18894
#     res  = await api.post("createAccount",
#                           params={
#                             "customerId": cust_id,
#                               "newAccountType" : 1,
#                               "fromAccountId": from_acc_id,
#                           },
#                   headers={"Accept": "application/json"}, )
#     body = await res.json()
#     print(body)
    #{'id': 95484, 'customerId': 12212, 'type': 'SAVINGS', 'balance': 0}  

#----------------using with token------------
@pytest.mark.asyncio
async def test_get_acc(api_git):
    user_name = "vighnesh-hub"
    repo = "Automation-1"
    res =await api_git.get(f"repos/{user_name}/{repo}")
    data =await res.json()
    #print(data)
    print(f"name of repos: {data['name']}")
    print(f"Private: {data['private']}")
    print(f" default branch: {data['default_branch']}")
    
    res = await api_git.get(f"repos/{user_name}/{repo}/commits")
    data = await res.json()
    print(f"Total commits: {len(data)}")
    
    #-----------------Get the branches of a repository using the API----------------
    
    res = await api_git.get(f"repos/{user_name}/{repo}/branches")
    if res.status != 200:
        print(f"Failed to fetch branches. Status code: {res.status}")
        return
        
    branches = await res.json()
    print(f"Total branches: {len(branches)}")
    for branch in branches:
            print(f"Branch name: {branch['name']}")
    