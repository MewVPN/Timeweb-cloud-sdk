import pytest_asyncio
import httpx
from timeweb_cloud_sdk import TimewebCloud


@pytest_asyncio.fixture
async def client():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    transport = httpx.MockTransport(handler)

    async with TimewebCloud(
        token="eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjFrYnhacFJNQGJSI0tSbE1xS1lqIn0.eyJ1c2VyIjoiYXhlbG9mIiwidHlwZSI6ImFwaV9rZXkiLCJhcGlfa2V5X2lkIjoiOTVlOTJhODItMjIzOS00YzI2LWEwMWQtODlkNjQ5NDQ0ZTg0IiwiaWF0IjoxNzcxOTU2NDY0fQ.nASGNPGO0n9dM_f7iub4EyTTnBs0cBWxO6jKPuCWwkFyMKRZ0yVluEUvuoPAmxNiqixAhwcrlpNBXMBQzK9ApjE2Ik84rOxHpBs6xwHCr2Q_q5daCsvrACY69aqf76xBuNkgrzQLxmdbHNXHDKPGJNctaywf4rQUjvt9YpOdoA1DyAK6ERqqtdYRbK45VSuclFZxPlxG32KUUbBB80bw1XOS755tkTwGpEWqavpfCffw8ZH05plCGV3y7gCK_1tMhdM1DnzIcnAmHthmnrE7upm1QnZFnvXLu6l1Ax4mitxzHtFpprwufRjjmboL5kcTuDKpVTce-q2BwbZgavM5bSlL4TKKcgX2pygWpdnqxGLvg7bXYeDVYqSlzywXfJ4Saj4peikZIOy2hFqtEg5aOas02MUK6UQveyNB1evKzMI2nRyQQ86gHmEa0U9ZZzRYwYmE6vZSgvquJcOXN_PboEJ5BUnY7tVf_Y6jk0WMzzNhXXgEy0AByDQpbxDNwOvF",
        transport=transport,
    ) as c:
        yield c
