import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style
import os
import fitz
import sys
sys.path.append('service')
from logs_processing import logging
from cli_init import print_ps_cli_report

def extract_text_from_pdf(filename: str) -> str:
    try:
        logging.info('TEXT EXTRACTION FROM PDF (PAGESEARCH): OK')
        doc = fitz.open(filename=filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(Fore.RED + f"Can't open some PDF file. See journal for details" + Style.RESET_ALL)
        logging.error(f'TEXT EXTRACTION FROM PDF (PAGESEARCH): ERROR. REASON: {e}')
        pass

def find_keywords_in_pdfs(ps_docs_path, keywords: list) -> dict:
    try:
        logging.info('KEYWORDS SEARCH IN PDF (PAGESEARCH): OK')
        pdf_files = [f for f in os.listdir(ps_docs_path) if f.lower().endswith(".pdf")]
        results = {}
        pdf_with_keywords = 0
        for pdf_file in pdf_files:
            pdf_path = os.path.join(ps_docs_path, pdf_file)
            extracted_text = extract_text_from_pdf(pdf_path)
            for keyword in keywords:
                if keyword.lower() in extracted_text.lower():
                    if pdf_file not in results:
                        results[pdf_file] = []
                    results[pdf_file].append(keyword)
                    pdf_with_keywords += 1
        return results, pdf_with_keywords
    except Exception as e:
        print(Fore.RED + f"Can't find keywords. See journal for details")
        logging.error(f'KEYWORDS SEARCH IN PDF (PAGESEARCH): ERROR. REASON: {e}')
        pass

def clean_bad_pdfs(ps_docs_path):
    pdf_files = [f for f in os.listdir(ps_docs_path) if f.lower().endswith(".pdf")]
    bad_pdfs = []
    for pdf_file in pdf_files:
        try:
            full_path = os.path.join(ps_docs_path, pdf_file)
            fitz.open(filename=full_path)
        except Exception:
            bad_pdfs.append(pdf_file)
            pass
    if len(bad_pdfs) > 0:
        corrupted_pdfs_counter = 0
        for pdfs in bad_pdfs:
            os.remove(os.path.join(ps_docs_path, pdfs))
            corrupted_pdfs_counter += 1
        print(Fore.GREEN + f"Found {corrupted_pdfs_counter} corrupted PDF files. Deleting...")
    else:
        print(Fore.GREEN + "Corrupted PDF files were not found" + Style.RESET_ALL)

def subdomains_parser(subdomains_list, report_folder, keywords, keywords_flag):
    ps_docs_path = report_folder + '//ps_documents'
    if not os.path.exists(ps_docs_path):
        os.makedirs(ps_docs_path)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    total_emails = []
    accessible_subdomains = 0
    files_counter = 0
    website_elements_counter = 0
    exposed_passwords_counter = 0
    api_keys_counter = 0
    cookies_counter = 0

    for url in subdomains_list:
        try:
            logging.info('ACCESSING SUBDOMAIN (PAGESEARCH): OK')
            response = requests.get('http://' + url)
            if response.status_code == 200:
                accessible_subdomains += 1
                soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(Fore.RED + "Can't access some subdomain. See journal for details")
            logging.error(f'ACCESSING SUBDOMAIN (PAGESEARCH): ERROR. REASON: {e}')
            pass

        try:
            logging.info('WEB RESOURCE ADDITIONAL INFO GATHERING (PAGESEARCH): OK')
            title = soup.title.string
            emails = re.findall(email_pattern, soup.text)
            total_emails.append(emails)
            if not emails:
                emails = ['None']
            hidden_inputs = soup.find_all(type='hidden')
            search_query_input = soup.find('input', {'name': 'q'})
            customization_input = soup.find('input', {'name': 'language'})
            passwords = soup.find_all('input', {'type': 'password'})
            print(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
            print(Fore.GREEN + "Page URL: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{url}" + Style.RESET_ALL)
            print(Fore.GREEN + "Page title: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{title}" + Style.RESET_ALL)
            print(Fore.GREEN + "Found e-mails: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(emails)}" + Style.RESET_ALL)

            if customization_input and customization_input.get('value') is not None and len(customization_input.get('value')) > 0:
                print(Fore.GREEN + "Found site customization setting: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{customization_input.get('value')}" + Style.RESET_ALL)
                website_elements_counter += 1
            if search_query_input and search_query_input.get('value') is not None and len(search_query_input.get('value')) > 0:
                print(Fore.GREEN + "Found search query: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{search_query_input.get('value')}" + Style.RESET_ALL)
                website_elements_counter += 1
            for hidden_input in hidden_inputs:
                if hidden_input is not None and hidden_input.get('value') is not None and len(hidden_input.get('value')) > 0:
                    print(Fore.GREEN + "Found hidden form data: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{hidden_input.get('value')}" + Style.RESET_ALL)
                    website_elements_counter += 1
            for password in passwords:
                if password is not None and password.get('value') is not None and len(password.get('value')) > 0:
                    print(Fore.GREEN + "Found exposed password: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{password.get('value')}" + Style.RESET_ALL)
                    exposed_passwords_counter += 1

            api_keys = soup.find_all('input', attrs={'type': 'apikey'})
            for key in api_keys:
                key_value = key.get('value')
                print(Fore.GREEN + f"Found API Key: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{key_value}")
                api_keys_counter += 1

            cookies_dict = response.cookies
            for cookie_name, cookie_value in cookies_dict.items():
                print(Fore.GREEN + "Found cookie: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookie_name}. " + Style.RESET_ALL + Fore.GREEN + "Value: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookie_value}" + Style.RESET_ALL)
                cookies_counter += 1
        except Exception as e:
            print(Fore.RED + "Error while getting detailed info on web resource. See journal for details")
            logging.error(f'WEB RESOURCE ADDITIONAL INFO GATHERING (PAGESEARCH): ERROR. REASON: {e}')
            pass

        try:
            logging.info('FILES EXTRACTION (PAGESEARCH): OK')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    if href.lower().endswith(('.docx', '.xlsx', '.csv', '.pdf', '.pptx', '.doc', '.ppt', '.xls', '.rtf', '.conf', '.config', '.db', '.sql', '.json', '.txt')):
                        document_url = 'http://' + url + href
                        print(Fore.GREEN + "Found document: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{document_url}" + Style.RESET_ALL)
                        response = requests.get(document_url)
                        file_extensions = {
                            '.docx': 'extracted_{}.docx',
                            '.xlsx': 'extracted_{}.xlsx',
                            '.pdf': 'extracted_{}.pdf',
                            '.csv': 'extracted_{}.csv',
                            '.pptx': 'extracted_{}.pptx',
                            '.doc': 'extracted_{}.doc',
                            '.ppt': 'extracted_{}.ppt',
                            '.xls': 'extracted_{}.xls',
                            '.json': 'extracted_{}.json',
                            '.txt': 'extracted_{}.txt',
                            '.sql': 'extracted_{}.sql',
                            '.db': 'extracted_{}.db',
                            '.config': 'extracted_{}.config',
                            '.conf': 'extracted_{}.conf'
                        }
                        if response.status_code == 200:
                            if href:
                                file_extension = os.path.splitext(href.lower())[1]
                                if file_extension in file_extensions:
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, file_extensions[file_extension].format(
                                        os.path.splitext(filename)[0]))
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
        except Exception as e:
            print(Fore.RED + "This file can't be accessed to extract it. See journal for details")
            logging.error(f'FILES EXTRACTION (PAGESEARCH): ERROR. REASON: {e}')
            pass

    ps_emails_list = [x for x in total_emails if x]
    ps_emails_return = [', '.join(sublist) for sublist in ps_emails_list]

    clean_bad_pdfs(ps_docs_path)
    keywords_messages_list = []
    if keywords_flag == 1:
        print(Fore.GREEN + "Searching keywords in PDF files..." + Style.RESET_ALL)
        try:
            pdf_results, pdf_with_keywords = find_keywords_in_pdfs(ps_docs_path, keywords)
            for pdf_file, found_keywords in pdf_results.items():
                print(Fore.GREEN + f"Keywords " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(found_keywords)}" + Style.RESET_ALL + Fore.GREEN + f" found in '{pdf_file}'" + Style.RESET_ALL)
                keywords_messages_list.append(f"Keywords {', '.join(found_keywords)} found in '{pdf_file}'")
        except Exception as e:
            print(Fore.RED + f"Can't find keywords. See journal for details")
            logging.error(f'KEYWORDS SEARCH IN PDF (PAGESEARCH): ERROR. REASON: {e}')
            pdf_with_keywords = 0
    print_ps_cli_report(subdomains_list, accessible_subdomains, ps_emails_return, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter)

    if keywords_flag == 0:
        print(Fore.RED + "[+] Keywords were not gathered because of None user input")
        return ps_emails_return, accessible_subdomains, len(ps_emails_return), files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, ['No keywords were found because of None user input']
    else:
        print(Fore.GREEN + f"[+] Total {pdf_with_keywords} keywords were found in PDF files")
        return ps_emails_return, accessible_subdomains, len(ps_emails_return), files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list
