from colorama import Fore, Style
from pagesearch_parsers import subdomains_parser

def normal_search(to_search_array, report_folder, keywords):
    print(Fore.GREEN + "Conducting PageSearch. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    subdomains_parser(to_search_array[0], report_folder, keywords)

