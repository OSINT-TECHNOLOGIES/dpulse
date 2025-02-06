from datetime import datetime
import requests
import sqlite3
from colorama import Fore, Style
import re

def virustotal_html_prep(formatted_output):
    formatted_output = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', formatted_output)
    start_marker = "=== VIRUSTOTAL API REPORT ==="
    end_marker = "[+] Domain Information:"
    start_index = formatted_output.find(start_marker)
    end_index = formatted_output.find(end_marker)
    if start_index != -1 and end_index != -1:
        formatted_output = formatted_output[:start_index] + formatted_output[end_index:]
    return formatted_output

def check_domain(domain, api_key):
    api_key = api_key.strip()
    api_key = re.sub(r'[\s\u200B\uFEFF]+', '', api_key)

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        "x-apikey": api_key
    }
    response = requests.get(url, headers=headers)

    try:
        result = response.json()
        formatted_output = Fore.LIGHTBLUE_EX + "\n=== VIRUSTOTAL API REPORT ===\n" + Style.RESET_ALL
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Domain Information:{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Domain:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{domain}{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Creation Date:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{datetime.fromtimestamp(result['data']['attributes']['creation_date']).strftime('%Y-%m-%d')}{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Last Update:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{datetime.fromtimestamp(result['data']['attributes']['last_update_date']).strftime('%Y-%m-%d')}{Style.RESET_ALL}\n"
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] DNS Records:{Style.RESET_ALL}\n"
        for record in result['data']['attributes']['last_dns_records']:
            formatted_output += f"{Fore.GREEN}Type:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{record['type']:<6}{Style.RESET_ALL} "
            formatted_output += f"{Fore.GREEN}TTL:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{record['ttl']:<6}{Style.RESET_ALL} "
            formatted_output += f"{Fore.GREEN}Value:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{record['value']}{Style.RESET_ALL}\n"
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Categories:{Style.RESET_ALL}\n"
        for vendor, category in result['data']['attributes']['categories'].items():
            formatted_output += f"{Fore.GREEN}{vendor:<25}:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{category}{Style.RESET_ALL}\n"
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Analysis Stats:{Style.RESET_ALL}\n"
        stats = result['data']['attributes']['last_analysis_stats']
        formatted_output += f"{Fore.GREEN}Harmless:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stats['harmless']}{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Malicious:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stats['malicious']}{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Suspicious:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stats['suspicious']}{Style.RESET_ALL}\n"
        formatted_output += f"{Fore.GREEN}Undetected:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stats['undetected']}{Style.RESET_ALL}\n"
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Detailed Analysis Results:{Style.RESET_ALL}\n"
        results = result['data']['attributes']['last_analysis_results']
        categories = {'harmless': [], 'malicious': [], 'suspicious': [], 'undetected': []}
        for engine, data in results.items():
            categories[data['category']].append(engine)
        for category, engines in categories.items():
            if engines:
                formatted_output += f"\n{Fore.GREEN}{category.title()} ({len(engines)}):{Style.RESET_ALL}\n"
                for engine in sorted(engines):
                    formatted_output += f"{Fore.LIGHTCYAN_EX}- {engine}{Style.RESET_ALL}\n"
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}=== END OF VIRUSTOTAL API REPORT ==={Style.RESET_ALL}\n"
        print(formatted_output)
        return formatted_output
    except Exception as e:
        formatted_output = Fore.RED + f"Error while parsing JSON: {e}" + Style.RESET_ALL
        print(formatted_output)
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
            print(Fore.GREEN + 'Got VirusTotal API key. Starting VirusTotal scan...')
            break
    if not api_key:
        print(Fore.RED + "VirusTutal API key was not found.")
        conn.close()
        return None

    formatted_output = check_domain(domain, api_key)
    return formatted_output
