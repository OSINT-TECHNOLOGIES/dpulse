"""
Program start point

You can call this script from your system terminal: python dpulse.py
"""

import sys
sys.path.append('modules')

import report_creation as rc
import cli_init

try:
    import time
    from colorama import Fore, Style, Back
    import webbrowser
    import sqlite3
    import os
except ImportError:
    print(Fore.RED + "[Error #001 - Import error] Can't import some requirements that are necessary to start DPULSE. Please check that all necessary requirements are installed!" + Style.RESET_ALL)
    sys.exit()

cli = cli_init.Menu()
progress_bar = cli_init.ProgressBar()

cli.welcome_menu()

def change_setting(filename):
    cfg_context = open(filename).read()
    print(Fore.LIGHTMAGENTA_EX + '\n[START OF CONFIG FILE]' + Style.RESET_ALL)
    print('\n' + Fore.LIGHTBLUE_EX + cfg_context + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + '[END OF CONFIG FILE]\n' + Style.RESET_ALL)
    setting = input(Fore.YELLOW + 'Enter setting to change >> ')
    new_value = input(Fore.YELLOW + 'Enter new value >> ')

    with open(filename, 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith(setting + ':'):
                lines[i] = f'{setting}: {new_value}\n'
        file.seek(0)
        file.writelines(lines)
        print('\n')
        print(Fore.GREEN + 'Setting {} successfully changed to {}'.format(setting, new_value))

def db_connect():
    sqlite_connection = sqlite3.connect('report_storage.db')
    cursor = sqlite_connection.cursor()
    return cursor, sqlite_connection

while True:
    cli.print_main_menu()
    choice = input(Fore.YELLOW + "Enter your choice >> ")
    print('\n')
    if choice == "1":
        short_domain = str(input(Fore.YELLOW + "Enter target's domain name >> "))
        url = "http://" + short_domain + "/"
        dorking_results_amount = int(input(Fore.YELLOW + 'Enter amount of printed Google Dorking results >> '))
        case_comment = str(input(Fore.YELLOW + "Enter case comment (or enter - if you don't need comment to the case) >> "))
        print(Fore.LIGHTMAGENTA_EX + "\n/// SUMMARY ///\n" + Style.RESET_ALL)
        print(Fore.GREEN + "Determined target: {}\nDetermined amount of Google Dorking results: {}\nCase comment: {}\n".format(short_domain, dorking_results_amount, case_comment) + Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + "/// SCANNING PROCESS ///\n" + Style.RESET_ALL)
        spinner_thread = progress_bar
        spinner_thread.start()
        try:
            rc.create_report(short_domain, url, dorking_results_amount, case_comment)
        finally:
            spinner_thread.do_run = False
            spinner_thread.join()
        print(Fore.LIGHTMAGENTA_EX + "\n/// SCANNING PROCESS END ///\n" + Style.RESET_ALL)
    elif choice == "2":
        cli.print_settings_menu()
        choice_settings = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_settings == '1':
            with open('config.txt', 'r') as cfg_file:
                print(Fore.LIGHTMAGENTA_EX + '\n[START OF CONFIG FILE]' + Style.RESET_ALL)
                print('\n' + Fore.LIGHTBLUE_EX + cfg_file.read() + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + '\n[END OF CONFIG FILE]\n' + Style.RESET_ALL)
                continue
        elif choice_settings == '2':
            change_setting('config.txt')
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
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-config-parameters-and-their-meanings')
        elif choice_help == '3':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-interface-colors-meaning')
        elif choice_help == '4':
            webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-report-storage-database')
        elif choice_help == '5':
            continue

    elif choice == "4":
        cli.print_db_menu()
        db_path = "report_storage.db"
        if not os.path.exists(db_path):
            print(Fore.RED + "Report storage database was not found. DPULSE will create it in a second")
            cursor, sqlite_connection = db_connect()
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

        cursor, sqlite_connection = db_connect()
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
                print(Fore.RED + "[Error #002 - Sqlite3 error] Failed to see storage database's details", error)
        elif choice_db == '2':
            try:
                select_query = "SELECT creation_date, target, id, comment FROM report_storage;"
                cursor.execute(select_query)
                records = cursor.fetchall()
                print(Fore.LIGHTMAGENTA_EX + "\n[DATABASE'S CONTENT]" + Style.RESET_ALL)
                for row in records:
                    print(Fore.LIGHTBLUE_EX + f"Case ID: {row[2]} | Case creation date: {row[0]} | Case name: {row[1]} | Case comment: {row[3]}" + Style.RESET_ALL)
            except sqlite3.Error as error:
                print(Fore.RED + "[Error #002 - Sqlite3 error] Failed to see storage database's content", error)
        elif choice_db == "3":
            print(Fore.LIGHTMAGENTA_EX + "\n[DATABASE'S CONTENT]" + Style.RESET_ALL)
            select_query = "SELECT creation_date, target, id, comment FROM report_storage;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            for row in records:
                print(Fore.LIGHTBLUE_EX + f"Case ID: {row[2]} | Case creation date: {row[0]} | Case name: {row[1]} | Case comment: {row[3]}" + Style.RESET_ALL)
            id_to_extract = int(input(Fore.YELLOW + "Enter report ID you want to extract >> "))
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
                print(Fore.GREEN + "Database connection is successfully closed")
            continue
    elif choice == "5":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
