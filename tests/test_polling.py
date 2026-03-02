import pytest
from timeweb_cloud_sdk._polling import wait_for_condition
from timeweb_cloud_sdk.exceptions import TimeoutError


@pytest.mark.asyncio
async def test_polling_timeout():
    async def fetch():
        return {"status": "off"}

    def check(_):
        return False

    with pytest.raises(TimeoutError):
        await wait_for_condition(fetch, check, interval=0.01, timeout=0.05)
