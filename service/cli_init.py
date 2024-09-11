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
        print(Fore.MAGENTA + Style.BRIGHT + 'DPULSE-CLI // 1.1 (stable) // OSINT-TECHNOLOGIES\n' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + 'Visit our pages:\nhttps://github.com/OSINT-TECHNOLOGIES\nhttps://pypi.org/project/dpulse/' + Style.RESET_ALL + '\n')

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
        print(Fore.CYAN + "1. Show current dorks list")
        print(Fore.CYAN + "2. Add Google Dork to config file")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL + '\n')

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
        print(Fore.MAGENTA + Back.WHITE + '[DATABASE MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show database content")
        print(Fore.CYAN + "2. Recreate report from database")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL)
