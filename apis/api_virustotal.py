import requests
import sqlite3
from colorama import Fore, Style

def check_domain(domain, api_key):
    url = "https://www.virustotal.com/vtapi/v2/domain/report"
    params = {
        'domain': domain,
        'apikey': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.RED + f"Error: {response.status_code}" + Style.RESET_ALL)
        return None


def api_virustotal_check(domain):
    conn = sqlite3.connect('apis//api_keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT api_name, api_key FROM api_keys")
    rows = cursor.fetchall()
    for row in rows:
        api_name, api_key = row
        if api_name == 'VirusTotal':
            api_key = str(row[1])
            print(Fore.GREEN + 'Got VirusTotal API key. Starting VirusTotal scan...\n')

    result = check_domain(domain, api_key)

    if result:
        print(Fore.GREEN + "[VIRUSTOTAL DOMAIN REPORT]")
        print(Fore.GREEN + f"Domain: {result.get('domain')}")
        print(Fore.GREEN + f"Categories: {result.get('categories')}")
        print(Fore.GREEN + f"Detected URLs: {len(result.get('detected_urls', []))}")
        print(Fore.GREEN + f"Detected Samples: {len(result.get('detected_samples', []))}")
        print(Fore.GREEN + f"Undetected Samples: {len(result.get('undetected_samples', []))}\n")
        print(Fore.LIGHTGREEN_EX + "-------------------------------------------------\n" + Style.RESET_ALL)
        conn.close()
        return result.get('categories'), len(result.get('detected_urls', [])), len(result.get('detected_samples', [])), len(result.get('undetected_samples', []))
    else:
        print(Fore.RED + "Failed to get domain report\n")
        print(Fore.LIGHTGREEN_EX + "-------------------------------------------------\n" + Style.RESET_ALL)
        conn.close()
        return 'Got no information from VirusTotal API', 'Got no information from VirusTotal API', 'Got no information from VirusTotal API', 'Got no information from VirusTotal API'
        pass


