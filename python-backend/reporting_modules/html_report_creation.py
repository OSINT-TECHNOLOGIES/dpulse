import sys
import os
import json
from jinja2 import Environment, FileSystemLoader
from colorama import Fore, Style

sys.path.append('service')
sys.path.append('service//pdf_report_templates')
sys.path.append('apis')

from logs_processing import logging
import db_processing as db
import files_processing as fp
from api_virustotal import virustotal_html_prep
from api_securitytrails import securitytrails_html_prep
from config_processing import read_config


def is_placeholder(value):
    if not isinstance(value, str):
        return False
    v = value.lower()
    markers = [
        'not found', 'not gathered', 'not determined', 'not selected',
        'not parsed', 'not available', 'not extracted', 'no info',
        'no results', 'empty', 'no contact'
    ]
    return any(m in v for m in markers)


def clean_list(items):
    if not isinstance(items, list):
        return []
    return [i for i in items if isinstance(i, str) and not is_placeholder(i)]


def ensure_list(val):
    if isinstance(val, list): return val
    if isinstance(val, str) and val.strip(): return [val.strip()]
    return []


def tojson_filter(obj):
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


def build_graph_data(short_domain, ip, subdomains, subdomain_ip, common_socials,
                      ports, vulns, web_servers, cms, programming_languages,
                      web_frameworks, analytics, javascript_frameworks,
                      hudsonrock_intel=None):
    nodes = []
    edges = []
    counter = {'n': 0}

    def add_node(label, group, extra=None):
        nid = counter['n']
        counter['n'] += 1
        node = {'id': nid, 'label': str(label)[:40], 'full_label': str(label), 'group': group}
        if extra:
            node.update(extra)
        nodes.append(node)
        return nid

    domain_id = add_node(short_domain, 'domain')

    tech_items = set()
    for lst in [web_servers, cms, programming_languages, web_frameworks, analytics, javascript_frameworks]:
        for item in clean_list(lst):
            tech_items.add(item)
    for tech in sorted(tech_items):
        tid = add_node(tech, 'service')
        edges.append({'from': domain_id, 'to': tid})

    if isinstance(subdomains, list):
        for sd in subdomains[:150]:
            if isinstance(sd, str) and sd:
                sid = add_node(sd, 'subdomain')
                edges.append({'from': domain_id, 'to': sid})

    ip_set = set()
    if isinstance(ip, str) and not is_placeholder(ip):
        ip_set.add(ip)
    for i in clean_list(subdomain_ip):
        ip_set.add(i)
    for ip_addr in sorted(ip_set):
        iid = add_node(ip_addr, 'ip')
        edges.append({'from': domain_id, 'to': iid})

    if isinstance(ports, list):
        for port in ports:
            if not is_placeholder(port):
                pid = add_node(str(port), 'port')
                edges.append({'from': domain_id, 'to': pid})

    if isinstance(vulns, list):
        for vuln in vulns:
            if isinstance(vuln, str) and not is_placeholder(vuln):
                vid = add_node(vuln, 'vuln', {'cve': vuln})
                edges.append({'from': domain_id, 'to': vid})

    if isinstance(common_socials, dict):
        for platform, links in common_socials.items():
            for link in clean_list(links):
                sid = add_node(platform, 'social', {'url': link})
                edges.append({'from': domain_id, 'to': sid})

    if hudsonrock_intel and isinstance(hudsonrock_intel, dict):
        seen_computers = set()
        for record in hudsonrock_intel.get('all_records', []):
            computer = record.get('computer_name', 'Unknown')
            if computer in seen_computers or computer == 'Unknown':
                continue
            seen_computers.add(computer)
            cid = add_node(computer, 'compromised_employee', {
                'stealer_family': record.get('stealer_family'),
                'date': record.get('date_compromised'),
            })
            edges.append({'from': domain_id, 'to': cid})

        for url_item in hudsonrock_intel.get('classified_urls', []):
            if url_item.get('criticality') in ('critical', 'high'):
                url_val = url_item.get('url', 'Unknown URL')
                eid = add_node(url_val, 'exposed_service', {
                    'url': url_val,
                    'criticality': url_item.get('criticality'),
                })
                edges.append({'from': domain_id, 'to': eid})

    return {'nodes': nodes, 'edges': edges}


