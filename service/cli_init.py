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
        print(Fore.MAGENTA + Style.BRIGHT + '[DPULSE-CLI] - [v1.1.3 rolling] - [OSINT-TECHNOLOGIES]\n' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + 'Visit our pages:\nhttps://github.com/OSINT-TECHNOLOGIES\nhttps://pypi.org/project/dpulse/' + Style.RESET_ALL)

    def print_main_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[MAIN MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Target selection & scanning")
        print(Fore.CYAN + "2. General settings")
        print(Fore.CYAN + "3. Dorking module manager")
        print(Fore.CYAN + "4. Report storage DB manager")
        print(Fore.CYAN + "5. API modules manager")
        print(Fore.CYAN + "6. Help")
        print(Fore.LIGHTRED_EX + "7. Exit DPULSE" + Style.RESET_ALL + '\n')

    def print_settings_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[SETTINGS MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Print current config file")
        print(Fore.CYAN + "2. Edit config file")
        print(Fore.CYAN + "3. Clear journal content")
        print(Fore.LIGHTRED_EX + "4. Return to main menu" + Style.RESET_ALL + '\n')

    def print_help_menu(self):
        print(Fore.MAGENTA + Back.WHITE + '[HELP MENU]' + Style.RESET_ALL)
        print(Fore.BLACK + Back.WHITE + '\nBe advised that choosing any of points below will open your web browser!' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Open DPULSE repository")
        print(Fore.CYAN + "2. Open DPULSE wiki")
        print(Fore.CYAN + "3. How to correctly input your targets in DPULSE")
        print(Fore.CYAN + "4. PageSearch user guide")
        print(Fore.CYAN + "5. Report storage database user guide")
        print(Fore.LIGHTRED_EX + "6. Return to main menu" + Style.RESET_ALL + '\n')

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
        print(Fore.LIGHTRED_EX + "2. Return to main menu" + Style.RESET_ALL)
        print('\n')

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
    print('\n')
    print(Fore.GREEN + "You've entered custom Dorking DB generator!\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Remember some rules in order to successfully create your custom Dorking DB:" + Style.RESET_ALL)
    print(Fore.GREEN + "[1] - dork_id variable must be unique, starting with 1 and then +1 every new dork" + Style.RESET_ALL)
    print(Fore.GREEN + "[2] - When it comes to define domain in dork, put {} in it\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Examples: related:{}, site:{} inurl:login and so on\n" + Style.RESET_ALL)
