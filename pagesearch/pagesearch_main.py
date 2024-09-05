from colorama import Fore, Style
from pagesearch_parsers import subdomains_parser
from pagesearch_deepsearch import sitemap_inspection

def normal_search(to_search_array, report_folder, keywords, keywords_flag):
    print(Fore.GREEN + "Conducting PageSearch. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    ps_emails_return, accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list = subdomains_parser(to_search_array[0], report_folder, keywords, keywords_flag)
    return ps_emails_return, accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list

def sitemap_inspection_search(report_folder):
    print(Fore.GREEN + "Conducting PageSearch in Sitemap Inspection mode. Please, be patient, it will take a long time\n" + Style.RESET_ALL)
    ds_emails_return, total_links_counter, accessed_links_counter, emails_amount = sitemap_inspection(report_folder)
    return ds_emails_return, total_links_counter, accessed_links_counter, emails_amount


