import aiohttp
from typing import Literal, Optional
from ..utils import __RequestLimiter__
from ..exceptions import *
from ..value_errors import *
class search_by_id_base:
    def __init__(self, type: Literal["anime", "manga"], id: int, limit_requests: Optional[bool] = False, debug_outputs: Optional[bool] = False):
        """
        fetches an anime/manga based on the provided id

        parameters:
            type (str): anime/manga
            id (int): the anime/manga id
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """
        self.id = id
        self.type = type
        valid_types = {"anime", "manga"}
        if self.type not in valid_types:
            raise INVALID_ARGUMENT("search type")
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = __RequestLimiter__()
        self.debug_outputs = debug_outputs
        self.cache_key = (self.type, self.id)
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
    async def _fetch_by_id(self):
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/{self.type}", params={
            "filter[id]": self.id
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
    async def kitsu_link(self):
        """
        the link of the anime/manga
        """
        if self.cache_key in self.cache_id:
            id = self.cache_id[self.cache_key]
            return f"https://kitsu.io/{self.type}/{id}"
        if not self.data_fetched:
            await self._fetch_by_id()
        id = self.result[0]["id"]
        self.cache_id[self.cache_key] = id
        return f"https://kitsu.io/{self.type}/{id}"
    async def id(self):
        """
        the id of the anime/manga
        """
        if self.cache_key in self.cache_id:
            return self.cache_id[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        id = self.result[0]['id']
        self.cache_id[self.cache_key] = id
        return int(id)
    async def name(self, title_type: str = "en_jp"):
        """
        the name of the anime/manga
        """
        valid_title_types = {"en_jp", "en", "ja_jp"}
        if title_type not in valid_title_types:
            raise INVALID_ARGUMENT("title type")
        if self.cache_key in self.cache_name:
            return self.cache_name[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        name = self.result[0]['attributes']['titles'][title_type]
        self.cache_name[self.cache_key] = name
        return name
    async def plot(self):
        """
        the plot of the anime/manga
        """
        if self.cache_key in self.cache_plot:
            return self.cache_plot[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        plot = self.result[0]['attributes']['synopsis']
        self.cache_plot[self.cache_key] = plot
        return plot
    async def poster_url(self, poster_size: str = "medium"):
        """
        the poster image url of the anime/manga
        """
        valid_poster_sizes = {"medium", "small", "large", "tiny", "original"}
        if poster_size not in valid_poster_sizes:
            raise INVALID_ARGUMENT("poster size")
        if self.cache_key in self.cache_poster_url:
            return self.cache_poster_url[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        poster_url = self.result[0]['attributes']['posterImage'][poster_size]
        self.cache_poster_url[self.cache_key] = poster_url
        return poster_url
    async def favoritesCount(self):
        """
        the favorites Count of the anime/manga
        """
        if self.cache_key in self.cache_favoritescount:
            return self.cache_favoritescount[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        favoritesCount = self.result[0]['attributes']['favoritesCount']
        self.cache_favoritescount[self.cache_key] = favoritesCount
        return favoritesCount
    async def averagerating(self):
        """
        the average rating of the anime/manga
        """
        if self.cache_key in self.cache_averagerating:
            return self.cache_averagerating[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        averagerating = self.result[0]['attributes']['averageRating']
        self.cache_averagerating[self.cache_key] = averagerating
        return averagerating
    async def rating_rank(self):
        """
        the rating rank of the anime/manga
        """
        if self.cache_key in self.cache_rating_rank:
            return self.cache_rating_rank[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        rating_rank = self.result[0]['attributes']['ratingRank']
        self.cache_rating_rank[self.cache_key] = rating_rank
        return rating_rank
    async def age_rating(self):
        """
        the age rating of the anime/manga
        """
        if self.cache_key in self.cache_age_rating:
            return self.cache_age_rating[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        age_rating = self.result[0]['attributes']['ageRatingGuide']
        self.cache_age_rating[self.cache_key] = age_rating
        return age_rating
    async def age_rating_type(self):
        """
        the age rating type of the anime/manga
        """
        if self.cache_key in self.cache_age_rating_type:
            return self.cache_age_rating_type[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        age_rating_type = self.result[0]['attributes']['ageRating']
        self.cache_age_rating_type[self.cache_key] = age_rating_type
        return age_rating_type
    async def show_type(self):
        """
        the show type of the anime
        """
        if self.type == "anime":
            if self.cache_key in self.cache_show_type:
                return self.cache_show_type[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            show_type = self.result[0]['attributes']['showType']
            self.cache_show_type[self.cache_key] = show_type
            return show_type
        else:
            raise REQUEST_TYPE_ERROR(_function="show_type:", _type_allowed="anime")
    async def manga_type(self):
        """
        the manga type of the manga
        """
        if self.type == "manga":
            if self.cache_key in self.cache_manga_type:
                return self.cache_manga_type[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            manga_type = self.result[0]['attributes']['mangaType']
            self.cache_manga_type[self.cache_key] = manga_type
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self):
        """
        the airing start date of the anime/manga
        """
        if self.cache_key in self.cache_airing_start_date:
            return self.cache_airing_start_date[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        airing_start_date = self.result[0]['attributes']['startDate']
        self.cache_airing_start_date[self.cache_key] = airing_start_date
        return airing_start_date
    async def airing_end_date(self):
        """
        the airing end date of the anime/manga
        """
        if self.cache_key in self.cache_airing_end_date:
            return self.cache_airing_end_date[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        airing_end_date = self.result[0]['attributes']['endDate']
        self.cache_airing_end_date[self.cache_key] = airing_end_date
        return airing_end_date
    async def nsfw_status(self):
        """
        the nsfw status of the anime
        """
        if self.type == "anime":
            if self.cache_key in self.cache_nsfw_status:
                return self.cache_nsfw_status[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            nsfw_status = self.result[0]['attributes']['nsfw']
            self.cache_nsfw_status[self.cache_key] = nsfw_status
            return nsfw_status
        else:
            raise REQUEST_TYPE_ERROR(_function="nsfw_status:", _type_allowed="anime")
    async def ep_count(self):
        """
        the ep count of the anime
        """
        if self.type == "anime":
            if self.cache_key in self.cache_ep_count:
                return self.cache_ep_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            ep_count = self.result[0]['attributes']['episodeCount']
            self.cache_ep_count[self.cache_key] = ep_count
            return ep_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_count:", _type_allowed="anime")
    async def ep_length(self):
        """
        the ep length of the anime
        """
        if self.type == "anime":
            if self.cache_key in self.cache_ep_length:
                return self.cache_ep_length[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            ep_length = self.result[0]['attributes']['episodeLength']
            self.cache_ep_length[self.cache_key] = ep_length
            return f"{ep_length}m"
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_length:", _type_allowed="anime")
    async def ch_count(self):
        """
        the ch count of the manga
        """
        if self.type == "manga":
            if self.cache_key in self.cache_ch_count:
                return self.cache_ch_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            ch_count = self.result[0]['attributes']['chapterCount']
            self.cache_ch_count[self.cache_key] = ch_count
            return ch_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ch_count:", _type_allowed="manga")
    async def vol_count(self):
        """
        the vol count of the manga
        """
        if self.type == "manga":
            if self.cache_key in self.cache_vol_count:
                return self.cache_vol_count[self.cache_key]
            if not self.data_fetched:
                await self._fetch_by_id()
            vol_count = self.result[0]['attributes']['volumeCount']
            self.cache_vol_count[self.cache_key] = vol_count
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self):
        """
        the airing status of the anime/manga
        """
        if self.cache_key in self.cache_status:
            return self.cache_status[self.cache_key]
        if not self.data_fetched:
            await self._fetch_by_id()
        status = self.result[0]['attributes']['status']
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