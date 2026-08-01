<div align="center">

# 🌐 DPULSE
### Advanced Domain OSINT & Reconnaissance Tool — Desktop Edition

<img src="https://github.com/user-attachments/assets/949c332b-790e-49da-81a3-a7cf21e9ddf2" width="500">

<br><br>

[![Latest Release](https://img.shields.io/github/v/release/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=success)](https://github.com/OSINT-TECHNOLOGIES/dpulse/releases)
[![Downloads](https://img.shields.io/github/downloads/OSINT-TECHNOLOGIES/dpulse/total?style=for-the-badge&color=blue)](https://github.com/OSINT-TECHNOLOGIES/dpulse/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/OSINT-TECHNOLOGIES/dpulse/build-release.yml?style=for-the-badge&label=Build)](https://github.com/OSINT-TECHNOLOGIES/dpulse/actions)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=for-the-badge)](https://osint-technologies.github.io/dpulse/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**A powerful, fast, and user-friendly desktop application for collecting domain intelligence from open sources — now with zero setup required.**

[**📥 Download**](https://osint-technologies.github.io/dpulse/) • [Report Bug](https://github.com/OSINT-TECHNOLOGIES/dpulse/issues) • [Request Feature](https://github.com/OSINT-TECHNOLOGIES/dpulse/issues) • [Roadmap](https://github.com/users/OSINT-TECHNOLOGIES/projects/1)

</div>

---

> ⚠️ **Disclaimer:** DPULSE is a research tool tailored for OSINT professionals. It is **not** intended for criminal activities. The developer is not responsible for any misuse of this tool. Use strictly on allowed domains and for legal purposes.

---

## 🖥️ Now Available as a Desktop Application

DPULSE has evolved from a CLI tool into a full **native desktop application** for Windows and Linux, built on **Tauri** with a **Python/FastAPI** backend running invisibly under the hood.

No Python installation. No dependency management. No terminal commands. Just download, install, and scan.

<div align="center">

### [👉 Download DPULSE for your OS](https://osint-technologies.github.io/dpulse/)

*The download page automatically detects your operating system and highlights the correct installer.*

</div>

---

## 🚀 Key Features

DPULSE automates the boring stuff in domain reconnaissance and compiles everything into a single, interactive HTML report.

| Feature | Description |
| :--- | :--- |
| 🔍 **Core Reconnaissance** | Automates WHOIS, subdomain enumeration, email harvesting, IP resolution, social media discovery, SSL certificate analysis, open port detection, and technology stack fingerprinting. |
| 🕸️ **Interactive Infrastructure Graph** | A live, explorable network graph (powered by vis-network) visualizing the relationship between the domain, its subdomains, IPs, services, ports, and vulnerabilities. |
| 📊 **Live Charts & Statistics** | Chart.js-powered visualizations of scan results — at-a-glance metrics for subdomains, socials, emails, ports, and vulnerabilities. |
| 🛡️ **Security Analysis** | Shodan InternetDB integration for open ports and known CVEs, with on-demand severity lookup via the NVD API. |
| 🔗 **API Integrations** | Native support for **VirusTotal**, **SecurityTrails**, and **HudsonRock** (compromised hosts / infostealer intelligence). |
| 💾 **Local Scan History** | Every scan is automatically saved to a local SQLite database — browse, re-open, or delete past reports anytime from the app. |
| 🔑 **Built-in API Key Manager** | Securely store and manage your third-party API credentials directly inside the application. |
| 🔎 **Smart Report Tables** | Every data category is presented in searchable, sortable, paginated tables with CSV export support. |
| 🌍 **Live Report Enrichment** | Real-time DNS lookups, IP geolocation, and Wayback Machine checks performed directly inside the generated report. |
| 🖨️ **Print-Ready Reports** | Clean print/PDF export layout with properly paginated sections. |
| 🌓 **Light/Dark Theme** | Toggle between themes directly inside the report. |

---

## ⚡ Quick Start

### Windows

1. Go to the [**Download Page**](https://osint-technologies.github.io/dpulse/) or grab the installer directly from [Releases](https://github.com/OSINT-TECHNOLOGIES/dpulse/releases/latest)
2. Run `DPULSE_x.x.x_x64-setup.exe`
3. If Windows SmartScreen shows a warning (expected for unsigned open-source apps), click **"More info"** → **"Run anyway"**
4. Launch DPULSE from the Start Menu

### Linux

```bash
# AppImage (universal)
chmod +x dpulse_x.x.x_amd64.AppImage
./dpulse_x.x.x_amd64.AppImage

# or Debian/Ubuntu .deb package
sudo dpkg -i dpulse_x.x.x_amd64.deb
sudo apt-get install -f
```

### Using DPULSE

1. Launch the app — wait a few seconds for the backend to initialize
2. Go to the **Scan** tab, enter a target domain, add an optional case comment
3. *(Optional)* Enable third-party API checks in the scan form — configure your keys first in the **API Manager** tab
4. Click **Start Scan** — the interactive report opens directly inside the app once complete
5. Browse previous scans anytime in the **Reports DB** tab

---

## 📖 Report Sections

The generated report is a full single-page application with sidebar navigation:

| Section | Contents |
|---|---|
| ℹ️ **General Information** | Scan configuration, file discovery status, timestamps |
| 📊 **Scan Statistics** | Key metrics with bar/doughnut charts |
| 🕸️ **Infrastructure Graph** | Interactive, filterable, exportable (PNG/SVG/JSON) network graph |
| 🪪 **WHOIS Information** | Registrar, dates, organization, contacts |
| 🔐 **DNS & SSL Info** | Name servers, MX records, full certificate details |
| 📱 **Social Media** | Platform-categorized links with live reachability checks |
| 🌐 **Subdomains** | Full enumeration with bulk reachability/DNS/WHOIS tools |
| 🔢 **IP Addresses** | Geolocation, reverse DNS, pivot links to Shodan/VirusTotal/AbuseIPDB |
| ⚙️ **Technology Stack** | Detected servers, CMS, languages, frameworks, with on-demand CVE search |
| 🛡️ **Security Analysis** | Open ports (Nmap command generator) and vulnerabilities (NVD severity lookup) |
| 📄 **Technical Files** | robots.txt and sitemap.xml raw content |
| 🔌 **API Results** | *(if enabled)* Raw output from VirusTotal, SecurityTrails, HudsonRock |

---

## 🔌 Third-Party API Integration

| Provider | Free Tier | Get API Key |
|---|---|---|
| **VirusTotal** | 4 requests/minute | [virustotal.com/gui/join-us](https://www.virustotal.com/gui/join-us) |
| **SecurityTrails** | 50 requests/month | [securitytrails.com/app/signup](https://securitytrails.com/app/signup) |
| **HudsonRock** | No key required | Works out of the box |

API scanning is entirely optional — DPULSE performs its full core reconnaissance using only free, keyless public sources by default.

---

## 🏗️ Building from Source

<details>
<summary><b>Prerequisites & build instructions</b></summary>

**Requirements:**
- [Rust](https://rustup.rs/) 1.75+
- [Node.js](https://nodejs.org/) 18 LTS+
- [Python](https://python.org/) 3.10+

**Windows additionally requires:**
- Microsoft C++ Build Tools ("Desktop development with C++")
- WebView2 Runtime (pre-installed on most Windows 10/11 systems)

**Linux (Debian/Ubuntu) additionally requires:**
```bash
sudo apt update
sudo apt install -y libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

**Setup:**
```bash
git clone https://github.com/OSINT-TECHNOLOGIES/dpulse.git
cd dpulse

npm install

cd python-backend
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cd ..
```

**Run in development mode** (two terminals):
```bash
# Terminal 1
cd python-backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2
npm run tauri dev
```

**Build production installer:**
```bash
npm run tauri build
```

Automated multi-platform builds run via GitHub Actions on every version tag — see `.github/workflows/build-release.yml`.

</details>

---


## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Desktop Shell | Tauri 2 (Rust) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, FastAPI, Uvicorn |
| Templating | Jinja2 |
| Data Storage | SQLite |
| Report Visualization | Chart.js, vis-network |
| Packaging | PyInstaller |
| CI/CD | GitHub Actions |

---

## 🏆 Community & Mentions

We are proud to be mentioned by industry leaders and the cybersecurity community.

* **HudsonRock:** [Featured in cybercrime intelligence update](https://www.linkedin.com/feed/update/urn:li:share:7294336938495385600/)
* **DarkWebInformer:** [Tool for complex approach to domain OSINT](https://darkwebinformer.com/dpulse-tool-for-complex-approach-to-domain-osint/)
* **Ethical Hackers Academy:** [Tool Review](https://ethicalhacksacademy.com/blogs/cyber-security-tools/dpulse)

<details>
<summary><b>View all mentions (Social Media & Blogs)</b></summary>

### X.com (Twitter)
* [@DarkWebInformer](https://x.com/DarkWebInformer/status/1787583156775759915?t=Ak1W9ddUPpDvLAkVyQG8fQ&s=19)
* [@OSINTech_](https://x.com/OSINTech_/status/1805902553885888649)
* [@cyb_detective](https://x.com/cyb_detective/status/1821337404763959487?t=vbyRUeXM2C6gf47l7XvJnQ&s=19)
* [@DailyOsint](https://x.com/DailyOsint/status/1823013991951523997?t=Fr-oDCZ2pFmFJpUT3BKl5A&s=19)
* [@UndeadSec](https://x.com/UndeadSec/status/1827692406797689032)
* [@0xtechrock](https://x.com/0xtechrock/status/1804470459741978974?t=us1EVJEECNZdSmSe5CQjQA&s=19)

### LinkedIn
* [Maory Schroder](https://fr.linkedin.com/posts/maory-schroder_osint-cybers%C3%A9curit%C3%A9-pentest-activity-7227562302009491456-sXoZ?trk=public_profile)
* [Maxim Marshak](https://www.linkedin.com/pulse/bormaxi8080-osint-timeline-64-27062024-maxim-marshak-jojbf)
* [DailyOSINT](https://www.linkedin.com/posts/daily-osint_osint-reconnaissance-infosec-activity-7228779678096850946-H-zC)

### Telegram Channels
* Cyber Detective
* Hackers Factory
* C.I.T Security
* Реальний OSINT

</details>

---

## 🗺️ Roadmap

- [ ] Google Dorking module (full implementation)
- [ ] PageSearch deep-crawl module (full implementation)
- [ ] Screenshot/HTML/Wayback snapshotting module (full implementation)
- [ ] Native PDF export

Have an idea? [Open a feature request](https://github.com/OSINT-TECHNOLOGIES/dpulse/issues/new).

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, commit your changes, and open a Pull Request. For major changes, please open an issue first to discuss the approach.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Created by OSINT-TECHNOLOGIES**

[📥 Download](https://osint-technologies.github.io/dpulse/) • [Documentation](https://dpulse.readthedocs.io) • [Contact Developer](https://dpulse.readthedocs.io/en/latest/contact_dev/#)

</div>
