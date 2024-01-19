# we import the required packages
from pykitsu import Client
from pykitsu.exceptions import *
import asyncio
# set an instance of the client class
client = Client()
async def func():
    # start a loop
    while 5 > 2:
        # set the search type
        search_type = input("what are you trying to search for?: ")
        # handle invalid search types
        if search_type != "anime":
            if search_type != "manga":
                print("invalid search type.")
                break
        # set the searching term
        term = input(f"enter the {search_type} name: ")
        # search
        anime = client.search(search_term=term, type=search_type, debug_outputs=True, limit_requests=True)
       # handle exceptions
        try:
            # fetch and print the data
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
            # clear the cache
            await anime.clear_cache()
            # end the loop
            break
        except NO_DATA_FOUND:
            print("no results.")
# run the function using asyncio
asyncio.run(func())