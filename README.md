<div align="center">

# 🌐 DPULSE
### Advanced Domain OSINT & Reconnaissance Tool

<img src="https://github.com/user-attachments/assets/949c332b-790e-49da-81a3-a7cf21e9ddf2" width="500">

<br><br>

[![Stable Version](https://img.shields.io/badge/v1.4-STABLE-success?style=for-the-badge)](https://github.com/OSINT-TECHNOLOGIES/dpulse/releases)
[![Rolling Version](https://img.shields.io/badge/v1.4.1-DEV_BUILD-orange?style=for-the-badge)](https://github.com/OSINT-TECHNOLOGIES/dpulse/tree/rolling)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/osinttechnologies/dpulse)
[![Documentation](https://img.shields.io/badge/Docs-ReadTheDocs-informational?style=for-the-badge&logo=readthedocs&logoColor=white)](https://dpulse.readthedocs.io)

**Convenient, fast, and user-friendly collector of domain information from open sources.**

[Report Bug](https://github.com/OSINT-TECHNOLOGIES/dpulse/issues) • [Request Feature](https://github.com/OSINT-TECHNOLOGIES/dpulse/issues) • [Roadmap](https://github.com/users/OSINT-TECHNOLOGIES/projects/1)

</div>

---

> ⚠️ **Disclaimer:** DPULSE is a research tool tailored for OSINT professionals. It is **not** intended for criminal activities. The developer is not responsible for any misuse of this tool. Use strictly on allowed domains and for legal purposes.

---

## 🚀 Key Features

DPULSE automates the boring stuff in domain reconnaissance. It compiles data into clean **HTML/XLSX reports**.

| Feature | Description |
| :--- | :--- |
| 🔍 **Basic Scan** | Automates WHOIS, subdomains, emails, IPs, social media, SSL info, open ports, and tech stack detection. |
| 🕵️‍♂️ **PageSearch** | Deep dive into subdomains to find API keys, exposed passwords, cookies, hidden forms, and sensitive documents (PDF, config files). |
| 🧩 **Dorking Mode** | Automated Google Dorking for IoT, admin panels, sensitive files, and custom user-defined dorks. |
| 🔗 **API Integrations** | Native support for **VirusTotal**, **SecurityTrails**, and **HudsonRock** (compromised hosts check). |
| 📸 **Snapshotting** | Captures target via Screenshots, HTML downloads, or Wayback Machine archiving. |

---

## ⚡ Quick Start

### Option 1: Docker (Recommended)
The fastest way to run DPULSE without worrying about dependencies.

```bash
# 1. Pull the image
docker pull osinttechnologies/dpulse:latest

# 2. Run DPULSE (Linux/macOS)
docker run --rm -it -v "$PWD":/data -w /data osinttechnologies/dpulse:latest

# 2. Run DPULSE (Windows PowerShell)
docker run --rm -it -v "${PWD}:/data" -w /data osinttechnologies/dpulse:latest
```

### Option 2: Source Code (Poetry)
For developers or those who prefer a local environment.

```bash
git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
cd dpulse
poetry install
poetry run python dpulse.py
```

<details>
<summary><b>Click to see Legacy Installation (pip)</b></summary>
<br>
If you don't use Poetry, you can use standard pip (might have conflicts):

```bash
git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
cd dpulse
pip install -r requirements.txt
python dpulse.py
```
</details>

---

## 🖥️ Interface & Reports

**Main Menu**  
Clean CLI interface for easy navigation.  
![dpulse_start](https://github.com/user-attachments/assets/9ec0ab73-2206-4d38-bae6-e88656e17f95)

**Scanning Process**  
Real-time feedback during the scan.  
![dpulse_bs](https://github.com/user-attachments/assets/b0ad7827-6dac-4f82-a369-4447a0e1c878)

**Output**  
Organized report folders with timestamps.  
![Report Folder](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7de73250-c9b6-4373-b21e-16bbb7a63882)

---

## 🏆 Community & Mentions

We are proud to be mentioned by industry leaders and the cybersecurity community.

*   **HudsonRock:** [Featured in cybercrime intelligence update](https://www.linkedin.com/feed/update/urn:li:share:7294336938495385600/)
*   **DarkWebInformer:** [Tool for complex approach to domain OSINT](https://darkwebinformer.com/dpulse-tool-for-complex-approach-to-domain-osint/)
*   **Ethical Hackers Academy:** [Tool Review](https://ethicalhacksacademy.com/blogs/cyber-security-tools/dpulse)

<details>
<summary><b>View all mentions (Social Media & Blogs)</b></summary>

### X.com (Twitter)
*   [@DarkWebInformer](https://x.com/DarkWebInformer/status/1787583156775759915?t=Ak1W9ddUPpDvLAkVyQG8fQ&s=19)
*   [@OSINTech_](https://x.com/OSINTech_/status/1805902553885888649)
*   [@cyb_detective](https://x.com/cyb_detective/status/1821337404763959487?t=vbyRUeXM2C6gf47l7XvJnQ&s=19)
*   [@DailyOsint](https://x.com/DailyOsint/status/1823013991951523997?t=Fr-oDCZ2pFmFJpUT3BKl5A&s=19)
*   [@UndeadSec](https://x.com/UndeadSec/status/1827692406797689032)
*   [@0xtechrock](https://x.com/0xtechrock/status/1804470459741978974?t=us1EVJEECNZdSmSe5CQjQA&s=19)

### LinkedIn
*   [Maory Schroder](https://fr.linkedin.com/posts/maory-schroder_osint-cybers%C3%A9curit%C3%A9-pentest-activity-7227562302009491456-sXoZ?trk=public_profile)
*   [Maxim Marshak](https://www.linkedin.com/pulse/bormaxi8080-osint-timeline-64-27062024-maxim-marshak-jojbf)
*   [DailyOSINT](https://www.linkedin.com/posts/daily-osint_osint-reconnaissance-infosec-activity-7228779678096850946-H-zC)

### Telegram Channels
*   Cyber Detective
*   Hackers Factory
*   C.I.T Security
*   Реальний OSINT

</details>

---

<div align="center">

**Created by OSINT-TECHNOLOGIES**

[Documentation](https://dpulse.readthedocs.io) • [Contact Developer](https://dpulse.readthedocs.io/en/latest/contact_dev/#)

</div>
