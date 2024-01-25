import asyncio
from typing import Union
class __RequestLimiter__:
    def __init__(self, max_requests_per_interval: Union[int, float] = 5, interval_seconds: Union[int, float] = 0.4):
        self.semaphore = asyncio.Semaphore(max_requests_per_interval)
        self.interval_seconds = interval_seconds
    async def _limit_request(self):
        async with self.semaphore:
            await asyncio.sleep(self.interval_seconds)