import sys
sys.path.append('service')
from logs_processing import logging

try:
    import socket
    import whois
    import re
    import requests
    import urllib.parse
    from colorama import Fore, Style
    from urllib.parse import urlparse
    from collections import defaultdict
    from bs4 import BeautifulSoup
    import random
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

def ip_gather(short_domain):
    ip_address = socket.gethostbyname(short_domain)
    return ip_address

def whois_gather(short_domain):
    try:
        logging.info('WHOIS INFO GATHERING: OK')
        w = whois.whois(short_domain)
        if w.org is None:
            w['org'] = 'n/a'
            logging.info('WHOIS INFO GATHERING: OK')
        return w
    except Exception as e:
        print(Fore.RED + "Error while gathering WHOIS information. See journal for details")
        logging.error(f'WHOIS GATHERING: ERROR. REASON: {e}')
        w = {
            'registrar': 'N/A',
            'creation_date': 'N/A',
            'expiration_date': 'N/A',
            'name_servers': ['N/A'],
            'org': 'N/A'
        }
        return w
        pass

def contact_mail_gather(url):
    try:
        logging.info('CONTACT MAIL GATHERING: OK')
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        mails = []
        for i in soup.find_all(href=re.compile("mailto")):
            i.encode().decode()
            mails.append(i.string)
        mails = [mail for mail in mails if mail is not None]
        if (not mails) or (mails is None):
            logging.info('CONTACT MAIL GATHERING: OK (BUT NO MAILS WERE FOUND)')
            return 'No contact e-mails were found'
        else:
            logging.info('CONTACT MAIL GATHERING: OK')
            return ', '.join(map(str, mails))
    except requests.RequestException as e:
        print(Fore.RED + "Error while gathering e-mails. See journal for details")
        logging.error(f'CONTACT MAIL GATHERING: ERROR. REASON: {e}')
        pass

def subdomains_mail_gather(url):
    try:
        logging.info('SUBDOMAINS MAIL GATHERING: OK')
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        mails_uncleaned = []
        for i in soup.find_all(href=re.compile("mailto")):
            i.encode().decode()
            mails_uncleaned.append(i.string)
        mails_cleaned = [item for item in mails_uncleaned if item is not None]
        mails = [''.join(sublist) for sublist in mails_cleaned]
        return mails
    except requests.RequestException as e:
        print(Fore.RED + "Error while gathering e-mails. See journal for details")
        logging.error(f'SUBDOMAINS MAIL GATHERING: ERROR. REASON: {e}')
        pass

