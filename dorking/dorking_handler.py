import sys
from random import random

sys.path.append('service')
from logs_processing import logging
from ua_rotator import user_agent_rotator
from proxies_rotator import proxies_rotator

import random
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config_processing import read_config

try:
    import requests.exceptions
    from colorama import Fore, Style
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

def solid_google_dorking(query, proxy_flag, proxies_list, pages=1):
    result_query = []
    request_count = 0
    try:
        config_values = read_config()
        options = uc.ChromeOptions()
        options.binary_location = r"{}".format(config_values['dorking_browser'])
        dorking_browser_mode = config_values['dorking_browser_mode']
        if dorking_browser_mode.lower() == 'headless':
            options.add_argument("--headless=new")
        elif dorking_browser_mode.lower() == 'nonheadless':
            pass
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument(f"user-agent={user_agent_rotator.get_random_user_agent()}")
        if proxy_flag == 1:
            proxy = proxies_rotator.get_random_proxy(proxies_list)
            options.add_argument(f'--proxy-server={proxy["http"]}')
        driver = uc.Chrome(options=options)
        for page in range(pages):
            try:
                driver.get("https://www.google.com")
                time.sleep(random.uniform(2, 4))
                try:
                    accepted = False
                    try:
                        accept_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Принять все") or contains(text(), "Accept all")]')
                        driver.execute_script("arguments[0].click();", accept_btn)
                        print(Fore.GREEN + 'Pressed "Accept all" button!' + Style.RESET_ALL)
                        accepted = True
                        time.sleep(random.uniform(2, 3))
                    except:
                        pass
                    if not accepted:
                        iframes = driver.find_elements(By.TAG_NAME, "iframe")
                        for iframe in iframes:
                            driver.switch_to.frame(iframe)
                            try:
                                accept_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Принять все") or contains(text(), "Accept all")]')
                                driver.execute_script("arguments[0].click();", accept_btn)
                                print(Fore.GREEN + 'Pressed "Accept all" button!' + Style.RESET_ALL)
                                accepted = True
                                driver.switch_to.default_content()
                                time.sleep(random.uniform(2, 3))
                                break
                            except:
                                driver.switch_to.default_content()
                                continue
                        driver.switch_to.default_content()
                    if not accepted:
                        print(Fore.GREEN + "Google TOS button was not found. Seems good..." + Style.RESET_ALL)
                except Exception:
                    print(Fore.RED + f'Error with pressing "Accept all" button. Closing...' + Style.RESET_ALL)
                    driver.save_screenshot("consent_error.png")
                    driver.switch_to.default_content()
                search_box = driver.find_element(By.NAME, "q")
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.2))
                time.sleep(random.uniform(0.5, 1.2))
                search_box.send_keys(Keys.RETURN)
                time.sleep(random.uniform(2.5, 4))
                links = driver.find_elements(By.CSS_SELECTOR, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and href.startswith('http') and 'google.' not in href and 'webcache.googleusercontent.com' not in href:
                        result_query.append(href)
                        request_count += 1
                try:
                    next_button = driver.find_element(By.ID, 'pnnext')
                    next_button.click()
                    time.sleep(random.uniform(2, 3))
                except:
                    break
            except Exception as e:
                logging.error(f'DORKING PROCESSING (SELENIUM): ERROR. REASON: {e}')
                continue
        driver.quit()
        if len(result_query) >= 2:
            del result_query[-2:]
        return result_query
    except Exception as e:
        logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')
        print(Fore.RED + "Error while running Selenium dorking. See journal for details." + Style.RESET_ALL)
        return []

def save_results_to_txt(folderpath, table, queries, pages=1):
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
                    results = solid_google_dorking(query, proxy_flag, proxies_list, pages)
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
