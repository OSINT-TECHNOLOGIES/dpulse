"""
report_creation module

Contains the function to collect all the outputs from crawl_processor functions and compile them into PDF report

Arguments:
short_domain: domain name of certain website
url: http://short_domain/
"""

import crawl_processor as cp
import dorking_processor as dp

try:
    import requests
    from datetime import datetime
    import jinja2
    import pdfkit
    import os
    import sys
    from colorama import Fore, Style
    import webbrowser
    import sqlite3
except ImportError:
    print(Fore.RED + "[Error #001 - Import error] Can't import some requirements that are necessary to start DPULSE. Please check that all necessary requirements are installed!" + Style.RESET_ALL)
    sys.exit()
def insert_pdf(file):
    with open(file, 'rb') as pdf_file:
        blob_data = pdf_file.read()
        return blob_data
def insert_blob(pdf_blob, db_casename, creation_date, case_comment):
    try:
        sqlite_connection = sqlite3.connect('report_storage.db')
        cursor = sqlite_connection.cursor()
        print(Fore.GREEN + "Connected to report storage database")

        sqlite_insert_blob_query = """INSERT INTO report_storage
                                  (report_content, creation_date, target, comment) VALUES (?, ?, ?, ?)"""

        data_tuple = (pdf_blob, creation_date, db_casename, case_comment)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print(Fore.GREEN + "Scanning results are successfully saved in report storage database")
        cursor.close()
    except sqlite3.Error as error:
        print(Fore.RED + "[Error #002 - Sqlite3 error] Failed to insert scanning results in report storage database", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print(Fore.GREEN + "Database connection is successfully closed")

def find_files(filename):
    """
    Function which will find wkhtmltopdf executable file
    """
    root_directory = os.getcwd()
    for root, dirs, files in os.walk(root_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_config(cfg_string_name):
    """
    Function which reads config parameters using separator
    """
    with open("config.txt", 'r') as file:
        for line in file:
            if line.startswith(cfg_string_name):
                cfg_parameter = int(line.split(':')[1].strip())
                return cfg_parameter

try:
    current_script = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script)
    file_path = os.path.join(current_directory, find_files('wkhtmltopdf.exe'))
    print(Fore.GREEN + 'WKHTMLTOPDF was found at {}'.format(file_path))
except TypeError:
    print(Fore.RED + 'WKHTMLTOPDF was not found in DPULSE root directory. Download and install it in your DPULSE folder and retry scan' + Style.RESET_ALL)
    ask_whktmltopdf_install = input(Fore.YELLOW + "Would you like to open WKHTMLTOPDF page and download it? [Y/N] >> ")
    if ask_whktmltopdf_install == 'Y':
        print(Fore.GREEN + 'Opening WKHTMLTOPDF page in your browser. DPULSE will be closed' + Style.RESET_ALL)
        webbrowser.open('https://wkhtmltopdf.org/downloads.html')
        print(Fore.RED + 'Exiting the program...' + Style.RESET_ALL)
        sys.exit()
    elif ask_whktmltopdf_install == 'N':
        print(Fore.RED + 'Exiting the program...' + Style.RESET_ALL)
        sys.exit()

try:
    current_script = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script)
    cfg_file_path = os.path.join(current_directory, find_files('config.txt'))
    print(Fore.GREEN + 'Main config file was found at {}'.format(cfg_file_path))
except TypeError:
    print(Fore.RED + '[Error #003 - No CFG error] Main config file was not found in DPULSE root directory.' + Style.RESET_ALL)
    sys.exit()

short_domain = ''
def report_encoding_config():
    """
    Function which sets some configurations for PDF report file
    """
    return {
        'encoding': 'UTF-8',
        'enable-local-file-access': True
    }

