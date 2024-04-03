import aiohttp
from typing import Literal, Union, Optional, NoReturn
from ..utils import __RequestLimiter__
from ..exceptions import *
from ..value_errors import *
_cache = {}
class search_base:
    def __init__(self, type_: Literal["anime", "manga"], search_term: Union[str, int, float], limit_requests: Optional[bool] = False, debug_outputs: Optional[bool] = False) -> None:
        """
        fetches an anime/manga based on the provided search term (paginated)

        parameters:
            type_ (Literal): anime/manga
            search_term (str | int | float): the anime/manga name
            limit_requests (bool): the rate limiting status, options: True | False (default: False)
            debug_outputs (bool): debug outputs status, options: True | False (default: False)
        """ 
        self.type_ = type_
        valid_types = {"anime", "manga"}
        if self.type_ not in valid_types:
            raise INVALID_ARGUMENT("search type")
        self.search_term = search_term
        self.limit_requests = limit_requests
        if self.limit_requests:
            self.request_limiter = __RequestLimiter__()
        self.debug_outputs = debug_outputs
        self.data_fetched = False
    async def _fetch(self) -> Union[None, NoReturn]:
        if self.limit_requests:
            await self.request_limiter._limit_request()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://kitsu.io/api/edge/{self.type_}", params={
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
    async def _get_cached_data(self, offset: int, field: str, addons_title_type: str = None, addons_poster_zize: str = None) -> Union[str, None]:
        key = f"{self.type_}_{self.search_term}_{offset}"
        if addons_title_type:
            return _cache.get(key, {}).get(field, {}).get(addons_title_type)
        elif addons_poster_zize:
            return _cache.get(key, {}).get(field, {}).get(addons_poster_zize)
        else:
            return _cache.get(key, {}).get(field)
    async def _set_cached_data(self, offset: int, field: str, value: str, addons_title_type: str = None, addons_poster_zize: str = None) -> None:
        key = f"{self.type_}_{self.search_term}_{offset}"
        if addons_title_type:
            _cache.setdefault(key, {}).setdefault(field, {})[addons_title_type] = value
        elif addons_poster_zize:
            _cache.setdefault(key, {}).setdefault(field, {})[addons_poster_zize] = value
        else:
            _cache.setdefault(key, {})[field] = value
    async def link(self, offset: int = 0) -> str:
        """
        the link of the anime/manga
        
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        id_ = await self._get_cached_data(offset=offset, field="id")
        if id_:
            return f"https://kitsu.io/{self.type_}/{id_}"
        if not self.data_fetched:
            await self._fetch()
        id_ = self.result[offset]["id"]
        await self._set_cached_data(offset=offset, field="id", value=id_)
        return f"https://kitsu.io/{self.type_}/{id_}"
    async def id_(self, offset: int = 0) -> int:
        """
        the id of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        id_ = await self._get_cached_data(offset=offset, field="id")
        if id_:
            return f"https://kitsu.io/{self.type_}/{id_}"
        if not self.data_fetched:
            await self._fetch()
        id_ = self.result[offset]['id']
        await self._set_cached_data(offset=offset, field="id", value=id_)
        return int(id_)
    async def name(self, title_type: Literal["en_jp", "en", "ja_jp"] = "en_jp", offset: int = 0) -> str:
        """
        the name of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        valid_title_types = {"en_jp", "en", "ja_jp"}
        if title_type not in valid_title_types:
            raise INVALID_ARGUMENT("title type")
        name = await self._get_cached_data(offset=offset, field="name", addons_title_type=title_type)
        if name:
            return name
        if not self.data_fetched:
            await self._fetch()
        name = self.result[offset]['attributes']['titles'][title_type]
        await self._set_cached_data(offset=offset, field="name", value=name, addons_title_type=title_type)
        return name
    async def plot(self, offset: int = 0) -> str:
        """
        the plot of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        plot = await self._get_cached_data(offset=offset, field="plot")
        if plot:
            return plot
        if not self.data_fetched:
            await self._fetch()
        plot = self.result[offset]['attributes']['synopsis']
        await self._set_cached_data(offset=offset, field="plot", value=plot)
        return plot
    async def poster_url(self, poster_size: Literal["medium", "small", "large", "tiny", "original"] = "medium", offset: int = 0) -> str:
        """
        the poster image url of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        valid_poster_sizes = {"medium", "small", "large", "tiny", "original"}
        if poster_size not in valid_poster_sizes:
            raise INVALID_ARGUMENT("poster size")
        poster_url = await self._get_cached_data(offset=offset, field="poster_url", addons_poster_zize=poster_size)
        if poster_url:
            return poster_url
        if not self.data_fetched:
            await self._fetch()
        poster_url = self.result[offset]['attributes']['posterImage'][poster_size]
        await self._set_cached_data(offset=offset, field="poster_url", value=poster_url, addons_poster_zize=poster_size)
        return poster_url
    async def favorites_count(self, offset: int = 0) -> int:
        """
        the favorites Count of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        favorites_count = await self._get_cached_data(offset=offset, field="favorites_count")
        if favorites_count:
            return favorites_count
        if not self.data_fetched:
            await self._fetch()
        favorites_count = self.result[offset]['attributes']['favoritesCount']
        await self._set_cached_data(offset=offset, field="favorites_count", value=favorites_count)
        return favorites_count
    async def average_rating(self, offset: int = 0) -> int:
        """
        the average rating of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        average_rating = await self._get_cached_data(offset=offset, field="average_rating")
        if average_rating:
            return average_rating
        if not self.data_fetched:
            await self._fetch()
        average_rating = self.result[offset]['attributes']['averageRating']
        await self._set_cached_data(offset=offset, field="average_rating", value=average_rating)
        return average_rating
    async def rating_rank(self, offset: int = 0) -> int:
        """
        the rating rank of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        rating_rank = await self._get_cached_data(offset=offset, field="rating_rank")
        if rating_rank:
            return rating_rank
        if not self.data_fetched:
            await self._fetch()
        rating_rank = self.result[offset]['attributes']['ratingRank']
        await self._set_cached_data(offset=offset, field="rating_rank", value=rating_rank)
        return rating_rank
    async def age_rating(self, offset: int = 0) -> str:
        """
        the age rating of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        age_rating = await self._get_cached_data(offset=offset, field="age_rating")
        if age_rating:
            return age_rating
        if not self.data_fetched:
            await self._fetch()
        age_rating = self.result[offset]['attributes']['ageRatingGuide']
        await self._set_cached_data(offset=offset, field="age_rating", value=age_rating)
        return age_rating
    async def age_rating_type(self, offset: int = 0) -> str:
        """
        the age rating type of the anime/manga
        
        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        age_rating_type = await self._get_cached_data(offset=offset, field="age_rating_type")
        if age_rating_type:
            return age_rating_type
        if not self.data_fetched:
            await self._fetch()
        age_rating_type = self.result[offset]['attributes']['ageRating']
        await self._set_cached_data(offset=offset, field="age_rating_type", value=age_rating_type)
        return age_rating_type
    async def show_type(self, offset: int = 0) -> str:
        """
        the show type of the anime

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        show_type = await self._get_cached_data(offset=offset, field="show_type")
        if show_type:
            return show_type
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch()
            show_type = self.result[offset]['attributes']['showType']
            await self._set_cached_data(offset=offset, field="show_type", value=show_type)
            return show_type
        else:
            raise REQUEST_TYPE_ERROR(_function="show_type:", _type_allowed="anime")
    async def manga_type(self, offset: int = 0) -> str:
        """
        the type of the manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        manga_type = await self._get_cached_data(offset=offset, field="manga_type")
        if manga_type:
            return manga_type
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch()
            manga_type = self.result[offset]['attributes']['mangaType']
            await self._set_cached_data(offset=offset, field="manga_type", value=manga_type)
            return manga_type
        else:
            raise REQUEST_TYPE_ERROR(_function="manga_type:", _type_allowed="manga")
    async def airing_start_date(self, offset: int = 0) -> str:
        """
        the airing start date of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        airing_start_date = await self._get_cached_data(offset=offset, field="airing_start_date")
        if airing_start_date:
            return airing_start_date
        if not self.data_fetched:
            await self._fetch()
        airing_start_date = self.result[offset]['attributes']['startDate']
        await self._set_cached_data(offset=offset, field="airing_start_date", value=airing_start_date)
        return airing_start_date
    async def airing_end_date(self, offset: int = 0) -> str:
        """
        the airing end date of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        airing_end_date = await self._get_cached_data(offset=offset, field="airing_end_date")
        if airing_end_date:
            return airing_end_date
        if not self.data_fetched:
            await self._fetch()
        airing_end_date = self.result[offset]['attributes']['endDate']
        await self._set_cached_data(offset=offset, field="airing_end_date", value=airing_end_date)
        return airing_end_date
    async def nsfw_status(self, offset: int = 0) -> bool:
        """
        the nsfw status of the anime

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        nsfw_status = await self._get_cached_data(offset=offset, field="nsfw_status")
        if nsfw_status:
            return nsfw_status
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch()
            nsfw_status = self.result[offset]['attributes']['nsfw']
            await self._set_cached_data(offset=offset, field="nsfw_status", value=nsfw_status)
            return nsfw_status
        else:
            raise REQUEST_TYPE_ERROR(_function="nsfw_status:", _type_allowed="anime")
    async def ep_count(self, offset: int = 0) -> int:
        """
        the ep count of the anime

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        ep_count = await self._get_cached_data(offset=offset, field="ep_count")
        if ep_count:
            return ep_count
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch()
            ep_count = self.result[offset]['attributes']['episodeCount']
            await self._set_cached_data(offset=offset, field="ep_count", value=ep_count)
            return ep_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_count:", _type_allowed="anime")
    async def ep_length(self, offset: int = 0) -> str:
        """
        the ep length of the anime

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        ep_length = await self._get_cached_data(offset=offset, field="ep_length")
        if ep_length:
            return ep_length
        if self.type_ == "anime":
            if not self.data_fetched:
                await self._fetch()
            ep_length = self.result[offset]['attributes']['episodeLength']
            await self._set_cached_data(offset=offset, field="ep_length", value=ep_length)
            return f"{ep_length}m"
        else:
            raise REQUEST_TYPE_ERROR(_function="ep_length:", _type_allowed="anime")
    async def ch_count(self, offset: int = 0) -> int:
        """
        the ch count of the manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        ch_count = await self._get_cached_data(offset=offset, field="ch_count")
        if ch_count:
            return ch_count
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch()
            ch_count = self.result[offset]['attributes']['chapterCount']
            await self._set_cached_data(offset=offset, field="ch_count", value=ch_count)
            return ch_count
        else:
            raise REQUEST_TYPE_ERROR(_function="ch_count:", _type_allowed="manga")
    async def vol_count(self, offset: int = 0) -> int:
        """
        the vol count of the manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        vol_count = await self._get_cached_data(offset=offset, field="vol_count")
        if vol_count:
            return vol_count
        if self.type_ == "manga":
            if not self.data_fetched:
                await self._fetch()
            vol_count = self.result[offset]['attributes']['volumeCount']
            await self._set_cached_data(offset=offset, field="vol_count", value=vol_count)
            return vol_count
        else:
            raise REQUEST_TYPE_ERROR(_function="vol_count:", _type_allowed="manga")
    async def status(self, offset: int = 0) -> str:
        """
        the airing status of the anime/manga

        parameters:
            offset (int): the fetched data offset, (default: 0)
        """
        status = await self._get_cached_data(offset=offset, field="status")
        if status:
            return status
        if not self.data_fetched:
            await self._fetch()
        status = self.result[offset]['attributes']['status']
        await self._set_cached_data(offset=offset, field="status", value=status)
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