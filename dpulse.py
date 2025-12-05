import sys
import os
import re
import shutil
import webbrowser
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Callable, Dict, List, Optional
from colorama import Fore, Style
from rich.console import Console

sys.path.append('datagather_modules')
sys.path.append('service')
sys.path.append('reporting_modules')
sys.path.append('dorking')
sys.path.append('apis')
sys.path.append('snapshotting')

from config_processing import create_config, check_cfg_presence, read_config, print_and_return_config
import db_processing as db
import cli_init
from dorking_handler import dorks_files_check
from data_assembler import DataProcessing
from logs_processing import logging
from db_creator import get_columns_amount, manage_dorks
from misc import domain_precheck, time_processing

console = Console()
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'service' / 'config.ini'
DORKING_DIR = BASE_DIR / 'dorking'
APIS_DIR = BASE_DIR / 'apis'

data_processing = DataProcessing()
cli = cli_init.Menu()

class ReportType(str, Enum):
    HTML = "html"
    #XLSX = "xlsx"

class SnapshotMode(str, Enum):
    NONE = "n"
    SCREENSHOT = "s"
    PAGE_COPY = "p"
    WAYBACK = "w"

@dataclass
class ScanOptions:
    short_domain: str
    url: str
    case_comment: str
    report_type: ReportType
    page_search: bool
    keywords: Optional[List[str]]
    dorking_flag: str
    used_api_ids: List[str]
    snapshot_mode: SnapshotMode
    username: Optional[str] = None
    wb_from: str = 'N'
    wb_to: str = 'N'
    pagesearch_ui_mark: str = 'No'
    snapshotting_ui_mark: str = 'No'

def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"y", "yes", "да", "si", "1", "true", "t"}

def ask_choice(prompt: str, choices: Dict[str, object], default: Optional[str] = None):
    while True:
        raw = input(prompt).strip().lower()
        if not raw and default is not None:
            if default in choices:
                return choices[default]
        if raw in choices:
            return choices[raw]
        print(Fore.RED + f"Invalid choice. Available: {', '.join(choices.keys())}" + Style.RESET_ALL)

def is_valid_domain(domain: str) -> bool:
    pattern = r"^(?!-)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))

def validate_yyyymmdd(s: str) -> bool:
    return bool(re.fullmatch(r"\d{8}", s))

def sanitize_db_filename(name: str) -> str:
    safe = os.path.basename(name).split('.')[0]
    if not re.fullmatch(r"[a-zA-Z0-9_\-]{1,50}", safe):
        raise ValueError("Invalid DB name")
    return safe

def compute_dorking_ui_mark(dorking_flag: str) -> str:
    try:
        if dorking_flag == 'n':
            return 'No'
        if dorking_flag.startswith('custom+'):
            db_name = dorking_flag.split('+', 1)[1]
            rc = get_columns_amount(str(DORKING_DIR / db_name), 'dorks')
            return f'Yes, Custom table dorking ({rc} dorks)'

        mapping = {
            'basic': 'basic_dorking.db',
            'iot': 'iot_dorking.db',
            'files': 'files_dorking.db',
            'admins': 'adminpanels_dorking.db',
            'web': 'webstructure_dorking.db'
        }
        if dorking_flag in mapping:
            db_name = mapping[dorking_flag]
            table = f'{dorking_flag}_dorks'
            rc = get_columns_amount(str(DORKING_DIR / db_name), table)
            return f'Yes, {dorking_flag} dorking ({rc} dorks)'
    except Exception as e:
        logging.error("Failed to compute dorking UI mark: %s", e, exc_info=True)
        return 'Dorking info unavailable'
    return 'No'

def process_report(options: ScanOptions):
    #import xlsx_report_creation as xlsx_rc
    import html_report_creation as html_rc
    with console.status("[magenta]Processing scan...[/magenta]", spinner="dots"):
        start = perf_counter()
        pagesearch_flag_str = 'y' if options.page_search else 'n'
        keywords_flag = 1 if (options.page_search and options.keywords and len(options.keywords) > 0) else 0
        keywords_payload = options.keywords if options.page_search else ''

        data_array, report_info_array = data_processing.data_gathering(
            options.short_domain,
            options.url,
            options.report_type.value,
            pagesearch_flag_str,
            keywords_payload,
            keywords_flag,
            options.dorking_flag,
            options.used_api_ids if options.used_api_ids else ['Empty'],
            options.snapshot_mode.value,
            options.username,
            options.wb_from,
            options.wb_to
        )
        end_time_str = time_processing(perf_counter() - start)

    if options.report_type == ReportType.HTML:
        html_rc.report_assembling(
            options.short_domain, options.url, options.case_comment,
            data_array, report_info_array,
            options.pagesearch_ui_mark, end_time_str, options.snapshotting_ui_mark
        )

