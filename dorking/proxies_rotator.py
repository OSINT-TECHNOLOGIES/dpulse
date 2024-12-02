import random
import sys
sys.path.append('service')
from config_processing import read_config
from colorama import Fore, Style

class ProxiesRotator:
    def __init__(self):
        config_values = read_config()
        self.proxy = config_values['proxies_file_path']

    def check_proxy(self):
        if self.proxy == 'NONE':
            print(Fore.RED + "Path to file with proxies was not set in config file. Proxification of Google Dorking won't be applied" + Style.RESET_ALL)
            return 0, self.proxy
        else:
            print(Fore.GREEN + 'Found path to get proxies from. Continuation' + Style.RESET_ALL)
            return 1, self.proxy

    def get_random_proxy(self):
        print(Fore.GREEN + "Set proxy to " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{random.choice(self.proxy)}" + Style.RESET_ALL)
        return random.choice(self.proxy)

proxies_rotator = ProxiesRotator()