# Basic Scan

Basic scan is the default and most fundamental scanning mode in DPULSE-CLI. It starts automatically after all preparation steps and serves as the foundation for every investigation.

> **Note:** Basic scan always runs first — you cannot start any other scanning mode without it.

---

## What Basic Scan Returns

Basic scan extracts publicly available information about the target domain across multiple categories:

---

### 🌐 WHOIS Information

| Field | Description |
|-------|-------------|
| **Domain name** | Registered domain |
| **Full URL** | Complete web address |
| **IP address** | Resolved IP |
| **Registrar** | Domain registrar details |
| **Creation date** | When domain was registered |
| **Expiration date** | When registration expires |
| **Organization** | Registered organization name |
| **Contact emails** | Administrative contacts |

---

### 🔗 Domain Infrastructure

| Category | Details |
|----------|---------|
| **Subdomains** | Discovered subdomains list |
| **Email addresses** | Gathered from subdomains |
| **IP addresses** | Resolved from subdomains |

---

### 📱 Social Media Discovery

Supported platforms:

| Platform | Platform | Platform |
|----------|----------|----------|
| Facebook | Twitter (X.com) | Instagram |
| Telegram | TikTok | LinkedIn |
| VKontakte | YouTube | Odnoklassniki |
| WeChat | | |

> **Output:** Links, posts, and profiles associated with the target domain.

---

### 🔐 DNS & SSL Information

**DNS Records:**

- Name servers (NS)
- Mail exchange addresses (MX)

**SSL Certificate:**

| Field | Description |
|-------|-------------|
| **Issuer** | Certificate authority |
| **Subject** | Certificate owner |
| **Creation date** | When certificate was issued |
| **Expiration date** | When certificate expires |
| **Certificate name** | Common name (CN) |
| **Serial number** | Unique identifier |

---

### 🛡️ Security Analysis (Pre-Pentest)

| Category | What it finds |
|----------|---------------|
| **Vulnerabilities** | Possible CVEs associated with detected services |
| **Open ports** | Discovered network ports |
| **Hostnames** | Related hostnames |

---

### 🛠️ Technology Stack

Detects development and deployment technologies:

| Category | Examples |
|----------|----------|
| **CMS** | WordPress, Joomla, Drupal |
| **Web servers** | Nginx, Apache, IIS |
| **Programming languages** | PHP, Python, JavaScript |
| **Web frameworks** | React, Angular, Django |
| **Analytics services** | Google Analytics, Yandex Metrica |
| **Tags & trackers** | GTM, Facebook Pixel |

---

### 📁 Downloaded Files

Basic scan automatically downloads (if available):

- `sitemap.xml` — site structure map
- `robots.txt` — crawler directives

> **Location:** Downloaded files are saved in a report folder.

---
