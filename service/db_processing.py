from colorama import Fore, Style
import os
import sqlite3
import sys

sys.path.append('apis//api_keys.db')

def db_connect():
    sqlite_connection = sqlite3.connect('report_storage.db')
    cursor = sqlite_connection.cursor()
    return cursor, sqlite_connection

def check_rsdb_presence(db_path):
    if not os.path.exists(db_path):
        print(Fore.RED + "Report storage database was not found. DPULSE will create it in a second" + Style.RESET_ALL)
        return False
    else:
        return True

def db_creation(db_path):
    cursor, sqlite_connection = db_connect()
    create_table_sql = """
    CREATE TABLE "report_storage" (
            "id" INTEGER NOT NULL UNIQUE,
            "report_file_extension" TEXT NOT NULL, 
            "report_content" BLOB NOT NULL,
            "comment" TEXT NOT NULL,
            "target" TEXT NOT NULL,
            "creation_date" INTEGER NOT NULL,
            "dorks_results" TEXT,
            "robots_text" TEXT,
            "sitemap_text" TEXT,
            "sitemap_file" TEXT,
            "api_scan" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    cursor.execute(create_table_sql)
    sqlite_connection.commit()
    sqlite_connection.close()

def db_select():
    cursor, sqlite_connection = db_connect()
    if_rows = "SELECT * FROM report_storage"
    cursor.execute(if_rows)
    rows = cursor.fetchall()
    if rows:
        try:
            select_query = "SELECT creation_date, report_file_extension, target, id, comment, dorks_results, robots_text, sitemap_text, sitemap_file, api_scan FROM report_storage;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            print(Fore.LIGHTMAGENTA_EX + "\n[DATABASE'S CONTENT]\n" + Style.RESET_ALL)
            for row in records:
                dorks_presence = robots_presence = sitemap_presence = "None"
                if len(row[4]) > 1:
                    dorks_presence = "In DB"
                if len(row[5]) > 1:
                    robots_presence = "In DB"
                if len(row[6]) > 1:
                    sitemap_presence = "In DB"
                print(Fore.LIGHTBLUE_EX + f"Case ID: {row[3]} | Case name: {row[2]} | Case file extension: {row[1]} | Case comment: {row[4]} | Case creation date: {row[0]} | Dorking: {dorks_presence} | robots.txt: {robots_presence} | sitemap.xml: {sitemap_presence} | API scan: {row[-1]}" + Style.RESET_ALL)
                data_presence_flag = True
        except sqlite3.Error as e:
            print(Fore.RED + "Failed to see storage database's content. Reason: {}".format(e))
            sqlite_connection.close()
            data_presence_flag = False
    else:
        print(Fore.RED + 'No data found in report storage database')
        sqlite_connection.close()
        data_presence_flag = False
    return cursor, sqlite_connection, data_presence_flag

def db_select_silent():
    cursor, sqlite_connection = db_connect()
    if_rows = "SELECT * FROM report_storage"
    cursor.execute(if_rows)
    rows = cursor.fetchall()
    if rows:
        try:
            select_query = "SELECT creation_date, report_file_extension, target, id, comment, dorks_results, robots_text, sitemap_text, sitemap_file, api_scan FROM report_storage;"
            cursor.execute(select_query)
        except sqlite3.Error as e:
            sqlite_connection.close()
    else:
        sqlite_connection.close()
    return cursor, sqlite_connection

def db_report_recreate(extracted_folder_name, id_to_extract):
    cursor, sqlite_connection = db_select_silent()
    cursor.execute("SELECT report_content FROM report_storage WHERE id=?", (id_to_extract,))
    try:
        blob = cursor.fetchone()
        if blob is not None:
            blob_data = blob[0]
            cursor.execute("SELECT report_file_extension FROM report_storage WHERE id=?", (id_to_extract,))
            report_file_extension = (cursor.fetchone())[0]
            if str(report_file_extension) == 'XLSX':
                with open(extracted_folder_name + '//report_extracted.xlsx', 'wb') as file:
                    file.write(blob_data)
            elif str(report_file_extension) == 'HTML':
                with open(extracted_folder_name + '//report_extracted.html', 'wb') as file:
                    file.write(blob_data)
        cursor.execute("SELECT dorks_results FROM report_storage WHERE id=?", (id_to_extract,))
        dorks_results = (cursor.fetchone())[0]
        with open(extracted_folder_name + '//dorks_extracted.txt', 'w') as file:
            file.write(dorks_results)
        cursor.execute("SELECT robots_text FROM report_storage WHERE id=?", (id_to_extract,))
        robots_results = (cursor.fetchone())[0]
        with open(extracted_folder_name + '//robots_extracted.txt', 'w') as file:
            file.write(robots_results)
        cursor.execute("SELECT sitemap_file FROM report_storage WHERE id=?", (id_to_extract,))
        sitemap_results = (cursor.fetchone())[0]
        with open(extracted_folder_name + '//sitemap_extracted.txt', 'w') as file:
            file.write(sitemap_results)
        cursor.execute("SELECT sitemap_text FROM report_storage WHERE id=?", (id_to_extract,))
        sitemap_links_results = (cursor.fetchone())[0]
        with open(extracted_folder_name + '//sitemap_links_extracted.txt', 'w') as file:
            file.write(sitemap_links_results)
        print(Fore.GREEN + "\nReport was successfully recreated from report storage database and saved in {} folder".format(extracted_folder_name))
    except Exception as e:
        print(Fore.RED + "Error appeared when recreating report from database. Reason: {}".format(e))

def insert_blob(report_file_type, pdf_blob, db_casename, creation_date, case_comment, robots, sitemap_xml, sitemap_links, dorking_results, api_scan_db): 
    try:
        sqlite_connection = sqlite3.connect('report_storage.db')
        cursor = sqlite_connection.cursor()
        print(Fore.GREEN + "Connected to report storage database")
        if 'No' in api_scan_db:
            api_scan_insert = 'No'
        elif 'VirusTotal' and 'SecurityTrails' in api_scan_db:
            api_scan_insert = 'VirusTotal and SecurityTrails'
        elif 'VirusTotal' in api_scan_db:
            api_scan_insert = 'VirusTotal'
        elif 'SecurityTrails' in api_scan_db:
            api_scan_insert = 'SecurityTrails'

        sqlite_insert_blob_query = """INSERT INTO report_storage
                                  (report_file_extension, report_content, creation_date, target, comment, sitemap_file, robots_text, sitemap_text, dorks_results, api_scan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        data_tuple = (report_file_type, pdf_blob, creation_date, db_casename, case_comment, sitemap_xml, robots, sitemap_links, dorking_results, api_scan_insert)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print(Fore.GREEN + "Scanning results are successfully saved in report storage database")
        cursor.close()
    except sqlite3.Error as e:
        print(Fore.RED + "Failed to insert scanning results in report storage database. Reason: {}".format(e))
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print(Fore.GREEN + "Database connection is successfully closed")

def check_api_keys(used_api_flag):
    for key in used_api_flag:
        conn = sqlite3.connect('apis//api_keys.db')
        cursor = conn.cursor()
        cursor.execute("SELECT api_key FROM api_keys WHERE id = ?", (key,))
        result = cursor.fetchone()
        if result[0] == 'YOUR_API_KEY':
            return False
    return True

def select_api_keys(mode):
    conn = sqlite3.connect('apis//api_keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, api_name, api_key, limitations FROM api_keys")
    rows = cursor.fetchall()
    for row in rows:
        if row[2] != 'YOUR_API_KEY':
            print(Fore.LIGHTBLUE_EX + f"ID: {row[0]} | API Name: {row[1]} | API Key: {row[2]} | Limitations: {row[3]}\n" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTBLUE_EX + f"ID: {row[0]} | API Name: {row[1]} | " + Style.RESET_ALL + Fore.RED + f"API Key: {row[2]} " + Fore.LIGHTBLUE_EX + f"| Limitations: {row[3]}\n" + Style.RESET_ALL)
    if mode == 'printing':
        conn.close()
        return None
    else:
        pass
        return cursor, conn
