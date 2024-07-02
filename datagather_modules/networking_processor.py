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
        if len(mx_records) == 0:
            mx_records = ['MX records were not gathered']
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

def query_internetdb(ip, report_file_extension):
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
            vulns = ['Vulnerabilities were not found ']
        if report_file_extension == 'pdf':
            return ports, hostnames, cpes, tags, vulns
        elif report_file_extension == 'xlsx':
            return ports, ' // '.join(hostnames), ' // '.join(cpes), ' // '.join(tags), vulns
    else:
        print(Fore.RED + "No information was found on InternetDB" + Style.RESET_ALL)
        ports = hostnames = cpes = tags = vulns = "No info about this web resource on InternetDB"
        return ports, hostnames, cpes, tags, vulns

def get_robots_txt(url, robots_path):
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

def get_sitemap_xml(url, sitemap_path):
    try:
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
        print(Fore.RED + "Error while gathering sitemap.xml. Reason: {}".format(e))
        return 'Error occured during sitemap.xml gathering'

def extract_links_from_sitemap(sitemap_links_path, sitemap_path, report_file_type):
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        links = [elem.text for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if report_file_type == 'pdf':
            with open(sitemap_links_path, 'w') as f:
                for link in links:
                    f.write(f"=> {link}\n")
            return 'Links from "sitemap.txt" were successfully parsed'
        elif report_file_type == 'xlsx':
            parsed_links = []
            for link in links:
                parsed_links.append(link)
            return 'Links from "sitemap.txt" were successfully parsed', parsed_links
    except ET.ParseError as e:
        print(Fore.RED + "Links from sitemap.txt were not parsed. Reason: {}".format(e))
        return 'Links from "sitemap.txt" were not parsed'

def get_technologies(url):
    try:
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
    except:
        web_servers = cms = programming_languages = web_frameworks = analytics = javascript_frameworks = ['Found nothing related to web-technologies due to some error']
        return web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks
