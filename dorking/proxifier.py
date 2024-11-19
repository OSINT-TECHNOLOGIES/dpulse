import requests
from bs4 import BeautifulSoup
import concurrent.futures
from colorama import Fore, Style

class ProxyScraper:
    def __init__(self, test_url='http://httpbin.org/ip', timeout=5):
        self.test_url = test_url
        self.timeout = timeout
        self.proxies = []

    def get_proxies(self):
        url = "https://free-proxy-list.net/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.proxies = []
        table = soup.find("table", {"id": "proxylisttable"})
        for row in table.tbody.find_all("tr"):
            cells = row.find_all("td")
            ip = cells[0].text
            port = cells[1].text
            https = cells[6].text
            if https == "yes":
                self.proxies.append(f"http://{ip}:{port}")
        print(Fore.GREEN + f"Found {len(self.proxies)} proxies" + Style.RESET_ALL)

    def check_proxy(self, proxy):
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        try:
            response = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
            if response.status_code == 200:
                print(Fore.GREEN + f"Alive proxy: {proxy}" + Style.RESET_ALL)
                return proxy
        except requests.RequestException:
            return None
        return None

    def check_proxies(self):
        print(Fore.GREEN + "Starting proxies check..." + Style.RESET_ALL)
        working_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.check_proxy, proxy) for proxy in self.proxies]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    working_proxies.append(result)
        print(Fore.GREEN + f"Found {len(working_proxies)} alive proxies" + Style.RESET_ALL)
        return working_proxies



