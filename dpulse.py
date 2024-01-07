"""
Program start point

You can call this script from yours system terminal: python dpulse.py

"""

import report_creation as rc
import itertools
import time
import threading
from colorama import Fore, Style, Back
from pyfiglet import Figlet
from rich.console import Console
class ProgressBar(threading.Thread):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.do_run = True

    def run(self):
        for char in itertools.cycle('|/-\\'):
            if not self.do_run:
                break
            print(Fore.LIGHTMAGENTA_EX + Back.WHITE + char + Style.RESET_ALL, end='\r')
            time.sleep(0.1)

console = Console()
fig = Figlet(font='univers')
console.print(fig.renderText('DPULSE'), style="bold blue")
print(Fore.BLUE + Back.WHITE + 'HEARTBEAT // version: 0.2b' + Style.RESET_ALL)
print(Fore.BLUE + Back.WHITE + 'Developed by: OSINT-TECHNOLOGIES (https://github.com/OSINT-TECHNOLOGIES)' + Style.RESET_ALL + '\n\n')

def print_menu():
    print(Fore.GREEN + "1. Determine target and start scan")
    print(Fore.RED + "2. Exit DPULSE" + Style.RESET_ALL + '\n')

while True:
    print_menu()
    choice = input(Fore.YELLOW + "Enter your choice >> ")
    if choice == "1":
        short_domain = str(input(Fore.YELLOW + "Enter target's short domain >> "))
        url = "http://" + short_domain + "/"
        dorking_results_amount = int(input(Fore.YELLOW + 'Enter amount of printed Google Dorking results >> '))
        print(Fore.GREEN + 'Determined target >> {}\nShow {} Google Dorking result'.format(short_domain, dorking_results_amount) + Style.RESET_ALL)
        spinner_thread = ProgressBar()
        spinner_thread.start()
        try:
            rc.create_report(short_domain, url, dorking_results_amount)
        finally:
            spinner_thread.do_run = False
            spinner_thread.join()
    elif choice == "2":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