search_query = []
def create_report(short_domain, url, dorking_result_amount, case_comment):
    """
    Functions which calls all the functions from crawl_processor module and compiles them into PDF report.
    PDF report will be saved in main script directory
    """
    try:
        sleep_interval = read_config('sleep-interval:')
        timeout = read_config('timeout:')
        print(Fore.GREEN + 'Processing WHOIS scanning' + Style.RESET_ALL)
        res = cp.whois_gather(short_domain)
        print(Fore.GREEN + 'Processing subdomain gathering' + Style.RESET_ALL)
        subdomains, subdomains_amount = cp.subdomains_gather(url, short_domain)
        print(Fore.GREEN + 'Processing social medias gathering' + Style.RESET_ALL)
        social_medias = cp.sm_gather(url)
        print(Fore.GREEN + 'Processing subdomain analysis' + Style.RESET_ALL)
        subdomain_mails, sd_socials, subdomain_ip = cp.domains_reverse_research(subdomains)
        if dorking_result_amount > 0:
            print(Fore.GREEN + 'Processing Google Dorking' + Style.RESET_ALL)
            exp_docs, linkedin, databases = dp.solid_google_dorking(short_domain, sleep_interval, dorking_result_amount)
        elif dorking_result_amount == 0:
            print(Fore.RED + 'DPULSE will skip Google Dorking because user set the amount of results as 0' + Style.RESET_ALL)
            exp_docs = linkedin = databases = "Skipped because user set Google Dorking results amount to 0"

        ctime = datetime.now().strftime('%Y-%m-%d, %Hh%Mm%Ss')
        casename = short_domain.replace(".", "") + '~' + ctime + '.pdf'
        db_casename = short_domain.replace(".", "")
        now = datetime.now()
        db_creation_date = str(now.year) + str(now.month) + str(now.day)

        context = {'sh_domain': short_domain, 'full_url': url, 'ip_address': cp.ip_gather(short_domain),'registrar': res['registrar'],
                                'creation_date': res['creation_date'],'expiration_date': res['expiration_date'],
                                'name_servers': ', '.join(res['name_servers']),'org': res['org'],
                                'mails': cp.mail_gather(url), 'subdomain_mails': subdomain_mails, 'subdomain_socials': social_medias,
                                'subdomain_ip': subdomain_ip, 'fb_links_s': ', '.join(sd_socials['Facebook']), 'inst_links_s': ', '.join(sd_socials['Instagram']), 'tw_links_s': ', '.join(sd_socials['Twitter']),
                                'tg_links_s': ', '.join(sd_socials['Telegram']), 'tt_links_s': ', '.join(sd_socials['TikTok']),
                                'li_links_s': ', '.join(sd_socials['LinkedIn']), 'vk_links_s': ', '.join(sd_socials['VKontakte']), 'yt_links_s': ', '.join(sd_socials['YouTube']),
                                'wc_links_s': ', '.join(sd_socials['WeChat']), 'ok_links_s': ', '.join(sd_socials['Odnoklassniki']),
                                'subdomains': ', '.join(subdomains), 'fb_links': ', '.join(social_medias['Facebook']),
                                'tw_links': ', '.join(social_medias['Twitter']), 'inst_links': ', '.join(social_medias['Instagram']),
                                'tg_links': ', '.join(social_medias['Telegram']), 'tt_links': ', '.join(social_medias['TikTok']),
                                'li_links': ', '.join(social_medias['LinkedIn']), 'vk_links': ', '.join(social_medias['VKontakte']),
                                'yt_links': ', '.join(social_medias['YouTube']), 'wc_links': ', '.join(social_medias['WeChat']),
                                'ok_links': ', '.join(social_medias['Odnoklassniki']), 'exp_docs': exp_docs, 'linkedin': linkedin,
                                'exp_db': databases, 'ctime': ctime, 'a_tsf': subdomains_amount, 'a_gdr': dorking_result_amount}

        print(Fore.GREEN + 'Processing report for {} case...'.format(short_domain) + Style.RESET_ALL)

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template('report_template.html')
        output_text = template.render(context)
        config = pdfkit.configuration(wkhtmltopdf=file_path)
        pdfkit.from_string(output_text, casename, configuration=config, options=report_encoding_config())
        print(Fore.GREEN + "Report for {} case was created at {}".format(''.join(short_domain), ctime) + Style.RESET_ALL)
        insert_blob(insert_pdf(casename), db_casename, db_creation_date, case_comment)
    except:
        print(Fore.RED + '[Error #005 - Report creation error] Unable to create PDF report. Closing scan...')
