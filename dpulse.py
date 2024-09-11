import sys
sys.path.append('datagather_modules')
sys.path.append('service')
sys.path.append('reporting_modules')

import pdf_report_creation as pdf_rc
import cli_init
import db_processing as db
import xlsx_report_creation as xlsx_rc
import html_report_creation as html_rc
from data_assembler import DataProcessing

try:
    import time
    from colorama import Fore, Style, Back
    import webbrowser
    import sqlite3
    import os
    import itertools
    import threading
    from time import sleep, time
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

cli = cli_init.Menu()
cli.welcome_menu()
data_processing = DataProcessing()

def time_processing(end):
    if end < 60:
        endtime = round(end)
        endtime_string = f'approximately {endtime} seconds'
    else:
        time_minutes = round(end / 60)
        if time_minutes == 1:
            endtime_string = f'approximately {time_minutes} minute'
        else:
            endtime_string = f'approximately {time_minutes} minutes'
    return endtime_string

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

def run():
    while True:
        try:
            cli.print_main_menu()
            choice = input(Fore.YELLOW + "Enter your choice >> ")
            if choice == "1":
                while True:
                    short_domain = input(Fore.YELLOW + "\nEnter target's domain name (or 'back' to return to the menu) >> ")
                    if short_domain.lower() == "back":
                        print(Fore.RED + "\nReturned to main menu")
                        break
                    else:
                        if not short_domain:
                            print(Fore.RED + "\nEmpty domain names are not supported")
                        else:
                            url = "http://" + short_domain + "/"
                            case_comment = input(Fore.YELLOW + "Enter case comment >> ")
                            report_filetype = input(Fore.YELLOW + "Enter report file extension [xlsx/pdf/html] >> ")
                            if not report_filetype:
                                print(Fore.RED + "\nReport filetype cannot be empty")
                            if report_filetype.lower() not in ['pdf', 'xlsx', 'html']:
                                print(Fore.RED + '\nYou need to choose between PDF, XLSX or HTML report file types')
                            else:
                                print(Fore.GREEN + "[!] SI mode suppose you to have sitemap_links.txt file in report folder [!]\n[!] It'll visit every link from this file [!]")
                                pagesearch_flag = input(Fore.YELLOW + "Would you like to use PageSearch function? [Y/N/SI] >> ")
                                if pagesearch_flag.lower() == 'y':
                                    keywords_input = input(Fore.YELLOW + "Enter keywords (separate by comma) to search in files during PageSearch process (or write None if you don't need it) >> ")
                                    if keywords_input.lower() != "none":
                                        if len(keywords_input.lower()) > 0:
                                            keywords_list = [keyword.strip() for keyword in keywords_input.split(',')]
                                            keywords_flag = 1
                                        else:
                                            print(Fore.RED + "\nThis field must contain at least one keyword")
                                            break
                                    elif keywords_input.lower() == "none":
                                        keywords_list = None
                                        keywords_flag = 0
                                elif pagesearch_flag.lower() == 'n':
                                    keywords_flag = 0
                                elif pagesearch_flag.lower() == 'si':
                                    keywords_list = None
                                    keywords_flag = 0
                                if report_filetype.lower() == 'pdf' or report_filetype.lower() == 'xlsx' or report_filetype.lower() == 'html':
                                    if pagesearch_flag.lower() == 'y' or pagesearch_flag.lower() == 'n' or pagesearch_flag.lower() == 'si':
                                        if pagesearch_flag.lower() == "n":
                                            pagesearch_ui_mark = 'No'
                                        elif pagesearch_flag.lower() == 'y' and keywords_flag == 1:
                                            pagesearch_ui_mark = f'Yes, with {keywords_list} keywords search'
                                        elif pagesearch_flag.lower() == 'si':
                                            pagesearch_ui_mark = 'Yes, in Sitemap Inspection mode'
                                        else:
                                            pagesearch_ui_mark = 'Yes, without keywords search'
                                        print(Fore.LIGHTMAGENTA_EX + "\n[PRE-SCAN SUMMARY]\n" + Style.RESET_ALL)
                                        print(Fore.GREEN + "Determined target: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + short_domain + Style.RESET_ALL)
                                        print(Fore.GREEN + "Report type: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + report_filetype.lower() + Style.RESET_ALL)
                                        print(Fore.GREEN + "PageSearch conduction: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + pagesearch_ui_mark + Style.RESET_ALL)
                                        print(Fore.GREEN + "Case comment: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + case_comment + Style.RESET_ALL + "\n")
                                        print(Fore.LIGHTMAGENTA_EX + "[BASIC SCAN START]\n" + Style.RESET_ALL)
                                        spinner_thread = ProgressBar()
                                        spinner_thread.start()
                                        if report_filetype.lower() == 'pdf':
                                            try:
                                                if pagesearch_flag.lower() == 'y':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag)
                                                    end = time() - start
                                                endtime_string = time_processing(end)
                                                pdf_rc.report_assembling(short_domain, url, case_comment, data_array, report_info_array, pagesearch_ui_mark, pagesearch_flag.lower(), endtime_string)
                                            finally:
                                                spinner_thread.do_run = False
                                                spinner_thread.join()
                                        elif report_filetype.lower() == 'xlsx':
                                            try:
                                                if pagesearch_flag.lower() == 'y':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag)
                                                    end = time() - start
                                                endtime_string = time_processing(end)
                                                xlsx_rc.create_report(short_domain, url, case_comment, data_array, report_info_array, pagesearch_ui_mark, pagesearch_flag.lower(), endtime_string)
                                            finally:
                                                spinner_thread.do_run = False
                                                spinner_thread.join()
                                        elif report_filetype.lower() == 'html':
                                            try:
                                                if pagesearch_flag.lower() == 'y':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag)
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag)
                                                    end = time() - start
                                                endtime_string = time_processing(end)
                                                html_rc.report_assembling(short_domain, url, case_comment, data_array, report_info_array, pagesearch_ui_mark, pagesearch_flag.lower(), endtime_string)
                                            finally:
                                                spinner_thread.do_run = False
                                                spinner_thread.join()
                                    else:
                                        print(Fore.RED + "\nUnsupported PageSearch mode. Please choose between Y, N or SI")

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
                else:
                    print(Fore.RED + "\nInvalid menu item. Please select between existing menu items")

            elif choice == "3":
                cli.print_help_menu()
                choice_help = input(Fore.YELLOW + "Enter your choice >> ")
                if choice_help == '1':
                    webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse')
                elif choice_help == '2':
                    webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-WIKI')
                elif choice_help == '3':
                    webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/How-to-correctly-input-your-targets-address-in-DPULSE')
                elif choice_help == '4':
                    webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-PageSearch-function-guide')
                elif choice_help == '5':
                    webbrowser.open('https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-report-storage-database')
                elif choice_help == '6':
                    continue
                else:
                    print(Fore.RED + "\nInvalid menu item. Please select between existing menu items")

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
                        db.db_select()
                        id_to_extract = int(input(Fore.YELLOW + "\nEnter report ID you want to extract >> "))
                        extracted_folder_name = 'report_recreated_ID#{}'.format(id_to_extract)
                        try:
                            os.makedirs(extracted_folder_name)
                            db.db_report_recreate(extracted_folder_name, id_to_extract)
                        except FileExistsError:
                            print(Fore.RED + "Folder with the same name already exists. Delete it or just check it's content" + Style.RESET_ALL)
                            pass
                elif choice_db == "3":
                    print(Fore.GREEN + "\nDatabase connection is successfully closed")
                    continue
            elif choice == "5":
                print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "\nInvalid menu item. Please select between existing menu items")
        except KeyboardInterrupt:
            print(Fore.RED + "\nDPULSE process was ended using keyboard" + Style.RESET_ALL)
            sys.exit()

if __name__ == "__main__":
    run()
