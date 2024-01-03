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
                return
        term = input(f"enter the anime/manga name: ")
        anime = client.search(search_term=term, type=search_type, debug_outputs=True, limit_requests=True)
        name = await anime.name()
        plot = await anime.plot()
        asd = await anime.airing_start_date()
        aed = await anime.airing_end_date()
        idk = await anime.nsfw_status()
        print(name)
        print(plot)
        print(asd)
        print(aed)
        print(idk)
        await anime.clear_cache()
        break
asyncio.run(func())