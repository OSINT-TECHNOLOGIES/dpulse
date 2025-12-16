import sys
import socket
import re
import urllib
from collections import defaultdict
from urllib.parse import urlparse, unquote
import whois
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

sys.path.append('service')
from logs_processing import logging

def ip_gather(short_domain):
    ip_address = socket.gethostbyname(short_domain)
    return ip_address

def whois_gather(short_domain):
    try:
        logging.info('WHOIS INFO GATHERING: OK')
        w = whois.whois(short_domain)
        if w.org is None:
            w['org'] = 'Organization name was not extracted'
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
        return ['No subdomains were found'], 0

def sm_gather(url):
    social_domains = {
        'Facebook':       ('facebook.com',),
        'Twitter':        ('twitter.com',),
        'Instagram':      ('instagram.com',),
        'Telegram':       ('t.me',),
        'TikTok':         ('tiktok.com',),
        'LinkedIn':       ('linkedin.com',),
        'VKontakte':      ('vk.com',),
        'YouTube':        ('youtube.com', 'youtu.be'),
        'Odnoklassniki':  ('ok.ru',),
        'WeChat':         ('wechat.com',),
        'X.com':          ('x.com',),
    }

    categorized_links = {name: [] for name in social_domains.keys()}
    parsed_input = urlparse(url)
    host_input = (parsed_input.hostname or parsed_input.netloc or '').lower()

    if host_input.startswith('www.'):
        host_input = host_input[4:]

    for name, domains in social_domains.items():
        if any(host_input == d or host_input.endswith('.' + d) for d in domains):
            categorized_links[name].append(unquote(url))
            break

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        parsed = urlparse(href)
        host = parsed.hostname or parsed.netloc
        if not host:
            continue

        host = host.lower()
        if host.startswith('www.'):
            host = host[4:]

        for name, domains in social_domains.items():
            if any(host == d or host.endswith('.' + d) for d in domains):
                categorized_links[name].append(unquote(href))
                break

    for name, links in categorized_links.items():
        if not links:
            links.append(f'{name} links were not found')

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
    except Exception as e:
        print(Fore.RED + "Some URL seems unreachable! DPULSE will continue to work, but the URL causing the error won't be included in report. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS URL FORMING: ERROR. REASON: {e}')
        pass

    try:
        for subdomain in subdomains:
            subdomains_ip = ip_gather(subdomain)
            subdomain_ip.append(subdomains_ip)
            subdomain_ip = list(set(subdomain_ip))
    except Exception as e:
        print(Fore.RED + "Some URL seems unreachable! DPULSE will continue to work, but the URL causing the error won't be included in report. See journal for details" + Style.RESET_ALL)
        logging.error(f'SUBDOMAINS IP GATHERING: ERROR. REASON: {e}')
        pass

    try:
        for subdomain_url in subdomain_urls:
            subdomain_mail = subdomains_mail_gather(subdomain_url)
            subdomain_mails.append(subdomain_mail)
            subdomain_social = sm_gather(subdomain_url)
            subdomain_socials.append(subdomain_social)
    except Exception as e:
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
                  'VKontakte': [], 'YouTube': [], 'Odnoklassniki': [], 'WeChat': [], 'X.com': []}

    for inner_list in subdomain_socials_grouped:
        for link in inner_list:
            hostname = urlparse(link).hostname
            if hostname and (hostname == 'facebook.com' or hostname.endswith('.facebook.com')):
                sd_socials['Facebook'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'twitter.com' or hostname.endswith('.twitter.com')):
                sd_socials['Twitter'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'instagram.com' or hostname.endswith('.instagram.com')):
                sd_socials['Instagram'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 't.me' or hostname.endswith('.t.me')):
                sd_socials['Telegram'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'tiktok.com' or hostname.endswith('.tiktok.com')):
                sd_socials['TikTok'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'linkedin.com' or hostname.endswith('.linkedin.com')):
                sd_socials['LinkedIn'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'vk.com' or hostname.endswith('.vk.com')):
                sd_socials['VKontakte'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'youtube.com' or hostname.endswith('.youtube.com')):
                sd_socials['YouTube'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'wechat.com' or hostname.endswith('.wechat.com')):
                sd_socials['WeChat'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'ok.ru' or hostname.endswith('.ok.ru')):
                sd_socials['Odnoklassniki'].append(urllib.parse.unquote(link))
            elif hostname and (hostname == 'x.com' or hostname.endswith('.x.com')):
                sd_socials['Odnoklassniki'].append(urllib.parse.unquote(link))

    sd_socials = {k: list(set(v)) for k, v in sd_socials.items()}

    if not subdomain_mails:
        subdomain_mails = ['No subdomains mails were found']
    if not subdomain_ip:
        subdomain_ip = ["No subdomains IP's were found"]

    if report_file_type == 'html':
        return subdomain_mails, sd_socials, subdomain_ip
    elif report_file_type == 'xlsx':
        return subdomain_urls, subdomain_mails, subdomain_ip, sd_socials