def subdomains_gather(url, short_domain):
    try:
        logging.info('SUBDOMAINS GATHERING: OK')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        linked_domains = set()
        for link in soup.find_all('a', href=True):
            domain = urlparse(link['href']).netloc
            if domain and domain != urlparse(url).netloc:
                linked_domains.add(domain)
        finder = short_domain
        subdomains = [urllib.parse.unquote(i) for i in linked_domains if finder in i]
        subdomains_amount = len(subdomains)
        if not subdomains:
            subdomains = ['No subdomains were found']
            logging.info('SUBDOMAINS GATHERING: OK')
        return subdomains, subdomains_amount
    except Exception as e:
        print(Fore.RED + f"Cannot gather subdomains due to error. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS GATHERING: ERROR. REASON: {e}')
        pass

def sm_gather(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    categorized_links = {'Facebook': [], 'Twitter': [], 'Instagram': [],
                         'Telegram': [], 'TikTok': [], 'LinkedIn': [],
                         'VKontakte': [], 'YouTube': [], 'Odnoklassniki': [], 'WeChat': []}

    for link in links:
        if 'facebook.com' in link:
            categorized_links['Facebook'].append(urllib.parse.unquote(link))
        elif 'twitter.com' in link:
            categorized_links['Twitter'].append(urllib.parse.unquote(link))
        elif 'instagram.com' in link:
            categorized_links['Instagram'].append(urllib.parse.unquote(link))
        elif 't.me' in link:
            categorized_links['Telegram'].append(urllib.parse.unquote(link))
        elif 'tiktok.com' in link:
            categorized_links['TikTok'].append(urllib.parse.unquote(link))
        elif 'linkedin.com' in link:
            categorized_links['LinkedIn'].append(urllib.parse.unquote(link))
        elif 'vk.com' in link:
            categorized_links['VKontakte'].append(urllib.parse.unquote(link))
        elif 'youtube.com' in link:
            categorized_links['YouTube'].append(urllib.parse.unquote(link))
        elif 'wechat.com' in link:
            categorized_links['WeChat'].append(urllib.parse.unquote(link))
        elif 'ok.ru' in link:
            categorized_links['Odnoklassniki'].append(urllib.parse.unquote(link))

    if not categorized_links['Odnoklassniki']:
        categorized_links['Odnoklassniki'].append('Odnoklassniki links were not found')
    if not categorized_links['WeChat']:
        categorized_links['WeChat'].append('WeChat links were not found')
    if not categorized_links['YouTube']:
        categorized_links['YouTube'].append('YouTube links were not found')
    if not categorized_links['LinkedIn']:
        categorized_links['LinkedIn'].append('LinkedIn links were not found')
    if not categorized_links['VKontakte']:
        categorized_links['VKontakte'].append('VKontakte links were not found')
    if not categorized_links['TikTok']:
        categorized_links['TikTok'].append('TikTok links were not found')
    if not categorized_links['Telegram']:
        categorized_links['Telegram'].append('Telegram links were not found')
    if not categorized_links['Instagram']:
        categorized_links['Instagram'].append('Instagram links were not found')
    if not categorized_links['Twitter']:
        categorized_links['Twitter'].append('Twitter links were not found')
    if not categorized_links['Facebook']:
        categorized_links['Facebook'].append('Facebook links were not found')

    return categorized_links

def domains_reverse_research(subdomains, report_file_type):
    subdomain_urls = []
    subdomain_mails = []
    subdomain_socials = []
    subdomain_ip = []

    try:
        for subdomain in subdomains:
            subdomain_url = "http://" + subdomain + "/"
            subdomain_urls.append(subdomain_url)
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print(Fore.RED + "Some URL seems unreachable! DPULSE will continue to work, but the URL causing the error won't be included in report. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS URL FORMING: ERROR. REASON: {e}')
        pass

    try:
        for subdomain in subdomains:
            subdomains_ip = ip_gather(subdomain)
            subdomain_ip.append(subdomains_ip)
            subdomain_ip = list(set(subdomain_ip))
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print(Fore.RED + "Some URL seems unreachable! DPULSE will continue to work, but the URL causing the error won't be included in report. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS IP GATHERING: ERROR. REASON: {e}')
        pass

    try:
        for subdomain_url in subdomain_urls:
            subdomain_mail = subdomains_mail_gather(subdomain_url)
            subdomain_mails.append(subdomain_mail)
            subdomain_social = sm_gather(subdomain_url)
            subdomain_socials.append(subdomain_social)
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print(Fore.RED + "Some URL seems unreachable! DPULSE will continue to work, but the URL causing the error won't be included in report. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS MAIL/SOCIALS GATHERING: ERROR. REASON: {e}')
        pass

    subdomain_mails = [sublist for sublist in subdomain_mails if sublist]
    subdomain_mails = [sublist for sublist in subdomain_mails if sublist != [None]]
    subdomain_mails = list(map(''.join, subdomain_mails))
    subdomain_socials = [{k: v for k, v in d.items() if v} for d in subdomain_socials]
    subdomain_socials = [d for d in subdomain_socials if d]
    subdomain_socials_grouped = defaultdict(list)

    for d in subdomain_socials:
        for key, value in d.items():
            subdomain_socials_grouped[key].extend(value)

    subdomain_socials_grouped = list(dict(subdomain_socials_grouped).values())

    sd_socials = {'Facebook': [], 'Twitter': [], 'Instagram': [], 'Telegram': [], 'TikTok': [], 'LinkedIn': [],
                  'VKontakte': [], 'YouTube': [], 'Odnoklassniki': [], 'WeChat': []}

    for inner_list in subdomain_socials_grouped:
        for link in inner_list:
            if 'facebook.com' in link:
                sd_socials['Facebook'].append(urllib.parse.unquote(link))
            elif 'twitter.com' in link:
                sd_socials['Twitter'].append(urllib.parse.unquote(link))
            elif 'instagram.com' in link:
                sd_socials['Instagram'].append(urllib.parse.unquote(link))
            elif 't.me' in link:
                sd_socials['Telegram'].append(urllib.parse.unquote(link))
            elif 'tiktok.com' in link:
                sd_socials['TikTok'].append(urllib.parse.unquote(link))
            elif 'linkedin.com' in link:
                sd_socials['LinkedIn'].append(urllib.parse.unquote(link))
            elif 'vk.com' in link:
                sd_socials['VKontakte'].append(urllib.parse.unquote(link))
            elif 'youtube.com' in link:
                sd_socials['YouTube'].append(urllib.parse.unquote(link))
            elif 'wechat.com' in link:
                sd_socials['WeChat'].append(urllib.parse.unquote(link))
            elif 'ok.ru' in link:
                sd_socials['Odnoklassniki'].append(urllib.parse.unquote(link))

    sd_socials = {k: list(set(v)) for k, v in sd_socials.items()}

    if not subdomain_mails:
        subdomain_mails = ['No subdomains mails were found']
    if not subdomain_ip:
        subdomain_ip = ["No subdomains IP's were found"]

    if report_file_type == 'pdf' or report_file_type == 'html':
        return subdomain_mails, sd_socials, subdomain_ip
    elif report_file_type == 'xlsx':
        return subdomain_urls, subdomain_mails, subdomain_ip, sd_socials
