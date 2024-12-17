import requests
import sqlite3
from colorama import Fore, Style

def api_securitytrails_check(domain):
    conn = sqlite3.connect('apis//api_keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT api_name, api_key FROM api_keys")
    rows = cursor.fetchall()
    for row in rows:
        api_name, api_key = row
        if api_name == 'SecurityTrails':
            api_key = str(row[1])
            print(Fore.GREEN + 'Got SecurityTrails API key. Starting SecurityTrails scan...\n')

    alive_subdomains = []
    txt_records = []
    a_records_list = []
    mx_records_list = []
    ns_records_list = []
    soa_records_list = []
    subdomains_url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?apikey={api_key}"
    response = requests.get(subdomains_url)

    url = f"https://api.securitytrails.com/v1/domain/{domain}?apikey={api_key}"
    general_response = requests.get(url)
    general_data = general_response.json()

    print(Fore.GREEN + "[DOMAIN GENERAL INFORMATION]\n")
    print(Fore.GREEN + "Alexa Rank: " + Fore.LIGHTCYAN_EX + f"{general_data['alexa_rank']}")
    print(Fore.GREEN + "Apex Domain: " + Fore.LIGHTCYAN_EX + f"{general_data['apex_domain']}")
    print(Fore.GREEN + "Hostname: " + Fore.LIGHTCYAN_EX + f"{general_data['hostname']}" + Style.RESET_ALL)

    print(Fore.GREEN + "\n[DNS RECORDS]" + Style.RESET_ALL)
    for record_type, record_data in general_data['current_dns'].items():
        print(Fore.GREEN + f"\n[+] {record_type.upper()} RECORDS:" + Style.RESET_ALL)
        for value in record_data.get('values', []):
            if record_type == 'a':
                print(Fore.GREEN + "IP: " + Fore.LIGHTCYAN_EX + f"{value['ip']} " + Fore.GREEN + "| Organization: " + Fore.LIGHTCYAN_EX + f"{value['ip_organization']}")
                a_records_list.append({'ip': value.get('ip', ''), 'organization': value.get('ip_organization', '')})
            elif record_type == 'mx':
                print(Fore.GREEN + "Hostname: " + Fore.LIGHTCYAN_EX + f"{value['hostname']} " + Fore.GREEN + "| Priority: " + Fore.LIGHTCYAN_EX + f"{value['priority']} " + Fore.GREEN +  "| Organization: " + Fore.LIGHTCYAN_EX + f"{value['hostname_organization']}")
                mx_records_list.append({'mx_hostname': value.get('hostname', ''), 'mx_priority': value.get('priority', ''), 'mx_organization': value.get('hostname_organization', '')})
            elif record_type == 'ns':
                print(Fore.GREEN + "Nameserver: " + Fore.LIGHTCYAN_EX + f"{value['nameserver']} " + Fore.GREEN + "| Organization: " + Fore.LIGHTCYAN_EX + f"{value['nameserver_organization']}")
                ns_records_list.append({'ns_nameserver': value.get('nameserver', ''), 'ns_organization': value.get('nameserver_organization', '')})
            elif record_type == 'soa':
                print(Fore.GREEN + "Email: " + Fore.LIGHTCYAN_EX + f"{value['email']} " + Fore.GREEN + "| TTL: " + Fore.LIGHTCYAN_EX + f"{value['ttl']}")
                soa_records_list.append({'soa_email': value.get('email', ''), 'soa_ttl': value.get('ttl', '')})
            elif record_type == 'txt':
                print(Fore.GREEN + "Value: " + Fore.LIGHTCYAN_EX + f"{value['value']}")
                txt_records.append(value['value'])

    if response.status_code == 200:
        data = response.json()
        print(Fore.GREEN + "\n[SUBDOMAINS DEEP ENUMERATION]\n")
        print(Fore.GREEN + f"Found " + Fore.LIGHTCYAN_EX + f"{data['subdomain_count']} " + Fore.GREEN + "subdomains")
        print(Fore.GREEN + "Subdomains list: ")
        for i, subdomain in enumerate(data['subdomains'], start=1):
            subdomain_url = f"http://{subdomain}.{domain}"
            try:
                response = requests.get(subdomain_url, timeout=5)
                if response.status_code == 200:
                    print(Fore.GREEN + f"{i}. " + Fore.LIGHTCYAN_EX + f"{subdomain_url} " + Fore.GREEN + "is alive")
                    alive_subdomains.append(subdomain_url)
                else:
                    pass
            except Exception:
                pass
    else:
        pass

    return general_data['alexa_rank'], general_data['apex_domain'], general_data['hostname'], alive_subdomains, txt_records, a_records_list, mx_records_list, ns_records_list, soa_records_list
