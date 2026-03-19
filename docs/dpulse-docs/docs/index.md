# Welcome to DPULSE Documentation

**Convenient, fast and user-friendly domain intelligence collector from open sources**

---

## What is DPULSE-CLI?

DPULSE-CLI is a command-line OSINT tool designed for comprehensive domain reconnaissance. It automates the collection and analysis of publicly available information about any target domain.

---

## Core Features

### 🔍 Basic Scan

Extracts fundamental domain intelligence:

- **WHOIS data** — registration details, registrar, dates
- **DNS records** — subdomains, IP addresses
- **SSL/TLS certificates** — issuer, validity, SANs
- **Email addresses** — discovered across the domain
- **Social media** — links, posts, profiles
- **Web technologies** — frameworks, CMS, libraries
- **Security analysis** — open ports, CPEs, potential vulnerabilities
- **Files extraction** — `sitemap.xml`, `robots.txt`

---

### 📄 PageSearch Scan

Deep content analysis across all discovered subdomains:

| Category | What it finds |
|----------|---------------|
| **Credentials** | Exposed passwords, API keys, tokens |
| **Data elements** | Cookies, hidden forms, input fields |
| **Files** | Documents, configs, database dumps |
| **Custom search** | User-specified keywords in PDF files |

> **Note:** PageSearch can automatically download discovered files for offline analysis.

---

### 🎯 Dorking Scan

Automated Google Dorking with pre-built query databases:

- **IoT devices** — cameras, routers, sensors
- **Sensitive files** — backups, logs, configs
- **Admin panels** — login pages, dashboards
- **Web elements** — exposed directories, forms

You can also create and use **custom dorking databases** for specific research needs.

---

### 🔌 API Scan

Integration with third-party intelligence services:

| Service | Capabilities |
|---------|--------------|
| **VirusTotal** | Domain reputation, malware analysis, brief intel |
| **SecurityTrails** | Deep subdomain enumeration, historical DNS data |
| **HudsonRock** | Compromised credentials, infostealer data, breach intelligence |

---

### 📸 Snapshotting

Capture and preserve domain content:

| Snapshot Type | Description |
|---------------|-------------|
| **Screenshot** | Visual capture of the homepage |
| **PageCopy** | Complete page copy with all assets (CSS, JS, images) |
| **Wayback Machine** | Historical versions from Internet Archive |

---

## Output & Reporting

DPULSE-CLI generates:

- **HTML reports** — clean, readable format for analysis and presentation
- **Local database** — persistent storage for all scan results with restore capability

---
