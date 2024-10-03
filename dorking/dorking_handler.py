import sys

try:
    import requests.exceptions
    from colorama import Fore, Style
    import mechanicalsoup
    import re
    import requests
    import sqlite3
    import os
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()

def get_dorking_query(short_domain, dorking_db_path, table):
    print(Fore.GREEN + "Getting dorking query from database")
    conn = sqlite3.connect(dorking_db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT dork FROM {table}")
    rows = cursor.fetchall()
    search_query = [row[0].format(short_domain) for row in rows]
    conn.close()
    return search_query

def get_columns_amount(dorking_db_path, table):
    conn = sqlite3.connect(dorking_db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    row_count = cursor.fetchone()[0]
    conn.close()
    return row_count

def solid_google_dorking(query, pages=100):
    try:
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://www.google.com/")
        browser.select_form('form[action="/search"]')
        browser["q"] = str(query)
        browser.submit_selected(btnName="btnG")
        result_query = []
        for page in range(pages):
            for link in browser.links():
                target = link.attrs['href']
                if (target.startswith('/url?') and not
                target.startswith("/url?q=http://webcache.googleusercontent.com")):
                    target = re.sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
                    result_query.append(target)
            try:
                browser.follow_link(nr=page + 1)
            except mechanicalsoup.LinkNotFoundError:
                break
        del result_query[-2:]
        return result_query
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + "Error while establishing connection with domain. No results will appear. Reason: {}".format(e) + Style.RESET_ALL)

def save_results_to_txt(folderpath, table, queries, pages=10):
    try:
        txt_writepath = folderpath + '//04-dorking_results.txt'
        total_results = []
        total_dorks_amount = len(queries)
        with open(txt_writepath, 'w') as f:
            print(Fore.GREEN + "Started Google Dorking. Please, be patient, it may take some time")
            dorked_query_counter = 0
            for i, query in enumerate(queries, start=1):
                f.write(f"QUERY #{i}: {query}\n")
                results = solid_google_dorking(query, pages)
                if not results:
                    f.write("=> NO RESULT FOUND\n")
                    total_results.append((query, 0))
                else:
                    total_results.append((query, len(results)))
                    for result in results:
                        f.write(f"=> {result}\n")
                f.write("\n")
                dorked_query_counter += 1
                print(Fore.GREEN + f"  Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{dorked_query_counter}/{total_dorks_amount}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL, end="\r")
        print(Fore.GREEN + "Google Dorking end. Results successfully saved in TXT file\n" + Style.RESET_ALL)
        print(Fore.GREEN + f"During Google Dorking with {table.upper()}:")
        for query, count in total_results:
            if count == 0:
                count = 'no results'
            print(Fore.GREEN + f"[+] Found results for " + Fore.LIGHTCYAN_EX + f'{query}' + Fore.GREEN + ' query: ' + Fore.LIGHTCYAN_EX + f'{count}' + Style.RESET_ALL)
        return f'Successfully dorked domain with {table.upper()} dorks table', txt_writepath
    except Exception:
        print(Fore.RED + 'Error appeared while trying to dork target. See journal for details')
        return 'Domain dorking failed. See journal for details', txt_writepath

def transfer_results_to_xlsx(table, queries, pages=10):
    print(Fore.GREEN + "Started Google Dorking. Please, be patient, it may take some time")
    dorked_query_counter = 0
    total_dorks_amount = len(queries)
    dorking_return_list = []
    for i, query in enumerate(queries, start=1):
        dorking_return_list.append(f"QUERY #{i}: {query}\n")
        results = solid_google_dorking(query, pages)
        if not results:
            dorking_return_list.append("NO RESULT FOUND\n")
        else:
            for result in results:
                dorking_return_list.append(f"{result}\n")
        dorked_query_counter += 1
        dorking_return_list.append("\n")
        print(Fore.GREEN + f"  Dorking with " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{dorked_query_counter}/{total_dorks_amount}" + Style.RESET_ALL + Fore.GREEN + " dork" + Style.RESET_ALL, end="\r")
    print(Fore.GREEN + "Google Dorking end. Results successfully saved in XLSX report\n" + Style.RESET_ALL)
    return f'Successfully dorked domain with {table.upper()} dorks table', dorking_return_list

def dorks_files_check():
    dorks_path = 'dorking//'
    dorks_files = ['iot_dorking.db', 'files_dorking.db', 'basic_dorking.db', 'adminpanels_dorking.db']
    dorks_files_counter = 0
    for dork_files in dorks_files:
        files_path = os.path.join(dorks_path, dork_files)
        if os.path.isfile(files_path):
            dorks_files_counter += 1
        else:
            pass
    if dorks_files_counter == 4:
        print(Fore.GREEN + "Dorks databases presence: OK" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Dorks databases presence: NOT OK\nSome files may not be in folder. Please compare dorking folder with the same folder on the official repository\n" + Style.RESET_ALL)
        sys.exit()
