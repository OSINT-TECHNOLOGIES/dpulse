import requests
import os
import re
import time
import sys
from colorama import Fore, Style
from config_processing import read_config

sys.path.append('service')
CDX_API = "http://web.archive.org/cdx/search/cdx"


def get_values_from_config():
    config_values = read_config()
    retries = int(config_values['wayback_retries_amount'])
    pause_between_requests = int(config_values['wayback_requests_pause'])
    return retries, pause_between_requests


def get_snapshots(url, from_date, to_date):
    params = {
        "url": url,
        "from": from_date,
        "to": to_date,
        "output": "json",
        "fl": "timestamp,original,mime",
        "filter": "statuscode:200",
        "collapse": "digest"
    }
    print(Fore.GREEN + f"Sending request to Wayback CDX API for {url}, period: {from_date} - {to_date}..." + Style.RESET_ALL)
    response = requests.get(CDX_API, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data[1:]


def inject_base_tag(html_text: str, base_url: str) -> str:
    base_tag = f'<base href="{base_url}">'
    if re.search(r'<head[^>]*>', html_text, re.IGNORECASE):
        return re.sub(r'(<head[^>]*>)', r'\1' + base_tag, html_text, count=1, flags=re.IGNORECASE)
    elif re.search(r'<html[^>]*>', html_text, re.IGNORECASE):
        return re.sub(r'(<html[^>]*>)', r'\1<head>' + base_tag + '</head>', html_text, count=1, flags=re.IGNORECASE)
    else:
        return base_tag + html_text


def snapshot_enum(snapshot_storage_folder, timestamp, original_url, index):
    retries, _ = get_values_from_config()
    archive_url = f"https://web.archive.org/web/{timestamp}id_/{original_url}"
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(archive_url, timeout=15)
            response.raise_for_status()
            html_content = inject_base_tag(response.text, original_url)
            filename = f"{index}_{timestamp}.html"
            filepath = os.path.join(snapshot_storage_folder, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(Fore.GREEN + f"[{index}] Downloaded: " + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{archive_url}" + Style.RESET_ALL)
            return True
        except Exception:
            print(Fore.RED + f"[{index}] Attempt {attempt}/{retries} failed for {archive_url}. Retrying..." + Style.RESET_ALL)
            time.sleep(2)
    print(Fore.RED + f"[{index}] Failed to download after {retries} attempts: {archive_url}" + Style.RESET_ALL)
    return False


def download_snapshot(short_domain, from_date, end_date, report_folder):
    _, pause_between_requests = get_values_from_config()
    snapshot_storage_folder = report_folder + '//wayback_snapshots'
    os.makedirs(snapshot_storage_folder, exist_ok=True)
    snapshots = get_snapshots(short_domain, from_date, end_date)
    print(Fore.GREEN + "Total snapshots found:" + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f" {len(snapshots)}" + Style.RESET_ALL)
    html_snapshots = [
        s for s in snapshots
        if len(s) >= 2 and (
            s[1].endswith(".html") or s[1].endswith("/") or s[1] == short_domain)
    ]
    print(Fore.GREEN + "HTML snapshots to download:" + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f" {len(html_snapshots)}\n" + Style.RESET_ALL)
    if not html_snapshots:
        print(Fore.RED + "No HTML snapshots available for download." + Style.RESET_ALL)
        return
    for i, (timestamp, original_url, *_) in enumerate(html_snapshots):
        snapshot_enum(snapshot_storage_folder, timestamp, original_url, i + 1)
        time.sleep(pause_between_requests)
    print(Fore.GREEN + "\nFinished downloading HTML snapshots" + Style.RESET_ALL)
