import requests
from colorama import Fore, Style
import re

def hudsonrock_html_prep(formatted_output):
    formatted_output = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', formatted_output)

    start_marker = "===== HUDSONROCK API SCAN SUMMARY ====="
    end_marker = "=== EMAIL DATA ==="

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
    formatted_output = Fore.LIGHTMAGENTA_EX + "\n===== HUDSONROCK API SCAN SUMMARY =====\n\n" + Style.RESET_ALL
    formatted_output += (Fore.LIGHTMAGENTA_EX + "=== PROVIDED DATA ===\n" + Style.RESET_ALL + Fore.GREEN + "\nDomain: " +
            Fore.LIGHTCYAN_EX + f"{domain}\n" + Style.RESET_ALL +
            Fore.GREEN + "IP: " + Fore.LIGHTCYAN_EX + f"{ip}\n" + Style.RESET_ALL +
            Fore.GREEN + "E-mail: " + Fore.LIGHTCYAN_EX + f"{email}\n" + Style.RESET_ALL +
            Fore.GREEN + "Username: " + Fore.LIGHTCYAN_EX + f"{username}\n" + Style.RESET_ALL
    )

    def format_section(title, data):
        nonlocal formatted_output
        formatted_output += Fore.LIGHTMAGENTA_EX + f"\n=== {title.upper()} ===\n" + Style.RESET_ALL
        if 'error' in data:
            formatted_output += Fore.RED + f"\nError appeared when trying to get results for {title} requests. Probably given data is incorrect.\n\n" + Style.RESET_ALL
            return

        if title == 'Email Data':
            formatted_output += Fore.GREEN + f"\n{data.get('message', 'No message available')}\n" + Style.RESET_ALL
            for i, stealer in enumerate(data.get('stealers', []), 1):
                formatted_output += (
                        Fore.GREEN + f"\n--- STEALER {i}" +
                        Fore.GREEN + " ---\n" +
                        "Computer Name: " + Fore.LIGHTCYAN_EX + f"{stealer.get('computer_name', 'Not Found')}" + Fore.GREEN + "\n" +
                        "OS: " + Fore.LIGHTCYAN_EX + f"{stealer.get('operating_system', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Date Compromised: " + Fore.LIGHTCYAN_EX + f"{stealer.get('date_compromised', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Malware Path: " + Fore.LIGHTCYAN_EX + f"{stealer.get('malware_path', 'Not Found')}" + Fore.GREEN + "\n" +
                        "IP: " + Fore.LIGHTCYAN_EX + f"{stealer.get('ip', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Top Passwords: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_passwords', []))}" + Fore.GREEN + "\n" +
                        "Top Logins: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_logins', []))}" + "\n" +
                        Style.RESET_ALL
                )
        elif title == 'Username Data':
            formatted_output += Fore.GREEN + f"\n{data.get('message', 'No message available')}\n" + Style.RESET_ALL
            for i, stealer in enumerate(data.get('stealers', []), 1):
                formatted_output += (
                        Fore.GREEN + f"\n--- STEALER {i}" +
                        Fore.GREEN + " ---\n" +
                        "Stealer Family: " + Fore.LIGHTCYAN_EX + f"{stealer.get('stealer_family', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Computer Name: " + Fore.LIGHTCYAN_EX + f"{stealer.get('computer_name', 'Not Found')}" + Fore.GREEN + "\n" +
                        "OS: " + Fore.LIGHTCYAN_EX + f"{stealer.get('operating_system', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Date Compromised: " + Fore.LIGHTCYAN_EX + f"{stealer.get('date_compromised', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Malware Path: " + Fore.LIGHTCYAN_EX + f"{stealer.get('malware_path', 'Not Found')}" + Fore.GREEN + "\n" +
                        "IP: " + Fore.LIGHTCYAN_EX + f"{stealer.get('ip', 'Not Found')}" + Fore.GREEN + "\n" +
                        "Top Passwords: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_passwords', []))}" + Fore.GREEN + "\n" +
                        "Top Logins: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_logins', []))}" + "\n" +
                        Style.RESET_ALL
                )

        elif title == 'Domain Data':
            formatted_output += (
                    Fore.GREEN + "\nTotal Entries: " + Fore.LIGHTCYAN_EX + f"{data.get('total', 0)}" +
                    Fore.GREEN + "\nTotal Stealers: " + Fore.LIGHTCYAN_EX + f"{data.get('totalStealers', 0)}" +
                    "\n\n" + Style.RESET_ALL
            )
            formatted_output += Fore.GREEN + "Sample Employee URLs:\n" + Style.RESET_ALL
            employee_urls = data.get('data', {}).get('employees_urls', [])
            if employee_urls:
                for url_data in employee_urls[:10]:
                    formatted_output += (
                            Fore.GREEN + "Type: " + Fore.LIGHTCYAN_EX + f"{url_data.get('type', 'N/A')}" +
                            Fore.GREEN + " | URL: " + Fore.LIGHTCYAN_EX + f"{url_data.get('url', 'N/A')}" +
                            Fore.GREEN + " | Occurrence: " + Fore.LIGHTCYAN_EX + f"{url_data.get('occurrence', 'N/A')}" +
                            Fore.GREEN + "\n" +
                            Style.RESET_ALL
                    )
            else:
                formatted_output += Fore.RED + "No employee URLs available.\n" + Style.RESET_ALL
        elif title == 'Attack Surface Data':
            formatted_output += Fore.GREEN + f"\n{data.get('message', 'No message available')}\n" + Style.RESET_ALL
            formatted_output += Fore.GREEN + "\nSample Employee URLs:\n" + Style.RESET_ALL
            employees = data.get('data', {}).get('employees_urls', [])
            if employees:
                for url_data in employees[:10]:
                    formatted_output += (
                            Fore.GREEN + "Type: " + Fore.LIGHTCYAN_EX + f"{url_data.get('type', 'N/A')}" +
                            Fore.GREEN + " | URL: " + Fore.LIGHTCYAN_EX + f"{url_data.get('url', 'N/A')}" +
                            Fore.GREEN + " | Occurrence: " + Fore.LIGHTCYAN_EX + f"{url_data.get('occurrence', 'N/A')}" +
                            Fore.GREEN + "\n" +
                            Style.RESET_ALL
                    )
            else:
                formatted_output += Fore.RED + "No employee URLs available.\n" + Style.RESET_ALL

            formatted_output += Fore.GREEN + "\nSample Client URLs:\n" + Style.RESET_ALL
            clients = data.get('data', {}).get('clients_urls', [])
            if clients:
                for url_data in clients[:10]:
                    formatted_output += (
                            Fore.GREEN + "Type: " + Fore.LIGHTCYAN_EX + f"{url_data.get('type', 'N/A')}" +
                            Fore.GREEN + " | URL: " + Fore.LIGHTCYAN_EX + f"{url_data.get('url', 'N/A')}" +
                            Fore.GREEN + " | Occurrence: " + Fore.LIGHTCYAN_EX + f"{url_data.get('occurrence', 'N/A')}" +
                            Fore.GREEN + "\n" + Style.RESET_ALL
                    )
            else:
                formatted_output += "No client URLs available.\n"
        elif title == 'IP Data':
            formatted_output += Fore.GREEN + f"\n{data.get('message', 'No message available')}\n" + Style.RESET_ALL
            if data.get('stealers'):
                for i, stealer in enumerate(data.get('stealers', []), 1):
                    formatted_output += (
                            Fore.GREEN + f"--- STEALER {i} ---\n" +
                            "Computer Name: " + Fore.LIGHTCYAN_EX + f"{stealer.get('computer_name', 'Not Found')}" + Fore.GREEN + "\n" +
                            "OS: " + Fore.LIGHTCYAN_EX + f"{stealer.get('operating_system', 'Not Found')}" + Fore.GREEN + "\n" +
                            "Date Compromised: " + Fore.LIGHTCYAN_EX + f"{stealer.get('date_compromised', 'Not Found')}" + Fore.GREEN + "\n" +
                            "Malware Path: " + Fore.LIGHTCYAN_EX + f"{stealer.get('malware_path', 'Not Found')}" + Fore.GREEN + "\n" +
                            "IP: " + Fore.LIGHTCYAN_EX + f"{stealer.get('ip', 'Not Found')}" + Fore.GREEN + "\n" +
                            "Top Passwords: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_passwords', []))}" + Fore.GREEN + "\n" +
                            "Top Logins: " + Fore.LIGHTCYAN_EX + f"{', '.join(stealer.get('top_logins', []))}" + "\n" +
                            Style.RESET_ALL
                    )
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
