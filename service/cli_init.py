import sys
from config_processing import read_config
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

try:
    from colorama import Fore, Back, Style
    from pyfiglet import Figlet
    from rich.console import Console
except ImportError as e:
    print(Fore.RED + "Import error appeared. Reason: {}".format(e) + Style.RESET_ALL)
    sys.exit()


class Menu:
    def __init__(self):
        self.console = Console()

    def welcome_menu(self):
        config_values = read_config()
        preview_style = (config_values['preview_color']).lower()
        wm_font = (config_values['wm_font']).lower()
        fig = Figlet(font=wm_font)
        print('\n')
        combined_panel = Panel(
            Text.assemble(
                (fig.renderText('DPULSE'), preview_style),
                ("\n", ""),
                ("DPULSE-CLI - v1.3.2 stable - OSINT-TECHNOLOGIES\n\n", "magenta bold"),
                ("Visit our pages:\n", "white"),
                ("GitHub: ", "white"), ("https://github.com/OSINT-TECHNOLOGIES\n", "blue underline"),
                ("PyPi: ", "white"), ("https://pypi.org/project/dpulse/\n", "blue underline"),
                ("Docs: ", "white"), ("https://dpulse.readthedocs.io", "blue underline")
            ),
            title="Current version info",
            box=box.ROUNDED,
            border_style="magenta"
        )

        self.console.print(combined_panel)

    def print_main_menu(self):
        table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="magenta",
            show_edge=False
        )

        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Description", style="white")
        table.add_row("1.", "Target selection & scanning")
        table.add_row("2.", "General settings")
        table.add_row("3.", "Dorking module manager")
        table.add_row("4.", "Report storage DB manager")
        table.add_row("5.", "API modules manager")
        table.add_row("6.", "Help (browser will be opened!)")
        table.add_row("7.", "[red]Exit DPULSE[/red]")

        menu_panel = Panel(
            table,
            title="[white on magenta]MAIN MENU[/white on magenta]",
            border_style="magenta"
        )

        self.console.print("\n")
        self.console.print(menu_panel)

    def print_settings_menu(self):
        table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="magenta",
            show_edge=False
        )

        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Description", style="white")

        table.add_row("1.", "Print current config file")
        table.add_row("2.", "Edit config file")
        table.add_row("3.", "Clear journal content")
        table.add_row("4.", "[red]Return to main menu[/red]")

        menu_panel = Panel(
            table,
            title="[white on magenta]SETTINGS MENU[/white on magenta]",
            border_style="magenta"
        )

        self.console.print("\n")
        self.console.print(menu_panel)

    def print_db_menu(self):
        table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="magenta",
            show_edge=False
        )

        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Description", style="white")

        table.add_row("1.", "Show database content")
        table.add_row("2.", "Recreate report from database")
        table.add_row("3.", "[red]Return to main menu[/red]")

        menu_panel = Panel(
            table,
            title="[white on magenta]REPORTS DATABASE MANAGER[/white on magenta]",
            border_style="magenta"
        )

        self.console.print("\n")
        self.console.print(menu_panel)

    def dorking_db_manager(self):
        table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="magenta",
            show_edge=False
        )

        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Description", style="white")

        table.add_row("1.", "Generate custom Dorking DB")
        table.add_row("2.", "[red]Return to main menu[/red]")

        menu_panel = Panel(
            table,
            title="[white on magenta]DORKING DB MANAGER[/white on magenta]",
            border_style="magenta"
        )

        self.console.print("\n")
        self.console.print(menu_panel)

    def api_manager(self):
        table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="magenta",
            show_edge=False
        )

        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Description", style="white")

        table.add_row("1.", "Add API key")
        table.add_row("2.", "Restore reference API Keys DB")
        table.add_row("3.", "[red]Return to main menu[/red]")

        menu_panel = Panel(
            table,
            title="[white on magenta]API KEYS DB MANAGER[/white on magenta]",
            border_style="magenta"
        )

        self.console.print("\n")
        self.console.print(menu_panel)


