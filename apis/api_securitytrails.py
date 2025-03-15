import requests
import sqlite3
import re
from colorama import Fore, Style

def securitytrails_html_prep(formatted_output):
    formatted_output = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', formatted_output)
    start_marker = "=== SECURITYTRAILS API REPORT ==="
    end_marker = "[+] Domain General Information:"
    start_index = formatted_output.find(start_marker)
    end_index = formatted_output.find(end_marker)
    if start_index != -1 and end_index != -1:
        formatted_output = formatted_output[:start_index] + formatted_output[end_index:]
    return formatted_output

def check_domain_securitytrails(domain, api_key):
    api_key = api_key.strip()
    api_key = re.sub(r'[\s\u200B\uFEFF]+', '', api_key)

    subdomains_url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?apikey={api_key}"
    general_url = f"https://api.securitytrails.com/v1/domain/{domain}?apikey={api_key}"

    try:
        general_response = requests.get(general_url)
        general_data = general_response.json()
    except Exception as e:
        return Fore.RED + f"Error while parsing JSON: {e}" + Style.RESET_ALL

    formatted_output = Fore.LIGHTBLUE_EX + "=== SECURITYTRAILS API REPORT ===\n" + Style.RESET_ALL
    formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Domain General Information:{Style.RESET_ALL}\n"
    formatted_output += (
        f"{Fore.GREEN}Alexa Rank: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{general_data.get('alexa_rank')}{Style.RESET_ALL}\n"
        f"{Fore.GREEN}Apex Domain: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{general_data.get('apex_domain')}{Style.RESET_ALL}\n"
        f"{Fore.GREEN}Hostname: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{general_data.get('hostname')}{Style.RESET_ALL}\n"
    )

    formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] DNS Records:{Style.RESET_ALL}\n"
    current_dns = general_data.get('current_dns', {})
    for record_type, record_data in current_dns.items():
        formatted_output += f"\n{Fore.GREEN}[{record_type.upper()} RECORDS]:{Style.RESET_ALL}\n"
        for value in record_data.get('values', []):
            if record_type == 'a':
                ip = value.get('ip', '')
                org = value.get('ip_organization', '')
                formatted_output += (
                    f"{Fore.GREEN}IP: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{ip}{Style.RESET_ALL} "
                    f"{Fore.GREEN}| Organization: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{org}{Style.RESET_ALL}\n"
                )
            elif record_type == 'mx':
                hostname = value.get('hostname', '')
                priority = value.get('priority', '')
                org = value.get('hostname_organization', '')
                formatted_output += (
                    f"{Fore.GREEN}Hostname: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{hostname}{Style.RESET_ALL} "
                    f"{Fore.GREEN}| Priority: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{priority}{Style.RESET_ALL} "
                    f"{Fore.GREEN}| Organization: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{org}{Style.RESET_ALL}\n"
                )
            elif record_type == 'ns':
                nameserver = value.get('nameserver', '')
                org = value.get('nameserver_organization', '')
                formatted_output += (
                    f"{Fore.GREEN}Nameserver: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{nameserver}{Style.RESET_ALL} "
                    f"{Fore.GREEN}| Organization: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{org}{Style.RESET_ALL}\n"
                )
            elif record_type == 'soa':
                email = value.get('email', '')
                ttl = value.get('ttl', '')
                formatted_output += (
                    f"{Fore.GREEN}Email: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{email}{Style.RESET_ALL} "
                    f"{Fore.GREEN}| TTL: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{ttl}{Style.RESET_ALL}\n"
                )
            elif record_type == 'txt':
                txt_value = value.get('value', '')
                formatted_output += (
                    f"{Fore.GREEN}Value: {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{txt_value}{Style.RESET_ALL}\n"
                )

    subdomains_response = requests.get(subdomains_url)
    if subdomains_response.status_code == 200:
        subdomains_data = subdomains_response.json()
        sub_count = subdomains_data.get('subdomain_count', 0)
        subdomains = subdomains_data.get('subdomains', [])

        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Subdomains Deep Enumeration:{Style.RESET_ALL}\n"
        formatted_output += (
            f"{Fore.GREEN}Found {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{sub_count}{Style.RESET_ALL}"
            f"{Fore.GREEN} subdomains.{Style.RESET_ALL}\n"
        )

        if subdomains:
            formatted_output += f"{Fore.GREEN}Subdomains list:{Style.RESET_ALL}\n"
            alive_count = 0
            for i, subdomain in enumerate(subdomains, start=1):
                subdomain_url = f"http://{subdomain}.{domain}"
                try:
                    r = requests.get(subdomain_url, timeout=5)
                    if r.status_code == 200:
                        alive_count += 1
                        formatted_output += (
                            f"{Fore.GREEN}{i}. {Style.RESET_ALL}{Fore.LIGHTCYAN_EX}{subdomain_url}{Style.RESET_ALL}"
                            f"{Fore.GREEN} is alive{Style.RESET_ALL}\n"
                        )
                except Exception:
                    pass

            if alive_count == 0:
                formatted_output += (f"{Fore.RED}No alive subdomains found (by HTTP 200 check).{Style.RESET_ALL}\n")
        else:
            formatted_output += f"{Fore.RED}No subdomains found in SecurityTrails data.{Style.RESET_ALL}\n"
    else:
        formatted_output += (f"{Fore.RED}Error while gathering subdomains: {subdomains_response.status_code}{Style.RESET_ALL}\n")

    return formatted_output


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
            print(Fore.GREEN + 'Got SecurityTrails API key. Starting SecurityTrails scan...\n' + Style.RESET_ALL)
            break

    if not api_key:
        print(Fore.RED + "SecurityTrails API key not found." + Style.RESET_ALL)
        conn.close()
        return None

    formatted_output = check_domain_securitytrails(domain, api_key)
    conn.close()
    print(formatted_output)
    return formatted_output
