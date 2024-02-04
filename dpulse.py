"""
Program start point

You can call this script from yours system terminal: python dpulse.py
"""

import report_creation as rc

try:
    import itertools
    import time
    import threading
    from colorama import Fore, Style, Back
    from pyfiglet import Figlet
    from rich.console import Console
    import sys
    import webbrowser
except ImportError:
    print(Fore.RED + "Can't import some requirements that are necessary to start DPULSE. Please check that all necessary requirements are installed!" + Style.RESET_ALL)
    sys.exit()
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
print(Fore.BLUE + Back.WHITE + 'HEARTBEAT // version: 0.4b' + Style.RESET_ALL)
print(Fore.BLUE + Back.WHITE + 'Developed by: OSINT-TECHNOLOGIES (https://github.com/OSINT-TECHNOLOGIES)' + Style.RESET_ALL + '\n\n')

def print_main_menu():
    print('\n')
    print(Fore.BLUE + '[MAIN MENU]')
    print(Fore.GREEN + "1. Determine target and start scan")
    print(Fore.GREEN + "2. Settings")
    print(Fore.GREEN + "3. Help")
    print(Fore.RED + "4. Exit DPULSE" + Style.RESET_ALL + '\n')

def print_settings_menu():
    print('\n')
    print(Fore.BLUE + '[SETTINGS MENU]')
    print(Fore.GREEN + "1. Show current config")
    print(Fore.GREEN + "2. Edit config parameters")
    print(Fore.RED + "3. Return to main menu" + Style.RESET_ALL + '\n')

def print_cfg_edit_menu():
    print(Fore.BLUE + '[SETTINGS EDITING]')
    print(Fore.GREEN + "1. Change sleep-interval")
    print(Fore.GREEN + "2. Change timeout")
    print(Fore.GREEN + "3. Add Dorking query to the list")
    print(Fore.GREEN + "4. Remove Dorking query from the list")
    print(Fore.RED + "5. Return to main menu" + Style.RESET_ALL + '\n')

def print_help_menu():
    print(Fore.BLUE + '[HELP MENU]')
    print(Fore.BLUE + 'Choosing any of points below will open your web browser!')
    print(Fore.GREEN + "1. How to correctly input your targets URL in DPULSE")
    print(Fore.GREEN + "2. DPULSE config parameters and their meanings")
    print(Fore.RED + "3. Return to main menu" + Style.RESET_ALL + '\n')

def change_setting(filename):
    cfg_context = open(filename).read()

    print('\n~ START OF CONFIG FILE ~')
    print('\n' + Fore.BLUE + cfg_context + Style.RESET_ALL)
    print(Fore.YELLOW + '\n~ END OF CONFIG FILE ~\n')

    setting = input('Enter setting to change >> ')
    new_value = input('Enter new value >> ')

    with open(filename, 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith(setting + ':'):
                lines[i] = f'{setting}: {new_value}\n'
        file.seek(0)
        file.writelines(lines)
        print('\n')
        print(Fore.GREEN + 'Setting {} successfully changed to {}'.format(setting, new_value))

while True:
    print_main_menu()
    choice = input(Fore.YELLOW + "Enter your choice >> ")
    print('\n')
    if choice == "1":
        short_domain = str(input(Fore.YELLOW + "Enter target's domain name >> "))
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
        print_settings_menu()
        choice_settings = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_settings == '1':
            with open('config.txt', 'r') as cfg_file:
                print('\n~ START OF CONFIG FILE ~')
                print('\n' + Fore.BLUE + cfg_file.read() + Style.RESET_ALL)
                print(Fore.YELLOW + '\n~ END OF CONFIG FILE ~\n')
                continue
        elif choice_settings == '2':
            change_setting('config.txt')
            continue
        elif choice_settings == '3':
            continue
        break
    elif choice == "3":
        print_help_menu()
        choice_help = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_help == '1':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/How-to-correctly-input-your-targets-address-in-DPULSE')
        elif choice_help == '2':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-config-parameters-and-their-meanings')
        elif choice_help == '3':
            continue
    elif choice == "4":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
