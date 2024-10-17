import sys
sys.path.append('datagather_modules')
sys.path.append('service')
sys.path.append('reporting_modules')
sys.path.append('dorking')

from colorama import Fore, Style, Back
import cli_init
from config_processing import create_config, check_cfg_presence, read_config, print_and_return_config
import db_processing as db
import os

db.db_creation('report_storage.db')
cfg_presence = check_cfg_presence()
if cfg_presence is True:
    print(Fore.GREEN + "Global config file presence: OK" + Style.RESET_ALL)
else:
    print(Fore.RED + "Global config file presence: NOT OK")
    create_config()
    print(Fore.GREEN + "Successfully generated global config file")

from dorking_handler import dorks_files_check, get_columns_amount
dorks_files_check()
import pdf_report_creation as pdf_rc
import xlsx_report_creation as xlsx_rc
import html_report_creation as html_rc
from data_assembler import DataProcessing
from misc import time_processing, domain_precheck

try:
    import socket
    import re
    import time
    import webbrowser
    import sqlite3
    import itertools
    import threading
    from time import sleep, time
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

data_processing = DataProcessing()
config_values = read_config()

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

def run():
    while True:
        try:
            cli.print_main_menu()
            domain_patter = r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
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
                        elif re.match(domain_patter, short_domain) is None:
                            print(Fore.RED + '\nYour string does not match domain pattern')
                        else:
                            url = "http://" + short_domain + "/"
                            print(Fore.GREEN + 'Pinging domain...' + Style.RESET_ALL, end = ' ')
                            if domain_precheck(short_domain):
                                print(Fore.GREEN + 'Entered domain is accessible. Continuation' + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "Entered domain is not accessible. Scan is impossible" + Style.RESET_ALL)
                                break
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
                                    dorking_flag = input(Fore.YELLOW + "Select Dorking mode [Basic/IoT/Files/Admins/Web/Custom/None] >> ")
                                    #api_flag = input(Fore.YELLOW + "Would you like to use 3rd party API in scan? [Y/N] >> ")
                                    #if api_flag.lower() == 'y':
                                        #print api db content
                                        #write ID which you want to use using comma (ex: 1,3,4)
                                    #elif api_flag.lower() == 'n':
                                        #pass
                                    #else:
                                        #print invalid mode
                                    if pagesearch_flag.lower() == 'y' or pagesearch_flag.lower() == 'n' or pagesearch_flag.lower() == 'si':
                                        if pagesearch_flag.lower() == "n":
                                            pagesearch_ui_mark = 'No'
                                        elif pagesearch_flag.lower() == 'y' and keywords_flag == 1:
                                            pagesearch_ui_mark = f'Yes, with {keywords_list} keywords search'
                                        elif pagesearch_flag.lower() == 'si':
                                            pagesearch_ui_mark = 'Yes, in Sitemap Inspection mode'
                                        else:
                                            pagesearch_ui_mark = 'Yes, without keywords search'
                                        if dorking_flag.lower() not in ['basic', 'iot', 'none', 'admins', 'files', 'web', 'custom']:
                                            print(Fore.RED + "\nInvalid Dorking mode. Please select mode among Basic/IoT/Files/Web/Admins/Custom or None")
                                            break
                                        else:
                                            dorking_ui_mark = 'No'
                                            if dorking_flag.lower() in ('basic', 'iot', 'files', 'admins', 'web'):
                                                db_name = {
                                                    'basic': 'basic_dorking.db',
                                                    'iot': 'iot_dorking.db',
                                                    'files': 'files_dorking.db',
                                                    'admins': 'adminpanels_dorking.db',
                                                    'web': 'webstructure_dorking.db'}[dorking_flag.lower()]
                                                row_count = get_columns_amount(f'dorking//{db_name}', f'{dorking_flag.lower()}_dorks')
                                                dorking_ui_mark = f'Yes, {dorking_flag.lower().replace("_", " ")} dorking ({row_count} dorks)'
                                            elif dorking_flag.lower() == 'custom':
                                                custom_db_name = str(input(
                                                    Fore.YELLOW + "Enter your custom Dorking DB name (without any file extensions) >> "))
                                                row_count = get_columns_amount(f'dorking//{custom_db_name}.db', 'dorks')
                                                dorking_ui_mark = f'Yes, Custom table dorking ({row_count} dorks)'
                                                dorking_flag = str(dorking_flag.lower() + f"+{custom_db_name}.db")
                                        print(Fore.LIGHTMAGENTA_EX + "\n[PRE-SCAN SUMMARY]\n" + Style.RESET_ALL)
                                        print(Fore.GREEN + "Determined target: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + short_domain + Style.RESET_ALL)
                                        print(Fore.GREEN + "Report type: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + report_filetype.lower() + Style.RESET_ALL)
                                        print(Fore.GREEN + "PageSearch conduction: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + pagesearch_ui_mark + Style.RESET_ALL)
                                        print(Fore.GREEN + "Dorking conduction: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + dorking_ui_mark + Style.RESET_ALL)
                                        print(Fore.GREEN + "Case comment: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + case_comment + Style.RESET_ALL + "\n")
                                        print(Fore.LIGHTMAGENTA_EX + "[BASIC SCAN START]\n" + Style.RESET_ALL)
                                        spinner_thread = ProgressBar()
                                        spinner_thread.start()
                                        if report_filetype.lower() == 'pdf':
                                            try:
                                                if pagesearch_flag.lower() == 'y':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag, dorking_flag.lower())
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
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag, dorking_flag.lower())
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
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                elif pagesearch_flag.lower() == 'si':
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), keywords_list, keywords_flag, dorking_flag.lower())
                                                    end = time() - start
                                                else:
                                                    start = time()
                                                    data_array, report_info_array = data_processing.data_gathering(short_domain, url, report_filetype.lower(), pagesearch_flag.lower(), '', keywords_flag, str(dorking_flag.lower()))
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
                    import configparser
                    config = print_and_return_config()
                elif choice_settings == '2':
                    import configparser
                    config = print_and_return_config()
                    section = input(Fore.YELLOW + "Enter the section you want to update >> ")
                    option = input(Fore.YELLOW + "Enter the option you want to update >> ")
                    value = input(Fore.YELLOW + "Enter the new value >> ")
                    if not config.has_section(section):
                        config.add_section(section)
                    config.set(section, option, value)
                    with open('service//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.GREEN + "Configuration updated successfully" + Style.RESET_ALL)
                elif choice_settings == '4':
                    with open('journal.log', 'w'):
                        print(Fore.GREEN + "Journal file was successfully cleared" + Style.RESET_ALL)
                        pass
                elif choice_settings == '5':
                    continue
            elif choice == '3':
                cli.dorking_db_manager()
                choice_dorking = input(Fore.YELLOW + "Enter your choice >> ")
                if choice_dorking == '1':
                    from db_creator import manage_dorks
                    print('\n')
                    print(Fore.GREEN + "You've entered custom Dorking DB generator!\n" + Style.RESET_ALL)
                    print(Fore.GREEN + "Remember some rules in order to successfully create your custom Dorking DB:" + Style.RESET_ALL)
                    print(Fore.GREEN + "[1] - dork_id variable must be unique, starting with 1 and then +1 every new dork" + Style.RESET_ALL)
                    print(Fore.GREEN + "[2] - When it comes to define domain in dork, put {} in it\n" + Style.RESET_ALL)
                    print(Fore.GREEN + "Examples: related:{}, site:{} inurl:login and so on\n" + Style.RESET_ALL)
                    ddb_name = input(Fore.YELLOW + "Enter a name for your custom Dorking DB (without any extensions) >> ")
                    manage_dorks(ddb_name)
                elif choice_dorking == '2':
                    continue
            elif choice == "6":
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
                            print(Fore.RED + "Report with the same recreated folder already exists. Please check its content or delete it and try again" + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + "Error appeared when trying to recreate report from DB. See journal for details" + Style.RESET_ALL)

                elif choice_db == "3":
                    print(Fore.GREEN + "\nDatabase connection is successfully closed")
                    continue
            elif choice == "7":
                print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "\nInvalid menu item. Please select between existing menu items")
        except KeyboardInterrupt:
            print(Fore.RED + "\nDPULSE process was ended using keyboard" + Style.RESET_ALL)
            sys.exit()

if __name__ == "__main__":
    run()
