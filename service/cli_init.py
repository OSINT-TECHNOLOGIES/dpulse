import sys

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
        fig = Figlet(font='slant')
        print('\n')
        self.console.print(fig.renderText('DPULSE'), style="red")
        print(Fore.CYAN + Style.BRIGHT + 'DPULSE-CLI // version: 1.0\n' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + 'Developed by OSINT-TECHNOLOGIES\n' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + 'Visit our pages:\nhttps://github.com/OSINT-TECHNOLOGIES' + Style.RESET_ALL + '\n')

    def print_main_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[MAIN MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Determine target and start scan")
        print(Fore.CYAN + "2. Settings")
        print(Fore.CYAN + "3. Help")
        print(Fore.CYAN + "4. Manage/create report storage database")
        print(Fore.LIGHTRED_EX + "5. Exit DPULSE" + Style.RESET_ALL + '\n')

    def print_settings_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[SETTINGS MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show current config")
        print(Fore.CYAN + "2. Add Google Dork to config file")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL + '\n')

    def print_help_menu(self):
        print(Fore.MAGENTA + Back.WHITE + '[HELP MENU]' + Style.RESET_ALL)
        print(Fore.BLACK + Back.WHITE + 'Be advised that choosing any of points below will open your web browser!' + Style.RESET_ALL)
        print(Fore.CYAN + "1. How to correctly input your targets URL in DPULSE")
        print(Fore.CYAN + "2. DPULSE CLI colors and their meanings")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL + '\n')

    def print_db_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[DATABASE MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show database content")
        print(Fore.CYAN + "2. Recreate report from database")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL)
