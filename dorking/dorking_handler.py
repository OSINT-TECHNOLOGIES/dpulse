import sys
sys.path.append('service')
from config_processing import read_config
from logs_processing import logging
from ua_rotator import user_agent_rotator
from proxies_rotator import proxies_rotator

try:
    import requests.exceptions
    from colorama import Fore, Style
    import mechanicalsoup
    import re
    import requests
    import sqlite3
    import time
    import os
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

def proxy_transfer():
    proxy_flag, proxies_list = proxies_rotator.get_proxies()
    if proxy_flag == 0:
        pass
        return proxy_flag, ""
    else:
        working_proxies = proxies_rotator.check_proxies(proxies_list)
        return proxy_flag, working_proxies

def solid_google_dorking(query, dorking_delay, delay_step, proxy_flag, proxies_list, pages=100):
    try:
        browser = mechanicalsoup.StatefulBrowser()
        if proxy_flag == 1:
            browser.session.proxies = proxies_rotator.get_random_proxy(proxies_list)
        else:
            pass
        browser.open("https://www.google.com/")
        browser.select_form('form[action="/search"]')
        browser["q"] = str(query)
        browser.submit_selected(btnName="btnG")
        result_query = []
        request_count = 0
        for page in range(pages):
            try:
                for link in browser.links():
                    target = link.attrs['href']
                    if (target.startswith('/url?') and not target.startswith("/url?q=http://webcache.googleusercontent.com")):
                        target = re.sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
                        result_query.append(target)
                        request_count += 1
                        if request_count % delay_step == 0:
                            time.sleep(dorking_delay)
                browser.session.headers['User-Agent'] = user_agent_rotator.get_random_user_agent()
                browser.follow_link(nr=page + 1)
            except mechanicalsoup.LinkNotFoundError:
                break
            except Exception as e:
                logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')
        del result_query[-2:]
        return result_query
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + "Error while establishing connection with domain. No results will appear. See journal for details" + Style.RESET_ALL)
        logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')
    except Exception as e:
        logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')

def save_results_to_txt(folderpath, table, queries, pages=10):
    try:
        config_values = read_config()
        dorking_delay = int(config_values['dorking_delay (secs)'])
        delay_step = int(config_values['delay_step'])
        txt_writepath = folderpath + '//04-dorking_results.txt'
        total_results = []
        total_dorks_amount = len(queries)
        with open(txt_writepath, 'w') as f:
            print(Fore.GREEN + "Started Google Dorking. Please, be patient, it may take some time")
            print(Fore.GREEN + f"{dorking_delay} seconds delay after each {delay_step} dorking requests was configured" + Style.RESET_ALL)
            proxy_flag, proxies_list = proxy_transfer()
            dorked_query_counter = 0
            for i, query in enumerate(queries, start=1):
                f.write(f"QUERY #{i}: {query}\n")
                try:
                    results = solid_google_dorking(query, dorking_delay, delay_step, proxy_flag, proxies_list, pages)
                    if not results:
                        f.write("=> NO RESULT FOUND\n")
                        total_results.append((query, 0))
                    else:
                        total_results.append((query, len(results)))
                        for result in results:
                            f.write(f"=> {result}\n")
                except Exception as e:
                    logging.error(f"DORKING PROCESSING: ERROR. REASON: {e}")
                    total_results.append((query, 0))
                f.write("\n")
                dorked_query_counter += 1
                print(Fore.GREEN + f"  Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{dorked_query_counter}/{total_dorks_amount}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL, end="\r")
        print(Fore.GREEN + "\nGoogle Dorking end. Results successfully saved in HTML report\n" + Style.RESET_ALL)
        print(Fore.GREEN + f"During Google Dorking with {table.upper()}:")
        for query, count in total_results:
            if count == 0:
                count = 'no results'
                print(Fore.GREEN + f"[+] Found results for " + Fore.LIGHTCYAN_EX + f'{query}' + Fore.GREEN + ' query: ' + Fore.LIGHTRED_EX + f'{count}' + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"[+] Found results for " + Fore.LIGHTCYAN_EX + f'{query}' + Fore.GREEN + ' query: ' + Fore.LIGHTCYAN_EX + f'{count}' + Style.RESET_ALL)
        return f'Successfully dorked domain with {table.upper()} dorks table', txt_writepath
    except Exception as e:
        print(Fore.RED + 'Error appeared while trying to dork target. See journal for details')
        logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')
        return 'Domain dorking failed. See journal for details', txt_writepath

def transfer_results_to_xlsx(table, queries, pages=10):
    config_values = read_config()
    dorking_delay = int(config_values['dorking_delay (secs)'])
    delay_step = int(config_values['delay_step'])
    print(Fore.GREEN + "Started Google Dorking. Please, be patient, it may take some time")
    print(Fore.GREEN + f"{dorking_delay} seconds delay after each {delay_step} dorking requests was configured" + Style.RESET_ALL)
    proxy_flag, proxies_list = proxy_transfer()
    dorked_query_counter = 0
    total_dorks_amount = len(queries)
    dorking_return_list = []
    for i, query in enumerate(queries, start=1):
        dorking_return_list.append(f"QUERY #{i}: {query}\n")
        results = solid_google_dorking(query, dorking_delay, delay_step, proxy_flag, proxies_list)
        if not results:
            dorking_return_list.append("NO RESULT FOUND\n")
        else:
            for result in results:
                dorking_return_list.append(f"{result}\n")
        dorked_query_counter += 1
        dorking_return_list.append("\n")
        print(Fore.GREEN + f"  Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{dorked_query_counter}/{total_dorks_amount}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL, end="\r")
    print(Fore.GREEN + "\nGoogle Dorking end. Results successfully saved in XLSX report\n" + Style.RESET_ALL)
    return f'Successfully dorked domain with {table.upper()} dorks table', dorking_return_list

def dorks_files_check():
    dorks_path = 'dorking//'
    dorks_files = ['iot_dorking.db', 'files_dorking.db', 'basic_dorking.db', 'adminpanels_dorking.db', 'webstructure_dorking.db']
    dorks_files_counter = 0
    for dork_files in dorks_files:
        files_path = os.path.join(dorks_path, dork_files)
        if os.path.isfile(files_path):
            dorks_files_counter += 1
        else:
            pass
    if dorks_files_counter == 5:
        print(Fore.GREEN + "Dorks databases presence: OK" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Dorks databases presence: NOT OK\nSome files may not be in folder. Please compare dorking folder with the same folder on the official repository\n" + Style.RESET_ALL)
        sys.exit()
