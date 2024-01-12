import aiohttp
import random
from colorama import Fore
from ..utils import _RequestLimiter
from ..utils import get_latest
from ..exceptions import *
from ..value_errors import *
class random_base:
    def __init__(self, type: str, limit_requests: bool = False, debug_outputs: bool = False):
        """
        fetches an anime/manga randomly

        parameters:
            type (str): anime/manga
            latest_data (bool): fetch the latest data (only use if you want to fetch a newer random animes), options: True | False (defuelt: False)
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """
        self.type = type
        if self.type != "anime":
            if self.type != "manga":
                raise INVALID_ARGUMENT("search type")
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = _RequestLimiter()
        self.debug_outputs = debug_outputs
        self.data_fetched = False
    async def _fetch_random(self):
        rand_int = random.randint(1, await get_latest(type=self.type))
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/{self.type}", params={
            "filter[id]": rand_int
        }) as response:
                if response.status == 200:
                    self.data = await response.json()
                    await session.close()
                    self.result = self.data['data']
                    self.data_fetched = True
                    if self.debug_outputs:
                        print(f"{Fore.BLUE}[pykitsu: {Fore.RED}debug output{Fore.BLUE}] {Fore.MAGENTA}data fetched.{Fore.RESET}")
                elif response.status == 429:
                    raise RATE_LIMITED
                else: 
                    raise FETCH_ERROR
    async def kitsu_link(self):
        """
        the link of the anime/manga
        """
        if self.cache_key in self.cache_id:
            id = self.cache_id[self.cache_key]
            return f"https://kitsu.io/{self.type}/{id}"
        if not self.data_fetched:
            await self._fetch_random()
        id = self.result[0]["id"]
        self.cache_id[self.cache_key] = id
        return f"https://kitsu.io/{self.type}/{id}"
    async def id(self):
        """
        the id of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        id = self.result[0]['id']
        return id
    async def name(self, title_type: str = "en_jp"):
        """
        the name of the anime/manga
        """
        if title_type != "en_jp":
            if title_type != "en":
                if title_type != "ja_jp":
                    raise INVALID_ARGUMENT("title type")
        if not self.data_fetched:
            await self._fetch_random()
        name = self.result[0]['attributes']['titles'][self.title_type]
        return name
    async def plot(self):
        """
        the plot of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        plot = self.result[0]['attributes']['synopsis']
        return plot
    async def poster_url(self, poster_size: str = "medium"):
        """
        the poster image url of the anime/manga
        """
        if poster_size != "medium":
            if poster_size != "small":
                if poster_size != "large": 
                    if poster_size != "tiny":
                        if poster_size != "original":
                            raise INVALID_ARGUMENT("poster size")
        if not self.data_fetched:
            await self._fetch_random()
        poster_url = self.result[0]['attributes']['posterImage'][self.poster_size]
        return poster_url
    async def favoritesCount(self):
        """
        the favorites Count of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        favoritesCount = self.result[0]['attributes']['favoritesCount']
        return favoritesCount
    async def averagerating(self):
        """
        the average rating of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        averagerating = self.result[0]['attributes']['averageRating']
        return averagerating
    async def rating_rank(self):
        """
        the rating rank of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        rating_rank = self.result[0]['attributes']['ratingRank']
        return rating_rank
    async def age_rating(self):
        """
        the age rating of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        age_rating = self.result[0]['attributes']['ageRatingGuide']
        return age_rating
    async def age_rating_type(self):
        """
        the age rating type of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        age_rating_type = self.result[0]['attributes']['ageRating']
        return age_rating_type
    async def show_type(self):
        """
        the show type of the anime
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_random()
            show_type = self.result[0]['attributes']['showType']
            return show_type
        else:
            raise REQUEST_TYPE_ERROR(_function="show_type:", _type_allowed="anime")
    async def manga_type(self):
        """
        the manga type of the manga
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_random()
            manga_type = self.result[0]['attributes']['mangaType']
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self):
        """
        the airing start date of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        airing_start_date = self.result[0]['attributes']['startDate']
        return airing_start_date
    async def airing_end_date(self):
        """
        the airing end date of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        airing_end_date = self.result[0]['attributes']['endDate']
        return airing_end_date
    async def nsfw_status(self):
        """
        the nsfw status of the anime
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_random()
            nsfw_status = self.result[0]['attributes']['nsfw']
            return nsfw_status
        else:
            raise REQUEST_TYPE_ERROR(_function="nsfw_status:", _type_allowed="anime")
    async def ep_count(self):
        """
        the ep count of the anime
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_random()
            ep_count = self.result[0]['attributes']['episodeCount']
            return ep_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_count:", _type_allowed="anime")
    async def ep_length(self):
        """
        the ep length of the anime
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_random()
            ep_length = self.result[0]['attributes']['episodeLength']
            return f"{ep_length}m"
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_length:", _type_allowed="anime")
    async def ch_count(self):
        """
        the ch count of the manga
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_random()
            ch_count = self.result[0]['attributes']['chapterCount']
            return ch_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ch_count:", _type_allowed="manga")
    async def vol_count(self):
        """
        the vol count of the manga
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_random()
            vol_count = self.result[0]['attributes']['volumeCount']
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self):
        """
        the airing status of the anime/manga
        """
        if not self.data_fetched:
            await self._fetch_random()
        status = self.result[0]['attributes']['status']
        return status