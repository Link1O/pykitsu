import aiohttp
from typing import Literal, Union, Optional, NoReturn
from ..utils import __RequestLimiter__
from ..exceptions import *
from ..value_errors import *
_cache = {}
class search_by_id_base:
    def __init__(self, type_: Literal["anime", "manga"], id_: int, limit_requests: Optional[bool] = False, debug_outputs: Optional[bool] = False) -> None:
        """
        fetches an anime/manga based on the provided id

        parameters:
            type_ (Literal): anime/manga
            id_ (int): the anime/manga id
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """
        self.type_ = type_
        self.id_ = id_
        valid_types = {"anime", "manga"}
        if self.type_ not in valid_types:
            raise INVALID_ARGUMENT("search type")
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = __RequestLimiter__()
        self.debug_outputs = debug_outputs
        self.data_fetched = False
    async def _fetch_by_id(self) -> Union[None, NoReturn]:
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/{self.type_}", params={
            "filter[id]": self.id_
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
    async def _get_cached_data(self, field: str, addons_title_type: str = None, addons_poster_zize: str = None) -> Union[str, None]:
        key = f"{self.type_}_{self.id_}"
        if addons_title_type:
            return _cache.get(key, {}).get(field, {}).get(addons_title_type)
        if addons_poster_zize:
            return _cache.get(key, {}).get(field, {}).get(addons_poster_zize)
        return _cache.get(key, {}).get(field)
    async def _set_cached_data(self, field: str, value: str, addons_title_type: str = None, addons_poster_zize: str = None) -> None:
        key = f"{self.type_}_{self.id_}"
        if addons_title_type:
            _cache.setdefault(key, {}).setdefault(field, {})[addons_title_type] = value
        elif addons_poster_zize:
            _cache.setdefault(key, {}).setdefault(field, {})[addons_poster_zize] = value
        else:
            _cache.setdefault(key, {})[field] = value
    async def link(self) -> str:
        """
        the link of the anime/manga
        """
        id_ = await self._get_cached_data(field="id")
        if id_:
            return f"https://kitsu.io/{self.type_}/{id_}"
        if not self.data_fetched:
            await self._fetch_by_id()
        id_ = self.result[0]["id"]
        await self._set_cached_data(field="id", value=id_)
        return f"https://kitsu.io/{self.type_}/{id_}"
    async def id_(self) -> int:
        """
        the id of the anime/manga
        """
        id_ = await self._get_cached_data(field="id")
        if id_:
            return f"https://kitsu.io/{self.type_}/{id_}"
        if not self.data_fetched:
            await self._fetch_by_id()
        id_ = self.result[0]['id']
        await self._set_cached_data(field="id", value=id_)
        return int(id_)
    async def name(self, title_type: Literal["en_jp", "en", "ja_jp"] = "en_jp") -> str:
        """
        the name of the anime/manga
        """
        valid_title_types = {"en_jp", "en", "ja_jp"}
        if title_type not in valid_title_types:
            raise INVALID_ARGUMENT("title type")
        name = await self._get_cached_data(field="name", addons_title_type=title_type)
        if name:
            return name
        if not self.data_fetched:
            await self._fetch_by_id()
        name = self.result[0]['attributes']['titles'][title_type]
        await self._set_cached_data(field="name", value=name, addons_title_type=title_type)
        return name
    async def plot(self) -> str:
        """
        the plot of the anime/manga
        """
        plot = await self._get_cached_data(field="plot")
        if plot:
            return plot
        if not self.data_fetched:
            await self._fetch_by_id()
        plot = self.result[0]['attributes']['synopsis']
        await self._set_cached_data(field="plot", value=plot)
        return plot
    async def poster_url(self, poster_size: Literal["medium", "small", "large", "tiny", "original"] = "medium") -> str:
        """
        the poster image url of the anime/manga        
        """
        valid_poster_sizes = {"medium", "small", "large", "tiny", "original"}
        if poster_size not in valid_poster_sizes:
            raise INVALID_ARGUMENT("poster size")
        poster_url = await self._get_cached_data(field="poster_url", addons_poster_zize=poster_size)
        if poster_url:
            return poster_url
        if not self.data_fetched:
            await self._fetch_by_id()
        poster_url = self.result[0]['attributes']['posterImage'][poster_size]
        await self._set_cached_data(field="poster_url", value=poster_url, addons_poster_zize=poster_size)
        return poster_url
    async def favorites_count(self) -> int:
        """
        the favorites Count of the anime/manga
        """
        favorites_count = await self._get_cached_data(field="favorites_count")
        if favorites_count:
            return favorites_count
        if not self.data_fetched:
            await self._fetch_by_id()
        favorites_count = self.result[0]['attributes']['favoritesCount']
        await self._set_cached_data(field="favorites_count", value=favorites_count)
        return favorites_count
    async def average_rating(self) -> int:
        """
        the average rating of the anime/manga
        """
        average_rating = await self._get_cached_data(field="average_rating")
        if average_rating:
            return average_rating
        if not self.data_fetched:
            await self._fetch_by_id()
        average_rating = self.result[0]['attributes']['averageRating']
        await self._set_cached_data(field="average_rating", value=average_rating)
        return average_rating
    async def rating_rank(self) -> int:
        """
        the rating rank of the anime/manga
        """
        rating_rank = await self._get_cached_data(field="rating_rank")
        if rating_rank:
            return rating_rank
        if not self.data_fetched:
            await self._fetch_by_id()
        rating_rank = self.result[0]['attributes']['ratingRank']
        await self._set_cached_data(field="rating_rank", value=rating_rank)
        return rating_rank
    async def age_rating(self) -> str:
        """
        the age rating of the anime/manga
        """
        age_rating = await self._get_cached_data(field="age_rating")
        if age_rating:
            return age_rating
        if not self.data_fetched:
            await self._fetch_by_id()
        age_rating = self.result[0]['attributes']['ageRatingGuide']
        await self._set_cached_data(field="age_rating", value=age_rating)
        return age_rating
    async def age_rating_type(self) -> str:
        """
        the age rating type of the anime/manga
        """
        age_rating_type = await self._get_cached_data(field="age_rating_type")
        if age_rating_type:
            return age_rating_type
        if not self.data_fetched:
            await self._fetch_by_id()
        age_rating_type = self.result[0]['attributes']['ageRating']
        await self._set_cached_data(field="age_rating_type", value=age_rating_type)
        return age_rating_type
    async def show_type(self) -> str:
        """
        the show type of the anime
        """
        show_type = await self._get_cached_data(field="show_type")
        if show_type:
            return show_type
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch_by_id()
            show_type = self.result[0]['attributes']['showType']
            await self._set_cached_data(field="show_type", value=show_type)
            return show_type
        else:
            raise REQUEST_TYPE_ERROR(_function="show_type:", _type_allowed="anime")
    async def manga_type(self) -> str:
        """
        the type of the manga
        """
        manga_type = await self._get_cached_data(field="manga_type")
        if manga_type:
            return manga_type
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch_by_id()
            manga_type = self.result[0]['attributes']['mangaType']
            await self._set_cached_data(field="manga_type", value=manga_type)
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self) -> str:
        """
        the airing start date of the anime/manga
        """
        airing_start_date = await self._get_cached_data(field="airing_start_date")
        if airing_start_date:
            return airing_start_date
        if not self.data_fetched:
            await self._fetch_by_id()
        airing_start_date = self.result[0]['attributes']['startDate']
        await self._set_cached_data(field="airing_start_date", value=airing_start_date)
        return airing_start_date
    async def airing_end_date(self) -> str:
        """
        the airing end date of the anime/manga
        """
        airing_end_date = await self._get_cached_data(field="airing_end_date")
        if airing_end_date:
            return airing_end_date
        if not self.data_fetched:
            await self._fetch_by_id()
        airing_end_date = self.result[0]['attributes']['endDate']
        await self._set_cached_data(field="airing_end_date", value=airing_end_date)
        return airing_end_date
    async def nsfw_status(self) -> bool:
        """
        the nsfw status of the anime
        """
        nsfw_status = await self._get_cached_data(field="nsfw_status")
        if nsfw_status:
            return nsfw_status
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch_by_id()
            nsfw_status = self.result[0]['attributes']['nsfw']
            await self._set_cached_data(field="nsfw_status", value=nsfw_status)
            return nsfw_status
        else:
            raise REQUEST_TYPE_ERROR(_function="nsfw_status:", _type_allowed="anime")
    async def ep_count(self) -> int:
        """
        the ep count of the anime
        """
        ep_count = await self._get_cached_data(field="ep_count")
        if ep_count:
            return ep_count
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch_by_id()
            ep_count = self.result[0]['attributes']['episodeCount']
            await self._set_cached_data(field="ep_count", value=ep_count)
            return ep_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_count:", _type_allowed="anime")
    async def ep_length(self) -> str:
        """
        the ep length of the anime
        """
        ep_length = await self._get_cached_data(field="ep_length")
        if ep_length:
            return ep_length
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch_by_id()
            ep_length = self.result[0]['attributes']['episodeLength']
            await self._set_cached_data(field="ep_length", value=ep_length)
            return f"{ep_length}m"
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_length:", _type_allowed="anime")
    async def ch_count(self) -> int:
        """
        the ch count of the manga
        """
        ch_count = await self._get_cached_data(field="ch_count")
        if ch_count:
            return ch_count
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch_by_id()
            ch_count = self.result[0]['attributes']['chapterCount']
            await self._set_cached_data(field="ch_count", value=ch_count)
            return ch_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ch_count:", _type_allowed="manga")
    async def vol_count(self) -> int:
        """
        the vol count of the manga
        """
        vol_count = await self._get_cached_data(field="vol_count")
        if vol_count:
            return vol_count
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch_by_id()
            vol_count = self.result[0]['attributes']['volumeCount']
            await self._set_cached_data(field="vol_count", value=vol_count)
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self) -> str:
        """
        the airing status of the anime/manga
        """
        status = await self._get_cached_data(field="status")
        if status:
            return status
        if not self.data_fetched:
            await self._fetch_by_id()
        status = self.result[0]['attributes']['status']
        await self._set_cached_data(field="status", value=status)
        return status
    async def clear_cache(self, __targets__: Optional[list] = None) -> None:
        """
        clears the cache

        parameters:
            __targets__ (dict): the cache clearing targets
        """
        if __targets__:
            for target in __targets__:
                del _cache[target]
            return
        _cache.clear()
        if self.debug_outputs:
            print(f"{Fore.BLUE}[pykitsu: {Fore.RED}debug output{Fore.BLUE}] {Fore.MAGENTA}cache cleared.{Fore.RESET}")