def handle_scan():
    print(Fore.GREEN + "\nImported and activated reporting modules" + Style.RESET_ALL)
    while True:
        short_domain = input(Fore.YELLOW + "\nEnter target's domain name (or 'back' to return to the menu) >> ").strip()
        if short_domain.lower() == "back":
            print(Fore.RED + "\nReturned to main menu" + Style.RESET_ALL)
            return
        if not short_domain:
            print(Fore.RED + "\nEmpty domain names are not supported" + Style.RESET_ALL)
            continue
        if not is_valid_domain(short_domain):
            print(Fore.RED + '\nYour string does not match domain pattern' + Style.RESET_ALL)
            continue

        url = f"http://{short_domain}/"
        print(Fore.GREEN + 'Pinging domain...' + Style.RESET_ALL, end=' ')
        if domain_precheck(short_domain):
            print(Fore.GREEN + 'Entered domain is accessible. Continuation' + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Entered domain is not accessible. Scan is impossible" + Style.RESET_ALL)
            return

    case_comment = input(Fore.YELLOW + "Enter case comment >> ").strip()
    report_type = ReportType.HTML
    page_search = parse_bool(input(Fore.YELLOW + "Would you like to use PageSearch function? [Y/N] >> "))
    keywords = None
    pagesearch_ui_mark = 'No'
    if page_search:
        keywords_input = input(Fore.YELLOW + "Enter keywords (separate by comma) (or N) >> ").strip()
        if keywords_input.lower() != 'n':
            keywords_list = [k.strip() for k in keywords_input.split(',') if k.strip()]
            if not keywords_list:
                print(Fore.RED + "\nThis field must contain at least one keyword" + Style.RESET_ALL)
                return
            keywords = keywords_list
            pagesearch_ui_mark = f'Yes, with {keywords_list} keywords search'
        else:
            pagesearch_ui_mark = 'Yes, without keywords search'

    dorking_raw = input(Fore.YELLOW + "Select Dorking mode [Basic/IoT/Files/Admins/Web/Custom/N] >> ").strip().lower()
    if dorking_raw in {'basic', 'iot', 'files', 'admins', 'web'}:
        dorking_flag = dorking_raw
    elif dorking_raw == 'custom':
        try:
            custom_db_name = sanitize_db_filename(input(Fore.YELLOW + "Enter your custom Dorking DB name (no extension) >> ").strip())
        except ValueError as e:
            print(Fore.RED + f"\n{e}" + Style.RESET_ALL)
            return
        dorking_flag = f'custom+{custom_db_name}.db'
    elif dorking_raw == 'n':
        dorking_flag = 'n'
    else:
        print(Fore.RED + "\nInvalid Dorking mode. Please select mode among Basic/IoT/Files/Web/Admins/Custom or N" + Style.RESET_ALL)
        return

    api_yes = parse_bool(input(Fore.YELLOW + "Would you like to use 3rd party API in scan? [Y/N] >> "))
    used_api_ids: List[str] = ['Empty']
    username: Optional[str] = None
    used_api_ui = 'No'
    if api_yes:
        print("\n")
        db.select_api_keys('printing')
        print(Fore.GREEN + "\nPay attention that APIs with red-colored API Key field are unable to use!\n" + Style.RESET_ALL)
        to_use_api_flag = input(Fore.YELLOW + "Select APIs IDs you want to use in scan (separated by comma) >> ").strip()
        used_api_ids = [item.strip() for item in to_use_api_flag.split(',') if item.strip().isdigit()]
        if not used_api_ids:
            print(Fore.RED + "\nNo valid API IDs selected" + Style.RESET_ALL)
            return
        if '3' in used_api_ids:
            u = input(Fore.YELLOW + "If you know some username from this domain, please enter it here (or N if not) >> ").strip()
            username = None if u.lower() == 'n' else u
        if db.check_api_keys(used_api_ids):
            print(Fore.GREEN + 'Found API key. Continuation' + Style.RESET_ALL)
        else:
            print(Fore.RED + "\nAPI key was not found. Check if you've entered valid API key in API Keys DB" + Style.RESET_ALL)
            return
        used_api_ui = f'Yes, using APIs with following IDs: {", ".join(used_api_ids)}'

    snap_choice = ask_choice(
        Fore.YELLOW + "Select Snapshotting mode [S(creenshot)/P(age Copy)/W(ayback Machine)/N] >> ",
        {"s": SnapshotMode.SCREENSHOT, "p": SnapshotMode.PAGE_COPY, "w": SnapshotMode.WAYBACK, "n": SnapshotMode.NONE},
        default="n"
    )
    snapshotting_ui_mark = 'No'
    from_date = end_date = 'N'
    if snap_choice == SnapshotMode.SCREENSHOT:
        snapshotting_ui_mark = "Yes, domain's main page snapshotting as a screenshot"
    elif snap_choice == SnapshotMode.PAGE_COPY:
        snapshotting_ui_mark = "Yes, domain's main page snapshotting as a .HTML file"
    elif snap_choice == SnapshotMode.WAYBACK:
        from_date = input(Fore.YELLOW + 'Enter start date (YYYYMMDD format): ').strip()
        end_date = input(Fore.YELLOW + 'Enter end date (YYYYMMDD format): ').strip()
        if not (validate_yyyymmdd(from_date) and validate_yyyymmdd(end_date)):
            print(Fore.RED + "\nInvalid date format" + Style.RESET_ALL)
            return
        snapshotting_ui_mark = "Yes, domain's main page snapshotting using Wayback Machine"

    dorking_ui_mark = compute_dorking_ui_mark(dorking_flag)
    cli_init.print_prescan_summary(
        short_domain, report_type.value.upper(), pagesearch_ui_mark,
        dorking_ui_mark, used_api_ui, case_comment, snapshotting_ui_mark
    )

    options = ScanOptions(
        short_domain=short_domain,
        url=url,
        case_comment=case_comment,
        report_type=report_type,
        page_search=page_search,
        keywords=keywords,
        dorking_flag=dorking_flag,
        used_api_ids=used_api_ids,
        snapshot_mode=snap_choice,
        username=username,
        wb_from=from_date,
        wb_to=end_date,
        pagesearch_ui_mark=pagesearch_ui_mark,
        snapshotting_ui_mark=snapshotting_ui_mark,
    )

    try:
        process_report(options)
    except Exception as e:
        print(Fore.RED + "Error appeared during report processing. See journal for details" + Style.RESET_ALL)
        logging.error("PROCESS REPORT ERROR: %s", e, exc_info=True)

def handle_settings():
    cli.print_settings_menu()
    choice_settings = input(Fore.YELLOW + "\nEnter your choice >> ").strip()
    if choice_settings == '1':
        print_and_return_config()
    elif choice_settings == '2':
        config = print_and_return_config()
        section = input(Fore.YELLOW + "\nEnter the section you want to update >> ").strip()
        if not config.has_section(section.upper()):
            print(Fore.RED + "\nSection you've entered does not exist in config file. Please verify that section name is correct" + Style.RESET_ALL)
            return
        option = input(Fore.YELLOW + "Enter the option you want to update >> ").strip()
        if not config.has_option(section.upper(), option):
            print(Fore.RED + "\nOption you've entered does not exist in config file. Please verify that option name is correct" + Style.RESET_ALL)
            return
        value = input(Fore.YELLOW + "Enter the new value >> ").strip()
        config.set(section.upper(), option, value)
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        print(Fore.GREEN + "\nConfiguration updated successfully" + Style.RESET_ALL)
    elif choice_settings == '3':
        with open('journal.log', 'w'):
            print(Fore.GREEN + "Journal file was successfully cleared" + Style.RESET_ALL)
    elif choice_settings == '4':
        return

def handle_dorking_db():
    cli.dorking_db_manager()
    choice_dorking = input(Fore.YELLOW + "\nEnter your choice >> ").strip()
    if choice_dorking == '1':
        cli_init.print_api_db_msg()
        try:
            ddb_name = sanitize_db_filename(input(Fore.YELLOW + "Enter a name for your custom Dorking DB (no extension) >> ").strip())
        except ValueError as e:
            print(Fore.RED + f"{e}" + Style.RESET_ALL)
            return
        manage_dorks(ddb_name)
    elif choice_dorking == '2':
        return

def handle_db_menu():
    cli.print_db_menu()
    rsdb_presence = db.check_rsdb_presence('report_storage.db')
    if rsdb_presence:
        print(Fore.GREEN + "\nReport storage database presence: OK\n" + Style.RESET_ALL)
    else:
        db.db_creation('report_storage.db')
        print(Fore.GREEN + "Successfully created report storage database" + Style.RESET_ALL)

    choice_db = input(Fore.YELLOW + "Enter your choice >> ").strip()
    if choice_db == "1":
        db.db_select()
    elif choice_db == "2":
        cursor, sqlite_connection, data_presence_flag = db.db_select()
        if data_presence_flag:
            try:
                id_to_extract_raw = input(Fore.YELLOW + "\nEnter report ID you want to extract >> ").strip()
                if not id_to_extract_raw.isdigit():
                    print(Fore.RED + "Report ID must be a number" + Style.RESET_ALL)
                    return
                id_to_extract = int(id_to_extract_raw)
                extracted_folder_name = f'report_recreated_ID#{id_to_extract}'
                os.makedirs(extracted_folder_name)
                db.db_report_recreate(extracted_folder_name, id_to_extract)
            except FileExistsError:
                print(Fore.RED + "Report with the same recreated folder already exists. Please check its content or delete it and try again" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + "Error appeared when trying to recreate report from DB. See journal for details" + Style.RESET_ALL)
                logging.error("REPORT RECREATE ERROR: %s", e, exc_info=True)
        else:
            pass
    elif choice_db == "3":
        print(Fore.GREEN + "\nDatabase connection is successfully closed" + Style.RESET_ALL)
        return

def handle_docs():
    webbrowser.open('https://dpulse.readthedocs.io/en/latest/')

def handle_api_manager():
    cli.api_manager()
    choice_api = input(Fore.YELLOW + "\nEnter your choice >> ").strip()
    if choice_api == '1':
        cursor, conn = db.select_api_keys('updating')
        api_id_to_update = input(Fore.YELLOW + "\nEnter API's ID to update its key >> ").strip()
        new_api_key = input(Fore.YELLOW + "Enter new API key >> ").strip()
        try:
            cursor.execute("UPDATE api_keys SET api_key = ? WHERE id = ?", (new_api_key, api_id_to_update))
            conn.commit()
            print(Fore.GREEN + "\nSuccessfully added new API key" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Something went wrong when adding new API key. See journal for details" + Style.RESET_ALL)
            logging.error('API KEY ADDING: ERROR. REASON: %s', e, exc_info=True)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    elif choice_api == '2':
        try:
            (APIS_DIR / 'api_keys.db').unlink(missing_ok=True)
            print(Fore.GREEN + "Deleted old API Keys DB" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Failed to delete old API Keys DB" + Style.RESET_ALL)
            logging.error("DELETE API DB ERROR: %s", e, exc_info=True)
        try:
            shutil.copyfile(APIS_DIR / 'api_keys_reference.db', APIS_DIR / 'api_keys.db')
            print(Fore.GREEN + "Successfully restored reference API Keys DB" + Style.RESET_ALL)
        except FileNotFoundError:
            print(Fore.RED + "Reference API Keys DB was not found" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Failed to restore API Keys DB" + Style.RESET_ALL)
            logging.error("RESTORE API DB ERROR: %s", e, exc_info=True)
    else:
        return

def handle_exit():
    print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
    raise SystemExit

HANDLERS: Dict[str, Callable[[], None]] = {
    "1": handle_scan,
    "2": handle_settings,
    "3": handle_dorking_db,
    "4": handle_db_menu,
    "5": handle_api_manager,
    "6": handle_docs,
    "7": handle_exit,
}

def bootstrap():
    cfg_presence = check_cfg_presence()
    if cfg_presence:
        print(Fore.GREEN + "Global config file presence: OK" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Global config file presence: NOT OK" + Style.RESET_ALL)
        create_config()
        print(Fore.GREEN + "Successfully generated global config file" + Style.RESET_ALL)

    rsdb_presence = db.check_rsdb_presence('report_storage.db')
    if rsdb_presence:
        print(Fore.GREEN + "Report storage database presence: OK" + Style.RESET_ALL)
    else:
        db.db_creation('report_storage.db')
        print(Fore.GREEN + "Successfully created report storage database" + Style.RESET_ALL)

    dorks_files_check()

    try:
        _ = read_config()
        print('')
    except Exception as e:
        logging.error("CONFIG READ ERROR: %s", e, exc_info=True)
        print(Fore.RED + "Failed to read config. See journal for details" + Style.RESET_ALL)

    cli.welcome_menu()

def run():
    while True:
        try:
            cli.print_main_menu()
            choice = input(Fore.YELLOW + "\nEnter your choice >> ").strip()
            handler = HANDLERS.get(choice)
            if handler:
                handler()
            else:
                print(Fore.RED + "\nInvalid menu item. Please select between existing menu items" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\nDPULSE process was ended using keyboard" + Style.RESET_ALL)
            sys.exit()

if __name__ == "__main__":
    bootstrap()
    run()
