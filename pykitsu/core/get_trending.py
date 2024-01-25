import aiohttp
from typing import Literal, Optional
from ..utils import __RequestLimiter__
from ..exceptions import *
from ..value_errors import *
class get_trending_base:
    def __init__(self, type: Literal["anime", "manga"], limit_requests: Optional[bool] = False, debug_outputs: Optional[bool] = False):
        """
        fetches an anime/manga randomly

        parameters:
            type (str): anime/manga
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """
        self.type = type
        valid_types = {"anime", "manga"}
        if self.type not in valid_types:
            raise INVALID_ARGUMENT("search type")
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = __RequestLimiter__()
        self.debug_outputs = debug_outputs
        self.data_fetched = False
    async def _fetch_trending(self):
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/trending/{self.type}") as response:
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
    async def link(self, offset: int = 0):
        """
        the link of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_id:
            id = self.cache_id[self.cache_key]
            return f"https://kitsu.io/{self.type}/{id}"
        if not self.data_fetched:
            await self._fetch_trending()
        id = self.result[offset]["id"]
        self.cache_id[self.cache_key] = id
        return f"https://kitsu.io/{self.type}/{id}"
    async def id(self, offset: int = 0):
        """
        the id of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        id = self.result[offset]['id']
        return int(id)
    async def name(self, title_type: str = "en_jp", offset: int = 0):
        """
        the name of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        valid_title_types = {"en_jp", "en", "ja_jp"}
        if title_type not in valid_title_types:
            raise INVALID_ARGUMENT("title type")
        if not self.data_fetched:
            await self._fetch_trending()
        name = self.result[offset]['attributes']['titles'][title_type]
        return name
    async def plot(self, offset: int = 0):
        """
        the plot of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        plot = self.result[offset]['attributes']['synopsis']
        return plot
    async def poster_url(self, poster_size: str = "medium", offset: int = 0):
        """
        the poster image url of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        valid_poster_sizes = {"medium", "small", "large", "tiny", "original"}
        if poster_size not in valid_poster_sizes:
            raise INVALID_ARGUMENT("poster size")
        if not self.data_fetched:
            await self._fetch_trending()
        poster_url = self.result[offset]['attributes']['posterImage'][poster_size]
        return poster_url
    async def favoritesCount(self, offset: int = 0):
        """
        the favorites Count of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        favoritesCount = self.result[offset]['attributes']['favoritesCount']
        return favoritesCount
    async def averagerating(self, offset: int = 0):
        """
        the average rating of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        averagerating = self.result[offset]['attributes']['averageRating']
        return averagerating
    async def rating_rank(self, offset: int = 0):
        """
        the rating rank of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        rating_rank = self.result[offset]['attributes']['ratingRank']
        return rating_rank
    async def age_rating(self, offset: int = 0):
        """
        the age rating of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        age_rating = self.result[offset]['attributes']['ageRatingGuide']
        return age_rating
    async def age_rating_type(self, offset: int = 0):
        """
        the age rating type of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        age_rating_type = self.result[offset]['attributes']['ageRating']
        return age_rating_type
    async def show_type(self, offset: int = 0):
        """
        the show type of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_trending()
            show_type = self.result[offset]['attributes']['showType']
            return show_type
        else:
            raise REQUEST_TYPE_ERROR(_function="show_type:", _type_allowed="anime")
    async def manga_type(self, offset: int = 0):
        """
        the manga type of the manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_trending()
            manga_type = self.result[offset]['attributes']['mangaType']
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self, offset: int = 0):
        """
        the airing start date of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        airing_start_date = self.result[offset]['attributes']['startDate']
        return airing_start_date
    async def airing_end_date(self, offset: int = 0):
        """
        the airing end date of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        airing_end_date = self.result[offset]['attributes']['endDate']
        return airing_end_date
    async def nsfw_status(self, offset: int = 0):
        """
        the nsfw status of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_trending()
            nsfw_status = self.result[offset]['attributes']['nsfw']
            return nsfw_status
        else:
            raise REQUEST_TYPE_ERROR(_function="nsfw_status:", _type_allowed="anime")
    async def ep_count(self, offset: int = 0):
        """
        the ep count of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_trending()
            ep_count = self.result[offset]['attributes']['episodeCount']
            return ep_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_count:", _type_allowed="anime")
    async def ep_length(self, offset: int = 0):
        """
        the ep length of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if not self.data_fetched:
                await self._fetch_trending()
            ep_length = self.result[offset]['attributes']['episodeLength']
            return f"{ep_length}m"
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_length:", _type_allowed="anime")
    async def ch_count(self, offset: int = 0):
        """
        the ch count of the manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_trending()
            ch_count = self.result[offset]['attributes']['chapterCount']
            return ch_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ch_count:", _type_allowed="manga")
    async def vol_count(self, offset: int = 0):
        """
        the vol count of the manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "manga":
            if not self.data_fetched:
                await self._fetch_trending()
            vol_count = self.result[offset]['attributes']['volumeCount']
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self, offset: int = 0):
        """
        the airing status of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if not self.data_fetched:
            await self._fetch_trending()
        status = self.result[offset]['attributes']['status']
        return status