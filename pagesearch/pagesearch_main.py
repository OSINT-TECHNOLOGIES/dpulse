from colorama import Fore, Style
from pagesearch_parsers import subdomains_parser

def normal_search(to_search_array, report_folder, keywords, keywords_flag):
    print(Fore.GREEN + "Conducting PageSearch. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    ps_emails_return, accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list = subdomains_parser(to_search_array[0], report_folder, keywords, keywords_flag)
    return ps_emails_return, accessible_subdomains, emails_amount, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter, keywords_messages_list
