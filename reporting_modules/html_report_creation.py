import sys

sys.path.append('service')
sys.path.append('service//pdf_report_templates')
sys.path.append('apis')

from logs_processing import logging
import db_processing as db
import files_processing as fp
from api_hudsonrock import hudsonrock_html_prep
from api_virustotal import virustotal_html_prep
from api_securitytrails import securitytrails_html_prep
from config_processing import read_config

try:
    from datetime import datetime
    from jinja2 import Environment, FileSystemLoader
    import os
    from colorama import Fore, Style
    import sqlite3
    import re
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

def generate_report(data, output_file, template_path):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    html_output = template.render(data)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    return True

def report_assembling(short_domain, url, case_comment, data_array, report_info_array, pagesearch_ui_mark, end, snapshotting_ui_mark):
    try:
        ip = data_array[0]
        res = data_array[1]
        mails = data_array[2]
        subdomains = data_array[3]
        subdomains_amount = data_array[4]
        social_medias = data_array[5]
        subdomain_mails = data_array[6]
        subdomain_ip = data_array[8]
        issuer = data_array[9]
        subject = data_array[10]
        notBefore = data_array[11]
        notAfter = data_array[12]
        commonName = data_array[13]
        serialNumber = data_array[14]
        mx_records = data_array[15]
        robots_txt_result = data_array[16]
        sitemap_xml_result = data_array[17]
        sitemap_links_status = data_array[18]
        web_servers = data_array[19]
        cms = data_array[20]
        programming_languages = data_array[21]
        web_frameworks = data_array[22]
        analytics = data_array[23]
        javascript_frameworks = data_array[24]
        ports = data_array[25]
        hostnames = data_array[26]
        cpes = data_array[27]
        tags = data_array[28]
        vulns = data_array[29]
        common_socials = data_array[30]
        total_socials = data_array[31]
        ps_emails_return = data_array[32]
        accessible_subdomains = data_array[33]
        emails_amount = data_array[34]
        files_counter = data_array[35]
        cookies_counter = data_array[36]
        api_keys_counter = data_array[37]
        website_elements_counter = data_array[38]
        exposed_passwords_counter = data_array[39]
        total_links_counter = data_array[40]
        accessed_links_counter = data_array[41]
        keywords_messages_list = data_array[42]
        dorking_status = data_array[43]
        dorking_file_path = data_array[44]
        virustotal_output = data_array[45]
        securitytrails_output = data_array[46]
        hudsonrock_output = data_array[47]
        ps_string = data_array[48]
        total_ports = data_array[49]
        total_ips = data_array[50]
        total_vulns = data_array[51]
        casename = report_info_array[0]
        db_casename = report_info_array[1]
        db_creation_date = report_info_array[2]
        report_folder = report_info_array[3]
        report_ctime = report_info_array[6]
        api_scan_db = report_info_array[7]
        used_api_flag = report_info_array[8]

        hudsonrock_output = hudsonrock_html_prep(hudsonrock_output)
        virustotal_output = virustotal_html_prep(virustotal_output)
        securitytrails_output = securitytrails_html_prep(securitytrails_output)


        if len(ps_emails_return) > 0:
            subdomain_mails += ps_emails_return
            subdomain_mails = list(set(subdomain_mails))
            subdomain_mails_cleaned = []
            substrings = ['m=Base64', 'Ë','Á','Æ','Å','Ä','Ò','Á','ó','ð','É','ë','â']
            for substring in substrings:
                if any(substring in s for s in subdomain_mails):
                    subdomain_mails.remove(next(s for s in subdomain_mails if substring in s))
            for email in subdomain_mails:
                new_emails = email.split(', ')
                subdomain_mails_cleaned.extend(new_emails)
        else:
            subdomain_mails = list(set(subdomain_mails))
            subdomain_mails_cleaned = []
            substrings = ['m=Base64', 'Ë','Á','Æ','Å','Ä','Ò','Á','ó','ð','É','ë','â']
            for substring in substrings:
                if any(substring in s for s in subdomain_mails):
                    subdomain_mails.remove(next(s for s in subdomain_mails if substring in s))
            for email in subdomain_mails:
                new_emails = email.split(', ')
                subdomain_mails_cleaned.extend(new_emails)

        total_mails = len(subdomain_mails_cleaned)
        pdf_templates_path = 'service//pdf_report_templates'
        config_values = read_config()
        selected_template = config_values['template']
        delete_txt_files = config_values['delete_txt_files']
        if selected_template.lower() == 'modern':
            template_path = pdf_templates_path + '//modern_report_template.html'
        elif selected_template.lower() == 'legacy':
            template_path = pdf_templates_path + '//legacy_report_template.html'
        dorking_results_path = report_folder + '//04-dorking_results.txt'
        if os.path.isfile(dorking_results_path):
            with open(dorking_results_path, 'r') as f:
                add_dsi = f.read()
        else:
            add_dsi = 'Dorking mode was not enabled so there is no results to see'

        robots_content, sitemap_content, sitemap_links_content, dorking_content = fp.get_db_columns(report_folder)

        context = {'sh_domain': short_domain, 'full_url': url, 'ip_address': ip, 'registrar': res['registrar'],
                       'creation_date': res['creation_date'], 'expiration_date': res['expiration_date'],
                       'name_servers': ', '.join(res['name_servers']), 'org': res['org'],
                       'mails': mails, 'subdomain_mails': subdomain_mails_cleaned, 'subdomain_socials': social_medias,
                       'subdomain_ip': subdomain_ip,
                       'subdomains': subdomains, 'fb_links': common_socials['Facebook'],
                       'tw_links': common_socials['Twitter'], 'inst_links': common_socials['Instagram'],
                       'tg_links': common_socials['Telegram'], 'tt_links': common_socials['TikTok'],
                       'li_links': common_socials['LinkedIn'], 'vk_links': common_socials['VKontakte'],
                       'yt_links': common_socials['YouTube'], 'wc_links': common_socials['WeChat'],
                       'ok_links': common_socials['Odnoklassniki'], 'xcom_links': common_socials['X.com'], 'robots_txt_result': robots_txt_result,
                       'sitemap_xml_result': sitemap_xml_result,
                       'sitemap_links': sitemap_links_status, 'web_servers': web_servers, 'cms': cms,
                       'programming_languages': programming_languages, 'web_frameworks': web_frameworks,
                       'analytics': analytics,
                       'javascript_frameworks': javascript_frameworks,
                       'ctime': report_ctime, 'a_tsf': subdomains_amount, 'mx_records': mx_records, 'issuer': issuer,
                       'subject': subject, 'notBefore': notBefore, 'notAfter': notAfter,
                       'commonName': commonName, 'serialNumber': serialNumber, 'ports': ports, 'hostnames': hostnames,
                       'cpes': cpes,
                       'tags': tags, 'vulns': vulns, 'a_tsm': total_socials, 'pagesearch_ui_mark': pagesearch_ui_mark,
                       'dorking_status': dorking_status,
                       'add_dsi': add_dsi, 'ps_s': accessible_subdomains, 'ps_e': emails_amount, 'ps_f': files_counter, 'ps_c': cookies_counter, 'ps_a': api_keys_counter,
                        'ps_w': website_elements_counter, 'ps_p': exposed_passwords_counter, 'ss_l': total_links_counter, 'ss_a': accessed_links_counter, 'hudsonrock_output': hudsonrock_output, "snapshotting_ui_mark": snapshotting_ui_mark,
                        'virustotal_output': virustotal_output, 'securitytrails_output': securitytrails_output, 'ps_string': ps_string, 'a_tops': total_ports,
                        'a_temails': total_mails, 'a_tips': total_ips, 'a_tpv': total_vulns, 'robots_content': robots_content, 'sitemap_xml_content': sitemap_content, 'sitemap_txt_content': sitemap_links_content}

        html_report_name = report_folder + '//' + casename
        if generate_report(context, html_report_name, template_path):
            print(Fore.GREEN + "HTML report for {} case was created at {}".format(short_domain, report_ctime) + Style.RESET_ALL)
            print(Fore.GREEN + f"Scan elapsed time: {end}" + Style.RESET_ALL)
        pdf_blob = fp.get_blob(html_report_name)
        db.insert_blob('HTML', pdf_blob, db_casename, db_creation_date, case_comment, robots_content, sitemap_content, sitemap_links_content, dorking_content, api_scan_db)

        if delete_txt_files.lower() == 'y':
            files_to_remove = [
                '04-dorking_results.txt',
                '03-sitemap_links.txt',
                '02-sitemap.txt',
                '01-robots.txt'
            ]
            for file in files_to_remove:
                file_path = os.path.join(report_folder, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
        elif delete_txt_files.lower() == 'n':
            pass

    except Exception as e:
        print(Fore.RED + 'Unable to create HTML report. See journal for details')
        logging.error(f'HTML REPORT CREATION: ERROR. REASON: {e}')
