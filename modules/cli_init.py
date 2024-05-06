from colorama import Fore, Back, Style
from pyfiglet import Figlet
from rich.console import Console
from time import sleep
import itertools
import threading

class ProgressBar(threading.Thread):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.do_run = True

    def run(self):
        for char in itertools.cycle('|/-\\'):
            if not self.do_run:
                break
            print(Fore.LIGHTMAGENTA_EX + Back.WHITE + char + Style.RESET_ALL, end='\r')
            sleep(0.1)

class Menu:
    def __init__(self):
        self.console = Console()

    def welcome_menu(self):
        fig = Figlet(font='univers')
        self.console.print(fig.renderText('DPULSE'), style="bold blue")
        print(Fore.BLUE + Back.WHITE + 'HEARTBEAT // version: 0.8b\n' + Style.RESET_ALL)
        print(Fore.BLUE + Back.WHITE + 'Developed by OSINT-TECHNOLOGIES\n' + Style.RESET_ALL)
        print(Fore.BLUE + Back.WHITE + 'Visit our pages:\nhttps://github.com/OSINT-TECHNOLOGIES)' + Style.RESET_ALL + '\n\n')

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
        print(Fore.LIGHTRED_EX + "2. Return to main menu" + Style.RESET_ALL + '\n')

    def print_help_menu(self):
        print(Fore.MAGENTA + Back.WHITE + '[HELP MENU]' + Style.RESET_ALL)
        print(Fore.BLACK + Back.WHITE + 'Be advised that choosing any of points below will open your web browser!' + Style.RESET_ALL)
        print(Fore.CYAN + "1. How to correctly input your targets URL in DPULSE")
        print(Fore.CYAN + "2. DPULSE config parameters and their meanings")
        print(Fore.CYAN + "3. DPULSE CLI colors and their meanings")
        print(Fore.CYAN + "4. DPULSE config parameters and their meanings")
        print(Fore.LIGHTRED_EX + "5. Return to main menu" + Style.RESET_ALL + '\n')

    def print_db_menu(self):
        print(Fore.MAGENTA + Back.WHITE + '[DATABASE MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show database content")
        print(Fore.CYAN + "2. Recreate report from database")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL + '\n')
