# PageSearch Mode

PageSearch is an extended deep search function that analyzes all subdomains discovered during basic scan. It performs comprehensive content analysis to find sensitive data and hidden elements.

> **Note:** PageSearch is optional — you can enable or disable it during pre-scan preparation steps.

---

## How PageSearch Works

1. Takes all subdomains found during basic scan
2. Crawls each subdomain deeply
3. Analyzes page content, source code, and linked files
4. Extracts sensitive information and downloads discovered files

---

## What PageSearch Returns

PageSearch extends basic scan results with the following categories:

---

### 🔑 Credentials & Secrets

| Category | Description |
|----------|-------------|
| **Email addresses** | Additional emails not found during basic scan |
| **API keys** | Exposed API keys in source code or configs |
| **Exposed passwords** | Hardcoded or leaked credentials |
| **Cookies** | Cookie names and values |

---

### 📋 Web Page Elements

| Element | Description |
|---------|-------------|
| **Hidden forms** | Forms with `type="hidden"` attributes |
| **Input fields** | Data input elements |
| **Other elements** | Comments, metadata, debug info |

---

### 📁 Files Discovery & Download

PageSearch can find and **automatically download** various file types:

| File Type | Examples |
|-----------|----------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx` |
| **Config files** | `.env`, `.cfg`, `.ini`, `.yaml`, `.json` |
| **Database files** | `.sql`, `.db`, `.sqlite`, `.bak` |

> **Feature:** All discovered files are automatically downloaded to the report directory for offline analysis.

---

### 🔍 Keyword Search in PDFs

You can specify custom keywords during scan configuration. PageSearch will:

- Download all discovered PDF files
- Search for your keywords inside each PDF
- Report matches with context

---

## Example Output

![PageSearch Example](https://github.com/user-attachments/assets/ed91f37f-578f-462b-a464-5281dd06ba0c)

> **Note:** This example may not be fully representative as the scanned site is not a real-world domain.

---

## When to Use PageSearch

| Scenario | Recommendation |
|----------|----------------|
| Quick reconnaissance | ❌ Skip PageSearch |
| Deep investigation | ✅ Enable PageSearch |
| Looking for credentials | ✅ Enable PageSearch |
| Time-sensitive scan | ❌ Skip PageSearch |
| Comprehensive audit | ✅ Enable PageSearch |

> **Warning:** PageSearch significantly increases scan time depending on the number of subdomains and pages.
