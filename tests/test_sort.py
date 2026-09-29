import pytest

@pytest.mark.asyncio
async def test_drop(async_page):
    await async_page.goto("https://www.amazon.in/")

    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("books")

    lists = async_page.locator("//div[@class='s-suggestion s-suggestion-ellipsis-direction']")

    await lists.first.wait_for()

    options = await lists.all_inner_texts()
    options.sort(key=str.lower)

    expected_text = options[3]

    
    suggestion = lists.filter(has_text=expected_text).first

    await suggestion.click()

    act = await search_box.input_value()

    assert act.lower() == expected_text.lower()
