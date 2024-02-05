import aiohttp
from typing import Literal, Optional, Any
from ..utils import __RequestLimiter__
from ..exceptions import *
from ..value_errors import *
class search_base:
    def __init__(self, type: Literal["anime", "manga"], search_term: Any, limit_requests: Optional[bool] = False, debug_outputs: Optional[bool] = False):
        """
        fetches an anime/manga based on the provided search term (paginated)

        parameters:
            type (str): anime/manga
            search_term (str): the anime/manga name
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """ 
        self.type = type
        valid_types = {"anime", "manga"}
        if self.type not in valid_types:
            raise INVALID_ARGUMENT("search type")
        self.search_term = search_term
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = __RequestLimiter__()
        self.debug_outputs = debug_outputs
        self.cache_key = (self.type, self.search_term)
        self.cache_id = {}
        self.cache_name = {}
        self.cache_plot = {}
        self.cache_poster_url = {}
        self.cache_favoritescount = {}
        self.cache_averagerating = {}
        self.cache_rating_rank = {}
        self.cache_age_rating = {}
        self.cache_age_rating_type = {}
        self.cache_show_type = {}
        self.cache_manga_type = {}
        self.cache_airing_start_date = {}
        self.cache_airing_end_date = {}
        self.cache_nsfw_status = {}
        self.cache_ep_count = {}
        self.cache_ep_length = {}
        self.cache_ch_count = {}
        self.cache_vol_count = {}
        self.cache_status = {}
        self.data_fetched = False
    async def _fetch(self):
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/{self.type}", params={
            "filter[text]": self.search_term
        }) as response:
                if response.status == 200:
                    self.data = await response.json()
                    await session.close()
                    if self.data['data']:
                        self.result = self.data['data']
                        self.data_fetched = True
                        if self.debug_outputs:
                            print(f"{Fore.BLUE}[pykitsu: {Fore.RED}debug output{Fore.BLUE}] {Fore.MAGENTA}data fetched.{Fore.RESET}")
                    else:
                        raise NO_DATA_FOUND
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
            await self._fetch()
        id = self.result[offset]["id"]
        self.cache_id[self.cache_key] = id
        return f"https://kitsu.io/{self.type}/{id}"
    async def id(self, offset: int = 0):
        """
        the id of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_id:
            return self.cache_id[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        id = self.result[offset]['id']
        self.cache_id[self.cache_key] = id
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
        if self.cache_key in self.cache_name:
            return self.cache_name[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        name = self.result[offset]['attributes']['titles'][title_type]
        self.cache_name[self.cache_key] = name
        return name
    async def plot(self, offset: int = 0):
        """
        the plot of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_plot:
            return self.cache_plot[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        plot = self.result[offset]['attributes']['synopsis']
        self.cache_plot[self.cache_key] = plot
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
        if self.cache_key in self.cache_poster_url:
            return self.cache_poster_url[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        poster_url = self.result[offset]['attributes']['posterImage'][poster_size]
        self.cache_poster_url[self.cache_key] = poster_url
        return poster_url
    async def favoritesCount(self, offset: int = 0):
        """
        the favorites Count of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_favoritescount:
            return self.cache_favoritescount[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        favoritesCount = self.result[offset]['attributes']['favoritesCount']
        self.cache_favoritescount[self.cache_key] = favoritesCount
        return favoritesCount
    async def averagerating(self, offset: int = 0):
        """
        the average rating of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_averagerating:
            return self.cache_averagerating[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        averagerating = self.result[offset]['attributes']['averageRating']
        self.cache_averagerating[self.cache_key] = averagerating
        return averagerating
    async def rating_rank(self, offset: int = 0):
        """
        the rating rank of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_rating_rank:
            return self.cache_rating_rank[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        rating_rank = self.result[offset]['attributes']['ratingRank']
        self.cache_rating_rank[self.cache_key] = rating_rank
        return rating_rank
    async def age_rating(self, offset: int = 0):
        """
        the age rating of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_age_rating:
            return self.cache_age_rating[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        age_rating = self.result[offset]['attributes']['ageRatingGuide']
        self.cache_age_rating[self.cache_key] = age_rating
        return age_rating
    async def age_rating_type(self, offset: int = 0):
        """
        the age rating type of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_age_rating_type:
            return self.cache_age_rating_type[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        age_rating_type = self.result[offset]['attributes']['ageRating']
        self.cache_age_rating_type[self.cache_key] = age_rating_type
        return age_rating_type
    async def show_type(self, offset: int = 0):
        """
        the show type of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if self.cache_key in self.cache_show_type:
                return self.cache_show_type[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            show_type = self.result[offset]['attributes']['showType']
            self.cache_show_type[self.cache_key] = show_type
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
            if self.cache_key in self.cache_manga_type:
                return self.cache_manga_type[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            manga_type = self.result[offset]['attributes']['mangaType']
            self.cache_manga_type[self.cache_key] = manga_type
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self, offset: int = 0):
        """
        the airing start date of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_airing_start_date:
            return self.cache_airing_start_date[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        airing_start_date = self.result[offset]['attributes']['startDate']
        self.cache_airing_start_date[self.cache_key] = airing_start_date
        return airing_start_date
    async def airing_end_date(self, offset: int = 0):
        """
        the airing end date of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_airing_end_date:
            return self.cache_airing_end_date[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        airing_end_date = self.result[offset]['attributes']['endDate']
        self.cache_airing_end_date[self.cache_key] = airing_end_date
        return airing_end_date
    async def nsfw_status(self, offset: int = 0):
        """
        the nsfw status of the anime
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.type == "anime":
            if self.cache_key in self.cache_nsfw_status:
                return self.cache_nsfw_status[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            nsfw_status = self.result[offset]['attributes']['nsfw']
            self.cache_nsfw_status[self.cache_key] = nsfw_status
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
            if self.cache_key in self.cache_ep_count:
                return self.cache_ep_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            ep_count = self.result[offset]['attributes']['episodeCount']
            self.cache_ep_count[self.cache_key] = ep_count
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
            if self.cache_key in self.cache_ep_length:
                return self.cache_ep_length[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            ep_length = self.result[offset]['attributes']['episodeLength']
            self.cache_ep_length[self.cache_key] = ep_length
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
            if self.cache_key in self.cache_ch_count:
                return self.cache_ch_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            ch_count = self.result[offset]['attributes']['chapterCount']
            self.cache_ch_count[self.cache_key] = ch_count
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
            if self.cache_key in self.cache_vol_count:
                return self.cache_vol_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch()
            vol_count = self.result[offset]['attributes']['volumeCount']
            self.cache_vol_count[self.cache_key] = vol_count
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self, offset: int = 0):
        """
        the airing status of the anime/manga
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        if self.cache_key in self.cache_status:
            return self.cache_status[self.cache_key]
        if not self.data_fetched:
            await self._fetch()
        status = self.result[offset]['attributes']['status']
        self.cache_status[self.cache_key] = status
        return status
    async def clear_cache(self):
        """
        clears the cache
        """
        self.cache_name.clear()
        self.cache_plot.clear()
        self.cache_poster_url.clear()
        self.cache_favoritescount.clear()
        self.cache_averagerating.clear()
        self.cache_rating_rank.clear()
        self.cache_age_rating.clear()
        self.cache_age_rating_type.clear()
        self.cache_show_type.clear()
        self.cache_manga_type.clear()
        self.cache_airing_start_date.clear()
        self.cache_airing_end_date.clear()
        self.cache_nsfw_status.clear()
        self.cache_ep_count.clear()
        self.cache_ep_length.clear()
        self.cache_ch_count.clear()
        self.cache_vol_count.clear()
        self.cache_status.clear()
        if self.debug_outputs:
            print(f"{Fore.BLUE}[pykitsu: {Fore.RED}debug output{Fore.BLUE}] {Fore.MAGENTA}cache cleared.{Fore.RESET}")