def compute_social_counts(common_socials):
    counts = {}
    if isinstance(common_socials, dict):
        for platform, links in common_socials.items():
            real = clean_list(links)
            if real:
                counts[platform] = len(real)
    return counts


def generate_report(data, output_file, template_path):
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    template_dir = os.environ.get('DPULSE_TEMPLATE_DIR', '.')
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['tojson'] = tojson_filter
    env.globals['is_placeholder'] = is_placeholder
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
        hudsonrock_intel = data_array[47]
        ps_string = data_array[48]
        total_ports = data_array[49]
        total_ips = data_array[50]
        total_vulns = data_array[51]
        lunarcyber_intel = data_array[52]
        casename = report_info_array[0]
        db_casename = report_info_array[1]
        db_creation_date = report_info_array[2]
        report_folder = report_info_array[3]
        report_ctime = report_info_array[6]
        api_scan_db = report_info_array[7]
        used_api_flag = report_info_array[8]

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
        delete_txt_files = config_values['delete_txt_files']
        template_path = pdf_templates_path + '//modern_report_template.html'
        dorking_results_path = report_folder + '//04-dorking_results.txt'
        if os.path.isfile(dorking_results_path):
            with open(dorking_results_path, 'r') as f:
                add_dsi = f.read()
        else:
            add_dsi = 'Dorking mode was not enabled so there is no results to see'

        all_ips = ensure_list(subdomain_ip) + ensure_list(ip)
        robots_content, sitemap_content, sitemap_links_content, dorking_content = fp.get_db_columns(report_folder)

        graph_data = build_graph_data(
            short_domain, ip, subdomains, subdomain_ip, common_socials,
            ports, vulns, web_servers, cms, programming_languages,
            web_frameworks, analytics, javascript_frameworks,
            hudsonrock_intel=hudsonrock_intel
        )

        social_counts = compute_social_counts(common_socials)

        dorking_enabled = dorking_status != 'Google Dorking mode was not selected for this scan'
        pagesearch_enabled = isinstance(pagesearch_ui_mark, str) and pagesearch_ui_mark.strip().lower().startswith('yes')
        snapshotting_enabled = isinstance(snapshotting_ui_mark, str) and snapshotting_ui_mark.strip().lower().startswith('yes')
        api_enabled = used_api_flag != ['Empty'] or bool(hudsonrock_intel) or bool(lunarcyber_intel)

        robots_found = isinstance(robots_txt_result, str) and 'was extracted' in robots_txt_result
        sitemap_found = isinstance(sitemap_xml_result, str) and 'was extracted' in sitemap_xml_result

        sitemap_links_count = 0
        if isinstance(sitemap_links_content, str):
            sitemap_links_count = len([l for l in sitemap_links_content.splitlines() if l.strip()])

        ip_table_rows = []
        if isinstance(ip, str) and not is_placeholder(ip):
            ip_table_rows.append({'ip': ip, 'source': 'Primary domain'})
        for i in clean_list(subdomain_ip):
            ip_table_rows.append({'ip': i, 'source': 'Subdomain (aggregate)'})

        tech_table_rows = []
        for category, items in [
            ('Web Server', web_servers), ('CMS', cms),
            ('Programming Language', programming_languages),
            ('Web Framework', web_frameworks),
            ('Analytics', analytics),
            ('JavaScript Framework', javascript_frameworks),
        ]:
            for item in clean_list(items):
                tech_table_rows.append({'category': category, 'name': item})

        social_table_rows = []
        if isinstance(common_socials, dict):
            for platform, links in common_socials.items():
                for link in clean_list(links):
                    social_table_rows.append({'platform': platform, 'link': link})

        ports_clean = [p for p in (ports if isinstance(ports, list) else []) if not is_placeholder(p)]
        vulns_clean = [v for v in (vulns if isinstance(vulns, list) else []) if isinstance(v, str) and not is_placeholder(v)]
        hostnames_clean = clean_list(hostnames)
        cpes_clean = clean_list(cpes)
        tags_clean = clean_list(tags)
        subdomains_clean = [s for s in (subdomains if isinstance(subdomains, list) else []) if isinstance(s, str) and s]

        context = {
            'sh_domain': short_domain, 'case_comment': case_comment, 'full_url': url, 'ip_address': ip,
            'registrar': res['registrar'],
            'creation_date': res['creation_date'], 'expiration_date': res['expiration_date'],
            'name_servers': ', '.join(res['name_servers']), 'org': res['org'],
            'mails': mails, 'subdomain_mails': subdomain_mails_cleaned, 'subdomain_socials': social_medias,
            'subdomain_ip': subdomain_ip,
            'subdomains': subdomains_clean, 'fb_links': common_socials['Facebook'],
            'tw_links': common_socials['Twitter'], 'inst_links': common_socials['Instagram'],
            'tg_links': common_socials['Telegram'], 'tt_links': common_socials['TikTok'],
            'li_links': common_socials['LinkedIn'], 'vk_links': common_socials['VKontakte'],
            'yt_links': common_socials['YouTube'], 'wc_links': common_socials['WeChat'],
            'ok_links': common_socials['Odnoklassniki'], 'xcom_links': common_socials['X.com'],
            'robots_txt_result': robots_txt_result,
            'sitemap_xml_result': sitemap_xml_result,
            'sitemap_links': sitemap_links_status, 'web_servers': web_servers, 'cms': cms,
            'programming_languages': programming_languages, 'web_frameworks': web_frameworks,
            'analytics': analytics, 'ip_addresses': all_ips,
            'javascript_frameworks': javascript_frameworks,
            'ctime': report_ctime, 'a_tsf': subdomains_amount, 'mx_records': mx_records, 'issuer': issuer,
            'subject': subject, 'notBefore': notBefore, 'notAfter': notAfter,
            'commonName': commonName, 'serialNumber': serialNumber, 'ports': ports_clean, 'hostnames': hostnames_clean,
            'cpes': cpes_clean,
            'tags': tags_clean, 'vulns': vulns_clean, 'a_tsm': total_socials, 'pagesearch_ui_mark': pagesearch_ui_mark,
            'dorking_status': dorking_status,
            'add_dsi': add_dsi, 'ps_s': accessible_subdomains, 'ps_e': emails_amount, 'ps_f': files_counter,
            'ps_c': cookies_counter, 'ps_a': api_keys_counter,
            'ps_w': website_elements_counter, 'ps_p': exposed_passwords_counter, 'ss_l': total_links_counter,
            'ss_a': accessed_links_counter,
            "snapshotting_ui_mark": snapshotting_ui_mark,
            'virustotal_output': virustotal_output, 'securitytrails_output': securitytrails_output,
            'ps_string': ps_string, 'a_tops': total_ports,
            'a_temails': total_mails, 'a_tips': total_ips, 'a_tpv': total_vulns, 'robots_content': robots_content,
            'sitemap_xml_content': sitemap_content, 'sitemap_txt_content': sitemap_links_content,

            'graph_data': graph_data,
            'social_counts': social_counts,
            'dorking_enabled': dorking_enabled,
            'pagesearch_enabled': pagesearch_enabled,
            'snapshotting_enabled': snapshotting_enabled,
            'api_enabled': api_enabled,
            'robots_found': robots_found,
            'sitemap_found': sitemap_found,
            'sitemap_links_count': sitemap_links_count,
            'ip_table_rows': ip_table_rows,
            'tech_table_rows': tech_table_rows,
            'social_table_rows': social_table_rows,
            'hudsonrock_intel': hudsonrock_intel,
            'lunarcyber_intel': lunarcyber_intel,
        }

        html_report_name = report_folder + '//' + casename
        if generate_report(context, html_report_name, template_path):
            print(Fore.GREEN + "HTML report for {} case was created at {}".format(short_domain, report_ctime) + Style.RESET_ALL)
            print(Fore.GREEN + f"Scan elapsed time: {end}" + Style.RESET_ALL)
        pdf_blob = fp.get_blob(html_report_name)
        db.insert_blob('HTML', pdf_blob, db_casename, db_creation_date, case_comment, robots_content, sitemap_content, sitemap_links_content, dorking_content, api_scan_db)

        if delete_txt_files.lower() == 'y':
            files_to_remove = ['04-dorking_results.txt', '03-sitemap_links.txt', '02-sitemap.txt', '01-robots.txt']
            for file in files_to_remove:
                file_path = os.path.join(report_folder, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
        elif delete_txt_files.lower() == 'n':
            pass

    except Exception as e:
        print(Fore.RED + 'Unable to create HTML report. See journal for details')
        logging.error(f'HTML REPORT CREATION: ERROR. REASON: {e}')
