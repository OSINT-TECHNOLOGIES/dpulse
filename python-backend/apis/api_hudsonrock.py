import re
import time
import requests
from datetime import datetime, timezone
from typing import Optional, List

BASE_URL = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.15

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

MAX_EMAILS_CHECKED = 15
MAX_IPS_CHECKED = 5
MAX_GEO_LOOKUPS = 10

URL_CLASSIFICATION_RULES = [
    ("critical", "VPN / Remote Access / Admin Panel", [
        "vpn", "remote", "citrix", "rdp", "anydesk", "teamviewer", "pulse secure",
        "fortinet", "sonicwall", "globalprotect", "/admin", "cpanel", "phpmyadmin",
        "webmin", "plesk", "portainer", "jenkins", "wp-admin", "kubernetes"
    ]),
    ("high", "Webmail / Cloud Storage / Business SaaS", [
        "mail.", "webmail", "outlook", "office365", "salesforce", "hubspot",
        "zendesk", "jira", "confluence", "sharepoint", "onedrive", "drive.google",
        "dropbox", "aws.amazon", "console.cloud.google", "portal.azure"
    ]),
    ("medium", "Collaboration / Productivity Tools", [
        "slack", "zoom", "trello", "asana", "notion", "github", "gitlab",
        "bitbucket", "paypal", "stripe", "quickbooks", "workday", "bamboohr"
    ]),
]


def classify_url(url: str, type_field: str = "") -> dict:
    haystack = f"{url or ''} {type_field or ''}".lower()
    for criticality, label, keywords in URL_CLASSIFICATION_RULES:
        for kw in keywords:
            if kw in haystack:
                return {"criticality": criticality, "category_label": label}
    return {"criticality": "low", "category_label": "General / Uncategorized"}


def classify_attack_surface(employee_urls: list, client_urls: list) -> tuple:
    classified = []
    for u in employee_urls:
        info = classify_url(u.get("url", ""), u.get("type", ""))
        classified.append({**u, "audience": "Employee", **info})
    for u in client_urls:
        info = classify_url(u.get("url", ""), u.get("type", ""))
        classified.append({**u, "audience": "Client", **info})

    breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for item in classified:
        breakdown[item["criticality"]] = breakdown.get(item["criticality"], 0) + 1

    return classified, breakdown

COMMON_WEAK_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123",
    "111111", "1234567", "sunshine", "iloveyou", "admin", "welcome", "monkey",
    "login", "princess", "solo", "letmein", "dragon", "master", "hello",
    "freedom", "whatever", "qazwsx", "trustno1", "654321", "harley", "password1",
    "1234", "robert", "matthew", "jordan", "daniel", "andrew", "lakers",
    "andrea", "buster", "gandalf", "spanky", "bailey", "guitar", "michael",
    "amanda", "summer", "love", "ashley", "6969", "pepper", "computer",
    "michelle", "tigger", "hunter", "soccer", "anthony", "friends", "butterfly",
    "purple", "angel", "jennifer", "joshua", "bear", "1qaz2wsx", "hannah",
    "loveme", "hockey", "ranger", "yankees", "thomas", "tigers", "access",
    "startrek", "internet", "welcome1", "cheese", "banana", "shadow", "superman",
    "batman", "football", "baseball", "hockey1", "starwars", "changeme",
    "passw0rd", "qwerty123", "1q2w3e4r", "zaq12wsx", "123123", "aaaaaa",
    "000000", "121212", "asdfgh", "qwertyuiop", "asdasd", "iloveyou1",
    "monkey1", "dragon1", "master1", "admin123", "root", "toor", "test",
    "guest", "user", "demo", "temp", "default", "changeit", "letmein1",
    "qwerty1", "password123", "p@ssw0rd", "p@ssword", "welcome123", "abcd1234",
    "1qaz2wsx3edc", "zxcvbnm", "asdfghjkl", "555555", "777777", "888888"
}

