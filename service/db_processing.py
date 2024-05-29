from colorama import Fore, Style
import os
import sqlite3

def db_connect():
    sqlite_connection = sqlite3.connect('report_storage.db')
    cursor = sqlite_connection.cursor()
    print(Fore.GREEN + "Successfully established SQLite3 DB connection")
    return cursor, sqlite_connection

def db_creation(db_path):
    if not os.path.exists(db_path):
        print(Fore.RED + "Report storage database was not found. DPULSE will create it in a second" + Style.RESET_ALL)
        cursor, sqlite_connection = db_connect()
        create_table_sql = """
        CREATE TABLE "report_storage" (
            "id" INTEGER NOT NULL UNIQUE,
            "report_content" BLOB NOT NULL,
            "comment" TEXT NOT NULL,
            "target" TEXT NOT NULL,
            "creation_date" INTEGER NOT NULL,
            "dorks_results" TEXT,
            "robots_text" TEXT,
            "sitemap_text" TEXT,
            "sitemap_file" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        cursor.execute(create_table_sql)
        sqlite_connection.commit()
        sqlite_connection.close()
        print(Fore.GREEN + "Successfully created report storage database" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "Report storage database exists" + Style.RESET_ALL)

def db_select():
    db_creation('report_storage.db')
    cursor, sqlite_connection = db_connect()
    if_rows = "SELECT * FROM report_storage"
    cursor.execute(if_rows)
    rows = cursor.fetchall()
    if rows:
        try:
            select_query = "SELECT creation_date, target, id, comment, dorks_results, robots_text, sitemap_text, sitemap_file FROM report_storage;"
            cursor.execute(select_query)
            records = cursor.fetchall()
            for row in records:
                dorks_presence = robots_presence = sitemap_presence = "None"
                if len(row[4]) > 1:
                    dorks_presence = "In DB"
                if len(row[5]) > 1:
                    robots_presence = "In DB"
                if len(row[6]) > 1:
                    sitemap_presence = "In DB"
                print(Fore.LIGHTBLUE_EX + f"Case ID: {row[2]} | Case comment: {row[3]} | Case creation date: {row[0]} | Case name: {row[1]} | Dorks: {dorks_presence} | robots.txt: {robots_presence} | sitemap.xml: {sitemap_presence}" + Style.RESET_ALL)
        except sqlite3.Error as e:
            print(Fore.RED + "Failed to see storage database's content. Reason: {}".format(e))
            sqlite_connection.close()
    else:
        print(Fore.RED + 'No data found in report storage database')
        sqlite_connection.close()
        return None
    return cursor, sqlite_connection

def db_report_recreate(extracted_folder_name, id_to_extract):
    cursor, sqlite_connection = db_select()
    cursor.execute("SELECT report_content FROM report_storage WHERE id=?", (id_to_extract,))
    pdf_blob = cursor.fetchone()
    if pdf_blob is not None:
        blob_data = pdf_blob[0]
        with open(extracted_folder_name + '//report_extracted.pdf', 'wb') as file:
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

def insert_blob(pdf_blob, db_casename, creation_date, case_comment, robots, sitemap_xml, sitemap_links, dorking_results):
    try:
        sqlite_connection = sqlite3.connect('report_storage.db')
        cursor = sqlite_connection.cursor()
        print(Fore.GREEN + "Connected to report storage database")

        sqlite_insert_blob_query = """INSERT INTO report_storage
                                  (report_content, creation_date, target, comment, dorks_results, robots_text, sitemap_text, sitemap_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

        data_tuple = (pdf_blob, creation_date, db_casename, case_comment, dorking_results, robots, sitemap_links, sitemap_xml)
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
