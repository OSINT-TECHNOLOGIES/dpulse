import mechanicalsoup
from bs4 import BeautifulSoup
import requests
from colorama import Fore, Style

def scrape_dork(dork, short_domain):
    browser = mechanicalsoup.Browser(soup_config={'features': 'html.parser'})
    modified_dork = dork.replace("{}", f"{short_domain}")
    print(Fore.GREEN + f"Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + f"{modified_dork}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL)
    search_result = browser.get(f"https://www.google.com/search?q={modified_dork}")
    soup = BeautifulSoup(search_result.content, "html.parser")
    results = soup.find_all("a", href=True)
    full_urls = []
    for result in results:
        relative_link = result['href']
        if relative_link.startswith("/"):
            pass
        else:  # Sometimes Google might give an already full URL
            full_urls.append(relative_link)

    return full_urls

def composing_dorking(dorks, conn, short_domain, report_path):
    results_file = open(f"{report_path}//dork_results.txt", "w")
    for dork_id, dork in dorks:
        results = scrape_dork(dork, short_domain)
        #print(Fore.GREEN + f"\nDORK #{dork_id}: {dork}")
        results_file.write(f"\nDORK #{dork_id}: {dork}\n")
        if results:
            for result in results:
                #print(f"=> {result_link}")
                results_file.write(f"=> {result}\n")
            print(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
        else:
            #print("No results found for this dork.")
            results_file.write("No results found for this dork.\n")
    conn.close()
    results_file.close()