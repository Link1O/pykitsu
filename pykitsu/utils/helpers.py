import asyncio
class _RequestLimiter:
    def __init__(self, max_requests_per_interval: int = 5, interval_seconds: float = 0.4):
        self.semaphore = asyncio.Semaphore(max_requests_per_interval)
        self.interval_seconds = interval_seconds
    async def _limit_request(self):
        async with self.semaphore:
            await asyncio.sleep(self.interval_seconds)