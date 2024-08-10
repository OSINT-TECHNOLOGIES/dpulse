import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style
import os
import fitz

def extract_text_from_pdf(filename: str) -> str:
    try:
        doc = fitz.open(filename=filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(Fore.RED + f"Can't open some PDF file. Reason: {e}" + Style.RESET_ALL)
        pass

def find_keywords_in_pdfs(ps_docs_path, keywords: list) -> dict:
    try:
        pdf_files = [f for f in os.listdir(ps_docs_path) if f.lower().endswith(".pdf")]
        results = {}
        for pdf_file in pdf_files:
            pdf_path = os.path.join(ps_docs_path, pdf_file)
            extracted_text = extract_text_from_pdf(pdf_path)
            for keyword in keywords:
                if keyword.lower() in extracted_text.lower():
                    if pdf_file not in results:
                        results[pdf_file] = []
                    results[pdf_file].append(keyword)
        return results
    except Exception as e:
        print(Fore.RED + f"Can't find keywords. Reason: {e}")
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
        for pdfs in bad_pdfs:
            os.remove(os.path.join(ps_docs_path, pdfs))
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
    for url in subdomains_list:
        try:
            response = requests.get('http://' + url)
            if response.status_code == 200:
                accessible_subdomains += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string
                emails = re.findall(email_pattern, soup.text)
                total_emails.append(emails)
                if not emails:
                    emails = ['None']
                print(Fore.GREEN + "Page URL: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{url}" + Style.RESET_ALL)
                print(Fore.GREEN + "Page title: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{title}" + Style.RESET_ALL)
                print(Fore.GREEN + "Founded e-mails: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(emails)}" + Style.RESET_ALL)
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href:
                        if href.lower().endswith(('.docx', '.xlsx', '.csv', '.pdf', '.pptx', '.doc', '.ppt', '.xls', '.rtf')):
                            document_url = 'http://' + url + href
                            print(Fore.GREEN + "Found document: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{document_url}" + Style.RESET_ALL)
                            response = requests.get(document_url)
                            if response.status_code == 200:
                                if href and href.lower().endswith(('.docx')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.docx")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.xlsx')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.xlsx")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.pdf')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.pdf")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.csv')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.csv")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.pptx')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.pptx")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.doc')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.doc")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.ppt')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.ppt")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.xls')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.xls")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.json')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.json")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                                elif href and href.lower().endswith(('.txt')):
                                    filename = os.path.basename(href)
                                    extracted_path = os.path.join(ps_docs_path, f"extracted_{os.path.splitext(filename)[0]}.txt")
                                    with open(extracted_path, 'wb') as file:
                                        file.write(response.content)
                                    files_counter += 1
                                    print(Fore.GREEN + "File was successfully saved")
                print(Fore.LIGHTGREEN_EX + "-------------------------------------------------")
        except Exception as e:
            print(Fore.RED + "File extraction failed. Reason: {}".format(e) + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
            pass
    ps_emails_list = [x for x in total_emails if x]
    ps_emails_return = [', '.join(sublist) for sublist in ps_emails_list]
    clean_bad_pdfs(ps_docs_path)

    if keywords_flag == 1:
        print(Fore.GREEN + "Searching keywords in PDF files..." + Style.RESET_ALL)
        try:
            pdf_results = find_keywords_in_pdfs(ps_docs_path, keywords)
            for pdf_file, found_keywords in pdf_results.items():
                print(Fore.GREEN + f"Keywords " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{', '.join(found_keywords)}" + Style.RESET_ALL + Fore.GREEN + f" found in '{pdf_file}'" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Can't find keywords. Reason: {e}")
    elif keywords_flag == 0:
        print(Fore.RED + "Keywords gathering won't start because of None user input" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + "-------------------------------------------------" + Style.RESET_ALL)
    print(Fore.GREEN + f"\nDuring PageSearch process:\n[+] Total {len(subdomains_list)} subdomains were checked")
    print(Fore.GREEN + f"[+] Among them, {accessible_subdomains} subdomains were accessible")
    print(Fore.GREEN + f"[+] In result, {len(ps_emails_return)} unique e-mail addresses were found")
    print(Fore.GREEN + f"[+] Also, {files_counter} files were extracted")
    return ps_emails_return
