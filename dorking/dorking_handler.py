import sys
import random
import time
import os
import re
import shutil
import subprocess
import logging
from colorama import Fore, Style
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append('service')
from logs_processing import logging
from ua_rotator import user_agent_rotator
from proxies_rotator import proxies_rotator
from config_processing import read_config


GOOGLE_BLOCKED = '__GOOGLE_BLOCKED__'
GOOGLE_BLOCK_WAIT_SECS = 300
GOOGLE_BLOCK_POLL_SECS = 5


def resolve_browser_binary(configured_path):
    if configured_path:
        normalized_path = configured_path.strip()
        if normalized_path and normalized_path.lower() not in {'none', 'path\\to\\browser\\for\\dorking'} and os.path.isfile(normalized_path):
            return normalized_path

    for browser_name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        browser_path = shutil.which(browser_name)
        if browser_path:
            return browser_path

    return None


def resolve_browser_major_version(browser_binary):
    if not browser_binary:
        return None

    try:
        version_output = subprocess.check_output([browser_binary, '--version'], text=True).strip()
    except Exception:
        return None

    version_match = re.search(r'(\d+)\.', version_output)
    if version_match:
        return int(version_match.group(1))

    return None


def is_google_block_page(driver):
    try:
        current_url = (driver.current_url or '').lower()
        page_source = (driver.page_source or '').lower()
    except Exception:
        return False

    return (
        '/sorry/' in current_url
        or 'captcha-form' in page_source
        or 'our systems have detected unusual traffic' in page_source
        or 'detected unusual traffic from your computer network' in page_source
    )


def report_google_block(query):
    logging.warning(f'DORKING PROCESSING: Google block page detected for query: {query}')
    print(Fore.LIGHTYELLOW_EX + 'Google presented a bot-check / CAPTCHA page. Automated dorking was stopped for this run.' + Style.RESET_ALL)
    return GOOGLE_BLOCKED


def handle_google_block(driver, query, dorking_browser_mode):
    if dorking_browser_mode.lower() != 'nonheadless':
        return report_google_block(query)

    logging.warning(f'DORKING PROCESSING: Google block page detected for query in manual mode: {query}')
    print(Fore.LIGHTYELLOW_EX + 'Google presented a bot-check / CAPTCHA page.' + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'Solve it in the opened browser window. DPULSE will keep the browser open and resume automatically.' + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + f'Waiting up to {GOOGLE_BLOCK_WAIT_SECS} seconds. Press Ctrl+C to cancel dorking.' + Style.RESET_ALL)

    deadline = time.time() + GOOGLE_BLOCK_WAIT_SECS
    while time.time() < deadline:
        time.sleep(GOOGLE_BLOCK_POLL_SECS)
        try:
            if not is_google_block_page(driver):
                print(Fore.GREEN + 'Google challenge cleared. Resuming dorking...' + Style.RESET_ALL)
                return None
        except Exception:
            return report_google_block(query)

        remaining_seconds = max(0, int(deadline - time.time()))
        print(Fore.LIGHTYELLOW_EX + f'Google challenge is still active. Waiting... ({remaining_seconds}s remaining)' + Style.RESET_ALL)

    print(Fore.LIGHTYELLOW_EX + 'Timed out while waiting for the Google challenge to be solved.' + Style.RESET_ALL)
    return report_google_block(query)

def proxy_transfer():
    proxy_flag, proxies_list = proxies_rotator.get_proxies()
    if proxy_flag == 0:
        pass
        return proxy_flag, ""
    else:
        working_proxies = proxies_rotator.check_proxies(proxies_list)
        return proxy_flag, working_proxies


