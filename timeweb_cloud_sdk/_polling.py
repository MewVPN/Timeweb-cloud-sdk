import asyncio
import time
from .exceptions import TimeoutError


async def wait_for_condition(
    fetch,
    check,
    *,
    interval=3,
    timeout=300,
    backoff=True,
):
    start = time.monotonic()
    attempt = 0

    while True:
        resource = await fetch()

        if check(resource):
            return resource

        if time.monotonic() - start > timeout:
            raise TimeoutError()

        sleep_time = interval * (2**attempt) if backoff else interval
        await asyncio.sleep(sleep_time)

        if backoff:
            attempt = min(attempt + 1, 5)