WEAK_PATTERN_REGEXES = [
    re.compile(r'(spring|summer|fall|autumn|winter)\d{0,4}', re.IGNORECASE),
    re.compile(r'(19|20)\d{2}$'),
    re.compile(r'^(123456|1234567|12345678|123456789|1234567890|qwerty|asdf|zxcv|abcdef)', re.IGNORECASE),
    re.compile(r'(.)\1{3,}'),
]


def is_weak_password(pw: str) -> bool:
    if not pw:
        return False
    lowered = pw.lower()
    if lowered in COMMON_WEAK_PASSWORDS:
        return True
    for rex in WEAK_PATTERN_REGEXES:
        if rex.search(pw):
            return True
    if len(pw) < 8:
        return True
    return False


def compute_password_hygiene(all_records: list) -> dict:
    password_sources = {}
    total = 0
    weak_count = 0
    weak_samples = []

    for record in all_records:
        source_ctx = f"{record.get('computer_name', 'Unknown')} ({record.get('source', '?')})"
        for pw in (record.get('top_passwords') or []):
            total += 1
            if is_weak_password(pw):
                weak_count += 1
                if len(weak_samples) < 10:
                    weak_samples.append(pw)
            key = pw.lower()
            password_sources.setdefault(key, set()).add(source_ctx)

    reuse_groups = []
    for pw_lower, sources in password_sources.items():
        if len(sources) > 1:
            if len(pw_lower) > 2:
                masked = pw_lower[0] + '*' * max(len(pw_lower) - 2, 1) + pw_lower[-1]
            else:
                masked = '**'
            reuse_groups.append({"password_masked": masked, "sources": sorted(list(sources))})

    unique_score = round(((total - weak_count) / total) * 100) if total > 0 else 100

    return {
        "total_passwords_analyzed": total,
        "weak_count": weak_count,
        "unique_score": unique_score,
        "weak_samples": weak_samples,
        "reuse_groups": reuse_groups[:10],
    }


STEALER_PROFILES = {
    "redline": {
        "display_name": "RedLine Stealer",
        "description": "One of the most prevalent infostealers globally, commonly distributed via cracked software, fake game cheats, and malicious ads.",
        "typical_vector": "Cracked software, fake installers, malvertising",
        "data_targeted": "Browser-saved passwords, cookies, crypto wallets, FTP/VPN configs, Discord/Telegram session tokens",
    },
    "raccoon": {
        "display_name": "Raccoon Stealer",
        "description": "A malware-as-a-service infostealer popular on underground forums, known for frequent updates evading detection.",
        "typical_vector": "Phishing attachments, pirated software bundles",
        "data_targeted": "Browser credentials, autofill data, cryptocurrency wallet files",
    },
    "vidar": {
        "display_name": "Vidar Stealer",
        "description": "Derived from Arkei stealer, frequently distributed through fake cracked software and YouTube video descriptions.",
        "typical_vector": "Fake cracks, YouTube malvertising",
        "data_targeted": "Browser data, two-factor authentication backups, crypto wallets, messaging app data",
    },
    "lumma": {
        "display_name": "Lumma Stealer",
        "description": "A rapidly growing infostealer-as-a-service, frequently updated to bypass antivirus and browser protections.",
        "typical_vector": "Fake CAPTCHA pages, cracked software, malicious browser extensions",
        "data_targeted": "Browser credentials, crypto wallet extensions, session cookies",
    },
    "meta": {
        "display_name": "META Stealer",
        "description": "A RedLine-derived stealer sold as malware-as-a-service, targeting similar data with added evasion techniques.",
        "typical_vector": "Phishing emails, cracked software",
        "data_targeted": "Browser passwords, crypto wallets, system information",
    },
    "risepro": {
        "display_name": "RisePro Stealer",
        "description": "An infostealer often distributed via pay-per-install (PPI) malware distribution networks.",
        "typical_vector": "PPI networks, bundled software installers",
        "data_targeted": "Browser data, crypto wallets, credit card autofill data",
    },
    "stealc": {
        "display_name": "StealC",
        "description": "A modular infostealer designed to closely mimic Vidar and Raccoon's functionality, sold on underground forums.",
        "typical_vector": "Malvertising, cracked software",
        "data_targeted": "Browser credentials, cookies, crypto wallets",
    },
    "aurora": {
        "display_name": "Aurora Stealer",
        "description": "A Go-based infostealer known for its low antivirus detection rates at the time of distribution.",
        "typical_vector": "Fake software cracks, YouTube descriptions",
        "data_targeted": "Browser data, crypto wallets, FTP credentials",
    },
    "azorult": {
        "display_name": "AZORult",
        "description": "One of the longest-running infostealer families, historically used in numerous large-scale campaigns.",
        "typical_vector": "Exploit kits, phishing, malicious documents",
        "data_targeted": "Browser credentials, crypto wallets, FTP/email client credentials",
    },
    "formbook": {
        "display_name": "FormBook",
        "description": "A widely used infostealer and form-grabber historically sold as malware-as-a-service.",
        "typical_vector": "Malicious email attachments",
        "data_targeted": "Form input data, browser credentials, clipboard contents",
    },
    "mars": {
        "display_name": "Mars Stealer",
        "description": "An evolution of Oski stealer, targeting a broad range of browser and cryptocurrency data.",
        "typical_vector": "Cracked software, malvertising",
        "data_targeted": "Browser credentials, 2FA extensions, crypto wallets",
    },
    "unknown": {
        "display_name": "Unknown / Unclassified",
        "description": "The specific malware family could not be determined from available telemetry.",
        "typical_vector": "Not identified",
        "data_targeted": "Not identified",
    },
}


