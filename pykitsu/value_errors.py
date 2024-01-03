from colorama import Fore
class INVALID_ARGUMENT(ValueError):
    def __init__(self, _argument: str):
        super().__init__(f"{Fore.BLUE}[pykitsu: {Fore.RED}value error{Fore.BLUE}] {Fore.MAGENTA}invalid {_argument}.{Fore.RESET}")