from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

BASE_URL = "https://api.lunarcyber.com/domain-exposure"
REQUEST_TIMEOUT = 20
READY_STATUS = "REPORT_READY"
PENDING_STATUS = "GENERATING_REPORT"
KNOWN_STATUSES = {READY_STATUS, PENDING_STATUS, "NOT_AUTHORIZED", "INVALID_DOMAIN"}


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _parse_date(value: Any) -> Optional[str]:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return text[:10] if len(text) >= 10 else None


def _empty_result(domain: str, status: str, message: str, error: Optional[str] = None) -> dict:
    return {
        "available": False,
        "status": status,
        "pending": status == PENDING_STATUS,
        "queried_domain": domain,
        "request_uuid": None,
        "period": {"from": None, "to": None},
        "generated_at": None,
        "report": {},
        "raw_response": None,
        "summary": {},
        "summary_text": message,
        "error": error,
        "source": "Lunar Domain Exposure API",
    }


def unavailable_result(domain: str, error: str) -> dict:
    return _empty_result(domain, "ERROR", f"Lunar Domain Exposure analysis failed: {error}", error)


def _status_message(status: str, domain: str) -> str:
    messages = {
        PENDING_STATUS: f"Lunar is still generating the exposure report for {domain}. Retry later to retrieve the completed report.",
        "NOT_AUTHORIZED": f"Lunar did not authorize an exposure report for {domain}.",
        "INVALID_DOMAIN": f"Lunar rejected {domain} as an invalid domain.",
    }
    return messages.get(status, f"Lunar returned report status {status} for {domain}.")


def _safe_get(domain: str) -> dict:
    try:
        response = requests.get(
            BASE_URL,
            params={"domain": domain},
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code < 200 or response.status_code >= 300:
            return {"error": f"HTTP {response.status_code}: {response.text[:300]}"}
        payload = response.json()
        if not isinstance(payload, dict):
            return {"error": "Lunar returned a non-object JSON response."}
        return payload
    except requests.RequestException as exc:
        return {"error": str(exc)}
    except ValueError as exc:
        return {"error": f"Invalid JSON response: {exc}"}


def _build_summary_text(domain: str, report: dict) -> str:
    summary = report.get("summary") or {}
    total = _as_int(summary.get("total_events"))
    infostealer = _as_int(summary.get("infostealer_events"))
    breaches = _as_int(summary.get("data_breach_events"))
    employees = _as_int(summary.get("employee_events"))
    clients = _as_int(summary.get("client_events"))
    last_seen = summary.get("last_seen") or "unknown"
    return (
        f"Lunar identified {total:,} credential exposure event(s) associated with {domain} "
        f"over the last 12 months: {infostealer:,} infostealer event(s), {breaches:,} data-breach event(s), "
        f"{employees:,} employee event(s), and {clients:,} client event(s). "
        f"The most recent exposure date is {last_seen}."
    )


def _build_exposure_indicator(report: dict) -> dict:
    summary = report.get("summary") or {}
    total = _as_int(summary.get("total_events"))
    infostealer = _as_int(summary.get("infostealer_events"))
    employees = _as_int(summary.get("employee_events"))
    last_seen = _parse_date(summary.get("last_seen"))

    score = min(40, round(min(total, 100000) / 100000 * 40))
    score += min(25, round(min(infostealer, 10000) / 10000 * 25))
    score += min(20, round(min(employees, 50000) / 50000 * 20))
    if last_seen:
        try:
            age_days = (datetime.now(timezone.utc).date() - datetime.strptime(last_seen, "%Y-%m-%d").date()).days
            if age_days <= 90:
                score += 15
            elif age_days <= 180:
                score += 8
        except ValueError:
            pass

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
    return {"score": min(score, 100), "level": level, "method": "DPULSE indicator; not a Lunar-published score"}


def build_lunarcyber_intelligence(domain: str) -> dict:
    data = _safe_get(domain)
    if "error" in data:
        return _empty_result(domain, "ERROR", f"Lunar request failed for {domain}.", data["error"])

    status = str(data.get("status") or "UNKNOWN")
    if status != READY_STATUS:
        return {
            **_empty_result(domain, status, _status_message(status, domain)),
            "request_uuid": data.get("requestUuid"),
            "period": {"from": data.get("periodFrom"), "to": data.get("periodTo")},
            "raw_response": data,
        }

    report = data.get("report")
    if not isinstance(report, dict):
        return _empty_result(domain, "INVALID_RESPONSE", "Lunar reported success without a report object.", "Missing report object")

    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    report_period = report.get("period") if isinstance(report.get("period"), dict) else {}
    return {
        "available": True,
        "status": status,
        "pending": False,
        "queried_domain": data.get("domain") or domain,
        "request_uuid": data.get("requestUuid"),
        "period": {
            "from": data.get("periodFrom") or report_period.get("from"),
            "to": data.get("periodTo") or report_period.get("to"),
        },
        "generated_at": report.get("generated_at"),
        "report": report,
        "raw_response": data,
        "summary": summary,
        "summary_text": _build_summary_text(domain, report),
        "exposure_indicator": _build_exposure_indicator(report),
        "error": None,
        "source": "Lunar Domain Exposure API",
    }
