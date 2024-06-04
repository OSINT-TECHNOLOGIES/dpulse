import sys

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

def get_dns_info(short_domain):
    try:
        resolver = dns.resolver.Resolver()
        mx_records = str(resolver.resolve(short_domain, 'MX'))
        return mx_records
    except dns.resolver.NoAnswer as error_noans:
        print(Fore.RED + "No answer from domain about MX records. Reason: {}".format(error_noans))
        return 'No information about MX records was gathered'
    except dns.resolver.Timeout as error_timeout:
        print(Fore.RED + "Timeout while getting MX records. Reason: {}".format(error_timeout))
        return 'No information about MX records was gathered'

def get_ssl_certificate(short_domain, port=443):
    try:
        context = ssl.create_default_context()
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
    except (ssl.CertificateError, ssl.SSLError, socket.gaierror) as e:
        print(Fore.RED + "Error while gathering info about SSL certificate. Reason: {}".format(e))
        return "No information about SSL certificate was gathered"

def query_internetdb(ip):
    url = f"https://internetdb.shodan.io/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ports = data.get("ports", [])
        hostnames = data.get("hostnames", [])
        cpes = data.get("cpes", [])
        tags = data.get("tags", [])
        vulns = data.get("vulns", [])
        return ports, ' // '.join(hostnames), ' // '.join(cpes), ' // '.join(tags), ' // '.join(vulns)
    else:
        print(Fore.RED + "No information was found on InternetDB" + Style.RESET_ALL)
        ports = hostnames = cpes = tags = vulns = "No info about this web resource on InternetDB"
        return ports, hostnames, cpes, tags, vulns

def get_robots_txt(url, report_folder):
    filepath = report_folder + '//01-robots.txt'
    if not url.startswith('http'):
        url = 'http://' + url
    robots_url = url + '/robots.txt'
    response = requests.get(robots_url)
    if response.status_code == 200:
        with open(filepath, 'w') as f:
            f.write(response.text)
        return 'File "robots.txt" was extracted to text file in report folder'
    else:
        return 'File "robots.txt" was not found'

def get_sitemap_xml(url, report_folder):
    filepath = report_folder + '//02-sitemap.txt'
    if not url.startswith('http'):
        url = 'http://' + url
    sitemap_url = url + '/sitemap.xml'
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        with open(filepath, 'w') as f:
            f.write(response.text)
        return 'File "sitemap.xml" was extracted to text file in report folder'
    else:
        return 'File "sitemap.xml" was not found'

def extract_links_from_sitemap(report_folder):
    file_name = report_folder + '//02-sitemap.txt'
    links_file = report_folder + '//03-sitemap_links.txt'
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        links = [elem.text for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        with open(links_file, 'w') as f:
            for link in links:
                f.write(f"=> {link}\n")
        return 'Links from "sitemap.txt" were successfully parsed'
    except ET.ParseError as e:
        print(Fore.RED + "Links from sitemap.txt were not parsed. Reason: {}".format(e))
        return 'Links from "sitemap.txt" were not parsed'

def get_technologies(url):
    try:
        tech = builtwith.parse(url)
        web_servers = ', '.join(tech.get('web-servers', []))
        cms = ', '.join(tech.get('cms', []))
        programming_languages = ', '.join(tech.get('programming-languages', []))
        web_frameworks = ', '.join(tech.get('web-frameworks', []))
        analytics = ', '.join(tech.get('analytics', []))
        javascript_frameworks = ', '.join(tech.get('javascript-frameworks', []))
        return web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks
    except:
        web_servers = cms = programming_languages = web_frameworks = analytics = javascript_frameworks = 'Found nothing related to web-technologies'
        return web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks

