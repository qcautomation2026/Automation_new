import pytest
from playwright.async_api import expect
from pathlib import Path
# File_downloads
@pytest.mark.asyncio
async def test_download(async_page):
    await async_page.goto("https://the-internet.herokuapp.com/download")
    async_page.wait_for_timeout(5000)
    download_folder = Path("downloads")
    download_folder.mkdir(
        exist_ok=True
    )
    download_link = async_page.get_by_text("app.js")
    async with async_page.expect_download() as download_info:
        await download_link.click()
    download = await download_info.value
    file_name = download.suggested_filename
    file_path = download_folder / file_name
    await download.save_as(
        str(file_path)
    )
    print("Downloaded:", file_path)
    assert file_path.exists()