import aiohttp
import asyncio
from bs4 import BeautifulSoup
from colorama import Fore

async def check_proxy(session, proxy):
    try:
        async with session.get("http://www.google.com", proxy=proxy, timeout=2) as response:
            if response.status == 200:
                return proxy
    except:
        return None

async def get_proxies():
    async with aiohttp.ClientSession() as session:
        print(Fore.GREEN + "Started parsing proxies")
        r = await session.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(await r.text(), 'html.parser')
        table = soup.find('table')
        tasks = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                ip = columns[0].get_text()
                port = columns[1].get_text()
                https = columns[6].get_text()
                if https == 'no':
                    proxy = f"http://{ip}:{port}"
                    tasks.append(check_proxy(session, proxy))
        proxies = await asyncio.gather(*tasks)
        proxies_list = [proxy for proxy in proxies if proxy is not None]
        print(Fore.GREEN + "Finished parsing proxies. Final amount: {}".format(len(proxies_list)))
        return proxies_list