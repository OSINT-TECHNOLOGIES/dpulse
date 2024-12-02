import random
import sys
sys.path.append('service')
from config_processing import read_config
from colorama import Fore, Style

class ProxiesRotator:
    def __init__(self):
        config_values = read_config()
        self.proxy_file_path = config_values['proxies_file_path']

    def check_proxy(self):
        if self.proxy_file_path == 'NONE':
            print(Fore.RED + "Path to file with proxies was not set in config file. Proxification of Google Dorking won't be applied" + Style.RESET_ALL)
            return 0, ""
        else:
            with open(self.proxy_file_path, 'r') as f:
                print(Fore.GREEN + 'Found path to get proxies from. Continuation' + Style.RESET_ALL)
                proxies_list = [proxy.strip() for proxy in f]
            return 1, proxies_list

    def get_random_proxy(self, proxies_list):
        print(Fore.GREEN + "Set proxy to " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{random.choice(proxies_list)}" + Style.RESET_ALL)
        return random.choice(proxies_list)

proxies_rotator = ProxiesRotator()
