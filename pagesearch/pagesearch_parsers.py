import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style
import os
def subdomains_parser(subdomains_list, report_folder):
    ps_docs_path = report_folder + '//ps_documents'
    if not os.path.exists(ps_docs_path):
        os.makedirs(ps_docs_path)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    counter = 1
    for url in subdomains_list:
        try:
            response = requests.get('http://' + url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            emails = re.findall(email_pattern, soup.text)
            print(Fore.GREEN + f"Page URL: {url}" + Style.RESET_ALL)
            print(Fore.GREEN + f"Page title: {title}" + Style.RESET_ALL)
            print(Fore.GREEN + f"Founded e-mails: {', '.join(emails)}" + Style.RESET_ALL)
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    #print(f"Found link: {href}")  # Debugging line
                    if href.lower().endswith(('.docx', '.xlsx', '.csv', '.pdf', '.pptx', '.doc', '.ppt', '.xls', '.rtf')):
                        document_url = 'http://' + url + href
                        print(Fore.GREEN + f"Found document: {document_url}" + Style.RESET_ALL)
                        response = requests.get(document_url)
                        if response.status_code == 200:
                            if href and href.lower().endswith(('.docx')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.docx")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.xlsx')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.xlsx")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.pdf')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.pdf")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.csv')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.csv")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.pptx')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.pptx")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.doc')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.doc")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.ppt')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.ppt")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.xls')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.xls")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                            elif href and href.lower().endswith(('.rtf')):
                                filename = os.path.basename(href)
                                extracted_path = os.path.join(ps_docs_path, f"extracted_{counter}_{os.path.splitext(filename)[0]}.rtf")
                                with open(extracted_path, 'wb') as file:
                                    file.write(response.content)
                                print(Fore.GREEN + f"File {filename} was successfully saved")
                        else:
                            print(Fore.RED + "Error" + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX + "-------------------------------------------------")
        except Exception as e:
            print(Fore.RED + "Error {}".format(e) + Style.RESET_ALL)
            pass
