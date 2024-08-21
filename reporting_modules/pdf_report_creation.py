import sys
sys.path.append('service')

import db_processing as db
import files_processing as fp

try:
    import requests
    from datetime import datetime
    from jinja2 import Environment, FileSystemLoader
    from xhtml2pdf import pisa
    import os
    from io import BytesIO
    from colorama import Fore, Style
    import webbrowser
    import sqlite3
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

try:
    current_script = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script)
    cfg_file_path = os.path.join(current_directory, fp.find_files('dorkslist.txt'))
    print(Fore.GREEN + 'Dorks list was found at {}'.format(cfg_file_path))
except TypeError as e:
    print(Fore.RED + 'Dorks list was not found in DPULSE root directory. Reason: {}'.format(e) + Style.RESET_ALL)
    sys.exit()

short_domain = ''
search_query = []

def create_pdf(template_src, output_dst, context_data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_src)
    rendered_html = template.render(context_data)
    with open(output_dst, "w+b") as result_file:
        pdf = pisa.pisaDocument(BytesIO(rendered_html.encode('UTF-8')), result_file, encoding='utf-8')
        if pdf.err:
            return False
    return True

def report_assembling(short_domain, url, case_comment, data_array, report_info_array, pagesearch_ui_mark):
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
        dorking_status = data_array[30]
        common_socials = data_array[31]
        total_socials = data_array[32]
        ps_emails_return = data_array[33]
        log_file_name = data_array[34]
        casename = report_info_array[0]
        db_casename = report_info_array[1]
        db_creation_date = report_info_array[2]
        report_folder = report_info_array[3]
        report_ctime = report_info_array[6]
        if len(ps_emails_return) > 0:
            subdomain_mails += ps_emails_return
            subdomain_mails = list(set(subdomain_mails))

        context = {'sh_domain': short_domain, 'full_url': url, 'ip_address': ip, 'registrar': res['registrar'],
                                    'creation_date': res['creation_date'],'expiration_date': res['expiration_date'],
                                    'name_servers': ', '.join(res['name_servers']),'org': res['org'],
                                    'mails': mails, 'subdomain_mails': subdomain_mails, 'subdomain_socials': social_medias,
                                    'subdomain_ip': subdomain_ip, 'log_file_name': log_file_name,
                                    'subdomains': subdomains, 'fb_links': common_socials['Facebook'],
                                    'tw_links': common_socials['Twitter'], 'inst_links': common_socials['Instagram'],
                                    'tg_links': common_socials['Telegram'], 'tt_links': common_socials['TikTok'],
                                    'li_links': common_socials['LinkedIn'], 'vk_links': common_socials['VKontakte'],
                                    'yt_links': common_socials['YouTube'], 'wc_links': common_socials['WeChat'],
                                    'ok_links': common_socials['Odnoklassniki'], 'robots_txt_result': robots_txt_result, 'sitemap_xml_result': sitemap_xml_result, 'dorking_status': dorking_status,
                                    'sitemap_links': sitemap_links_status, 'web_servers': web_servers, 'cms': cms, 'programming_languages': programming_languages, 'web_frameworks': web_frameworks, 'analytics': analytics,
                                    'javascript_frameworks': javascript_frameworks,
                                     'ctime': report_ctime, 'a_tsf': subdomains_amount, 'mx_records': mx_records, 'issuer': issuer, 'subject': subject, 'notBefore': notBefore, 'notAfter': notAfter,
                                    'commonName': commonName, 'serialNumber': serialNumber, 'ports': ports, 'hostnames': hostnames, 'cpes': cpes,
                                    'tags': tags, 'vulns': vulns, 'a_tsm': total_socials, 'pagesearch_ui_mark': pagesearch_ui_mark}

        pdf_report_name = report_folder + '//' + casename
        template_path = 'report_template.html'
        if create_pdf(template_path, pdf_report_name, context):
            print(Fore.GREEN + "PDF report for {} case was created at {}".format(''.join(short_domain), report_ctime) + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Unable to create PDF report. Reason: {}')
        robots_content, sitemap_content, sitemap_links_content, dorking_content = fp.get_db_columns(report_folder)
        pdf_blob = fp.get_blob(pdf_report_name)
        db.insert_blob('PDF', pdf_blob, db_casename, db_creation_date, case_comment, robots_content, sitemap_content, sitemap_links_content, dorking_content)
    except Exception as e:
        print(Fore.RED + 'Unable to create PDF report. Reason: {}'.format(e))
