from colorama import Fore, Style
#from pagesearch_reports import report_creation WIP
from pagesearch_parsers import subdomains_parser

def normal_search(to_search_array, report_folder):
    print(Fore.GREEN + "Conducting PageSearch in normal mode. Please, be patient, it may take a long time\n" + Style.RESET_ALL)
    subdomains_parser(to_search_array[0], report_folder)

