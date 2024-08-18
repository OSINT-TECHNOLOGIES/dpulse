import logging
import os
from colorama import Fore, Style
def create_log_folder():
    scan_logs_folder = 'scan_logs'
    os.makedirs(scan_logs_folder, exist_ok=True)
    return scan_logs_folder

def write_logs(ctime, whois_gather_status, contact_mail_gather_status, subdomains_gather_status, list_to_log, get_ssl_certificate_status, get_dns_info_status, get_sitemap_xml_status, extract_links_from_sitemap_status):
    to_log = [whois_gather_status, contact_mail_gather_status, subdomains_gather_status, get_ssl_certificate_status, get_dns_info_status, get_sitemap_xml_status, extract_links_from_sitemap_status]
    subdomains_processes_logs = [item for sublist in list_to_log for item in sublist]
    scan_logs_folder = create_log_folder()
    log_file_name = f"scan_log_{ctime}.log"
    logging.basicConfig(level=logging.INFO, filename=scan_logs_folder + "// " + log_file_name, filemode="w", format="%(asctime)s %(message)s")
    logging.info("# THIS FILE REPRESENTS DPULSE SCAN LOGS\n")
    print(Fore.GREEN + "Created log file for this scan" + Style.RESET_ALL)

    for log in to_log:
        logging.info(log)

    for log in subdomains_processes_logs:
        logging.info(log)

    logging.shutdown()
    return log_file_name