def create_dorking_driver(proxy_flag, proxies_list):
    config_values = read_config()
    options = uc.ChromeOptions()
    browser_binary = resolve_browser_binary(config_values['dorking_browser'])
    browser_major_version = resolve_browser_major_version(browser_binary)
    if browser_binary:
        options.binary_location = browser_binary
    dorking_browser_mode = config_values['dorking_browser_mode']
    if dorking_browser_mode.lower() == 'headless':
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument(f"user-agent={user_agent_rotator.get_random_user_agent()}")
    if proxy_flag == 1:
        proxy = proxies_rotator.get_random_proxy(proxies_list)
        options.add_argument(f'--proxy-server={proxy["http"]}')
    chrome_kwargs = {'options': options}
    if browser_binary:
        chrome_kwargs['browser_executable_path'] = browser_binary
    if browser_major_version:
        chrome_kwargs['version_main'] = browser_major_version
    return uc.Chrome(**chrome_kwargs), dorking_browser_mode

def solid_google_dorking(query, proxy_flag, proxies_list, pages=1, driver=None, dorking_browser_mode=None):
    result_query = []
    request_count = 0
    own_driver = driver is None
    try:
        if own_driver:
            driver, dorking_browser_mode = create_dorking_driver(proxy_flag, proxies_list)
        for page in range(pages):
            try:
                driver.get("https://www.google.com")
                time.sleep(random.uniform(2, 4))
                if is_google_block_page(driver):
                    block_result = handle_google_block(driver, query, dorking_browser_mode)
                    if block_result == GOOGLE_BLOCKED:
                        return block_result
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
                if is_google_block_page(driver):
                    block_result = handle_google_block(driver, query, dorking_browser_mode)
                    if block_result == GOOGLE_BLOCKED:
                        return block_result
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
        if len(result_query) >= 2:
            del result_query[-2:]
        return result_query
    except Exception as e:
        logging.error(f'DORKING PROCESSING: ERROR. REASON: {e}')
        print(Fore.RED + "Error while running Selenium dorking. See journal for details." + Style.RESET_ALL)
        return []
    finally:
        if own_driver and driver:
            driver.quit()

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
            driver, dorking_browser_mode = create_dorking_driver(proxy_flag, proxies_list)
            dorked_query_counter = 0
            try:
                for i, query in enumerate(queries, start=1):
                    f.write(f"QUERY #{i}: {query}\n")
                    try:
                        results = solid_google_dorking(query, proxy_flag, proxies_list, pages, driver=driver, dorking_browser_mode=dorking_browser_mode)
                        if results == GOOGLE_BLOCKED:
                            f.write("=> GOOGLE BLOCK PAGE DETECTED. AUTOMATED DORKING STOPPED\n")
                            total_results.append((query, 'blocked'))
                            f.write("\n")
                            break
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
            finally:
                driver.quit()
        print(Fore.GREEN + "\nGoogle Dorking end. Results successfully saved in HTML report\n" + Style.RESET_ALL)
        print(Fore.GREEN + f"During Google Dorking with {table.upper()}:")
        for query, count in total_results:
            if count == 'blocked':
                print(Fore.GREEN + f"[+] Google blocked automated dorking at query " + Fore.LIGHTCYAN_EX + f'{query}' + Fore.GREEN + '. ' + Fore.LIGHTYELLOW_EX + 'Scan stopped before continuing through the remaining dorks.' + Style.RESET_ALL)
            elif count == 0:
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
    driver, dorking_browser_mode = create_dorking_driver(proxy_flag, proxies_list)
    dorked_query_counter = 0
    total_dorks_amount = len(queries)
    dorking_return_list = []
    try:
        for i, query in enumerate(queries, start=1):
            dorking_return_list.append(f"QUERY #{i}: {query}\n")
            results = solid_google_dorking(query, proxy_flag, proxies_list, pages, driver=driver, dorking_browser_mode=dorking_browser_mode)
            if results == GOOGLE_BLOCKED:
                dorking_return_list.append("GOOGLE BLOCK PAGE DETECTED. AUTOMATED DORKING STOPPED\n")
                dorking_return_list.append("\n")
                break
            if not results:
                dorking_return_list.append("NO RESULT FOUND\n")
            else:
                for result in results:
                    dorking_return_list.append(f"{result}\n")
            dorked_query_counter += 1
            dorking_return_list.append("\n")
            print(Fore.GREEN + f"  Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{dorked_query_counter}/{total_dorks_amount}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL, end="\r")
    finally:
        driver.quit()
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
