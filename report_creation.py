"""
report_creation module

Contains the function to collect all the outputs from crawl_processor functions and compile them into PDF report

Arguments:
short_domain: website address (-sd value) which you enter in console
url: http://short_domain/
n: -ra amount that you which you enter in console
"""

from datetime import datetime
import jinja2
import pdfkit
import os
import sys
import crawl_processor as cp
from colorama import Fore, Style

def find_wkhtmltopdf():
    """
    Function which will find wkhtmltopdf executionable file
    """
    root_directory = os.getcwd()
    filename = 'wkhtmltopdf.exe'
    for root, dirs, files in os.walk(root_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

try:
    current_script = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script)
    file_path = os.path.join(current_directory, find_wkhtmltopdf())
    print(Fore.GREEN + 'WKHTMLTOPDF was found at {}'.format(file_path))
except TypeError:
    print(Fore.RED + 'WKHTMLTOPDF was not found in DPULSE root directory. Download and install it in your DPULSE folder and retry scan' + Style.RESET_ALL)
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
def create_report(short_domain, url, n):
    """
    Functions which calls all the functions from crawl_processor module and compiles them into PDF report.
    PDF report will be saved in main script directory
    """
    print(Fore.GREEN + 'Processing WHOIS scanning' + Style.RESET_ALL)
    res = cp.whois_gather(short_domain)
    print(Fore.GREEN + 'Processing subdomain gathering' + Style.RESET_ALL)
    subdomains, subdomains_amount = cp.subdomains_gather(url, short_domain)
    print(Fore.GREEN + 'Processing social medias gathering' + Style.RESET_ALL)
    social_medias = cp.sm_gather(url)
    print(Fore.GREEN + 'Processing subdomain analysis' + Style.RESET_ALL)
    subdomain_mails, sd_socials, subdomain_ip = cp.domains_reverse_research(subdomains)
    if n > 0:
        print(Fore.GREEN + 'Processing Google Dorking' + Style.RESET_ALL)
    elif n == 0:
        print(Fore.RED + 'DPULSE will skip Google Dorking because user set the amount of resulst as 0' + Style.RESET_ALL)
    exp_docs, linkedin, related_pages = cp.dorking_processing(short_domain, num_results=n, lang="en", sleep_interval=0, timeout=5)

    ctime = datetime.now().strftime('%Y-%m-%d, %Hh%Mm%Ss')
    casename = short_domain.replace(".", "") + '~' + ctime + '.pdf'

    context = {'sh_domain': short_domain, 'full_url': url, 'ip_address': cp.ip_gather(short_domain),'registrar': res['registrar'],
                        'creation_date': res['creation_date'],'expiration_date': res['expiration_date'],
                        'name_servers': ', '.join(res['name_servers']),'org': res['org'],
                        'mails': cp.mail_gather(url), 'subdomain_mails': subdomain_mails, 'subdomain_socials': social_medias,
                        'subdomain_ip': subdomain_ip, 'fb_links_s': ', '.join(sd_socials['Facebook']), 'inst_links_s': ', '.join(sd_socials['Instagram']), 'tw_links_s': ', '.join(sd_socials['Twitter']),
                        'tg_links_s': ', '.join(sd_socials['Telegram']), 'tt_links_s': ', '.join(sd_socials['TikTok']),
                        'li_links_s': ', '.join(sd_socials['LinkedIn']), 'vk_links_s': ', '.join(sd_socials['VKontakte']), 'yt_links_s': ', '.join(sd_socials['YouTube']),
                        'subdomains': ', '.join(subdomains), 'fb_links': ', '.join(social_medias['Facebook']),
                        'tw_links': ', '.join(social_medias['Twitter']), 'inst_links': ', '.join(social_medias['Instagram']),
                        'tg_links': ', '.join(social_medias['Telegram']), 'tt_links': ', '.join(social_medias['TikTok']),
                        'li_links': ', '.join(social_medias['LinkedIn']), 'vk_links': ', '.join(social_medias['VKontakte']),
                        'yt_links': ', '.join(social_medias['YouTube']), 'exp_docs': exp_docs, 'linkedin': linkedin, 'related_pages': related_pages,
                         'ctime': ctime, 'a_tsf': subdomains_amount, 'a_gdr': n}

    print(Fore.GREEN + 'Processing report for {} case...'.format(short_domain) + Style.RESET_ALL)

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('report_template.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf=file_path)
    pdfkit.from_string(output_text, casename, configuration=config, options=report_encoding_config())
    print(Fore.GREEN + "Report for {} case was created at {}".format(''.join(short_domain), ctime) + Style.RESET_ALL)
