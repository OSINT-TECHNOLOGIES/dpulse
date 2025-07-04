import sys
from datetime import datetime
import os
from colorama import Fore, Style

sys.path.extend(['service', 'pagesearch', 'dorking', 'snapshotting'])

from logs_processing import logging
from config_processing import read_config
from db_creator import get_dorking_query
import crawl_processor as cp
import dorking_handler as dp
import networking_processor as np
from pagesearch_parsers import subdomains_parser
from api_virustotal import api_virustotal_check
from api_securitytrails import api_securitytrails_check
from api_hudsonrock import api_hudsonrock_check
from screen_snapshotting import take_screenshot
from html_snapshotting import save_page_as_html
from archive_snapshotting import download_snapshot

def establishing_dork_db_connection(dorking_flag):
    dorking_db_paths = {
        'basic': 'dorking//basic_dorking.db',
        'iot': 'dorking//iot_dorking.db',
        'files': 'dorking//files_dorking.db',
        'admins': 'dorking//adminpanels_dorking.db',
        'web': 'dorking//webstructure_dorking.db',
    }
    dorking_tables = {
        'basic': 'basic_dorks',
        'iot': 'iot_dorks',
        'files': 'files_dorks',
        'admins': 'admins_dorks',
        'web': 'web_dorks',
    }
    if dorking_flag in dorking_db_paths:
        dorking_db_path = dorking_db_paths[dorking_flag]
        table = dorking_tables[dorking_flag]
    elif dorking_flag.startswith('custom'):
        lst = dorking_flag.split('+')
        dorking_db_name = lst[1]
        dorking_db_path = 'dorking//' + dorking_db_name
        table = 'dorks'
    else:
        raise ValueError(f"Invalid dorking flag: {dorking_flag}")
    return dorking_db_path, table

