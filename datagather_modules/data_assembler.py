import sys
import logging
sys.path.append('service')
sys.path.append('pagesearch')

import crawl_processor as cp
import dorking_processor as dp
import networking_processor as np
from pagesearch_main import normal_search, sitemap_inspection_search
from logs_processing import write_logs

try:
    import requests
    from datetime import datetime
    import jinja2
    import os
    from colorama import Fore, Style
    import webbrowser
    import sqlite3
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

class DataProcessing():
    def report_preprocessing(self, short_domain, report_file_type):
        report_ctime = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        files_ctime = datetime.now().strftime('(%d-%m-%Y, %Hh%Mm%Ss)')
        files_body = short_domain.replace(".", "") + '_' + files_ctime
        if report_file_type == 'pdf':
            casename = files_body + '.pdf'
        elif report_file_type == 'xlsx':
            casename = files_body + '.xlsx'
        foldername = files_body
        db_casename = short_domain.replace(".", "")
        now = datetime.now()
        db_creation_date = str(now.year) + str(now.month) + str(now.day)
        report_folder = "report_{}".format(foldername)
        robots_filepath = report_folder + '//01-robots.txt'
        sitemap_filepath = report_folder + '//02-sitemap.txt'
        sitemap_links_filepath = report_folder + '//03-sitemap_links.txt'
        os.makedirs(report_folder, exist_ok=True)
        return casename, db_casename, db_creation_date, robots_filepath, sitemap_filepath, sitemap_links_filepath, report_file_type, report_folder, files_ctime, report_ctime

    def data_gathering(self, short_domain, url, report_file_type, pagesearch_flag, keywords, keywords_flag):
        casename, db_casename, db_creation_date, robots_filepath, sitemap_filepath, sitemap_links_filepath, report_file_type, report_folder, ctime, report_ctime = self.report_preprocessing(short_domain, report_file_type)
        print(Fore.GREEN + "Started scanning domain" + Style.RESET_ALL)
        print(Fore.GREEN + "Getting domain IP address" + Style.RESET_ALL)
        ip = cp.ip_gather(short_domain)
        print(Fore.GREEN + 'Gathering WHOIS information' + Style.RESET_ALL)
        res, whois_gather_status = cp.whois_gather(short_domain)
        print(Fore.GREEN + 'Processing e-mails gathering' + Style.RESET_ALL)
        mails, contact_mail_gather_status = cp.contact_mail_gather(url)
        print(Fore.GREEN + 'Processing subdomain gathering' + Style.RESET_ALL)
        subdomains, subdomains_amount, subdomains_gather_status = cp.subdomains_gather(url, short_domain)
        print(Fore.GREEN + 'Processing social medias gathering' + Style.RESET_ALL)
        social_medias = cp.sm_gather(url)
        print(Fore.GREEN + 'Processing subdomain analysis' + Style.RESET_ALL)
        if report_file_type == 'pdf':
            subdomain_mails, sd_socials, subdomain_ip, list_to_log = cp.domains_reverse_research(subdomains, report_file_type)
        elif report_file_type == 'xlsx':
            subdomain_urls, subdomain_mails, subdomain_ip, sd_socials, list_to_log = cp.domains_reverse_research(subdomains, report_file_type)
        print(Fore.GREEN + 'Processing SSL certificate gathering' + Style.RESET_ALL)
        issuer, subject, notBefore, notAfter, commonName, serialNumber, get_ssl_certificate_status = np.get_ssl_certificate(short_domain)
        print(Fore.GREEN + 'Processing DNS records gathering' + Style.RESET_ALL)
        mx_records, get_dns_info_status = np.get_dns_info(short_domain, report_file_type)
        print(Fore.GREEN + 'Extracting robots.txt and sitemap.xml' + Style.RESET_ALL)
        robots_txt_result, get_robots_txt_status = np.get_robots_txt(short_domain, robots_filepath)
        sitemap_xml_result, get_sitemap_xml_status = np.get_sitemap_xml(short_domain, sitemap_filepath)
        if report_file_type == 'pdf':
            sitemap_links_status, extract_links_from_sitemap_status = np.extract_links_from_sitemap(sitemap_links_filepath, sitemap_filepath)
        elif report_file_type == 'xlsx':
            try:
                sitemap_links_status, extract_links_from_sitemap_status = np.extract_links_from_sitemap(sitemap_links_filepath, sitemap_filepath)
            except Exception as e:
                sitemap_links_status = 'Sitemap links were not parsed'
                extract_links_from_sitemap_status = f'LINKS EXTRACTION FROM SITEMAP: NOT OK. REASON: {e}'
                pass

        print(Fore.GREEN + 'Gathering info about website technologies' + Style.RESET_ALL)
        web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks, get_technologies_status = np.get_technologies(url)
        print(Fore.GREEN + 'Processing Shodan InternetDB search' + Style.RESET_ALL)
        ports, hostnames, cpes, tags, vulns, query_internetdb_status = np.query_internetdb(ip, report_file_type)
        print(Fore.GREEN + 'Processing Google Dorking' + Style.RESET_ALL)
        if report_file_type == 'pdf':
            dorking_status = dp.save_results_to_txt(report_folder, dp.get_dorking_query(short_domain))
        elif report_file_type == 'xlsx':
            dorking_status, dorking_results = dp.transfer_results_to_xlsx(dp.get_dorking_query(short_domain))
        common_socials = {key: social_medias.get(key, []) + sd_socials.get(key, []) for key in set(social_medias) | set(sd_socials)}
        for key in common_socials:
            common_socials[key] = list(set(common_socials[key]))
        total_socials = sum(len(values) for values in common_socials.values())
        print(Fore.LIGHTMAGENTA_EX + "\n[BASIC SCAN END]\n" + Style.RESET_ALL)
        if report_file_type == 'pdf':
            if pagesearch_flag.lower() == 'y':
                if subdomains[0] != 'No subdomains were found':
                    to_search_array = [subdomains, social_medias, sd_socials]
                    print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN START: PAGESEARCH]\n" + Style.RESET_ALL)
                    ps_emails_return, ps_to_log_list = normal_search(to_search_array, report_folder, keywords, keywords_flag)
                    print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN END: PAGESEARCH]\n" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Cant start PageSearch because no subdomains were detected")
                    ps_emails_return = ""
                    pass
            elif pagesearch_flag.lower() == 'si':
                print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN START: PAGESEARCH SITEMAP INSPECTION]\n" + Style.RESET_ALL)
                ps_emails_return = sitemap_inspection_search(report_folder)
                print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN END: PAGESEARCH SITEMAP INSPECTION]\n" + Style.RESET_ALL)
            elif pagesearch_flag.lower() == 'n':
                ps_emails_return = ""
                pass
            log_file_name = write_logs(ctime, whois_gather_status, contact_mail_gather_status, subdomains_gather_status,
                                       list_to_log, get_ssl_certificate_status, get_dns_info_status,
                                       get_sitemap_xml_status,
                                       extract_links_from_sitemap_status, get_robots_txt_status,
                                       get_technologies_status, query_internetdb_status, ps_to_log_list)
            data_array = [ip, res, mails, subdomains, subdomains_amount, social_medias, subdomain_mails, sd_socials,
                          subdomain_ip, issuer, subject, notBefore, notAfter, commonName, serialNumber, mx_records,
                          robots_txt_result, sitemap_xml_result, sitemap_links_status,
                          web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks, ports,
                          hostnames, cpes, tags, vulns, dorking_status, common_socials, total_socials, ps_emails_return, log_file_name]
        elif report_file_type == 'xlsx':
            if pagesearch_flag.lower() == 'y':
                if subdomains[0] != 'No subdomains were found':
                    to_search_array = [subdomains, social_medias, sd_socials]
                    print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN START: PAGESEARCH]\n" + Style.RESET_ALL)
                    ps_emails_return, ps_to_log_list = normal_search(to_search_array, report_folder, keywords, keywords_flag)
                    print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN END: PAGESEARCH]\n" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Cant start PageSearch because no subdomains were detected")
                    ps_emails_return = ""
                    pass
            elif pagesearch_flag.lower() == 'si':
                print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN START: PAGESEARCH SITEMAP INSPECTION]\n" + Style.RESET_ALL)
                ps_emails_return = sitemap_inspection_search(report_folder)
                print(Fore.LIGHTMAGENTA_EX + "\n[EXTENDED SCAN END: PAGESEARCH SITEMAP INSPECTION]\n" + Style.RESET_ALL)
            elif pagesearch_flag.lower() == 'n':
                ps_emails_return = ""
                pass
            log_file_name = write_logs(ctime, whois_gather_status, contact_mail_gather_status, subdomains_gather_status,
                                       list_to_log, get_ssl_certificate_status, get_dns_info_status,
                                       get_sitemap_xml_status,
                                       extract_links_from_sitemap_status, get_robots_txt_status,
                                       get_technologies_status, query_internetdb_status, ps_to_log_list)
            data_array = [ip, res, mails, subdomains, subdomains_amount, social_medias, subdomain_mails, sd_socials,
                          subdomain_ip, issuer, subject, notBefore, notAfter, commonName, serialNumber, mx_records,
                          robots_txt_result, sitemap_xml_result, sitemap_links_status,
                          web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks, ports,
                          hostnames, cpes, tags, vulns, dorking_status, common_socials, total_socials, subdomain_urls, dorking_results, ps_emails_return, log_file_name]

        report_info_array = [casename, db_casename, db_creation_date, report_folder, ctime, report_file_type, report_ctime]
        return data_array, report_info_array
