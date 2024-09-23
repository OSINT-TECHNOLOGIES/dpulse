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
        #return "Google Dorking results file was not created"

def save_results_to_txt(folderpath, queries, pages=10):
    txt_writepath = folderpath + '//04-dorking_results.txt'
    with open(txt_writepath, 'w') as f:
        for i, query in enumerate(queries, start=1):
            f.write(f"QUERY #{i}: {query}\n")
            results = solid_google_dorking(query, pages)
            print(Fore.GREEN + f"Dorking with {query} dork")
            if not results:
                f.write("=> NO RESULT FOUND\n")
                print(Fore.RED + f"No results were found for {query} dork")
            else:
                for result in results:
                    f.write(f"=> {result}\n")
            f.write("\n")
    print(Fore.GREEN + "Google Dorking results successfully saved in TXT file" + Style.RESET_ALL)
    #return "File with gathered links was successfully created"

def transfer_results_to_xlsx(queries, pages=10):
    dorking_return_list = []
    for i, query in enumerate(queries, start=1):
        dorking_return_list.append(f"QUERY #{i}: {query}\n")
        results = solid_google_dorking(query, pages)
        if not results:
            dorking_return_list.append("NO RESULT FOUND\n")
        else:
            for result in results:
                dorking_return_list.append(f"{result}\n")
        dorking_return_list.append("\n")
    #return "File with gathered links was successfully created", dorking_return_list

def dorks_files_check():
    dorks_path = 'dorking//'
    dorks_files = ['iot_dorking.db', 'files_dorking.db', 'basic_dorking.db']
    dorks_files_counter = 0
    for dork_files in dorks_files:
        files_path = os.path.join(dorks_path, dork_files)
        if os.path.isfile(files_path):
            dorks_files_counter += 1
        else:
            pass

    if dorks_files_counter == 3:
        print(Fore.GREEN + "Dorks databases presence: OK" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Dorks databases presence: NOT OK\nSome files may not be in folder. Please compare dorking folder with the same folder on the official repository\n" + Style.RESET_ALL)
        sys.exit()