def print_prescan_summary(short_domain, report_filetype, pagesearch_ui_mark, dorking_ui_mark, used_api_ui, case_comment, snapshotting_ui_mark):
    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="magenta"
    )

    table.add_column("Parameter", style="green")
    table.add_column("Value", style="cyan bold")

    table.add_row("Determined target:", short_domain)
    table.add_row("Report type:", report_filetype.lower())
    table.add_row("PageSearch conduction:", pagesearch_ui_mark)
    table.add_row("Dorking conduction:", dorking_ui_mark)
    table.add_row("APIs scan:", used_api_ui)
    table.add_row("Snapshotting conduction:", snapshotting_ui_mark)
    table.add_row("Case comment:", case_comment)

    summary_panel = Panel(
        table,
        title="[magenta]PRE-SCAN SUMMARY[/magenta]",
        border_style="magenta"
    )

    Console().print("\n")
    Console().print(summary_panel)

def print_api_db_msg():
    print(Fore.GREEN + "\nYou've entered custom Dorking DB generator!\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Remember some rules in order to successfully create your custom Dorking DB:" + Style.RESET_ALL)
    print(Fore.GREEN + "[1] - dork_id variable must be unique, starting with 1 and then +1 every new dork" + Style.RESET_ALL)
    print(Fore.GREEN + "[2] - When it comes to define domain in dork, put {} in it\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Examples: related:{}, site:{} inurl:login and so on\n" + Style.RESET_ALL)

def print_ps_cli_report(subdomains_list,  accessible_subdomains, ps_emails_return, files_counter, cookies_counter, api_keys_counter, website_elements_counter, exposed_passwords_counter):
    if len(subdomains_list) == 0:
        print(Fore.GREEN + "\nDuring subdomains analysis:\n[+] Total " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{len(subdomains_list)}" + Style.RESET_ALL + Fore.GREEN + " subdomains were checked" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nDuring subdomains analysis:\n[+] Total " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{len(subdomains_list)}" + Style.RESET_ALL + Fore.GREEN + " subdomains were checked" + Style.RESET_ALL)
    if accessible_subdomains == 0:
        print(Fore.GREEN + "[+] Among them " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{accessible_subdomains}" + Style.RESET_ALL + Fore.GREEN + " subdomains were accessible" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Among them " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{accessible_subdomains}" + Style.RESET_ALL + Fore.GREEN + " subdomains were accessible" + Style.RESET_ALL)
    if len(ps_emails_return) == 0:
        print(Fore.GREEN + "[+] In result, " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{len(ps_emails_return)}" + Style.RESET_ALL + Fore.GREEN + " unique e-mail addresses were found" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] In result, " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{len(ps_emails_return)}" + Style.RESET_ALL + Fore.GREEN + " unique e-mail addresses were found" + Style.RESET_ALL)
    if files_counter == 0:
        print(Fore.GREEN + "[+] Also, " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{files_counter}" + Style.RESET_ALL + Fore.GREEN + " files were extracted" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Also, " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{files_counter}" + Style.RESET_ALL + Fore.GREEN + " files were extracted" + Style.RESET_ALL)
    if cookies_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{cookies_counter}" + Style.RESET_ALL + Fore.GREEN + " cookies with values" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{cookies_counter}" + Style.RESET_ALL + Fore.GREEN + " cookies with values" + Style.RESET_ALL)
    if api_keys_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{api_keys_counter}" + Style.RESET_ALL + Fore.GREEN + " API keys" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{api_keys_counter}" + Style.RESET_ALL + Fore.GREEN + " API keys" + Style.RESET_ALL)
    if website_elements_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{website_elements_counter}" + Style.RESET_ALL + Fore.GREEN + " different web page elements" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{website_elements_counter}" + Style.RESET_ALL + Fore.GREEN + " different web page elements" + Style.RESET_ALL)
    if exposed_passwords_counter == 0:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTRED_EX + Style.BRIGHT + f"{exposed_passwords_counter}" + Style.RESET_ALL + Fore.GREEN + " exposed passwords" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "[+] Found " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{exposed_passwords_counter}" + Style.RESET_ALL + Fore.GREEN + " exposed passwords" + Style.RESET_ALL)