def get_stealer_profile(family_name: str) -> dict:
    if not family_name:
        return STEALER_PROFILES["unknown"]
    key = family_name.strip().lower()
    for profile_key, profile in STEALER_PROFILES.items():
        if profile_key in key:
            return profile
    return STEALER_PROFILES["unknown"]



VIP_PATTERNS = [
    r'\bceo\b', r'\bcfo\b', r'\bcto\b', r'\badmin\b', r'^dc-', r'^dc\d',
    r'\bserver\b', r'^it-', r'finance', r'\bhr-', r'\bdirector\b', r'\bmanager\b',
    r'domain.?controller', r'\bexec\b',
]
VIP_REGEX = re.compile('|'.join(VIP_PATTERNS), re.IGNORECASE)


def flag_vip_records(records: list) -> list:
    flagged = []
    for r in records:
        name = r.get('computer_name') or ''
        if VIP_REGEX.search(name):
            flagged.append({**r, "vip_reason": "Hostname pattern suggests a high-value asset (admin/executive/server)"})
    return flagged



def cross_verify_findings(classified_urls: list, tech_keywords: Optional[List[str]]) -> list:
    if not tech_keywords:
        return []
    findings = []
    lowered_keywords = [k.lower() for k in tech_keywords if isinstance(k, str) and len(k) >= 4]
    for u in classified_urls:
        haystack = f"{u.get('url', '')} {u.get('type', '')}".lower()
        for kw in lowered_keywords:
            if kw in haystack:
                findings.append({
                    "url": u.get("url"),
                    "matched_technology": kw,
                    "note": f"This exposed URL appears related to '{kw}', independently detected in the site's technology stack scan.",
                })
                break
    return findings


def geolocate_ip_bulk(ips: List[str]) -> dict:
    results = {}
    for ip in ips[:MAX_GEO_LOOKUPS]:
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = resp.json()
            if data.get("status") == "success":
                results[ip] = {"country": data.get("country") or "Unknown", "city": data.get("city") or "Unknown"}
            else:
                results[ip] = {"country": "Unknown", "city": "Unknown"}
        except Exception:
            results[ip] = {"country": "Unknown", "city": "Unknown"}
        time.sleep(REQUEST_DELAY)
    return results


