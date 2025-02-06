import requests
import sqlite3
from colorama import Fore, Style
import re


def api_securitytrails_check(domain):
    conn = sqlite3.connect('apis//api_keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT api_name, api_key FROM api_keys")
    rows = cursor.fetchall()
    api_key = None
    for row in rows:
        api_name, key = row
        if api_name == 'SecurityTrails':
            api_key = str(key)
            api_key = api_key.strip()
            api_key = re.sub(r'[\s\u200B\uFEFF]+', '', api_key)
            print(Fore.GREEN + 'Got SecurityTrails API key. Starting SecurityTrails scan...\n')
            break

    if not api_key:
        print(Fore.RED + "SecurityTrails API key not found.")
        conn.close()
        return None

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

    try:
        general_data = general_response.json()
    except Exception as e:
        print(Fore.RED + f"Error while parsing JSON: {e}")
        conn.close()
        return None

    print(Fore.GREEN + "[DOMAIN GENERAL INFORMATION]\n")
    print(Fore.GREEN + "Alexa Rank: " + Fore.LIGHTCYAN_EX + f"{general_data.get('alexa_rank')}")
    print(Fore.GREEN + "Apex Domain: " + Fore.LIGHTCYAN_EX + f"{general_data.get('apex_domain')}")
    print(Fore.GREEN + "Hostname: " + Fore.LIGHTCYAN_EX + f"{general_data.get('hostname')}" + Style.RESET_ALL)

    print(Fore.GREEN + "\n[DNS RECORDS]" + Style.RESET_ALL)
    for record_type, record_data in general_data.get('current_dns', {}).items():
        print(Fore.GREEN + f"\n[+] {record_type.upper()} RECORDS:" + Style.RESET_ALL)
        for value in record_data.get('values', []):
            if record_type == 'a':
                print(Fore.GREEN + "IP: " + Fore.LIGHTCYAN_EX + f"{value.get('ip')}" +
                      Fore.GREEN + " | Organization: " + Fore.LIGHTCYAN_EX + f"{value.get('ip_organization')}")
                a_records_list.append({'ip': value.get('ip', ''), 'organization': value.get('ip_organization', '')})
            elif record_type == 'mx':
                print(Fore.GREEN + "Hostname: " + Fore.LIGHTCYAN_EX + f"{value.get('hostname')}" +
                      Fore.GREEN + " | Priority: " + Fore.LIGHTCYAN_EX + f"{value.get('priority')}" +
                      Fore.GREEN + " | Organization: " + Fore.LIGHTCYAN_EX + f"{value.get('hostname_organization')}")
                mx_records_list.append(
                    {'mx_hostname': value.get('hostname', ''), 'mx_priority': value.get('priority', ''),
                     'mx_organization': value.get('hostname_organization', '')})
            elif record_type == 'ns':
                print(Fore.GREEN + "Nameserver: " + Fore.LIGHTCYAN_EX + f"{value.get('nameserver')}" +
                      Fore.GREEN + " | Organization: " + Fore.LIGHTCYAN_EX + f"{value.get('nameserver_organization')}")
                ns_records_list.append({'ns_nameserver': value.get('nameserver', ''),
                                        'ns_organization': value.get('nameserver_organization', '')})
            elif record_type == 'soa':
                print(Fore.GREEN + "Email: " + Fore.LIGHTCYAN_EX + f"{value.get('email')}" +
                      Fore.GREEN + " | TTL: " + Fore.LIGHTCYAN_EX + f"{value.get('ttl')}")
                soa_records_list.append({'soa_email': value.get('email', ''), 'soa_ttl': value.get('ttl', '')})
            elif record_type == 'txt':
                print(Fore.GREEN + "Value: " + Fore.LIGHTCYAN_EX + f"{value.get('value')}")
                txt_records.append(value.get('value'))

    if response.status_code == 200:
        data = response.json()
        print(Fore.GREEN + "\n[SUBDOMAINS DEEP ENUMERATION]\n")
        print(
            Fore.GREEN + f"Found " + Fore.LIGHTCYAN_EX + f"{data.get('subdomain_count')}" + Fore.GREEN + " subdomains")
        print(Fore.GREEN + "Subdomains list: ")
        for i, subdomain in enumerate(data.get('subdomains', []), start=1):
            subdomain_url = f"http://{subdomain}.{domain}"
            try:
                r = requests.get(subdomain_url, timeout=5)
                if r.status_code == 200:
                    print(Fore.GREEN + f"{i}. " + Fore.LIGHTCYAN_EX + f"{subdomain_url}" + Fore.GREEN + " is alive")
                    alive_subdomains.append(subdomain_url)
            except Exception:
                pass
    else:
        print(Fore.RED + "Error while gathering subdomains: " + str(response.status_code))

    conn.close()
    return (
        general_data.get('alexa_rank'),
        general_data.get('apex_domain'),
        general_data.get('hostname'),
        alive_subdomains,
        txt_records,
        a_records_list,
        mx_records_list,
        ns_records_list,
        soa_records_list
    )
