# Third-Party API Scan Mode

DPULSE-CLI integrates with external intelligence services to enhance domain reconnaissance capabilities. API scan is optional and can be enabled during pre-scan preparation steps.

---

## Supported APIs

| Service | Purpose | API Key Required |
|---------|---------|------------------|
| **SecurityTrails** | Deep subdomain and DNS enumeration | ✅ Yes |
| **VirusTotal** | Domain reputation and malware analysis | ✅ Yes |
| **HudsonRock** | Compromised credentials and infostealer data | ❌ No |

---

## SecurityTrails API

> **Website:** [securitytrails.com](https://securitytrails.com)
> **Key Required:** Yes

SecurityTrails provides comprehensive DNS intelligence and historical data for domain research.

### What It Returns

| Category | Details |
|----------|---------|
| **Domain info** | Alexa rank, apex domain, hostname |
| **DNS records** | A, MX, NS, SOA, TXT records |
| **Subdomains** | Complete subdomains list |
| **Alive subdomains** | Pingable/active subdomains only |

---

## VirusTotal API

> **Website:** [virustotal.com](https://virustotal.com)
> **Key Required:** Yes

VirusTotal analyzes domains using multiple antivirus engines and website scanners to identify malicious activity.

### What It Returns

| Category | Details |
|----------|---------|
| **Categories** | Domain categorization by security vendors |
| **Detected samples** | Malicious files associated with domain |
| **Undetected samples** | Clean files associated with domain |
| **Detected URLs** | Malicious URLs found on domain |

---

## HudsonRock API

> **Website:** [hudsonrock.com](https://hudsonrock.com)
> **Key Required:** No

HudsonRock Cavalier API provides access to cybercrime intelligence data from over **30,821,440 compromised computers** collected through global infostealer malware campaigns.

### What It Returns

| Category | Details |
|----------|---------|
| **Compromised credentials** | Stolen logins associated with domain |
| **Infostealer data** | Data from malware-infected machines |
| **Breach intelligence** | Threat actor campaign information |

---

## API Keys Management

DPULSE-CLI uses a local database to store your API keys securely.

---

### Database Structure

![API Storage Database](https://github.com/user-attachments/assets/02233813-781e-4bf8-be7c-76ec7627be06)

---

### Key Status Indicators

| Color | Status | Meaning |
|-------|--------|---------|
| 🔴 Red | Invalid | Filler/placeholder — API not usable |
| 🟢 Green | Valid | Real key entered — API ready to use |

---

### Adding Your API Keys

**Step 1:** Open API Keys DB Manager in DPULSE-CLI

**Step 2:** Select the API service you want to configure

**Step 3:** Enter your actual API key

![API Key Process](https://github.com/user-attachments/assets/effb27ab-dd4b-4470-b90c-34c6f9a43d8c)

---

### Resetting API Keys Database

If you need to start fresh, you can reset to the reference database:

| Action | Description |
|--------|-------------|
| **Reset database** | Deletes current keys, copies reference database |
| **When to use** | Corrupted database or complete reset needed |

> **Note:** This action is optional. You can simply overwrite individual keys using the standard key entry process.

---

## API Rate Limits

> **Warning:** Free API plans have usage limitations. Check the limits displayed in DPULSE-CLI for each service.

| Service | Free Tier Limitations |
|---------|----------------------|
| **SecurityTrails** | Limited queries per month |
| **VirusTotal** | Limited queries per minute/day |
| **HudsonRock** | No key required, but rate limits may apply |

---

## When to Use API Scan

| Scenario | Recommendation |
|----------|----------------|
| Deep subdomain enumeration | ✅ Use SecurityTrails |
| Malware/reputation check | ✅ Use VirusTotal |
| Credential breach search | ✅ Use HudsonRock |
| Quick reconnaissance | ❌ Skip API scan |
| No API keys available | ✅ Use HudsonRock only |
| Comprehensive investigation | ✅ Use all APIs |
