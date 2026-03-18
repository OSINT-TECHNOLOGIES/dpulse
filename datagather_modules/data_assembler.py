import sys
import os
from datetime import datetime
from urllib.parse import urlparse

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


STEP_IP = "[1/11] Getting domain IP address"
STEP_WHOIS = "[2/11] Gathering WHOIS information"
STEP_EMAILS = "[3/11] Processing e-mail gathering"
STEP_SUBDOMAINS = "[4/11] Processing subdomain gathering"
STEP_SOCIALS = "[5/11] Processing social media gathering"
STEP_SUBDOMAIN_ANALYSIS = "[6/11] Processing subdomain analysis"
STEP_SSL = "[7/11] Processing SSL certificate gathering"
STEP_DNS = "[8/11] Processing DNS records gathering"
STEP_ROBOTS_SITEMAP = "[9/11] Extracting robots.txt and sitemap.xml"
STEP_TECHNOLOGIES = "[10/11] Gathering info about website technologies"
STEP_SHODAN = "[11/11] Processing Shodan InternetDB search"
MSG_NOT_FOUND_TPL = "{name} links were not found"
MSG_NO_SUBDOMAINS_FOUND = "No subdomains were found"
MSG_SITEMAP_NOT_PARSED = "Sitemap links were not parsed"
MSG_ROBOTS_NOT_RETRIEVED = "robots.txt was not retrieved"
MSG_SITEMAP_NOT_RETRIEVED = "sitemap.xml was not retrieved"

MSG_PS_NOT_SELECTED = (
    "No results because user did not select PageSearch for this scan"
)
MSG_PS_NO_SUBDOMAINS = "No results because no subdomains were found"
MSG_PS_LISTING_NOT_SELECTED = (
    "No PageSearch listing provided because user did not select "
    "PageSearch mode for this scan"
)
MSG_PS_LISTING_NO_SUBDOMAINS = (
    "No PageSearch listing provided because no subdomains were found"
)
MSG_PS_NO_CATEGORIES = (
    "No results because PageSearch does not gather these categories"
)
MSG_PS_CANT_START = (
    "Cannot start PageSearch because no subdomains were detected"
)

MSG_DORKING_NOT_SELECTED = "Google Dorking mode was not selected for this scan"

MSG_VT_NOT_SELECTED = (
    "No results because user did not select VirusTotal API scan"
)
MSG_ST_NOT_SELECTED = (
    "No results because user did not select SecurityTrails API scan"
)
MSG_HR_NOT_SELECTED = (
    "No results because user did not select HudsonRock API scan"
)

MSG_KEYWORDS_NOT_FOUND = "No keywords were found"
MSG_KEYWORDS_NO_DATA = "No data was gathered because no subdomains were found"


SOCIAL_KEYS = [
    'Facebook', 'Twitter', 'Instagram', 'Telegram', 'TikTok',
    'LinkedIn', 'VKontakte', 'YouTube', 'Odnoklassniki', 'WeChat', 'X.com',
]


DORKING_DB = {
    'basic':  ('basic_dorking.db',       'basic_dorks'),
    'iot':    ('iot_dorking.db',          'iot_dorks'),
    'files':  ('files_dorking.db',        'files_dorks'),
    'admins': ('adminpanels_dorking.db',  'admins_dorks'),
    'web':    ('webstructure_dorking.db', 'web_dorks'),
}


_SSL_DEFAULTS = ('N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')
_TECH_DEFAULTS = ([], [], [], [], [], [])
_INTERNETDB_DEFAULTS = ([], [], [], [], [])


def make_socials_dict(with_not_found: bool = False) -> dict:
    if with_not_found:
        return {
            name: [MSG_NOT_FOUND_TPL.format(name=name)]
            for name in SOCIAL_KEYS
        }
    return {name: [] for name in SOCIAL_KEYS}


