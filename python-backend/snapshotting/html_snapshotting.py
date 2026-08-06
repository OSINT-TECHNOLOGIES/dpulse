import os
import json
import requests
from colorama import Fore, Style


def save_page_as_html(url, filename):
    try:
        print(Fore.GREEN + "Getting web page's content" + Style.RESET_ALL)
        response = requests.get(url, timeout=15)
        print(Fore.GREEN + "Creating .HTML file" + Style.RESET_ALL)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

        meta_path = filename + '.meta.json'
        with open(meta_path, 'w', encoding='utf-8') as meta_file:
            json.dump({'source_url': url}, meta_file)

        print(Fore.GREEN + ".HTML snapshot was successfully created" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        return False
