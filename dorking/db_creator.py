import sqlite3
from colorama import Fore
import os

def manage_dorks(db_name):
    db_prep_string = str(db_name) + '.db'
    if os.path.exists('dorking//' + db_prep_string):
        print(Fore.RED + f"Sorry, but {db_prep_string} database is already exists. Choose other name for your custom DB")
        pass
    else:
        conn = sqlite3.connect('dorking//' + str(db_prep_string))
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dorks (
            dork_id INTEGER PRIMARY KEY,
            dork TEXT NOT NULL
        )
        ''')
        conn.commit()

        def add_dork(dork_id, dork):
            try:
                cursor.execute('INSERT INTO dorks (dork_id, dork) VALUES (?, ?)', (dork_id, dork))
                conn.commit()
                print(Fore.GREEN + "Successfully added new dork")
            except sqlite3.IntegrityError:
                print(Fore.RED + "Attention, dork_id variable must be unique")
    
        while True:
            dork_id = input(Fore.YELLOW + "Enter dork_id (or 'q' to quit this mode and save changes) >> ")
            if dork_id.lower() == 'q':
                break
            dork = input(Fore.YELLOW + "Enter new dork >> ")
            add_dork(int(dork_id), dork)
        conn.close()