def ensure_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def is_real_url(value: str) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def establishing_dork_db_connection(dorking_flag: str) -> tuple:
    flag = dorking_flag.lower().strip()

    if flag in DORKING_DB:
        db_file, table = DORKING_DB[flag]
        return os.path.join('dorking', db_file), table

    if flag.startswith('custom+'):
        parts = flag.split('+', 1)
        if len(parts) < 2 or not parts[1].strip():
            raise ValueError(
                f"Custom dorking flag must follow 'custom+filename' format, "
                f"got: '{dorking_flag}'"
            )
        return os.path.join('dorking', parts[1].strip()), 'dorks'

    raise ValueError(f"Invalid dorking flag: '{dorking_flag}'")



def _print_step(msg: str) -> None:
    print(Fore.GREEN + msg + Style.RESET_ALL)


def _print_section(msg: str) -> None:
    print(Fore.LIGHTMAGENTA_EX + msg + Style.RESET_ALL)


def _print_error(msg: str) -> None:
    print(Fore.RED + msg + Style.RESET_ALL)


def _safe_step(step_name: str, func, *args, default=None):
    try:
        return func(*args)
    except Exception as e:
        _print_error(f"[ERROR] {step_name} failed: {e}")
        logging.exception(f"Error during {step_name}")
        return default


def _unpack_tuple(result, expected_len: int, defaults: tuple):
    if isinstance(result, tuple) and len(result) == expected_len:
        return result
    return defaults