def build_geo_distribution(all_records: list) -> list:
    ip_counts = {}
    for r in all_records:
        ip = r.get("ip")
        if ip and ip != "Unknown":
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

    unique_ips = list(ip_counts.keys())
    geo_data = geolocate_ip_bulk(unique_ips)

    distribution = []
    for ip, count in ip_counts.items():
        info = geo_data.get(ip, {"country": "Unknown", "city": "Unknown"})
        distribution.append({"ip": ip, "count": count, "country": info["country"], "city": info["city"]})

    distribution.sort(key=lambda x: x["count"], reverse=True)
    return distribution


def build_remediation_plan(all_records: list, classified_urls: list, compromised_emails: list,
                            password_hygiene: dict, vip_records: list) -> list:
    plan = []

    if compromised_emails:
        sample = ', '.join(compromised_emails[:10])
        plan.append(f"Force password reset for {len(compromised_emails)} identified compromised account(s): {sample}")

    critical_urls = [u for u in classified_urls if u.get('criticality') == 'critical']
    if critical_urls:
        plan.append(
            f"Immediately audit access logs for {len(critical_urls)} critical exposed service(s) "
            f"(VPN/admin panels) and rotate associated credentials."
        )

    if vip_records:
        plan.append(
            f"Prioritize incident response for {len(vip_records)} potentially high-value compromised "
            f"asset(s) flagged by hostname heuristics."
        )

    if password_hygiene.get('reuse_groups'):
        plan.append(
            "Enforce a password policy prohibiting shared/reused passwords — duplicate passwords "
            "were detected across multiple compromised accounts."
        )

    if password_hygiene.get('weak_count', 0) > 0:
        plan.append(
            f"Provide security awareness training — {password_hygiene['weak_count']} weak/common "
            f"password(s) were identified among compromised credentials."
        )

    stealer_families = sorted(set(
        r['stealer_family'] for r in all_records
        if r.get('stealer_family') and r['stealer_family'] != 'Unknown'
    ))
    if stealer_families:
        plan.append(f"Deploy or verify endpoint protection capable of detecting: {', '.join(stealer_families)}.")

    if not plan:
        plan.append("No specific action items identified — continue routine credential hygiene monitoring.")

    plan.append("Consider enabling multi-factor authentication (MFA) organization-wide if not already enforced.")
    return plan


