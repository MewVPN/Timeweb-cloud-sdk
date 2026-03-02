import asyncio
import time


class RateLimiter:
    def __init__(self, rate: int):
        self._rate = rate
        self._tokens = rate
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self._updated

                refill = int(elapsed * self._rate)
                if refill > 0:
                    self._tokens = min(self._rate, self._tokens + refill)
                    self._updated = now

                if self._tokens > 0:
                    self._tokens -= 1
                    return

            await asyncio.sleep(1 / self._rate)
