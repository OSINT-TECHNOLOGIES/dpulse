import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup
import re
import os

def sitemap_inspection(report_folder):
    if os.path.exists(report_folder + '//03-sitemap_links.txt'):
        try:
            accessed_links_counter = 0
            print(Fore.GREEN + "Trying to access sitemap_links.txt file" + Style.RESET_ALL)
            with open(report_folder + '//03-sitemap_links.txt', "r") as file:
                links = file.readlines()
            print(Fore.GREEN + "Reading file and forming links list" + Style.RESET_ALL)
            ps_docs_path = report_folder + '//sitemap_inspection'
            if not os.path.exists(ps_docs_path):
                os.makedirs(ps_docs_path)
            total_emails = []
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            links = [link.strip() for link in links]
            total_links_counter = len(links)
            for url in links:
                response = requests.get(url)
                if response.status_code == 200:
                    accessed_links_counter += 1
                    soup = BeautifulSoup(response.content, 'html.parser')
                    emails = re.findall(email_pattern, soup.text)
                    total_emails.append(emails)

                print(Fore.GREEN + f"  Inspecting links: " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"Link #{accessed_links_counter}" + Style.RESET_ALL, end="\r")

            ds_emails_list = [x for x in total_emails if x]
            ds_emails_cleaned = [', '.join(sublist) for sublist in ds_emails_list]
            ds_emails_return = list(set(ds_emails_cleaned))
            print(Fore.GREEN + "PageSearch Sitemap Inspection successfully ended\n")
            print(Fore.LIGHTGREEN_EX + "-------------------------------------------------")
            print(Fore.GREEN + f"\nDuring PageSearch Sitemap Inspection process:\n[+] Total {total_links_counter} links were checked")
            print(Fore.GREEN + f"[+] Among them, {accessed_links_counter} links were accessible")
            print(Fore.GREEN + f"[+] In result, {len(ds_emails_return)} unique e-mail addresses were found")
            with open(ps_docs_path + "//inspection_logs.txt", "w") as si_logs:
                si_logs.write('# THIS IS PAGESEARCH SITEMAP INSPECTION LOGS' + '\n')
                si_logs.write('# HERE YOU CAN FIND INFO THAT WAS DISCOVERED DURING SITEMAP INSPECTION PROCESS' + '\n' * 3)
                si_logs.write(f'[+] LINKS: Received {total_links_counter} links. Amount of accessible links: {accessed_links_counter}' + '\n')
                si_logs.write(f'[+] EMAILS: Returned and stored in PDF/XLSX report. Total {len(ds_emails_return)} unique emails found' + '\n')
            return ds_emails_return, total_links_counter, accessed_links_counter, len(ds_emails_return)
        except FileNotFoundError:
            print(Fore.RED + f"Cannot start PageSearch in Sitemap Inspection mode because sitemap_links.txt file doesn't exist" + Style.RESET_ALL)
            return 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered'
    else:
        print(Fore.RED + f"Cannot start PageSearch in Sitemap Inspection mode because sitemap_links.txt file doesn't exist" + Style.RESET_ALL)
        return 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered', 'PageSearch Sitemap Inspection was not started because sitemap_links.txt file was not gathered'

