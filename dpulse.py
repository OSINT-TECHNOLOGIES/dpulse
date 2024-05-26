"""
Program start point

You can call this script from your system terminal: python dpulse.py
"""

import sys
sys.path.append('modules')

import pdf_report_creation as pdf_rc
import cli_init

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
def db_connect():
    sqlite_connection = sqlite3.connect('report_storage.db')
    cursor = sqlite_connection.cursor()
    return cursor, sqlite_connection

def db_interaction(db_path):
    if not os.path.exists(db_path):
        print(Fore.RED + "Report storage database was not found. DPULSE will create it in a second" + Style.RESET_ALL)
        cursor, sqlite_connection = db_connect()
        create_table_sql = """
        CREATE TABLE "report_storage" (
            "id" INTEGER NOT NULL UNIQUE,
            "report_content" BLOB NOT NULL,
            "comment" TEXT NOT NULL,
            "target" TEXT NOT NULL,
            "creation_date" INTEGER NOT NULL,
            "dorks_results" TEXT,
            "robots_text" TEXT,
            "sitemap_text" TEXT,
            "sitemap_file" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        cursor.execute(create_table_sql)
        sqlite_connection.commit()
        sqlite_connection.close()
        print(Fore.GREEN + "Successfully created report storage database" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "Report storage database exists" + Style.RESET_ALL)

while True:
    cli.print_main_menu()
    choice = input(Fore.YELLOW + "Enter your choice >> ")
    print('\n')
    if choice == "1":
        db_path = "report_storage.db"
        db_interaction(db_path)
        short_domain = str(input(Fore.YELLOW + "\nEnter target's domain name >> "))
        url = "http://" + short_domain + "/"
        case_comment = str(input(Fore.YELLOW + "Enter case comment (or enter - if you don't need comment to the case) >> "))
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
        print(Fore.LIGHTMAGENTA_EX + "\n[SCANNING PROCESS END]\n" + Style.RESET_ALL)

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
            with open('config.txt', 'a+') as cfg_file:
                print(Fore.LIGHTMAGENTA_EX + '\n[START OF CONFIG FILE]' + Style.RESET_ALL)
                cfg_file.seek(0)
                print('\n' + Fore.LIGHTBLUE_EX + cfg_file.read() + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + '\n[END OF CONFIG FILE]\n' + Style.RESET_ALL)
                new_line = str(input(Fore.YELLOW + "Input new dork >> ") + Style.RESET_ALL)
                print(Fore.GREEN + "New dork successfully added to config.txt" + Style.RESET_ALL)
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
        db_path = "report_storage.db"
        db_interaction(db_path)
        cursor, sqlite_connection = db_connect()
        print(Fore.GREEN + "Connected to report storage database\n")
        choice_db = input(Fore.YELLOW + "Enter your choice >> ")
        if choice_db == '1':
            try:
                select_query = "SELECT creation_date, target, id, comment, dorks_results, robots_text, sitemap_text, sitemap_file FROM report_storage;"
                cursor.execute(select_query)
                records = cursor.fetchall()
                for row in records:
                    dorks_presence = robots_presence = sitemap_presence = "None"
                    if len(row[4]) > 1:
                        dorks_presence = "In DB"
                    if len(row[5]) > 1:
                        robots_presence = "In DB"
                    if len(row[6]) > 1:
                        sitemap_presence = "In DB"
                    print(Fore.LIGHTBLUE_EX + f"Case ID: {row[2]} | Case comment: {row[3]} | Case creation date: {row[0]} | Case name: {row[1]} | Dorks: {dorks_presence} | robots.txt: {robots_presence} | sitemap.xml: {sitemap_presence}" + Style.RESET_ALL)
            except sqlite3.Error as e:
                print(Fore.RED + "Failed to see storage database's content. Reason: {}".format(e))
        elif choice_db == "2":
            print(Fore.LIGHTMAGENTA_EX + "\n[DATABASE'S CONTENT]" + Style.RESET_ALL)
            select_query = "SELECT creation_date, target, id, comment, dorks_results, robots_text, sitemap_text, sitemap_file FROM report_storage;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            for row in records:
                dorks_presence = robots_presence = sitemap_presence = "None"
                if len(row[4]) > 1:
                    dorks_presence = "In DB"
                if len(row[5]) > 1:
                    robots_presence = "In DB"
                if len(row[6]) > 1:
                    sitemap_presence = "In DB"
                print(Fore.LIGHTBLUE_EX + f"Case ID: {row[2]} | Case comment: {row[3]} | Case creation date: {row[0]} | Case name: {row[1]} | Dorks: {dorks_presence} | robots.txt: {robots_presence} | sitemap.xml: {sitemap_presence}" + Style.RESET_ALL)
            id_to_extract = int(input(Fore.YELLOW + "Enter report ID you want to extract >> "))
            extracted_folder_name = 'report_recreated_ID#{}'.format(id_to_extract)
            os.makedirs(extracted_folder_name)
            cursor.execute("SELECT report_content FROM report_storage WHERE id=?", (id_to_extract,))
            pdf_blob = cursor.fetchone()
            if pdf_blob is not None:
                blob_data = pdf_blob[0]
                with open(extracted_folder_name + '//report_extracted.pdf', 'wb') as file:
                    file.write(blob_data)
            cursor.execute("SELECT dorks_results FROM report_storage WHERE id=?", (id_to_extract,))
            dorks_results = (cursor.fetchone())[0]
            with open(extracted_folder_name + '//dorks_extracted.txt', 'w') as file:
                file.write(dorks_results)
            cursor.execute("SELECT robots_text FROM report_storage WHERE id=?", (id_to_extract,))
            robots_results = (cursor.fetchone())[0]
            with open(extracted_folder_name + '//robots_extracted.txt', 'w') as file:
                file.write(robots_results)
            cursor.execute("SELECT sitemap_file FROM report_storage WHERE id=?", (id_to_extract,))
            sitemap_results = (cursor.fetchone())[0]
            with open(extracted_folder_name + '//sitemap_extracted.txt', 'w') as file:
                file.write(sitemap_results)
            cursor.execute("SELECT sitemap_text FROM report_storage WHERE id=?", (id_to_extract,))
            sitemap_links_results = (cursor.fetchone())[0]
            with open(extracted_folder_name + '//sitemap_links_extracted.txt', 'w') as file:
                file.write(sitemap_links_results)
            print(Fore.GREEN + "Report was successfully recreated from report storage database and saved in {} folder".format(extracted_folder_name))
        elif choice_db == "3":
            if sqlite_connection:
                sqlite_connection.close()
                print(Fore.GREEN + "Database connection is successfully closed")
            continue
    elif choice == "5":
        print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter an existing menu item" + Style.RESET_ALL)
