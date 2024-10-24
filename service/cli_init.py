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
        print(Fore.MAGENTA + Style.BRIGHT + '[DPULSE-CLI] - [v1.1.2 stable] - [OSINT-TECHNOLOGIES]\n' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + 'Visit our pages:\nhttps://github.com/OSINT-TECHNOLOGIES\nhttps://pypi.org/project/dpulse/' + Style.RESET_ALL)

    def print_main_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[MAIN MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Target selection & scanning")
        print(Fore.CYAN + "2. General settings")
        print(Fore.CYAN + "3. Dorking module manager")
        print(Fore.CYAN + "4. Report storage DB manager")
        print(Fore.CYAN + "5. API modules manager (not active)")
        print(Fore.CYAN + "6. Help")
        print(Fore.LIGHTRED_EX + "7. Exit DPULSE" + Style.RESET_ALL + '\n')

    def print_settings_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[SETTINGS MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Print current config file")
        print(Fore.CYAN + "2. Edit config file")
        print(Fore.CYAN + "3. Add API key for existing API (not active)")
        print(Fore.CYAN + "4. Clear journal content")
        print(Fore.LIGHTRED_EX + "5. Return to main menu" + Style.RESET_ALL + '\n')

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
