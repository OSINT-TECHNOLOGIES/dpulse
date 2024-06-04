import sys
sys.path.append('datagather_modules')
sys.path.append('service')

import pdf_report_creation as pdf_rc
import cli_init
import db_processing as db

try:
    import time
    from colorama import Fore, Style, Back
    import webbrowser
    import sqlite3
    import os
    import itertools
    import threading
    from time import sleep
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

cli = cli_init.Menu()
cli.welcome_menu()

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

db.db_creation('report_storage.db')

while True:
    cli.print_main_menu()
    choice = input(Fore.YELLOW + "Enter your choice >> ")
    if choice == "1":
        print('\n')
        while True:
            short_domain = input(Fore.YELLOW + "\nEnter target's domain name (or 'back' to return to the menu) >> ")
            if short_domain.lower() == "back":
                print(Fore.RED + "\nReturned to main menu")
                break
            else:
                url = "http://" + short_domain + "/"
                case_comment = input(Fore.YELLOW + "Enter case comment (or enter '-' if you don't need comment to the case) >> ")
                print(Fore.LIGHTMAGENTA_EX + "\n[PRE-SCAN SUMMARY]\n" + Style.RESET_ALL)
                print(Fore.GREEN + "Determined target: {}\nCase comment: {}\n".format(short_domain, case_comment) + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + "[SCANNING PROCESS]\n" + Style.RESET_ALL)
                spinner_thread = ProgressBar()
                spinner_thread.start()
                try:
                    pdf_rc.create_report(short_domain, url, case_comment)
                finally:
                    spinner_thread.do_run = False
                    spinner_thread.join()

    elif choice == "2":
        cli.print_settings_menu()
        choice_settings = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_settings == '1':
            with open('dorkslist.txt', 'r') as cfg_file:
                print(Fore.LIGHTMAGENTA_EX + '\n[START OF CONFIG FILE]' + Style.RESET_ALL)
                print('\n' + Fore.LIGHTBLUE_EX + cfg_file.read() + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + '\n[END OF CONFIG FILE]\n' + Style.RESET_ALL)
                continue
        elif choice_settings == '2':
            with open('dorkslist.txt', 'a+') as cfg_file:
                print(Fore.LIGHTMAGENTA_EX + '\n[START OF CONFIG FILE]' + Style.RESET_ALL)
                cfg_file.seek(0)
                print('\n' + Fore.LIGHTBLUE_EX + cfg_file.read() + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + '\n[END OF CONFIG FILE]\n' + Style.RESET_ALL)
                new_line = str(input(Fore.YELLOW + "Input new dork >> ") + Style.RESET_ALL)
                print(Fore.GREEN + "New dork successfully added to dorks list" + Style.RESET_ALL)
                cfg_file.write(new_line + '\n')
                continue
        elif choice_settings == '3':
            continue
        break

    elif choice == "3":
        cli.print_help_menu()
        choice_help = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_help == '1':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/How-to-correctly-input-your-targets-address-in-DPULSE')
        elif choice_help == '2':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-interface-colors-meaning')
        elif choice_help == '3':
            continue

    elif choice == "4":
        cli.print_db_menu()
        print('\n')
        db.db_creation('report_storage.db')
        print('\n')
        choice_db = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_db == '1':
            db.db_select()
        elif choice_db == "2":
            if db.db_select() is None:
                pass
            else:
                print(Fore.LIGHTMAGENTA_EX + "\n[DATABASE'S CONTENT]\n" + Style.RESET_ALL)
                cursor, sqlite_connection = db.db_select()
                id_to_extract = int(input(Fore.YELLOW + "\nEnter report ID you want to extract >> "))
                extracted_folder_name = 'report_recreated_ID#{}'.format(id_to_extract)
                try:
                    os.makedirs(extracted_folder_name)
                    db.db_report_recreate(extracted_folder_name, id_to_extract)
                except FileExistsError:
                    print(Fore.RED + "Folder with the same name alredy exists. Delete it or just check it's content" + Style.RESET_ALL)
                    pass
        elif choice_db == "3":
            print(Fore.GREEN + "\nDatabase connection is successfully closed")
            continue
    elif choice == "5":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
