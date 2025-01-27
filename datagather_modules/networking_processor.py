import sys
sys.path.append('service')
from logs_processing import logging

try:
    import dns.resolver
    import ssl
    import socket
    from colorama import Fore, Style
    import requests
    import xml.etree.ElementTree as ET
    import builtwith
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

def get_dns_info(short_domain, report_file_extension):
    try:
        logging.info('DNS INFO GATHERING: OK')
        mx_list = []
        mx_records = dns.resolver.resolve(short_domain, 'MX')
        for record in mx_records:
            mx_list.append(record.exchange)
        if not mx_list:
            mx_list.append('MX records were not gathered')
        if report_file_extension == 'xlsx':
            return ', '.join(map(str, mx_list))
        elif report_file_extension == 'pdf':
            return ', '.join(map(str, mx_list))
    except dns.resolver.NoAnswer as error_noans:
        print(Fore.RED + "No answer from domain about MX records. See journal for details")
        logging.error(f'DNS INFO GATHERING: ERROR. REASON: {error_noans}')
        return 'No information about MX records was gathered'
    except dns.resolver.Timeout as error_timeout:
        print(Fore.RED + "Timeout while getting MX records. See journal for details")
        logging.error(f'DNS INFO GATHERING: ERROR. REASON: {error_timeout}')
        return 'No information about MX records was gathered'

def get_ssl_certificate(short_domain, port=443):
    try:
        logging.info('SSL CERTIFICATE GATHERING: OK')
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        conn = socket.create_connection((short_domain, port))
        sock = context.wrap_socket(conn, server_hostname=short_domain)
        cert = sock.getpeercert()
        issuer = cert['issuer'][0][0][1]
        subject = cert['subject'][0][0][1]
        notBefore = cert['notBefore']
        notAfter = cert['notAfter']
        commonName = str(cert['issuer'][2][0][1]) + ', version: ' + str(cert['version'])
        serialNumber = cert['serialNumber']
        return issuer, subject, notBefore, notAfter, commonName, serialNumber
    except Exception as e:
        print(Fore.RED + "Error while gathering info about SSL certificate. See journal for details")
        logging.error(f'SSL CERTIFICATE GATHERING: ERROR. REASON: {e}')
        issuer = subject = notBefore = notAfter = commonName = serialNumber = "No information about SSL certificate was gathered"
        return issuer, subject, notBefore, notAfter, commonName, serialNumber

def query_internetdb(ip, report_file_extension):
    try:
        logging.info('INTERNETDB DATA GATHERING: OK')
        url = f"https://internetdb.shodan.io/{ip}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ports = data.get("ports", [])
            hostnames = data.get("hostnames", [])
            cpes = data.get("cpes", [])
            tags = data.get("tags", [])
            vulns = data.get("vulns", [])
            if not ports:
                ports = ['Open ports were not found']
            if not hostnames:
                hostnames = ['Hostnames were not found']
            if not cpes:
                cpes = ['CPEs were not found']
            if not tags:
                tags = ['Tags were not found']
            if not vulns:
                vulns = ['Vulnerabilities were not found']
            if report_file_extension == 'pdf' or report_file_extension == 'html':
                return ports, hostnames, cpes, tags, vulns
            elif report_file_extension == 'xlsx':
                return ports, hostnames, cpes, tags, vulns
        else:
            print(Fore.RED + "No information was found on InternetDB" + Style.RESET_ALL)
            ports = hostnames = cpes = tags = vulns = ["No info about this web resource on InternetDB"]
            return ports, hostnames, cpes, tags, vulns
    except Exception as e:
        print(Fore.RED + "No information was found on InternetDB due to some error. See journal for details" + Style.RESET_ALL)
        ports = hostnames = cpes = tags = vulns = ["No info about this web resource on InternetDB"]
        logging.error(f'INTERNETDB DATA GATHERING: ERROR. REASON: {e}')
        return ports, hostnames, cpes, tags, vulns


def get_robots_txt(url, robots_path):
    try:
        logging.info('ROBOTS.TXT EXTRACTION: OK')
        if not url.startswith('http'):
            url = 'http://' + url
        robots_url = url + '/robots.txt'
        response = requests.get(robots_url)
        if response.status_code == 200:
            with open(robots_path, 'w') as f:
                f.write(response.text)
            return 'File "robots.txt" was extracted to text file in report folder'
        else:
            return 'File "robots.txt" was not found'
    except Exception as e:
        print(Fore.RED + 'robots.txt file was not extracted due to some error. See journal for details')
        logging.error(f'ROBOTS.TXT EXTRACTION: ERROR. REASON: {e}')
        return 'File "robots.txt" was not found'

def get_sitemap_xml(url, sitemap_path):
    try:
        logging.info('SITEMAP.XML EXTRACTION: OK')
        if not url.startswith('http'):
            url = 'http://' + url
        sitemap_url = url + '/sitemap.xml'
        response = requests.get(sitemap_url)
        if len(response.text) > 0:
            if response.status_code == 200:
                with open(sitemap_path, 'w') as f:
                    f.write(response.text)
                return 'File "sitemap.xml" was extracted to text file in report folder'
            else:
                return 'File "sitemap.xml" was not found'
        else:
            with open(sitemap_path, 'w') as f:
                f.write('0')
            print(Fore.RED + "Error while gathering sitemap.xml. Probably it's unreachable")
            return 'File "sitemap.xml" was not found'
    except Exception as e:
        print(Fore.RED + "Error while gathering sitemap.xml. See journal for details")
        logging.error(f'SITEMAP.XML EXTRACTION: ERROR. REASON: {e}')
        return 'Error occured during sitemap.xml gathering'

def extract_links_from_sitemap(sitemap_links_path, sitemap_path):
    try:
        logging.info('SITEMAP.XML LINKS EXTRACTION: OK')
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        links = [elem.text for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        with open(sitemap_links_path, 'w') as f:
            for link in links:
                f.write(f"{link}\n")
        return 'Links from "sitemap.txt" were successfully parsed'
    except (ET.ParseError, FileNotFoundError) as e:
        print(Fore.RED + "Links from sitemap.txt were not parsed. See journal for details")
        logging.error(f'SITEMAP.XML LINKS EXTRACTION: ERROR. REASON: {e}')
        return 'Links from "sitemap.txt" were not parsed'

def get_technologies(url):
    try:
        logging.info('WEB-TECHNOLOGIES GATHERING: OK')
        tech = builtwith.parse(url)
        web_servers = tech.get('web-servers', [])
        cms = tech.get('cms', [])
        programming_languages = tech.get('programming-languages', [])
        web_frameworks = tech.get('web-frameworks', [])
        analytics = tech.get('analytics', [])
        javascript_frameworks = tech.get('javascript-frameworks', [])
        if not web_servers:
            web_servers = ['Web-servers were not found']
        if not cms:
            cms = ['CMS were not found']
        if not programming_languages:
            programming_languages = ['Used programming languages were not determined']
        if not web_frameworks:
            web_frameworks = ['Used web frameworks were not determined']
        if not analytics:
            analytics = ['Used analytics services were not determined']
        if not javascript_frameworks:
            javascript_frameworks = ['Used JS frameworks were not determined']
        return web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks
    except Exception as e:
        web_servers = cms = programming_languages = web_frameworks = analytics = javascript_frameworks = ['Found nothing related to web-technologies due to some error']
        print(Fore.RED + "Error when gathering info about web technologies. See journal for details")
        logging.error(f'WEB-TECHNOLOGIES GATHERING: ERROR. REASON: {e}')
        return web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks
