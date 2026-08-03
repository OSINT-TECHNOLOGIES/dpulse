import sys
import os
import re
import sqlite3
import configparser
import socket
import requests
import whois as whois_lib
import dns.resolver
from pathlib import Path
from time import perf_counter
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

if getattr(sys, 'frozen', False):
    RESOURCE_DIR = Path(sys._MEIPASS)
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    RESOURCE_DIR = Path(__file__).resolve().parent
    BASE_DIR = RESOURCE_DIR

os.chdir(BASE_DIR)
os.environ['DPULSE_TEMPLATE_DIR'] = str(RESOURCE_DIR)

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'datagather_modules'))
sys.path.append(str(BASE_DIR / 'service'))
sys.path.append(str(BASE_DIR / 'reporting_modules'))
sys.path.append(str(BASE_DIR / 'dorking'))
sys.path.append(str(BASE_DIR / 'apis'))
sys.path.append(str(BASE_DIR / 'snapshotting'))
sys.path.append(str(BASE_DIR / 'pagesearch'))

from config_processing import create_config, check_cfg_presence
import db_processing as db
from data_assembler import DataProcessing
from misc import domain_precheck, time_processing
import html_report_creation as html_rc
import networking_processor as npmod

app = FastAPI(title="DPULSE Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

data_processing = DataProcessing()

DOMAIN_PATTERN = re.compile(r"^(?!-)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$")
YYYYMMDD_PATTERN = re.compile(r"^\d{8}$")
SAFE_FOLDER_PATTERN = re.compile(r'^report_[\w\-.,() ]+$')
SAFE_FILENAME_PATTERN = re.compile(r'^[A-Za-z0-9_\-.]+\.html$')

CONFIG_PATH = BASE_DIR / 'service' / 'config.ini'
REPORT_STORAGE_DB = BASE_DIR / 'report_storage.db'
API_KEYS_DB = BASE_DIR / 'apis' / 'api_keys.db'

API_ID_TO_NAME = {'1': 'VirusTotal', '2': 'SecurityTrails', '3': 'HudsonRock'}


def is_valid_domain(domain: str) -> bool:
    return bool(DOMAIN_PATTERN.match(domain))


def is_valid_yyyymmdd(value: str) -> bool:
    return bool(YYYYMMDD_PATTERN.match(value or ''))


def validate_report_folder(folder: str) -> Path:
    if not folder or '..' in folder or not SAFE_FOLDER_PATTERN.match(folder):
        raise HTTPException(status_code=400, detail="Invalid folder name")
    full_path = (BASE_DIR / folder).resolve()
    if not str(full_path).startswith(str(BASE_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Report folder not found")
    return full_path


def inject_base_tag(html_text: str, base_url: str) -> str:
    base_tag = f'<base href="{base_url}">'
    if re.search(r'<head[^>]*>', html_text, re.IGNORECASE):
        return re.sub(r'(<head[^>]*>)', r'\1' + base_tag, html_text, count=1, flags=re.IGNORECASE)
    elif re.search(r'<html[^>]*>', html_text, re.IGNORECASE):
        return re.sub(r'(<html[^>]*>)', r'\1<head>' + base_tag + '</head>', html_text, count=1, flags=re.IGNORECASE)
    else:
        return base_tag + html_text


def bootstrap():
    if not check_cfg_presence():
        create_config()
    if not db.check_rsdb_presence(str(REPORT_STORAGE_DB)):
        db.db_creation(str(REPORT_STORAGE_DB))
    if not API_KEYS_DB.exists():
        API_KEYS_DB.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(API_KEYS_DB)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY,
                api_name TEXT,
                api_key TEXT,
                limitations TEXT
            )
        """)
        cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (1, 'VirusTotal', 'YOUR_API_KEY', 'Free tier: 4 req/min')")
        cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (2, 'SecurityTrails', 'YOUR_API_KEY', 'Free tier: 50 req/month')")
        cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (3, 'HudsonRock', 'YOUR_API_KEY', 'No key required actually')")
        conn.commit()
        conn.close()


@app.on_event("startup")
def on_startup():
    bootstrap()


@app.get("/health")
def health():
    return {"status": "ok"}


class ScanRequest(BaseModel):
    domain: str = Field(..., description="Target domain, e.g. example.com")
    comment: str = Field(default="")
    use_virustotal: bool = False
    use_securitytrails: bool = False
    use_hudsonrock: bool = False
    hudsonrock_username: Optional[str] = None
    snapshot_mode: str = Field(default="n", description="n=none, s=screenshot, p=page copy, w=wayback")
    wayback_from: Optional[str] = None
    wayback_to: Optional[str] = None


class ScanResponse(BaseModel):
    status: str
    domain: str
    report_id: Optional[int] = None
    report_folder: Optional[str] = None
    report_file: Optional[str] = None
    report_html: Optional[str] = None
    elapsed: Optional[str] = None
    snapshot_type: Optional[str] = None
    has_screenshot: bool = False
    has_html_copy: bool = False
    wayback_files: List[str] = []


@app.post("/scan", response_model=ScanResponse)
def run_scan(request: ScanRequest):
    short_domain = request.domain.strip().lower()
    case_comment = request.comment.strip()

    if not short_domain:
        raise HTTPException(status_code=400, detail="Domain must not be empty")
    if not is_valid_domain(short_domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    url = f"http://{short_domain}/"

    if not domain_precheck(short_domain):
        raise HTTPException(status_code=422, detail="Domain is not accessible")

    snapshot_mode = (request.snapshot_mode or 'n').lower()
    if snapshot_mode not in ('n', 's', 'p', 'w'):
        raise HTTPException(status_code=400, detail="Invalid snapshot_mode, must be one of: n, s, p, w")

    wayback_from = 'N'
    wayback_to = 'N'
    if snapshot_mode == 'w':
        wayback_from = (request.wayback_from or '').strip()
        wayback_to = (request.wayback_to or '').strip()
        if not is_valid_yyyymmdd(wayback_from) or not is_valid_yyyymmdd(wayback_to):
            raise HTTPException(status_code=400, detail="Wayback dates must be in YYYYMMDD format")

    used_api_ids: List[str] = []
    if request.use_virustotal:
        used_api_ids.append('1')
    if request.use_securitytrails:
        used_api_ids.append('2')
    if request.use_hudsonrock:
        used_api_ids.append('3')

    used_api_flag = used_api_ids if used_api_ids else ['Empty']
    username = request.hudsonrock_username if (request.use_hudsonrock and request.hudsonrock_username) else None

    snapshotting_ui_mark = 'No'
    if snapshot_mode == 's':
        snapshotting_ui_mark = "Yes, domain's main page snapshotting as a screenshot"
    elif snapshot_mode == 'p':
        snapshotting_ui_mark = "Yes, domain's main page snapshotting as a .HTML file"
    elif snapshot_mode == 'w':
        snapshotting_ui_mark = "Yes, domain's main page snapshotting using Wayback Machine"

    try:
        start = perf_counter()

        data_array, report_info_array = data_processing.data_gathering(
            short_domain,
            url,
            'html',
            'n',
            '',
            0,
            'n',
            used_api_flag,
            snapshot_mode,
            username,
            wayback_from,
            wayback_to,
        )

        end_time_str = time_processing(perf_counter() - start)

        html_rc.report_assembling(
            short_domain, url, case_comment,
            data_array, report_info_array,
            'No', end_time_str, snapshotting_ui_mark
        )

        report_folder = report_info_array[3]
        casename = report_info_array[0]
        report_path = BASE_DIR / report_folder
        report_file_path = report_path / casename

        html_content = None
        if report_file_path.exists():
            html_content = report_file_path.read_text(encoding='utf-8')

        report_id = None
        conn = sqlite3.connect(REPORT_STORAGE_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM report_storage")
        row = cursor.fetchone()
        if row and row[0]:
            report_id = row[0]
        conn.close()

        has_screenshot = (report_path / "screensnapshot.png").exists()
        has_html_copy = (report_path / "domain_html_copy.html").exists()
        wayback_files: List[str] = []
        wb_dir = report_path / "wayback_snapshots"
        if wb_dir.exists():
            wayback_files = sorted([f.name for f in wb_dir.iterdir() if f.is_file()])

        return ScanResponse(
            status="success",
            domain=short_domain,
            report_id=report_id,
            report_folder=str(report_folder),
            report_file=str(report_file_path),
            report_html=html_content,
            elapsed=end_time_str,
            snapshot_type=None if snapshot_mode == 'n' else snapshot_mode,
            has_screenshot=has_screenshot,
            has_html_copy=has_html_copy,
            wayback_files=wayback_files,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {e}")


@app.get("/snapshot/screenshot")
def get_screenshot(folder: str):
    folder_path = validate_report_folder(folder)
    screenshot_path = folder_path / "screensnapshot.png"
    if not screenshot_path.exists():
        raise HTTPException(status_code=404, detail="Screenshot not found")
    return FileResponse(screenshot_path, media_type="image/png")


@app.get("/snapshot/html", response_class=HTMLResponse)
def get_html_copy(folder: str):
    folder_path = validate_report_folder(folder)
    html_path = folder_path / "domain_html_copy.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="HTML copy not found")

    content = html_path.read_text(encoding='utf-8', errors='replace')

    meta_path = folder_path / "domain_html_copy.html.meta.json"
    if meta_path.exists():
        try:
            import json
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            source_url = meta.get('source_url')
            if source_url:
                content = inject_base_tag(content, source_url)
        except Exception:
            pass

    return content


@app.get("/snapshot/wayback/list")
def list_wayback_snapshots(folder: str):
    folder_path = validate_report_folder(folder)
    wayback_dir = folder_path / "wayback_snapshots"
    if not wayback_dir.exists():
        return {"files": []}
    files = sorted([f.name for f in wayback_dir.iterdir() if f.is_file()])
    return {"files": files}


@app.get("/snapshot/wayback/file", response_class=HTMLResponse)
def get_wayback_file(folder: str, filename: str):
    folder_path = validate_report_folder(folder)
    if not filename or '..' in filename or not SAFE_FILENAME_PATTERN.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    file_path = folder_path / "wayback_snapshots" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Snapshot file not found")
    return file_path.read_text(encoding='utf-8', errors='replace')


class ReportSummary(BaseModel):
    id: int
    target: str
    extension: str
    comment: str
    created: str
    api_scan: str


@app.get("/reports", response_model=List[ReportSummary])
def list_reports():
    if not REPORT_STORAGE_DB.exists():
        return []
    conn = sqlite3.connect(REPORT_STORAGE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, target, report_file_extension, comment, creation_date, api_scan
        FROM report_storage ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        ReportSummary(
            id=r[0], target=r[1], extension=r[2],
            comment=r[3] or "", created=str(r[4]), api_scan=r[5] or "No"
        ) for r in rows
    ]


@app.get("/reports/{report_id}")
def get_report(report_id: int):
    conn = sqlite3.connect(REPORT_STORAGE_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT report_content, report_file_extension, target FROM report_storage WHERE id=?",
        (report_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    content, extension, target = row
    if str(extension).upper() != 'HTML':
        raise HTTPException(status_code=400, detail="Only HTML reports can be viewed inline")

    html_content = content.decode('utf-8', errors='replace')
    return {"id": report_id, "target": target, "html": html_content}


@app.delete("/reports/{report_id}")
def delete_report(report_id: int):
    conn = sqlite3.connect(REPORT_STORAGE_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM report_storage WHERE id=?", (report_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}


class ApiKeyInfo(BaseModel):
    id: int
    name: str
    is_set: bool
    masked_key: str
    limitations: str


class ApiKeyUpdate(BaseModel):
    api_key: str


@app.get("/api-keys", response_model=List[ApiKeyInfo])
def get_api_keys():
    conn = sqlite3.connect(API_KEYS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, api_name, api_key, limitations FROM api_keys")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        key = r[2] or ''
        is_set = key != 'YOUR_API_KEY' and bool(key.strip())
        if is_set and len(key) > 8:
            masked = key[:4] + '...' + key[-4:]
        elif is_set:
            masked = '****'
        else:
            masked = 'Not set'
        result.append(ApiKeyInfo(
            id=r[0], name=r[1], is_set=is_set,
            masked_key=masked, limitations=r[3] or ""
        ))
    return result


@app.post("/api-keys/{key_id}")
def update_api_key(key_id: int, payload: ApiKeyUpdate):
    new_key = payload.api_key.strip()
    if not new_key:
        raise HTTPException(status_code=400, detail="API key must not be empty")

    conn = sqlite3.connect(API_KEYS_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE api_keys SET api_key=? WHERE id=?", (new_key, key_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="API key ID not found")
    return {"status": "updated"}


@app.post("/api-keys/{key_id}/reset")
def reset_api_key(key_id: int):
    conn = sqlite3.connect(API_KEYS_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE api_keys SET api_key='YOUR_API_KEY' WHERE id=?", (key_id,))
    conn.commit()
    conn.close()
    return {"status": "reset"}


@app.get("/config")
def get_config():
    if not check_cfg_presence():
        create_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    result = {}
    for section in config.sections():
        if section == 'USER-AGENTS':
            continue
        result[section] = dict(config[section])
    return result


class ConfigUpdate(BaseModel):
    section: str
    option: str
    value: str


@app.post("/config")
def update_config(payload: ConfigUpdate):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    section = payload.section

    if not config.has_section(section):
        raise HTTPException(status_code=400, detail=f"Section '{section}' does not exist")
    if not config.has_option(section, payload.option):
        raise HTTPException(status_code=400, detail=f"Option '{payload.option}' does not exist in section '{section}'")

    config.set(section, payload.option, payload.value)
    with open(CONFIG_PATH, 'w') as f:
        config.write(f)
    return {"status": "updated"}


@app.post("/journal/clear")
def clear_journal():
    journal_path = BASE_DIR / 'journal.log'
    with open(journal_path, 'w'):
        pass
    return {"status": "cleared"}


@app.get("/utils/dns-lookup")
def utils_dns_lookup(domain: str, record_type: str = "A"):
    record_type = record_type.upper()
    try:
        answers = dns.resolver.resolve(domain, record_type)
        values = [str(r) for r in answers]
        return {"domain": domain, "record_type": record_type, "values": values}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"DNS lookup failed: {e}")


@app.get("/utils/whois")
def utils_whois(domain: str):
    try:
        w = whois_lib.whois(domain)
        return {
            "domain": domain,
            "registrar": str(w.registrar) if w.registrar else "N/A",
            "creation_date": str(w.creation_date) if w.creation_date else "N/A",
            "expiration_date": str(w.expiration_date) if w.expiration_date else "N/A",
            "name_servers": [str(ns) for ns in w.name_servers] if w.name_servers else [],
            "org": str(w.org) if w.org else "N/A",
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"WHOIS lookup failed: {e}")


@app.get("/utils/reverse-dns")
def utils_reverse_dns(ip: str):
    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)
        return {"ip": ip, "hostname": hostname, "aliases": aliases}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Reverse DNS failed: {e}")


@app.get("/utils/geolocate")
def utils_geolocate(ip: str):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = resp.json()
        if data.get("status") == "fail":
            raise HTTPException(status_code=422, detail=data.get("message", "Geolocation failed"))
        return {
            "ip": ip,
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Geolocation failed: {e}")


@app.get("/utils/check-url")
def utils_check_url(url: str):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        resp = requests.get(url, timeout=8, allow_redirects=True)
        return {"url": url, "status_code": resp.status_code, "final_url": resp.url, "reachable": True}
    except Exception as e:
        return {"url": url, "reachable": False, "error": str(e)}


@app.get("/utils/security-headers")
def utils_security_headers(url: str):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        resp = requests.get(url, timeout=8)
        headers_of_interest = [
            "Strict-Transport-Security", "Content-Security-Policy",
            "X-Frame-Options", "X-Content-Type-Options",
            "Referrer-Policy", "Permissions-Policy", "X-XSS-Protection"
        ]
        result = {h: resp.headers.get(h, "Not set") for h in headers_of_interest}
        return {"url": url, "headers": result}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to fetch headers: {e}")


@app.get("/utils/ssl-check")
def utils_ssl_check(domain: str):
    try:
        issuer, subject, notBefore, notAfter, commonName, serialNumber = npmod.get_ssl_certificate(domain)
        return {
            "domain": domain, "issuer": issuer, "subject": subject,
            "not_before": notBefore, "not_after": notAfter,
            "common_name": commonName, "serial_number": serialNumber,
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"SSL check failed: {e}")


@app.get("/utils/cve-info")
def utils_cve_info(cve: str):
    try:
        resp = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}", timeout=10)
        data = resp.json()
        vulns = data.get("vulnerabilities", [])
        if not vulns:
            raise HTTPException(status_code=404, detail="CVE not found in NVD")
        cve_data = vulns[0]["cve"]
        descriptions = cve_data.get("descriptions", [])
        description = next((d["value"] for d in descriptions if d["lang"] == "en"), "No description available")
        metrics = cve_data.get("metrics", {})
        severity = "Unknown"
        score = None
        for metric_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            if metric_key in metrics and metrics[metric_key]:
                cvss_data = metrics[metric_key][0]["cvssData"]
                severity = metrics[metric_key][0].get("baseSeverity", cvss_data.get("baseSeverity", "Unknown"))
                score = cvss_data.get("baseScore")
                break
        return {"cve": cve, "description": description, "severity": severity, "score": score}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to fetch CVE info: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
