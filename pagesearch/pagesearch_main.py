from colorama import Fore, Style
from pagesearch_parsers import subdomains_parser
from pagesearch_deepsearch import sitemap_inspection

def normal_search(to_search_array, report_folder, keywords, keywords_flag):
    print(Fore.GREEN + "Conducting PageSearch. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    ps_emails_return, extract_text_from_pdf_status, find_keywords_in_pdfs_status = subdomains_parser(to_search_array[0], report_folder, keywords, keywords_flag)
    ps_to_log_list = [extract_text_from_pdf_status, find_keywords_in_pdfs_status]
    return ps_emails_return, ps_to_log_list

def sitemap_inspection_search(report_folder):
    print(Fore.GREEN + "Conducting PageSearch in Sitemap Inspection mode. Please, be patient, it will take a long time\n" + Style.RESET_ALL)
    ds_emails_return = sitemap_inspection(report_folder)
    if ds_emails_return is not None:
        return ds_emails_return
    else:
        return ""

