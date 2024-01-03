import pykitsu
from pykitsu import Client
from pykitsu.exceptions import *
import asyncio
client = Client()
async def func():
    while 5 > 2:
        search_type = input("what are you trying to search for?: ")
        if search_type != "anime":
            if search_type != "manga":
                print("invalid search type.")
                break
        term = input(f"enter the {search_type} name: ")
        anime = client.search(search_term=term, type=search_type, debug_outputs=True, limit_requests=True)
        try:
            name = await anime.name()
            plot = await anime.plot()
            airing_start_date = await anime.airing_start_date()
            airing_end_date = await anime.airing_end_date()
            nsfw_status = await anime.nsfw_status()
            print(name)
            print(plot)
            print(airing_start_date)
            print(airing_end_date)
            print(nsfw_status)
            await anime.clear_cache()
            break
        except NO_DATA_FOUND:
            print("no results.")
asyncio.run(func())