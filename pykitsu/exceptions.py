from colorama import Fore
class NO_DATA_FOUND(Exception):
    "raised if the client fails to get the expected response"
    def __init__(self):
        super().__init__(f"{Fore.BLUE}[pykitsu: {Fore.RED}exception{Fore.BLUE}] {Fore.MAGENTA}no data found.{Fore.RESET}")
class FETCH_ERROR(Exception):
    "raised if the client encounters an error when fetching the data"
    def __init__(self):
        super().__init__(f"{Fore.BLUE}[pykitsu: {Fore.RED}exception{Fore.BLUE}] {Fore.MAGENTA}error fetching the data, likely an issue at kitsu.io side. (you can check the api status from here: https://status.kitsu.io/){Fore.RESET}")
class RATE_LIMITED(Exception):
    "raised if you are rate limited"
    def __init__(self):
        super().__init__(f"{Fore.BLUE}[pykitsu: {Fore.RED}exception{Fore.BLUE}] {Fore.MAGENTA}you are rate limited.{Fore.RESET}")
class REQUEST_TYPE_ERROR(Exception):
    "raised if you use a function that doesn't support the chosen request type"
    def __init__(self, _function: str, _type_allowed: str):
        super().__init__(f"{Fore.BLUE}[pykitsu: {Fore.RED}exception{Fore.BLUE}] {Fore.MAGENTA}{_function} only requests with `{_type_allowed}` type are allowed for this function.{Fore.RESET}")