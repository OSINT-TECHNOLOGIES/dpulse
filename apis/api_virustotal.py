import requests
import sqlite3
from colorama import Fore, Style
import re

def check_domain(domain, api_key):
    api_key = api_key.strip()
    api_key = re.sub(r'[\s\u200B\uFEFF]+', '', api_key)
    print(Fore.GREEN + "Prepared and cleaned-up API key" + Style.RESET_ALL)

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        "x-apikey": api_key
    }
    response = requests.get(url, headers=headers)
    print(Fore.GREEN + "Status:", response.status_code)
    print(Fore.GREEN + "Answer:", response.text)
    try:
        return response.json()
    except Exception as e:
        print(Fore.RED + "Error while parsing JSON: ", e)
        return None


def api_virustotal_check(domain):
    conn = sqlite3.connect('apis//api_keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT api_name, api_key FROM api_keys")
    rows = cursor.fetchall()
    api_key = None
    for row in rows:
        api_name, key = row
        if api_name == 'VirusTotal':
            api_key = key
            print(Fore.GREEN + 'Got VirusTotal API key. Starting VirusTotal scan...\n')
            break

    if not api_key:
        print(Fore.RED + "VirusTutal API key was not found.")
        conn.close()
        return None

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
        return (result.get('categories'),
                len(result.get('detected_urls', [])),
                len(result.get('detected_samples', [])),
                len(result.get('undetected_samples', [])))
    else:
        print(Fore.RED + "Failed to get domain report\n")
        print(Fore.LIGHTGREEN_EX + "-------------------------------------------------\n" + Style.RESET_ALL)
        conn.close()
        return ('No information', 'No information', 'No information', 'No information')