def compute_trend(timeline: list) -> dict:
    if not timeline:
        return {"direction": "unknown", "description": "Not enough dated records to determine a trend."}

    now = datetime.now(timezone.utc)
    recent = 0
    older = 0

    for entry in timeline:
        try:
            d = datetime.strptime(entry["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception:
            continue
        days_ago = (now - d).days
        if days_ago <= 90:
            recent += 1
        elif days_ago <= 180:
            older += 1

    if recent == 0 and older == 0:
        return {"direction": "unknown", "description": "All recorded infections are older than 6 months."}
    if recent > older:
        return {"direction": "increasing",
                "description": f"{recent} infection(s) in the last 90 days vs {older} in the prior 90 days — exposure appears to be worsening."}
    elif recent < older:
        return {"direction": "decreasing",
                "description": f"{recent} infection(s) in the last 90 days vs {older} in the prior 90 days — exposure appears to be improving."}
    else:
        return {"direction": "stable",
                "description": f"Infection rate has remained stable ({recent} in each of the last two 90-day periods)."}


def _safe_get(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def _parse_date(value) -> Optional[str]:
    if not value or not isinstance(value, str):
        return None
    candidates = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ", "%d-%m-%Y", "%m/%d/%Y"]
    for fmt in candidates:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    match = re.search(r'\d{4}-\d{2}-\d{2}', value)
    return match.group(0) if match else None


def check_domain(domain: str) -> dict:
    data = _safe_get(f"{BASE_URL}search-by-domain?domain={domain}")
    if "error" in data:
        return {"available": False, "error": data["error"], "total_entries": 0, "total_stealers": 0}
    return {
        "available": True,
        "total_entries": data.get("total", 0) or 0,
        "total_stealers": data.get("totalStealers", 0) or 0,
    }


def check_attack_surface(domain: str) -> dict:
    data = _safe_get(f"{BASE_URL}urls-by-domain?domain={domain}")
    if "error" in data:
        return {"available": False, "error": data["error"], "employees_urls": [], "clients_urls": []}
    payload = data.get("data") or {}
    return {
        "available": True,
        "message": data.get("message", ""),
        "employees_urls": payload.get("employees_urls", []) or [],
        "clients_urls": payload.get("clients_urls", []) or [],
    }


def _extract_stealer_records(data: dict, source_label: str) -> List[dict]:
    records = []
    for stealer in (data.get("stealers") or []):
        records.append({
            "source": source_label,
            "computer_name": stealer.get("computer_name") or "Unknown",
            "operating_system": stealer.get("operating_system") or "Unknown",
            "date_compromised": _parse_date(stealer.get("date_compromised")),
            "malware_path": stealer.get("malware_path") or "Unknown",
            "ip": stealer.get("ip") or "Unknown",
            "stealer_family": stealer.get("stealer_family") or "Unknown",
            "top_logins": stealer.get("top_logins") or [],
            "top_passwords": stealer.get("top_passwords") or [],
        })
    return records


def check_email(email: str) -> dict:
    data = _safe_get(f"{BASE_URL}search-by-email?email={email}")
    if "error" in data:
        return {"target": email, "available": False, "compromised": False, "records": []}
    records = _extract_stealer_records(data, f"email:{email}")
    return {"target": email, "available": True, "compromised": len(records) > 0, "records": records}


def check_ip(ip: str) -> dict:
    data = _safe_get(f"{BASE_URL}search-by-ip?ip={ip}")
    if "error" in data:
        return {"target": ip, "available": False, "compromised": False, "records": []}
    records = _extract_stealer_records(data, f"ip:{ip}")
    return {"target": ip, "available": True, "compromised": len(records) > 0, "records": records}


def check_username(username: str) -> dict:
    data = _safe_get(f"{BASE_URL}search-by-username?username={username}")
    if "error" in data:
        return {"target": username, "available": False, "compromised": False, "records": []}
    records = _extract_stealer_records(data, f"username:{username}")
    return {"target": username, "available": True, "compromised": len(records) > 0, "records": records}


def extract_candidate_emails(*sources) -> List[str]:
    found = set()
    for s in sources:
        if isinstance(s, str):
            found.update(EMAIL_REGEX.findall(s))
        elif isinstance(s, list):
            for item in s:
                if isinstance(item, str):
                    found.update(EMAIL_REGEX.findall(item))
    return sorted(found)


def compute_risk_score(total_stealers_domain: int, compromised_email_count: int,
                        compromised_ip_count: int, has_recent_infection: bool) -> dict:
    score = 0
    score += min(total_stealers_domain, 20) * 2
    score += min(compromised_email_count, 10) * 3
    score += min(compromised_ip_count, 5) * 4
    if has_recent_infection:
        score += 10
    score = min(score, 100)

    if score == 0:
        level = "none"
    elif score < 25:
        level = "low"
    elif score < 50:
        level = "medium"
    elif score < 75:
        level = "high"
    else:
        level = "critical"

    return {"score": score, "level": level}


def build_hudsonrock_intelligence(domain: str, ip: Optional[str], subdomain_ips: Optional[list],
                                   site_emails: Optional[list], username: Optional[str] = None,
                                   tech_keywords: Optional[List[str]] = None) -> dict:
    domain_summary = check_domain(domain)
    time.sleep(REQUEST_DELAY)
    attack_surface = check_attack_surface(domain)
    time.sleep(REQUEST_DELAY)

    candidate_emails = extract_candidate_emails(*(site_emails or []))[:MAX_EMAILS_CHECKED]

    email_checks = []
    for email in candidate_emails:
        email_checks.append(check_email(email))
        time.sleep(REQUEST_DELAY)

    candidate_ips = []
    if ip:
        candidate_ips.append(ip)
    for extra_ip in (subdomain_ips or []):
        if extra_ip not in candidate_ips:
            candidate_ips.append(extra_ip)
    candidate_ips = candidate_ips[:MAX_IPS_CHECKED]

    ip_checks = []
    for target_ip in candidate_ips:
        ip_checks.append(check_ip(target_ip))
        time.sleep(REQUEST_DELAY)

    username_check = None
    if username:
        username_check = check_username(username)
        time.sleep(REQUEST_DELAY)

    all_records = []
    for check in email_checks + ip_checks:
        all_records.extend(check.get("records", []))
    if username_check:
        all_records.extend(username_check.get("records", []))

    stealer_family_breakdown = {}
    for record in all_records:
        family = record.get("stealer_family") or "Unknown"
        stealer_family_breakdown[family] = stealer_family_breakdown.get(family, 0) + 1

    stealer_profiles_used = {
        family: get_stealer_profile(family) for family in stealer_family_breakdown.keys()
    }

    timeline = []
    has_recent_infection = False
    now = datetime.now(timezone.utc)
    for record in all_records:
        date_str = record.get("date_compromised")
        if date_str:
            timeline.append({"date": date_str, "stealer_family": record.get("stealer_family") or "Unknown", "source": record.get("source")})
            try:
                record_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if (now - record_date).days <= 180:
                    has_recent_infection = True
            except Exception:
                pass
    timeline.sort(key=lambda x: x["date"])

    compromised_email_count = sum(1 for c in email_checks if c.get("compromised"))
    compromised_ip_count = sum(1 for c in ip_checks if c.get("compromised"))

    risk = compute_risk_score(
        total_stealers_domain=domain_summary.get("total_stealers", 0),
        compromised_email_count=compromised_email_count,
        compromised_ip_count=compromised_ip_count,
        has_recent_infection=has_recent_infection,
    )

    classified_urls, criticality_breakdown = classify_attack_surface(
        attack_surface.get("employees_urls", []), attack_surface.get("clients_urls", [])
    )

    password_hygiene = compute_password_hygiene(all_records)
    vip_records = flag_vip_records(all_records)
    cross_verified = cross_verify_findings(classified_urls, tech_keywords)
    geo_distribution = build_geo_distribution(all_records)
    trend = compute_trend(timeline)

    matched_emails = [c["target"] for c in email_checks if c.get("compromised")]

    remediation_plan = build_remediation_plan(
        all_records, classified_urls, matched_emails, password_hygiene, vip_records
    )

    total_employee_urls = len(attack_surface.get("employees_urls", []))
    total_client_urls = len(attack_surface.get("clients_urls", []))

    if risk["score"] == 0 and domain_summary.get("total_stealers", 0) == 0:
        summary_text = f"No Infostealer infections were found associated with {domain} or its discovered contacts."
    else:
        summary_text = (
            f"HudsonRock Cavalier identified {domain_summary.get('total_stealers', 0)} historical Infostealer "
            f"infection(s) associated with {domain}. Of {len(candidate_emails)} discovered contact email(s) checked, "
            f"{compromised_email_count} were found in compromised credential dumps. "
            f"{total_employee_urls} employee-related and {total_client_urls} client-related exposed URLs were identified."
        )

    return {
        "queried_domain": domain,
        "domain_summary": domain_summary,
        "attack_surface": attack_surface,
        "candidate_emails_checked": candidate_emails,
        "email_checks": email_checks,
        "candidate_ips_checked": candidate_ips,
        "ip_checks": ip_checks,
        "username_check": username_check,
        "all_records": all_records,
        "stealer_family_breakdown": stealer_family_breakdown,
        "stealer_profiles_used": stealer_profiles_used,
        "timeline": timeline,
        "risk_score": risk["score"],
        "risk_level": risk["level"],
        "summary_text": summary_text,
        "matched_emails": matched_emails,
        "total_employee_urls": total_employee_urls,
        "total_client_urls": total_client_urls,
        "classified_urls": classified_urls,
        "criticality_breakdown": criticality_breakdown,
        "password_hygiene": password_hygiene,
        "vip_records": vip_records,
        "cross_verified_findings": cross_verified,
        "geo_distribution": geo_distribution,
        "remediation_plan": remediation_plan,
        "trend": trend,
    }
