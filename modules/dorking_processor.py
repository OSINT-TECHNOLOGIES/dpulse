from googlesearch import search
from time import sleep
from colorama import Fore, Style
import get_proxies as gp
import nest_asyncio
import asyncio
import random

nest_asyncio.apply()
def get_query(short_domain):
    with open('config.txt', 'r') as cfg_file:
        lines = cfg_file.readlines()
        index = lines.index('[SOLID DORKS]\n')
        lines_after = lines[index + 2:]
        search_query = [line.format(short_domain) for line in lines_after]
        return search_query

def select_random_proxy(proxies_list):
    selected_proxy = random.choice(proxies_list)
    proxies_list.remove(selected_proxy)
    return selected_proxy
def solid_google_dorking(short_domain, sleep_interval, dorking_results_amount):
    proxies_list = asyncio.run(gp.get_proxies())
    search_delay = 5
    print(Fore.GREEN + "Sleep interval set to {} seconds".format(sleep_interval))
    print(Fore.GREEN + "Processing Google Dorking" + Style.RESET_ALL)
    exposed_documents_query = str(get_query(short_domain)[0])
    linkedin_query = str(get_query(short_domain)[1])
    exposed_databases_query = str(get_query(short_domain)[2])
    try:
        proxy = select_random_proxy(proxies_list)
        print(Fore.GREEN + "Dorking {} with {} proxy".format(exposed_documents_query, proxy))
        exposed_documents = list(search(exposed_documents_query, sleep_interval=sleep_interval, num_results=dorking_results_amount, proxy=proxy))
        print(exposed_documents)
        sleep(search_delay)
        print(Fore.GREEN + "Initiated {} seconds delay. Please, wait".format(search_delay) + Style.RESET_ALL)
        proxy = select_random_proxy(proxies_list)
        print(Fore.GREEN + "Dorking {} with {} proxy".format(exposed_documents_query, proxy))
        linkedin_links = list(search(linkedin_query, sleep_interval=sleep_interval, num_results=dorking_results_amount))
        sleep(search_delay)
        print(Fore.GREEN + "Initiated {} seconds delay. Please, wait".format(search_delay) + Style.RESET_ALL)
        proxy = select_random_proxy(proxies_list)
        print(Fore.GREEN + "Dorking {} with {} proxy".format(exposed_documents_query, proxy))
        exposed_databases = list(search(exposed_databases_query, sleep_interval=sleep_interval, num_results=dorking_results_amount))
    except Exception:
        print(Fore.RED + "[Error #004] - Request error. Error while processing Google Dorking, possibly caused by 429 Client Error" + Style.RESET_ALL)

    return exposed_documents, linkedin_links, exposed_databases