import sys
sys.path.append('service')

import crawl_processor as cp
import dorking_processor as dp
import networking_processor as np
import db_processing as db
import files_processing as fp

try:
    import requests
    from datetime import datetime
    import jinja2
    import pdfkit
    import os
    from colorama import Fore, Style
    import webbrowser
    import sqlite3
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

try:
    current_script = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script)
    file_path = os.path.join(current_directory, fp.find_files('wkhtmltopdf.exe'))
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
    cfg_file_path = os.path.join(current_directory, fp.find_files('dorkslist.txt'))
    print(Fore.GREEN + 'Main config file was found at {}'.format(cfg_file_path))
except TypeError as e:
    print(Fore.RED + 'Main config file was not found in DPULSE root directory. Reason: {}'.format(e) + Style.RESET_ALL)
    sys.exit()

short_domain = ''
def report_encoding_config():
    return {
        'encoding': 'UTF-8',
        'enable-local-file-access': True
    }

search_query = []
def create_report(short_domain, url, case_comment):
    try:
        ctime = datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')
        casename = short_domain.replace(".", "") + '_' + ctime + '.pdf'
        foldername = short_domain.replace(".", "") + '_' + ctime
        db_casename = short_domain.replace(".", "")
        now = datetime.now()
        db_creation_date = str(now.year) + str(now.month) + str(now.day)
        report_folder = "report_{}".format(foldername)
        os.makedirs(report_folder, exist_ok=True)
        print(Fore.GREEN + "Started scanning domain" + Style.RESET_ALL)
        print(Fore.GREEN + "Getting domain IP address" + Style.RESET_ALL)
        ip = cp.ip_gather(short_domain)
        print(Fore.GREEN + 'Gathering WHOIS information' + Style.RESET_ALL)
        res = cp.whois_gather(short_domain)
        print(Fore.GREEN + 'Processing e-mails gathering' + Style.RESET_ALL)
        mails = cp.mail_gather(url)
        print(Fore.GREEN + 'Processing subdomain gathering' + Style.RESET_ALL)
        subdomains, subdomains_amount = cp.subdomains_gather(url, short_domain)
        print(Fore.GREEN + 'Processing social medias gathering' + Style.RESET_ALL)
        social_medias = cp.sm_gather(url)
        print(Fore.GREEN + 'Processing subdomain analysis' + Style.RESET_ALL)
        subdomain_mails, sd_socials, subdomain_ip = cp.domains_reverse_research(subdomains)
        print(Fore.GREEN + 'Processing SSL certificate gathering' + Style.RESET_ALL)
        issuer, subject, notBefore, notAfter, commonName, serialNumber = np.get_ssl_certificate(short_domain)
        print(Fore.GREEN + 'Processing MX records gathering' + Style.RESET_ALL)
        mx_records = np.get_dns_info(short_domain)
        print(Fore.GREEN + 'Extracting robots.txt and sitemap.xml' + Style.RESET_ALL)
        robots_txt_result = np.get_robots_txt(short_domain, report_folder)
        sitemap_xml_result = np.get_sitemap_xml(short_domain, report_folder)
        sitemap_links_status = np.extract_links_from_sitemap(report_folder)
        print(Fore.GREEN + 'Gathering info about website technologies' + Style.RESET_ALL)
        web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks = np.get_technologies(url)
        print(Fore.GREEN + 'Processing Shodan InternetDB search' + Style.RESET_ALL)
        ports, hostnames, cpes, tags, vulns = np.query_internetdb(ip)
        print(Fore.GREEN + 'Processing Google Dorking' + Style.RESET_ALL)
        dorking_status = dp.save_results_to_txt(report_folder, dp.get_dorking_query(short_domain))

        common_socials = {key: social_medias.get(key, []) + sd_socials.get(key, []) for key in set(social_medias) | set(sd_socials)}
        for key in common_socials:
            common_socials[key] = list(set(common_socials[key]))

        total_socials = sum(len(values) for values in common_socials.values())

        context = {'sh_domain': short_domain, 'full_url': url, 'ip_address': cp.ip_gather(short_domain),'registrar': res['registrar'],
                                    'creation_date': res['creation_date'],'expiration_date': res['expiration_date'],
                                    'name_servers': ', '.join(res['name_servers']),'org': res['org'],
                                    'mails': mails, 'subdomain_mails': subdomain_mails, 'subdomain_socials': social_medias,
                                    'subdomain_ip': subdomain_ip,
                                    'subdomains': ' // '.join(subdomains), 'fb_links': '   '.join(common_socials['Facebook']),
                                    'tw_links': '  '.join(common_socials['Twitter']), 'inst_links': '  '.join(common_socials['Instagram']),
                                    'tg_links': '  '.join(common_socials['Telegram']), 'tt_links': '  '.join(common_socials['TikTok']),
                                    'li_links': '  '.join(common_socials['LinkedIn']), 'vk_links': '  '.join(common_socials['VKontakte']),
                                    'yt_links': '  '.join(common_socials['YouTube']), 'wc_links': '  '.join(common_socials['WeChat']),
                                    'ok_links': '  '.join(common_socials['Odnoklassniki']), 'robots_txt_result': robots_txt_result, 'sitemap_xml_result': sitemap_xml_result, 'dorking_status': dorking_status,
                                    'sitemap_links': sitemap_links_status, 'web_servers': web_servers, 'cms': cms, 'programming_languages': programming_languages, 'web_frameworks': web_frameworks, 'analytics': analytics,
                                    'javascript_frameworks': javascript_frameworks,
                                     'ctime': ctime, 'a_tsf': subdomains_amount, 'mx_records': mx_records, 'issuer': issuer, 'subject': subject, 'notBefore': notBefore, 'notAfter': notAfter,
                                    'commonName': commonName, 'serialNumber': serialNumber, 'ports': ports, 'hostnames': hostnames, 'cpes': cpes,
                                    'tags': tags, 'vulns': vulns, 'a_tsm': total_socials}

        print(Fore.GREEN + 'Processing report for {} case...'.format(short_domain) + Style.RESET_ALL)
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('report_template.html')
        output_text = template.render(context)
        config = pdfkit.configuration(wkhtmltopdf=file_path)
        report_file = report_folder + "//" + casename
        pdfkit.from_string(output_text, report_file, configuration=config, options=report_encoding_config())
        print(Fore.GREEN + "Report for {} case was created at {}".format(''.join(short_domain), ctime) + Style.RESET_ALL)
        robots_content, sitemap_content, sitemap_links_content, dorking_content = fp.get_db_columns(report_folder)
        pdf_blob = fp.get_pdf_blob(report_file)
        db.insert_blob(pdf_blob, db_casename, db_creation_date, case_comment, robots_content, sitemap_content, sitemap_links_content, dorking_content)
    except Exception as e:
        print(Fore.RED + 'Unable to create PDF report. Reason: {}'.format(e))