import pytest
import aiohttp


# чтобы не падал тест с получением данных
@pytest.mark.asyncio
async def test_add_user_banner():
    tag_ids = [10, 11]
    feature_id = 1
    title = 'Заголовок'
    text = 'Текст'
    url_body = 'https://google.com'
    is_active = True
    token = "admin_token"

    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:8000/banner"
        headers = {'accept': "application/json", 'token': f"{token}"}
        data = {
            "tag_ids": tag_ids,
            "feature_id": feature_id,
            "content": {
                "title": title,
                "text": text,
                "url": url_body,
            },
            "is_active": is_active
        }
        async with session.post(url, headers=headers, json=data) as response:
            assert response.status == 201
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