class DataProcessing():
    def report_preprocessing(self, short_domain, report_file_type):
        report_ctime = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        files_ctime = datetime.now().strftime('(%d-%m-%Y, %Hh%Mm%Ss)')
        files_body = short_domain.replace(".", "") + '_' + files_ctime
        casename = f"{files_body}.{report_file_type}"
        foldername = files_body
        db_casename = short_domain.replace(".", "")
        now = datetime.now()
        db_creation_date = str(now.year) + str(now.month) + str(now.day)
        report_folder = f"report_{foldername}"
        robots_filepath = os.path.join(report_folder, '01-robots.txt')
        sitemap_filepath = os.path.join(report_folder, '02-sitemap.txt')
        sitemap_links_filepath = os.path.join(report_folder, '03-sitemap_links.txt')
        os.makedirs(report_folder, exist_ok=True)
        return casename, db_casename, db_creation_date, robots_filepath, sitemap_filepath, sitemap_links_filepath, report_file_type, report_folder, files_ctime, report_ctime

    def data_gathering(self, short_domain, url, report_file_type, pagesearch_flag, keywords, keywords_flag, dorking_flag, used_api_flag, snapshotting_flag, username, from_date, end_date):
        casename, db_casename, db_creation_date, robots_filepath, sitemap_filepath, sitemap_links_filepath, report_file_type, report_folder, ctime, report_ctime = self.report_preprocessing(short_domain, report_file_type)
        logging.info(f'### THIS LOG PART FOR {casename} CASE, TIME: {ctime} STARTS HERE')
        print(Fore.LIGHTMAGENTA_EX + "\n[STARTED BASIC DOMAIN SCAN]" + Style.RESET_ALL)
        print(Fore.GREEN + "[1/11] Getting domain IP address" + Style.RESET_ALL)
        ip = cp.ip_gather(short_domain)
        print(Fore.GREEN + '[2/11] Gathering WHOIS information' + Style.RESET_ALL)
        res = cp.whois_gather(short_domain)
        print(Fore.GREEN + '[3/11] Processing e-mails gathering' + Style.RESET_ALL)
        mails = cp.contact_mail_gather(url)
        print(Fore.GREEN + '[4/11] Processing subdomain gathering' + Style.RESET_ALL)
        subdomains, subdomains_amount = cp.subdomains_gather(url, short_domain)
        print(Fore.GREEN + '[5/11] Processing social medias gathering' + Style.RESET_ALL)
        try:
            social_medias = cp.sm_gather(url)
        except:
            print(Fore.RED + "Social medias were not gathered because of error" + Style.RESET_ALL)
            social_medias = ['Social medias were not extracted because of error']
            pass
        print(Fore.GREEN + '[6/11] Processing subdomain analysis' + Style.RESET_ALL)
        if report_file_type == 'xlsx':
            subdomain_urls, subdomain_mails, subdomain_ip, sd_socials = cp.domains_reverse_research(subdomains, report_file_type)
        elif report_file_type == 'html':
            subdomain_mails, sd_socials, subdomain_ip = cp.domains_reverse_research(subdomains, report_file_type)
        print(Fore.GREEN + '[7/11] Processing SSL certificate gathering' + Style.RESET_ALL)
        issuer, subject, notBefore, notAfter, commonName, serialNumber = np.get_ssl_certificate(short_domain)
        print(Fore.GREEN + '[8/11] Processing DNS records gathering' + Style.RESET_ALL)
        mx_records = np.get_dns_info(short_domain, report_file_type)
        print(Fore.GREEN + '[9/11] Extracting robots.txt and sitemap.xml' + Style.RESET_ALL)
        robots_txt_result = np.get_robots_txt(short_domain, robots_filepath)
        sitemap_xml_result = np.get_sitemap_xml(short_domain, sitemap_filepath)
        try:
            sitemap_links_status = np.extract_links_from_sitemap(sitemap_links_filepath, sitemap_filepath)
        except Exception:
            sitemap_links_status = 'Sitemap links were not parsed'
            pass

        print(Fore.GREEN + '[10/11] Gathering info about website technologies' + Style.RESET_ALL)
        web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks = np.get_technologies(url)
        print(Fore.GREEN + '[11/11] Processing Shodan InternetDB search' + Style.RESET_ALL)
        ports, hostnames, cpes, tags, vulns = np.query_internetdb(ip, report_file_type)
        common_socials = {key: social_medias.get(key, []) + sd_socials.get(key, []) for key in set(social_medias) | set(sd_socials)}
        for key in common_socials:
            common_socials[key] = list(set(common_socials[key]))
        total_socials = sum(len(values) for values in common_socials.values())
        total_ports = len(ports)
        total_ips = len(subdomain_ip) + 1
        total_vulns = len(vulns)
        print(Fore.LIGHTMAGENTA_EX + "[ENDED BASIC DOMAIN SCAN]\n" + Style.RESET_ALL)
        if report_file_type == 'xlsx':
            if pagesearch_flag.lower() == 'y':
                if subdomains[0] != 'No subdomains were found':
                    to_search_array = [subdomains, social_medias, sd_socials]
                    print(Fore.LIGHTMAGENTA_EX + "[STARTED EXTENDED DOMAIN SCAN WITH PAGESEARCH]\n" + Style.RESET_ALL)
                    ps_emails_return, accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list = subdomains_parser(to_search_array[0], report_folder, keywords, keywords_flag)
                    total_links_counter = accessed_links_counter = "No results because PageSearch does not gather these categories"
                    print(Fore.LIGHTMAGENTA_EX + "[ENDED EXTENDED DOMAIN SCAN WITH PAGESEARCH]\n" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Cant start PageSearch because no subdomains were detected")
                    accessible_subdomains = files_counter = cookies_counter = api_keys_counter = website_elements_counter = exposed_passwords_counter = total_links_counter = accessed_links_counter = emails_amount = 'No results because no subdomains were found'
                    ps_emails_return = ""
                    pass
            elif pagesearch_flag.lower() == 'n':
                ps_emails_return = ""
                accessible_subdomains = files_counter = cookies_counter = api_keys_counter = website_elements_counter = exposed_passwords_counter = total_links_counter = accessed_links_counter = emails_amount = "No results because user did not selected PageSearch for this scan"
                pass

            if dorking_flag == 'n':
                dorking_status = 'Google Dorking mode was not selected for this scan'
                dorking_results = ['Google Dorking mode was not selected for this scan']
            else:
                dorking_db_path, table = establishing_dork_db_connection(dorking_flag.lower())
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED EXTENDED DOMAIN SCAN WITH {dorking_flag.upper()} DORKING TABLE]\n" + Style.RESET_ALL)
                dorking_status, dorking_results = dp.transfer_results_to_xlsx(table, get_dorking_query(short_domain, dorking_db_path, table))
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED EXTENDED DOMAIN SCAN WITH {dorking_flag.upper()} DORKING TABLE]\n" + Style.RESET_ALL)

            api_scan_db = []
            if used_api_flag != ['Empty']:
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]\n" + Style.RESET_ALL)
                if '1' in used_api_flag:
                    virustotal_output = api_virustotal_check(short_domain)
                    api_scan_db.append('VirusTotal')
                if '2' in used_api_flag:
                    securitytrails_output = api_securitytrails_check(short_domain)
                    api_scan_db.append('SecurityTrails')
                if '3' in used_api_flag:
                    if username.lower() == 'n':
                        username = None
                        hudsonrock_output = api_hudsonrock_check(short_domain, ip, mails, username)
                        api_scan_db.append('HudsonRock')
                    else:
                        hudsonrock_output = api_hudsonrock_check(short_domain, ip, mails, username)
                        api_scan_db.append('HudsonRock')
                if '1' not in used_api_flag:
                    virustotal_output = 'No results because user did not selected VirusTotal API scan'
                if '2' not in used_api_flag:
                    securitytrails_output = 'No results because user did not selected SecurityTrails API scan'
                if '3' not in used_api_flag:
                    hudsonrock_output = 'No results because user did not selected HudsonRock API scan'
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]\n" + Style.RESET_ALL)
            else:
                virustotal_output = 'No results because user did not selected VirusTotal API scan'
                securitytrails_output = 'No results because user did not selected SecurityTrails API scan'
                hudsonrock_output = 'No results because user did not selected HudsonRock API scan'
                api_scan_db.append('No')
                pass
            if snapshotting_flag.lower() in ['s', 'p', 'w']:
                config_values = read_config()
                installed_browser = config_values['installed_browser']
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED DOMAIN SNAPSHOTTING]\n" + Style.RESET_ALL)
                if snapshotting_flag.lower() == 's':
                    take_screenshot(installed_browser, url, report_folder + '//screensnapshot.png')
                elif snapshotting_flag.lower() == 'p':
                    save_page_as_html(url, report_folder + '//domain_html_copy.html')
                elif snapshotting_flag.lower() == 'w':
                    download_snapshot(short_domain, from_date, end_date, report_folder)
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED DOMAIN SNAPSHOTTING]\n" + Style.RESET_ALL)
            else:
                pass

            cleaned_dorking = [item.strip() for item in dorking_results if item.strip()]

            data_array = [ip, res, mails, subdomains, subdomains_amount, social_medias, subdomain_mails, sd_socials,
                          subdomain_ip, issuer, subject, notBefore, notAfter, commonName, serialNumber, mx_records,
                          robots_txt_result, sitemap_xml_result, sitemap_links_status,
                          web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks, ports,
                          hostnames, cpes, tags, vulns, common_socials, total_socials, ps_emails_return,
                          accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter,
                          website_elements_counter, exposed_passwords_counter, total_links_counter, accessed_links_counter, cleaned_dorking,
                          virustotal_output, securitytrails_output, hudsonrock_output]

        elif report_file_type == 'html':
            if pagesearch_flag.lower() == 'y':
                if subdomains[0] != 'No subdomains were found':
                    to_search_array = [subdomains, social_medias, sd_socials]
                    print(Fore.LIGHTMAGENTA_EX + "[STARTED EXTENDED DOMAIN SCAN WITH PAGESEARCH]" + Style.RESET_ALL)
                    (
                        ps_emails_return,
                        accessible_subdomains,
                        emails_amount,
                        files_counter,
                        cookies_counter,
                        api_keys_counter,
                        website_elements_counter,
                        exposed_passwords_counter,
                        keywords_messages_list
                    ), ps_string = subdomains_parser(to_search_array[0], report_folder, keywords, keywords_flag)
                    total_links_counter = accessed_links_counter = "No results because PageSearch does not gather these categories"
                    if len(keywords_messages_list) == 0:
                        keywords_messages_list = ['No keywords were found']
                    print(Fore.LIGHTMAGENTA_EX + "[ENDED EXTENDED DOMAIN SCAN WITH PAGESEARCH]\n" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Cant start PageSearch because no subdomains were detected")
                    ps_emails_return = ""
                    accessible_subdomains = files_counter = cookies_counter = api_keys_counter = website_elements_counter = exposed_passwords_counter = total_links_counter = accessed_links_counter = emails_amount = 'No results because no subdomains were found'
                    ps_string = 'No PageSearch listing provided because no subdomains were found'
                    keywords_messages_list = ['No data was gathered because no subdomains were found']
                    pass
            elif pagesearch_flag.lower() == 'n':
                accessible_subdomains = files_counter = cookies_counter = api_keys_counter = website_elements_counter = exposed_passwords_counter = total_links_counter = accessed_links_counter = emails_amount = keywords_messages_list = "No results because user did not selected PageSearch for this scan"
                ps_emails_return = ""
                ps_string = 'No PageSearch listing provided because user did not selected PageSearch mode for this scan'
                pass

            if dorking_flag == 'n':
                dorking_status = 'Google Dorking mode was not selected for this scan'
                dorking_file_path = 'Google Dorking mode was not selected for this scan'
            else:
                dorking_db_path, table = establishing_dork_db_connection(dorking_flag.lower())
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED EXTENDED DOMAIN SCAN WITH {dorking_flag.upper()} DORKING TABLE]" + Style.RESET_ALL)
                dorking_status, dorking_file_path = dp.save_results_to_txt(report_folder, table, get_dorking_query(short_domain, dorking_db_path, table))
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED EXTENDED DOMAIN SCAN WITH {dorking_flag.upper()} DORKING TABLE]\n" + Style.RESET_ALL)

            api_scan_db = []
            if used_api_flag != ['Empty']:
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]" + Style.RESET_ALL)
                if '1' in used_api_flag:
                    virustotal_output = api_virustotal_check(short_domain)
                    api_scan_db.append('VirusTotal')
                if '2' in used_api_flag:
                    securitytrails_output = api_securitytrails_check(short_domain)
                    api_scan_db.append('SecurityTrails')
                if '3' in used_api_flag:
                    if username.lower() == 'n':
                        username = None
                        hudsonrock_output = api_hudsonrock_check(short_domain, ip, mails, username)
                        api_scan_db.append('HudsonRock')
                    else:
                        hudsonrock_output = api_hudsonrock_check(short_domain, ip, mails, username)
                        api_scan_db.append('HudsonRock')
                if '1' not in used_api_flag:
                    virustotal_output = 'No results because user did not selected VirusTotal API scan'
                if '2' not in used_api_flag:
                    securitytrails_output = 'No results because user did not selected SecurityTrails API scan'
                if '3' not in used_api_flag:
                    hudsonrock_output = 'No results because user did not selected HudsonRock API scan'
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]\n" + Style.RESET_ALL)
            else:
                virustotal_output = 'No results because user did not selected VirusTotal API scan'
                securitytrails_output = 'No results because user did not selected SecurityTrails API scan'
                hudsonrock_output = 'No results because user did not selected HudsonRock API scan'
                api_scan_db.append('No')
                pass
            if snapshotting_flag.lower() in ['s', 'p', 'w']:
                config_values = read_config()
                installed_browser = config_values['installed_browser']
                print(Fore.LIGHTMAGENTA_EX + f"[STARTED DOMAIN SNAPSHOTTING]" + Style.RESET_ALL)
                if snapshotting_flag.lower() == 's':
                    take_screenshot(installed_browser, url, report_folder + '//screensnapshot.png')
                elif snapshotting_flag.lower() == 'p':
                    save_page_as_html(url, report_folder + '//domain_html_copy.html')
                elif snapshotting_flag.lower() == 'w':
                    download_snapshot(short_domain, from_date, end_date, report_folder)
                print(Fore.LIGHTMAGENTA_EX + f"[ENDED DOMAIN SNAPSHOTTING]\n" + Style.RESET_ALL)
            else:
                pass

            data_array = [ip, res, mails, subdomains, subdomains_amount, social_medias, subdomain_mails, sd_socials,
                          subdomain_ip, issuer, subject, notBefore, notAfter, commonName, serialNumber, mx_records,
                          robots_txt_result, sitemap_xml_result, sitemap_links_status,
                          web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks, ports,
                          hostnames, cpes, tags, vulns, common_socials, total_socials, ps_emails_return,
                          accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter,
                          website_elements_counter, exposed_passwords_counter, total_links_counter, accessed_links_counter, keywords_messages_list, dorking_status, dorking_file_path,
                          virustotal_output, securitytrails_output, hudsonrock_output, ps_string, total_ports, total_ips, total_vulns]

        report_info_array = [casename, db_casename, db_creation_date, report_folder, ctime, report_file_type, report_ctime, api_scan_db, used_api_flag]
        logging.info(f'### THIS LOG PART FOR {casename} CASE, TIME: {ctime} ENDS HERE')
        return data_array, report_info_array
