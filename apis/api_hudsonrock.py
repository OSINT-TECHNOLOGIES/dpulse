import requests
from colorama import Fore, Style
import re

def hudsonrock_html_prep(formatted_output):
    formatted_output = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', formatted_output)
    start_marker = "=== HUDSONROCK API REPORT ==="
    end_marker = "[+] Email Data:"
    start_index = formatted_output.find(start_marker)
    end_index = formatted_output.find(end_marker)
    if start_index != -1 and end_index != -1:
        formatted_output = formatted_output[:start_index] + formatted_output[end_index:]
    return formatted_output

def api_hudsonrock_get(email=None, username=None, domain=None, ip=None):
    base_url = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
    results = {}

    def make_request(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}

    if email:
        email_url = f"{base_url}search-by-email?email={email}"
        results['email'] = make_request(email_url)

    if username:
        username_url = f"{base_url}search-by-username?username={username}"
        results['username'] = make_request(username_url)

    if domain:
        domain_url = f"{base_url}search-by-domain?domain={domain}"
        results['domain'] = make_request(domain_url)

        urls_by_domain_url = f"{base_url}urls-by-domain?domain={domain}"
        results['urls_by_domain'] = make_request(urls_by_domain_url)

    if ip:
        ip_url = f"{base_url}search-by-ip?ip={ip}"
        results['ip'] = make_request(ip_url)

    return results


def api_hudsonrock_check(domain, ip, email, username):
    results = api_hudsonrock_get(email, username, domain, ip)
    formatted_output = Fore.LIGHTBLUE_EX + "\n=== HUDSONROCK API REPORT ===\n" + Style.RESET_ALL
    formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] Provided Data:{Style.RESET_ALL}\n"
    formatted_output += f"{Fore.GREEN}Domain:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{domain}{Style.RESET_ALL}\n"
    formatted_output += f"{Fore.GREEN}IP:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{ip}{Style.RESET_ALL}\n"
    formatted_output += f"{Fore.GREEN}E-mail:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{email}{Style.RESET_ALL}\n"
    formatted_output += f"{Fore.GREEN}Username:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{username}{Style.RESET_ALL}\n"

    def format_section(title, data):
        nonlocal formatted_output
        formatted_output += f"\n{Fore.LIGHTBLUE_EX}[+] {title}:{Style.RESET_ALL}\n"
        if 'error' in data:
            formatted_output += f"{Fore.RED}Error appeared when trying to get results for {title} requests. Probably given data is incorrect.{Style.RESET_ALL}\n"
            return

        if title == 'Email Data':
            formatted_output += f"{Fore.GREEN}Message:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('message', 'No message available')}{Style.RESET_ALL}\n"
            for i, stealer in enumerate(data.get('stealers', []), 1):
                formatted_output += f"\n{Fore.GREEN}--- STEALER {i} ---{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Computer Name:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('computer_name', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}OS:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('operating_system', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Date Compromised:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('date_compromised', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Malware Path:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('malware_path', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}IP:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('ip', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Top Passwords:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_passwords', []))}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Top Logins:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_logins', []))}{Style.RESET_ALL}\n"

        elif title == 'Username Data':
            formatted_output += f"{Fore.GREEN}Message:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('message', 'No message available')}{Style.RESET_ALL}\n"
            for i, stealer in enumerate(data.get('stealers', []), 1):
                formatted_output += f"\n{Fore.GREEN}--- STEALER {i} ---{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Stealer Family:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('stealer_family', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Computer Name:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('computer_name', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}OS:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('operating_system', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Date Compromised:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('date_compromised', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Malware Path:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('malware_path', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}IP:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('ip', 'Not Found')}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Top Passwords:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_passwords', []))}{Style.RESET_ALL}\n"
                formatted_output += f"{Fore.GREEN}Top Logins:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_logins', []))}{Style.RESET_ALL}\n"

        elif title == 'Domain Data':
            formatted_output += f"{Fore.GREEN}Total Entries:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('total', 0)}{Style.RESET_ALL}\n"
            formatted_output += f"{Fore.GREEN}Total Stealers:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('totalStealers', 0)}{Style.RESET_ALL}\n"
            formatted_output += f"\n{Fore.GREEN}Sample Employee URLs:{Style.RESET_ALL}\n"
            employee_urls = data.get('data', {}).get('employees_urls', [])
            if employee_urls:
                for url_data in employee_urls[:10]:
                    formatted_output += f"{Fore.GREEN}Type:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('type', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| URL:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('url', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| Occurrence:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('occurrence', 'N/A')}{Style.RESET_ALL}\n"
            else:
                formatted_output += f"{Fore.RED}No employee URLs available.{Style.RESET_ALL}\n"

        elif title == 'Attack Surface Data':
            formatted_output += f"{Fore.GREEN}Message:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('message', 'No message available')}{Style.RESET_ALL}\n"
            formatted_output += f"\n{Fore.GREEN}Sample Employee URLs:{Style.RESET_ALL}\n"
            employees = data.get('data', {}).get('employees_urls', [])
            if employees:
                for url_data in employees[:10]:
                    formatted_output += f"{Fore.GREEN}Type:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('type', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| URL:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('url', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| Occurrence:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('occurrence', 'N/A')}{Style.RESET_ALL}\n"
            else:
                formatted_output += f"{Fore.RED}No employee URLs available{Style.RESET_ALL}\n"
            formatted_output += f"\n{Fore.GREEN}Sample Client URLs:{Style.RESET_ALL}\n"
            clients = data.get('data', {}).get('clients_urls', [])
            if clients:
                for url_data in clients[:10]:
                    formatted_output += f"{Fore.GREEN}Type:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('type', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| URL:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('url', 'N/A')}{Style.RESET_ALL}"
                    formatted_output += f" {Fore.GREEN}| Occurrence:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{url_data.get('occurrence', 'N/A')}{Style.RESET_ALL}\n"
            else:
                formatted_output += f"{Fore.RED}No client URLs available{Style.RESET_ALL}\n"

        elif title == 'IP Data':
            formatted_output += f"{Fore.GREEN}Message:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{data.get('message', 'No message available')}{Style.RESET_ALL}\n"
            if data.get('stealers'):
                for i, stealer in enumerate(data.get('stealers', []), 1):
                    formatted_output += f"\n{Fore.GREEN}--- STEALER {i} ---{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}Computer Name:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('computer_name', 'Not Found')}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}OS:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('operating_system', 'Not Found')}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}Date Compromised:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('date_compromised', 'Not Found')}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}Malware Path:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('malware_path', 'Not Found')}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}IP:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{stealer.get('ip', 'Not Found')}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}Top Passwords:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_passwords', []))}{Style.RESET_ALL}\n"
                    formatted_output += f"{Fore.GREEN}Top Logins:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{', '.join(stealer.get('top_logins', []))}{Style.RESET_ALL}\n"
        formatted_output += "\n"

    if 'email' in results:
        format_section('Email Data', results['email'])
    if 'username' in results:
        format_section('Username Data', results['username'])
    if 'domain' in results:
        format_section('Domain Data', results['domain'])
    if 'urls_by_domain' in results:
        format_section('Attack Surface Data', results['urls_by_domain'])
    if 'ip' in results:
        format_section('IP Data', results['ip'])

    print(formatted_output)
    return formatted_output
