import os
import re
import sys
import fitz
import requests

from bs4 import BeautifulSoup
from typing import List, Tuple
from colorama import Fore, Style

sys.path.append('service')
from logs_processing import logging
from cli_init import print_ps_cli_report

ansi_re = re.compile(r'\x1b\[[0-9;]*[mK]')

def make_recorder(storage: List[str]):
    def _rec(*parts, sep=" ", end="\n"):
        msg = sep.join(str(p) for p in parts) + end
        print(msg, end="")
        storage.append(ansi_re.sub("", msg))
    return _rec

def extract_text_from_pdf(filename: str) -> str:
    try:
        logging.info('TEXT EXTRACTION FROM PDF (PAGESEARCH): OK')
        doc = fitz.open(filename=filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(Fore.RED + "Can't open some PDF file. See journal for details" + Style.RESET_ALL)
        logging.error(f'TEXT EXTRACTION FROM PDF (PAGESEARCH): ERROR. REASON: {e}')
        return ""

def find_keywords_in_pdfs(ps_docs_path, keywords: List[str]) -> Tuple[dict, int]:
    try:
        logging.info('KEYWORDS SEARCH IN PDF (PAGESEARCH): OK')
        pdf_files = [f for f in os.listdir(ps_docs_path) if f.lower().endswith(".pdf")]
        results, pdf_with_keywords = {}, 0
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
        print(Fore.RED + "Can't find keywords. See journal for details" + Style.RESET_ALL)
        logging.error(f'KEYWORDS SEARCH IN PDF (PAGESEARCH): ERROR. REASON: {e}')
        return {}, 0

def clean_bad_pdfs(ps_docs_path):
    pdf_files = [f for f in os.listdir(ps_docs_path) if f.lower().endswith(".pdf")]
    for pdf_file in pdf_files:
        try:
            fitz.open(filename=os.path.join(ps_docs_path, pdf_file))
        except Exception:
            os.remove(os.path.join(ps_docs_path, pdf_file))

def subdomains_parser(subdomains_list, report_folder, keywords, keywords_flag):
    report_lines: List[str] = []
    p = make_recorder(report_lines)
    print(Fore.GREEN + "Conducting PageSearch. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    ps_docs_path = os.path.join(report_folder, 'ps_documents')
    if not os.path.exists(ps_docs_path):
        os.makedirs(ps_docs_path)

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    total_emails, keywords_messages_list = [], []
    accessible_subdomains = files_counter = website_elements_counter = 0
    exposed_passwords_counter = api_keys_counter = cookies_counter = 0
    tried_subdomains_counter = 0

    for url in subdomains_list:
        try:
            logging.info('ACCESSING SUBDOMAIN (PAGESEARCH): OK')
            response = requests.get('http://' + url)
            tried_subdomains_counter += 1
            if response.status_code == 200:
                accessible_subdomains += 1
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                continue
        except Exception as e:
            print(Fore.RED + "Can't access some subdomain. See journal for details" + Style.RESET_ALL)
            logging.error(f'ACCESSING SUBDOMAIN (PAGESEARCH): ERROR. REASON: {e}')
            continue

        try:
            logging.info('WEB RESOURCE ADDITIONAL INFO GATHERING (PAGESEARCH): OK')
            title = soup.title.string if soup.title else "No title"
            emails = re.findall(email_pattern, soup.text)
            total_emails.append(emails)
            if not emails:
                emails = ['None']
            hidden_inputs = soup.find_all(type='hidden')
            search_query_input = soup.find('input', {'name': 'q'})
            customization_input = soup.find('input', {'name': 'language'})
            passwords = soup.find_all('input', {'type': 'password'})
            p(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
            p(Fore.GREEN + "Page number: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{tried_subdomains_counter}/{len(subdomains_list)}" + Style.RESET_ALL)
            p(Fore.GREEN + "Page URL: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{url}" + Style.RESET_ALL)
            p(Fore.GREEN + "Page title: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{title}" + Style.RESET_ALL)
            p(Fore.GREEN + "Found e-mails: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(emails)}" + Style.RESET_ALL)

            if customization_input and customization_input.get('value'):
                p(Fore.GREEN + "Found site customization setting: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{customization_input.get('value')}" + Style.RESET_ALL)
                website_elements_counter += 1
            if search_query_input and search_query_input.get('value'):
                p(Fore.GREEN + "Found search query: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{search_query_input.get('value')}" + Style.RESET_ALL)
                website_elements_counter += 1
            for hidden_input in hidden_inputs:
                if hidden_input and hidden_input.get('value'):
                    p(Fore.GREEN + "Found hidden form data: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{hidden_input.get('value')}" + Style.RESET_ALL)
                    website_elements_counter += 1
            for password in passwords:
                if password and password.get('value'):
                    p(Fore.GREEN + "Found exposed password: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{password.get('value')}" + Style.RESET_ALL)
                    exposed_passwords_counter += 1
            api_keys = soup.find_all('input', attrs={'type': 'apikey'})
            for key in api_keys:
                key_value = key.get('value')
                p(Fore.GREEN + f"Found API Key: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{key_value}" + Style.RESET_ALL)
                api_keys_counter += 1

            cookies_dict = response.cookies
            for cookie_name, cookie_value in cookies_dict.items():
                p(Fore.GREEN + "Found cookie: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookie_name}. " + Style.RESET_ALL + Fore.GREEN + "Value: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookie_value}" + Style.RESET_ALL)
                cookies_counter += 1
        except Exception as e:
            print(Fore.RED + "Error while getting detailed info on web resource. See journal for details" + Style.RESET_ALL)
            logging.error(f'WEB RESOURCE ADDITIONAL INFO GATHERING (PAGESEARCH): ERROR. REASON: {e}')

        try:
            logging.info('FILES EXTRACTION (PAGESEARCH): OK')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.lower().endswith(('.docx', '.xlsx', '.csv', '.pdf', '.pptx', '.doc', '.ppt', '.xls', '.rtf', '.conf', '.config', '.db', '.sql', '.json', '.txt')):
                    document_url = 'http://' + url + href
                    p(Fore.GREEN + "Found document: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{document_url}" + Style.RESET_ALL)
                    response_doc = requests.get(document_url)
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
                    if response_doc.status_code == 200:
                        file_extension = os.path.splitext(href.lower())[1]
                        if file_extension in file_extensions:
                            filename = os.path.basename(href)
                            extracted_path = os.path.join(ps_docs_path, file_extensions[file_extension].format(os.path.splitext(filename)[0]))
                            with open(extracted_path, 'wb') as file:
                                file.write(response_doc.content)
                            files_counter += 1
                            p(Fore.GREEN + "File was successfully saved" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "This file can't be accessed to extract it. See journal for details" + Style.RESET_ALL)
            logging.error(f'FILES EXTRACTION (PAGESEARCH): ERROR. REASON: {e}')

    p(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
    ps_emails_list = [x for x in total_emails if x]
    ps_emails_return = [', '.join(sublist) for sublist in ps_emails_list]

    clean_bad_pdfs(ps_docs_path)

    pdf_with_keywords = 0
    if keywords_flag == 1:
        print(Fore.GREEN + "Searching keywords in PDF files..." + Style.RESET_ALL)
        pdf_results, pdf_with_keywords = find_keywords_in_pdfs(ps_docs_path, keywords)
        for pdf_file, found_keywords in pdf_results.items():
            p(Fore.GREEN + f"Keywords " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(found_keywords)}" + Style.RESET_ALL + Fore.GREEN + f" found in '{pdf_file}'" + Style.RESET_ALL)
            keywords_messages_list.append(f"Keywords {', '.join(found_keywords)} found in '{pdf_file}'")

    print_ps_cli_report(subdomains_list, accessible_subdomains, ps_emails_return, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter)

    if keywords_flag == 0:
        print(Fore.RED + "[+] Keywords were not gathered because of None user input" + Style.RESET_ALL)
        keywords_messages_list = ['No keywords were found because of None user input']
    else:
        print(Fore.GREEN + f"[+] Total {pdf_with_keywords} keywords were found in PDF files" + Style.RESET_ALL)

    data_tuple = (
        ps_emails_return,
        accessible_subdomains,
        len(ps_emails_return),
        files_counter,
        cookies_counter,
        api_keys_counter,
        website_elements_counter,
        exposed_passwords_counter,
        keywords_messages_list
    )

    exclude = ("Conducting PageSearch", "Searching keywords", "Keywords were not gathered", "Total ")
    pagesearch_query = "\n".join(line for line in report_lines if not line.startswith(exclude))
    return data_tuple, pagesearch_query
