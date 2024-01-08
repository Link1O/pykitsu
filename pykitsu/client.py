from .core.search import search_base
from .core.search_by_id import search_by_id_base
from .core.random import random_base
from .core.get_trending import get_trending_base
class Client:
    def __init__(self):
        pass
    class search(search_base):
        pass
    class search_by_id(search_by_id_base):
        pass
    class random(random_base):
        pass
    class get_trending(get_trending_base):
        pass