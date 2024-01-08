import aiohttp
import asyncio
from pykitsu.exceptions import NO_DATA_FOUND, FETCH_ERROR
async def get_id(type: str, search_term: str, offset: int = 0):
    """
    gets the anime/manga id by name
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://kitsu.io/api/edge/{type}", params={
            "filter[text]": search_term
        }) as response:
            await session.close()
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    id = data['data'][offset]['id']
                    return id
                else:
                    raise NO_DATA_FOUND
            else:
                raise FETCH_ERROR
async def get_latest(type: str):
   """
   gets the latest added anime/manga (returns the id)
   """
   async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://kitsu.io/api/edge/{type}", params={
            "sort": "-id",
            "page[limit]": 1
        }) as response:
            await session.close()
            if response.status == 200:
                data = await response.json()
                latest_id = data['data'][0]['id']
                return latest_id
            else:
                raise FETCH_ERROR