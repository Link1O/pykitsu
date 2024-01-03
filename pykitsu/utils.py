import aiohttp
import asyncio
from pykitsu.exceptions import FETCH_ERROR
async def get_latest_id(type: str):
   """
   gets the latest added anime/manga id
   """
   async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://kitsu.io/api/edge/{type}", params={
            "sort": "-id",
            "page[limit]": 1
        }) as response:
            if response.status == 200:
                data = await response.json()
                latest_id = data['data'][0]['id']
                return int(latest_id)
            else:
                raise FETCH_ERROR
class _RequestLimiter:
    def __init__(self, max_requests_per_interval: int = 5, interval_seconds: float = 0.4):
        self.semaphore = asyncio.Semaphore(max_requests_per_interval)
        self.interval_seconds = interval_seconds
    async def _limit_request(self):
        async with self.semaphore:
            await asyncio.sleep(self.interval_seconds)