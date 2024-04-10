import pytest
import aiohttp


@pytest.mark.asyncio
async def test_get_user_banner():
    tag_id = 10
    feature_id = 1
    use_last_revision = False
    token = "9e4328cad64f4e51aef1dbc6322db313"

    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/user_banner?tag_id={tag_id}&feature_id={feature_id}&use_last_revision={use_last_revision}"
        headers = {'accept': "application/json", 'token': f"{token}"}
        async with session.get(url, headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert 'title' in data
            assert 'text' in data
            assert 'url' in data


@pytest.mark.asyncio
async def test_error_get_user_banner():
    tag_id = 10
    feature_id = 1
    use_last_revision = False
    token = ""

    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/user_banner?tag_id={tag_id}&feature_id={feature_id}&use_last_revision={use_last_revision}"
        headers = {'accept': "application/json", 'token': f"{token}"}
        async with session.get(url, headers=headers) as response:
            assert response.status == 401
