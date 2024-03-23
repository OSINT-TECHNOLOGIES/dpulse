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
    import sqlite3
    import os
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
print(Fore.BLUE + Back.WHITE + 'HEARTBEAT // version: 0.5b' + Style.RESET_ALL)
print(Fore.BLUE + Back.WHITE + 'Developed by: OSINT-TECHNOLOGIES (https://github.com/OSINT-TECHNOLOGIES)' + Style.RESET_ALL + '\n\n')

def print_main_menu():
    print('\n')
    print(Fore.BLUE + '[MAIN MENU]')
    print(Fore.GREEN + "1. Determine target and start scan")
    print(Fore.GREEN + "2. Settings")
    print(Fore.GREEN + "3. Help")
    print(Fore.GREEN + "4. Manage report storage database")
    print(Fore.RED + "5. Exit DPULSE" + Style.RESET_ALL + '\n')
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

def print_db_menu():
    print(Fore.BLUE + '[DATABASE MENU]')
    print(Fore.GREEN + "1. Show database information")
    print(Fore.GREEN + "2. Show database content")
    print(Fore.GREEN + "3. Recreate report from database")
    print(Fore.RED + "4. Return to main menu" + Style.RESET_ALL + '\n')

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
        case_comment = str(input(Fore.YELLOW + "Enter case comment (or enter - if you don't need comment to the case) >> "))
        print(Fore.GREEN + 'Determined target >> {}\nShow {} Google Dorking result'.format(short_domain, dorking_results_amount) + Style.RESET_ALL)
        spinner_thread = ProgressBar()
        spinner_thread.start()
        try:
            rc.create_report(short_domain, url, dorking_results_amount, case_comment)
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
        print_db_menu()
        db_path = "report_storage.db"
        if not os.path.exists(db_path):
            print(Fore.RED + "Report storage database was not found. DPULSE will create it in a second")
            sqlite_connection = sqlite3.connect('report_storage.db')
            cursor = sqlite_connection.cursor()
            create_table_sql = """
            CREATE TABLE "report_storage" (
                "id" INTEGER NOT NULL UNIQUE,
                "report_content" BLOB NOT NULL,
                "comment" TEXT NOT NULL,
                "target" TEXT NOT NULL,
                "creation_date" INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
            cursor.execute(create_table_sql)
            sqlite_connection.commit()
            sqlite_connection.close()
            print(Fore.GREEN + "Successfully created report storage database")
        else:
            print(Fore.GREEN + "Report storage database exists")

        sqlite_connection = sqlite3.connect('report_storage.db')
        cursor = sqlite_connection.cursor()
        print(Fore.GREEN + "Connected to report storage database")
        choice_db = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_db == '1':
            try:
                cursor.execute("PRAGMA table_info(report_storage);")
                info = cursor.fetchall()
                print(Fore.YELLOW + "\n~ DATABASE'S COLUMNS ~" + Style.RESET_ALL)
                for column in info:
                    print(column)
                cursor.close()
            except sqlite3.Error as error:
                print(Fore.RED + "Failed to see storage database's details", error)
        elif choice_db == '2':
            try:
                select_query = "SELECT creation_date, target, id, comment FROM report_storage;"
                cursor.execute(select_query)
                records = cursor.fetchall()
                print(Fore.YELLOW + "\n~ DATABASE'S CONTENT ~" + Style.RESET_ALL)
                for row in records:
                    date = row[0]
                    name = row[1]
                    id = row[2]
                    comment = row[3]
                    print(Fore.BLUE + f"Case ID: {id} | Case creation date: {date} | Case name: {name} | Case comment: {comment}" + Style.RESET_ALL)
            except sqlite3.Error as error:
                print(Fore.RED + "Failed to see storage database's content", error)
        elif choice_db == "3":
            print(Fore.YELLOW + "\n~ DATABASE'S CONTENT ~" + Style.RESET_ALL)
            select_query = "SELECT creation_date, target, id, comment FROM report_storage;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            for row in records:
                date = row[0]
                name = row[1]
                id = row[2]
                comment = row[3]
                print(Fore.BLUE + f"Case ID: {id} | Case creation date: {date} | Case name: {name} | Case comment: {comment}" + Style.RESET_ALL)
            id_to_extract = int(input(Fore.YELLOW + "Enter ID which report you want to extract >> "))
            cursor.execute("SELECT report_content FROM report_storage WHERE id=?", (id_to_extract,))
            result = cursor.fetchone()
            if result is not None:
                blob_data = result[0]
                with open('report_extracted.pdf', 'wb') as file:
                    file.write(blob_data)
            print(Fore.GREEN + "Report was successfully recreated from report storage database as report_extracted.pdf")
        elif choice_db == "4":
            if sqlite_connection:
                sqlite_connection.close()
                print(Fore.RED + "Database connection is closed")
            continue
    elif choice == "5":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
