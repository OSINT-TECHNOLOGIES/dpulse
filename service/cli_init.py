import sys
from config_processing import read_config

try:
    from colorama import Fore, Back, Style
    from pyfiglet import Figlet
    from rich.console import Console
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

class Menu:
    def __init__(self):
        self.console = Console()

    def welcome_menu(self):
        config_values = read_config()
        preview_style = (config_values['preview_color']).lower()
        wm_font = (config_values['wm_font']).lower()
        fig = Figlet(font=wm_font)
        print('\n')
        self.console.print(fig.renderText('DPULSE'), style=preview_style)
        print(Fore.MAGENTA + Style.BRIGHT + '[DPULSE-CLI] - [v1.2 stable] - [OSINT-TECHNOLOGIES]\n' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + '[Visit our pages]\nGitHub repository: https://github.com/OSINT-TECHNOLOGIES\nPyPi page: https://pypi.org/project/dpulse/\nDocumentation: https://dpulse.readthedocs.io' + Style.RESET_ALL)

    def print_main_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[MAIN MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Target selection & scanning")
        print(Fore.CYAN + "2. General settings")
        print(Fore.CYAN + "3. Dorking module manager")
        print(Fore.CYAN + "4. Report storage DB manager")
        print(Fore.CYAN + "5. API modules manager")
        print(Fore.CYAN + "6. Help (browser will be opened!)")
        print(Fore.LIGHTRED_EX + "7. Exit DPULSE" + Style.RESET_ALL + '\n')

    def print_settings_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[SETTINGS MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Print current config file")
        print(Fore.CYAN + "2. Edit config file")
        print(Fore.CYAN + "3. Clear journal content")
        print(Fore.LIGHTRED_EX + "4. Return to main menu" + Style.RESET_ALL + '\n')

    def print_db_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[REPORTS DATABASE MANAGER]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show database content")
        print(Fore.CYAN + "2. Recreate report from database")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL)

    def dorking_db_manager(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[DORKING DB MANAGER]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Generate custom Dorking DB")
        print(Fore.LIGHTRED_EX + "2. Return to main menu\n" + Style.RESET_ALL)

    def api_manager(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[API KEYS DB MANAGER]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Add API key")
        print(Fore.CYAN + "2. Restore reference API Keys DB")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL)

def print_prescan_summary(short_domain, report_filetype, pagesearch_ui_mark, dorking_ui_mark, used_api_ui, case_comment):
    print(Fore.LIGHTMAGENTA_EX + "\n[PRE-SCAN SUMMARY]\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Determined target: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + short_domain + Style.RESET_ALL)
    print(Fore.GREEN + "Report type: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + report_filetype.lower() + Style.RESET_ALL)
    print(Fore.GREEN + "PageSearch conduction: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + pagesearch_ui_mark + Style.RESET_ALL)
    print(Fore.GREEN + "Dorking conduction: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + dorking_ui_mark + Style.RESET_ALL)
    print(Fore.GREEN + "APIs scan: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + used_api_ui + Style.RESET_ALL)
    print(Fore.GREEN + "Case comment: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + case_comment + Style.RESET_ALL + "\n")

def print_api_db_msg():
    print(Fore.GREEN + "\nYou've entered custom Dorking DB generator!\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Remember some rules in order to successfully create your custom Dorking DB:" + Style.RESET_ALL)
    print(Fore.GREEN + "[1] - dork_id variable must be unique, starting with 1 and then +1 every new dork" + Style.RESET_ALL)
    print(Fore.GREEN + "[2] - When it comes to define domain in dork, put {} in it\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Examples: related:{}, site:{} inurl:login and so on\n" + Style.RESET_ALL)

def print_ps_cli_report(subdomains_list,  accessible_subdomains, ps_emails_return, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter):
    if len(subdomains_list) == 0:
        print(Fore.GREEN + "\nDuring subdomains analysis:\n[+] Total " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{len(subdomains_list)}" + Style.RESET_ALL + Fore.GREEN + " subdomains were checked" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nDuring subdomains analysis:\n[+] Total " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{len(subdomains_list)}" + Style.RESET_ALL + Fore.GREEN + " subdomains were checked" + Style.RESET_ALL)
    if accessible_subdomains == 0:
        print(Fore.GREEN + "[+] Among them " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{accessible_subdomains}" + Style.RESET_ALL + Fore.GREEN + " subdomains were accessible" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Among them " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{accessible_subdomains}" + Style.RESET_ALL + Fore.GREEN + " subdomains were accessible" + Style.RESET_ALL)
    if len(ps_emails_return) == 0:
        print(Fore.GREEN + "[+] In result, " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{len(ps_emails_return)}" + Style.RESET_ALL + Fore.GREEN + " unique e-mail addresses were found" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] In result, " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{len(ps_emails_return)}" + Style.RESET_ALL + Fore.GREEN + " unique e-mail addresses were found" + Style.RESET_ALL)
    if files_counter == 0:
        print(Fore.GREEN + "[+] Also, " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{files_counter}" + Style.RESET_ALL + Fore.GREEN + " files were extracted" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Also, " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{files_counter}" + Style.RESET_ALL + Fore.GREEN + " files were extracted" + Style.RESET_ALL)
    if cookies_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{cookies_counter}" + Style.RESET_ALL + Fore.GREEN + " cookies with values" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookies_counter}" + Style.RESET_ALL + Fore.GREEN + " cookies with values" + Style.RESET_ALL)
    if api_keys_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{api_keys_counter}" + Style.RESET_ALL + Fore.GREEN + " API keys" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{api_keys_counter}" + Style.RESET_ALL + Fore.GREEN + " API keys" + Style.RESET_ALL)
    if website_elements_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{website_elements_counter}" + Style.RESET_ALL + Fore.GREEN + " different web page elements" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{website_elements_counter}" + Style.RESET_ALL + Fore.GREEN + " different web page elements" + Style.RESET_ALL)
    if exposed_passwords_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{exposed_passwords_counter}" + Style.RESET_ALL + Fore.GREEN + " exposed passwords" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{exposed_passwords_counter}" + Style.RESET_ALL + Fore.GREEN + " exposed passwords" + Style.RESET_ALL)