class DataProcessing:
    @staticmethod
    def report_preprocessing(short_domain: str) -> dict:
        now = datetime.now()
        report_ctime = now.strftime('%d-%m-%Y, %H:%M:%S')
        files_ctime = now.strftime('(%d-%m-%Y, %Hh%Mm%Ss)')
        files_body = f"{short_domain.replace('.', '')}_{files_ctime}"
        report_folder = f"report_{files_body}"

        os.makedirs(report_folder, exist_ok=True)

        return {
            'casename': f"{files_body}.html",
            'db_casename': short_domain.replace('.', ''),
            'db_creation_date': now.strftime('%Y%m%d'),
            'report_folder': report_folder,
            'files_ctime': files_ctime,
            'report_ctime': report_ctime,
            'robots_filepath': os.path.join(report_folder, '01-robots.txt'),
            'sitemap_filepath': os.path.join(report_folder, '02-sitemap.txt'),
            'sitemap_links_filepath': os.path.join(
                report_folder, '03-sitemap_links.txt'
            ),
        }


    @staticmethod
    def _gather_basic_info(short_domain: str, url: str) -> tuple:
        _print_step(STEP_IP)
        ip = _safe_step("IP gathering", cp.ip_gather, short_domain, default='N/A')

        _print_step(STEP_WHOIS)
        whois_info = _safe_step(
            "WHOIS gathering", cp.whois_gather, short_domain, default={}
        )

        _print_step(STEP_EMAILS)
        mails = _safe_step(
            "E-mail gathering", cp.contact_mail_gather, url, default=[]
        )

        _print_step(STEP_SUBDOMAINS)
        raw = _safe_step(
            "Subdomain gathering", cp.subdomains_gather,
            url, short_domain, default=([], 0)
        )
        subdomains, subdomains_amount = _unpack_tuple(raw, 2, ([], 0))

        _print_step(STEP_SOCIALS)
        social_medias = _safe_step(
            "Social media gathering", cp.sm_gather, url,
            default=make_socials_dict(with_not_found=True)
        )

        return ip, whois_info, mails, subdomains, subdomains_amount, social_medias


    @staticmethod
    def _gather_subdomain_details(subdomains: list) -> tuple:
        _print_step(STEP_SUBDOMAIN_ANALYSIS)
        raw = _safe_step(
            "Subdomain analysis",
            cp.domains_reverse_research, subdomains, 'html',
            default=([], make_socials_dict(), [])
        )
        defaults = ([], make_socials_dict(), [])
        subdomain_mails, sd_socials, subdomain_ip = _unpack_tuple(raw, 3, defaults)
        return subdomain_mails, sd_socials, subdomain_ip


    @staticmethod
    def _gather_network_info(short_domain: str, url: str,
                             ip: str, ctx: dict) -> dict:
        _print_step(STEP_SSL)
        ssl = _unpack_tuple(
            _safe_step(
                "SSL certificate", np.get_ssl_certificate,
                short_domain, default=_SSL_DEFAULTS
            ), 6, _SSL_DEFAULTS
        )

        _print_step(STEP_DNS)
        mx_records = _safe_step(
            "DNS records", np.get_dns_info,
            short_domain, 'html', default=[]
        )

        _print_step(STEP_ROBOTS_SITEMAP)
        robots = _safe_step(
            "robots.txt", np.get_robots_txt,
            short_domain, ctx['robots_filepath'],
            default=MSG_ROBOTS_NOT_RETRIEVED
        )
        sitemap = _safe_step(
            "sitemap.xml", np.get_sitemap_xml,
            short_domain, ctx['sitemap_filepath'],
            default=MSG_SITEMAP_NOT_RETRIEVED
        )
        sitemap_links = _safe_step(
            "Sitemap links", np.extract_links_from_sitemap,
            ctx['sitemap_links_filepath'], ctx['sitemap_filepath'],
            default=MSG_SITEMAP_NOT_PARSED
        )

        _print_step(STEP_TECHNOLOGIES)
        tech = _unpack_tuple(
            _safe_step(
                "Technology detection", np.get_technologies,
                url, default=_TECH_DEFAULTS
            ), 6, _TECH_DEFAULTS
        )

        _print_step(STEP_SHODAN)
        idb = _unpack_tuple(
            _safe_step(
                "Shodan InternetDB", np.query_internetdb,
                ip, 'html', default=_INTERNETDB_DEFAULTS
            ), 5, _INTERNETDB_DEFAULTS
        )

        return {
            'issuer': ssl[0], 'subject': ssl[1],
            'notBefore': ssl[2], 'notAfter': ssl[3],
            'commonName': ssl[4], 'serialNumber': ssl[5],
            'mx_records': mx_records,
            'robots_txt_result': robots,
            'sitemap_xml_result': sitemap,
            'sitemap_links_status': sitemap_links,
            'web_servers': tech[0], 'cms': tech[1],
            'programming_languages': tech[2],
            'web_frameworks': tech[3],
            'analytics': tech[4],
            'javascript_frameworks': tech[5],
            'ports': idb[0], 'hostnames': idb[1],
            'cpes': idb[2], 'tags': idb[3], 'vulns': idb[4],
        }


    @staticmethod
    def _merge_socials(social_medias, sd_socials) -> tuple:
        if not isinstance(social_medias, dict):
            logging.warning(
                'social_medias is %s, expected dict; replacing', type(social_medias)
            )
            social_medias = make_socials_dict()
        if not isinstance(sd_socials, dict):
            logging.warning(
                'sd_socials is %s, expected dict; replacing', type(sd_socials)
            )
            sd_socials = make_socials_dict()

        all_keys = set(SOCIAL_KEYS) | social_medias.keys() | sd_socials.keys()
        common_socials = {}
        total_socials = 0

        for key in all_keys:
            combined = (
                ensure_list(social_medias.get(key, []))
                + ensure_list(sd_socials.get(key, []))
            )
            seen = set()
            deduped = []
            for v in combined:
                if v not in seen:
                    seen.add(v)
                    deduped.append(v)

            real_links = [v for v in deduped if is_real_url(v)]
            if real_links:
                common_socials[key] = real_links
                total_socials += len(real_links)
            else:
                common_socials[key] = [MSG_NOT_FOUND_TPL.format(name=key)]

        return common_socials, total_socials


    @staticmethod
    def _run_pagesearch(pagesearch_flag: str, subdomains: list,
                        social_medias: dict, sd_socials: dict,
                        report_folder: str, keywords, keywords_flag) -> dict:

        not_selected = {
            'ps_emails_return': '',
            'accessible_subdomains': MSG_PS_NOT_SELECTED,
            'emails_amount': MSG_PS_NOT_SELECTED,
            'files_counter': MSG_PS_NOT_SELECTED,
            'cookies_counter': MSG_PS_NOT_SELECTED,
            'api_keys_counter': MSG_PS_NOT_SELECTED,
            'website_elements_counter': MSG_PS_NOT_SELECTED,
            'exposed_passwords_counter': MSG_PS_NOT_SELECTED,
            'total_links_counter': MSG_PS_NOT_SELECTED,
            'accessed_links_counter': MSG_PS_NOT_SELECTED,
            'keywords_messages_list': MSG_PS_NOT_SELECTED,
            'ps_string': MSG_PS_LISTING_NOT_SELECTED,
        }

        if pagesearch_flag.lower() != 'y':
            return not_selected

        has_subdomains = (
            isinstance(subdomains, list)
            and subdomains
            and subdomains[0] != MSG_NO_SUBDOMAINS_FOUND
        )
        if not has_subdomains:
            _print_error(MSG_PS_CANT_START)
            return {
                'ps_emails_return': '',
                'accessible_subdomains': MSG_PS_NO_SUBDOMAINS,
                'emails_amount': MSG_PS_NO_SUBDOMAINS,
                'files_counter': MSG_PS_NO_SUBDOMAINS,
                'cookies_counter': MSG_PS_NO_SUBDOMAINS,
                'api_keys_counter': MSG_PS_NO_SUBDOMAINS,
                'website_elements_counter': MSG_PS_NO_SUBDOMAINS,
                'exposed_passwords_counter': MSG_PS_NO_SUBDOMAINS,
                'total_links_counter': MSG_PS_NO_SUBDOMAINS,
                'accessed_links_counter': MSG_PS_NO_SUBDOMAINS,
                'keywords_messages_list': [MSG_KEYWORDS_NO_DATA],
                'ps_string': MSG_PS_LISTING_NO_SUBDOMAINS,
            }

        _print_section("[STARTED EXTENDED DOMAIN SCAN WITH PAGESEARCH]")
        (
            ps_emails_return, accessible_subdomains, emails_amount,
            files_counter, cookies_counter, api_keys_counter,
            website_elements_counter, exposed_passwords_counter,
            keywords_messages_list,
        ), ps_string = subdomains_parser(
            subdomains, report_folder, keywords, keywords_flag
        )

        if not keywords_messages_list:
            keywords_messages_list = [MSG_KEYWORDS_NOT_FOUND]

        _print_section("[ENDED EXTENDED DOMAIN SCAN WITH PAGESEARCH]\n")
        return {
            'ps_emails_return': ps_emails_return,
            'accessible_subdomains': accessible_subdomains,
            'emails_amount': emails_amount,
            'files_counter': files_counter,
            'cookies_counter': cookies_counter,
            'api_keys_counter': api_keys_counter,
            'website_elements_counter': website_elements_counter,
            'exposed_passwords_counter': exposed_passwords_counter,
            'total_links_counter': MSG_PS_NO_CATEGORIES,
            'accessed_links_counter': MSG_PS_NO_CATEGORIES,
            'keywords_messages_list': keywords_messages_list,
            'ps_string': ps_string,
        }


    @staticmethod
    def _run_dorking(dorking_flag: str, short_domain: str,
                     report_folder: str) -> dict:
        if dorking_flag.lower() == 'n':
            return {
                'dorking_status': MSG_DORKING_NOT_SELECTED,
                'dorking_file_path': MSG_DORKING_NOT_SELECTED,
            }

        dorking_db_path, table = establishing_dork_db_connection(dorking_flag)
        label = dorking_flag.upper()
        _print_section(
            f"[STARTED EXTENDED DOMAIN SCAN WITH {label} DORKING TABLE]"
        )
        dorking_status, dorking_file_path = dp.save_results_to_txt(
            report_folder, table,
            get_dorking_query(short_domain, dorking_db_path, table)
        )
        _print_section(
            f"[ENDED EXTENDED DOMAIN SCAN WITH {label} DORKING TABLE]\n"
        )
        return {
            'dorking_status': dorking_status,
            'dorking_file_path': dorking_file_path,
        }


    @staticmethod
    def _run_api_scans(used_api_flag: list, short_domain: str,
                       ip: str, mails: list, username) -> dict:
        if used_api_flag == ['Empty']:
            return {
                'virustotal_output': MSG_VT_NOT_SELECTED,
                'securitytrails_output': MSG_ST_NOT_SELECTED,
                'hudsonrock_output': MSG_HR_NOT_SELECTED,
                'api_scan_db': ['No'],
            }

        api_scan_db = []
        _print_section("[STARTED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]")

        if '1' in used_api_flag:
            vt = _safe_step(
                "VirusTotal API", api_virustotal_check,
                short_domain, default=MSG_VT_NOT_SELECTED
            )
            api_scan_db.append('VirusTotal')
        else:
            vt = MSG_VT_NOT_SELECTED

        if '2' in used_api_flag:
            st = _safe_step(
                "SecurityTrails API", api_securitytrails_check,
                short_domain, default=MSG_ST_NOT_SELECTED
            )
            api_scan_db.append('SecurityTrails')
        else:
            st = MSG_ST_NOT_SELECTED

        if '3' in used_api_flag:
            if username is None or (
                isinstance(username, str) and username.lower() == 'n'
            ):
                username = None
            hr = _safe_step(
                "HudsonRock API", api_hudsonrock_check,
                short_domain, ip, mails, username,
                default=MSG_HR_NOT_SELECTED
            )
            api_scan_db.append('HudsonRock')
        else:
            hr = MSG_HR_NOT_SELECTED

        _print_section("[ENDED EXTENDED DOMAIN SCAN WITH 3RD PARTY API]\n")
        return {
            'virustotal_output': vt,
            'securitytrails_output': st,
            'hudsonrock_output': hr,
            'api_scan_db': api_scan_db or ['No'],
        }


    @staticmethod
    def _run_snapshotting(snapshotting_flag: str, url: str,
                          short_domain: str, report_folder: str,
                          from_date, end_date) -> None:
        flag = snapshotting_flag.lower()
        if flag not in ('s', 'p', 'w'):
            return

        config_values = read_config()
        installed_browser = config_values.get('installed_browser', '')
        _print_section("[STARTED DOMAIN SNAPSHOTTING]")

        if flag == 's':
            _safe_step(
                "Screenshot", take_screenshot,
                installed_browser, url,
                os.path.join(report_folder, 'screensnapshot.png')
            )
        elif flag == 'p':
            _safe_step(
                "HTML page save", save_page_as_html,
                url,
                os.path.join(report_folder, 'domain_html_copy.html')
            )
        elif flag == 'w':
            if not from_date or not end_date:
                _print_error(
                    "[ERROR] from_date and end_date are required "
                    "for archive snapshotting"
                )
            else:
                _safe_step(
                    "Archive snapshot", download_snapshot,
                    short_domain, from_date, end_date, report_folder
                )

        _print_section("[ENDED DOMAIN SNAPSHOTTING]\n")


    def data_gathering(self, short_domain: str, url: str,
                       pagesearch_flag: str, keywords, keywords_flag: str,
                       dorking_flag: str, used_api_flag: list,
                       snapshotting_flag: str, username,
                       from_date, end_date) -> tuple:

        if not short_domain or not isinstance(short_domain, str):
            raise ValueError(f"Invalid short_domain: {short_domain!r}")
        if not url or not is_real_url(url):
            raise ValueError(f"Invalid URL: {url!r}")
        if not isinstance(pagesearch_flag, str) or pagesearch_flag.lower() not in ('y', 'n'):
            raise ValueError(f"pagesearch_flag must be 'y' or 'n', got: {pagesearch_flag!r}")
        if not isinstance(dorking_flag, str) or not dorking_flag.strip():
            raise ValueError(f"Invalid dorking_flag: {dorking_flag!r}")
        if not isinstance(used_api_flag, list):
            raise ValueError(f"used_api_flag must be a list, got: {type(used_api_flag)}")
        if not isinstance(snapshotting_flag, str):
            raise ValueError(f"Invalid snapshotting_flag: {snapshotting_flag!r}")

        ctx = self.report_preprocessing(short_domain)
        casename = ctx['casename']
        ctime = ctx['files_ctime']
        report_folder = ctx['report_folder']

        logging.info(
            '### THIS LOG PART FOR %s CASE, TIME: %s STARTS HERE',
            casename, ctime
        )

        _print_section("\n[STARTED BASIC DOMAIN SCAN]")

        ip, whois_info, mails, subdomains, subdomains_amount, social_medias = \
            self._gather_basic_info(short_domain, url)

        subdomain_mails, sd_socials, subdomain_ip = \
            self._gather_subdomain_details(subdomains)

        net = self._gather_network_info(short_domain, url, ip, ctx)

        common_socials, total_socials = self._merge_socials(
            social_medias, sd_socials
        )

        total_ports = len(net['ports']) if isinstance(net['ports'], list) else 0
        total_ips = (
            (len(subdomain_ip) if isinstance(subdomain_ip, list) else 0) + 1
        )
        total_vulns = len(net['vulns']) if isinstance(net['vulns'], list) else 0

        _print_section("[ENDED BASIC DOMAIN SCAN]\n")

        ps = self._run_pagesearch(
            pagesearch_flag, subdomains, social_medias, sd_socials,
            report_folder, keywords, keywords_flag
        )
        dork = self._run_dorking(dorking_flag, short_domain, report_folder)
        api = self._run_api_scans(
            used_api_flag, short_domain, ip, mails, username
        )
        self._run_snapshotting(
            snapshotting_flag, url, short_domain,
            report_folder, from_date, end_date
        )

        data_array = [
            ip, whois_info, mails, subdomains, subdomains_amount,
            social_medias, subdomain_mails, sd_socials, subdomain_ip,
            net['issuer'], net['subject'], net['notBefore'], net['notAfter'],
            net['commonName'], net['serialNumber'], net['mx_records'],
            net['robots_txt_result'], net['sitemap_xml_result'],
            net['sitemap_links_status'],
            net['web_servers'], net['cms'], net['programming_languages'],
            net['web_frameworks'], net['analytics'],
            net['javascript_frameworks'],
            net['ports'], net['hostnames'], net['cpes'],
            net['tags'], net['vulns'],
            common_socials, total_socials,
            ps['ps_emails_return'], ps['accessible_subdomains'],
            ps['emails_amount'], ps['files_counter'],
            ps['cookies_counter'], ps['api_keys_counter'],
            ps['website_elements_counter'],
            ps['exposed_passwords_counter'],
            ps['total_links_counter'], ps['accessed_links_counter'],
            ps['keywords_messages_list'],
            dork['dorking_status'], dork['dorking_file_path'],
            api['virustotal_output'], api['securitytrails_output'],
            api['hudsonrock_output'],
            ps['ps_string'],
            total_ports, total_ips, total_vulns,
        ]

        report_info_array = [
            casename, ctx['db_casename'], ctx['db_creation_date'],
            report_folder, ctime, 'html', ctx['report_ctime'],
            api['api_scan_db'], used_api_flag,
        ]

        logging.info('### THIS LOG PART FOR %s CASE, TIME: %s ENDS HERE', casename, ctime)
        return data_array, report_info_array
