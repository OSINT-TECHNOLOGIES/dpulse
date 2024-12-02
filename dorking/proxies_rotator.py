import random
import sys
sys.path.append('service')
from config_processing import read_config
from colorama import Fore, Style
import requests
from requests.exceptions import ProxyError, ConnectionError, Timeout

class ProxiesRotator:
    def __init__(self):
        config_values = read_config()
        self.proxy_file_path = str(config_values['proxies_file_path'])

    def check_proxies(self, proxies_list):
        working_proxies = []
        print(Fore.GREEN + f'Checking {len(proxies_list)} proxies, please wait...' + Style.RESET_ALL)
        for proxy in proxies_list:
            proxies = {
                "http": proxy
            }
            try:
                response = requests.get('https://google.com', proxies=proxies, timeout=5)
                if response.status_code == 200:
                    working_proxies.append(proxy)
                    #print(Fore.GREEN + f"Proxy {proxy} is working" + Style.RESET_ALL)
                else:
                    pass
                    #print(Fore.GREEN +f"Proxy {proxy} returned status code {response.status_code}" + Style.RESET_ALL)
            except (ProxyError, ConnectionError, Timeout):
                pass
                #print(Fore.GREEN + f"Proxy {proxy} is not working" + Style.RESET_ALL)
        print(Fore.GREEN + f'Found {len(working_proxies)} working proxies' + Style.RESET_ALL)
        return working_proxies

    def get_proxies(self):
        if self.proxy_file_path == 'NONE':
            print(Fore.RED + "Path to file with proxies was not set in config file. Proxification of Google Dorking won't be applied\n" + Style.RESET_ALL)
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
