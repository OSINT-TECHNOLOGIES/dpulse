# Snapshotting and Screenshotting

DPULSE provides multiple methods to capture and preserve target website content for analysis, documentation, and offline review.

---

## Overview

| Method | Type | Output | Interactive |
|--------|------|--------|-------------|
| **Screenshot** | Visual capture | Image file | ❌ No |
| **PageCopy** | Complete copy | HTML + assets | ✅ Yes |
| **Wayback Snapshot** | Historical versions | Multiple HTML files | ✅ Yes |

> **Note:** You will be prompted to select snapshotting mode during pre-scan configuration.

![Snapshotting Selection](https://github.com/user-attachments/assets/c24d297d-d52e-45e1-9770-97229abcc2ce)

---

## Screenshot vs Snapshot

| Feature | Screenshot | Snapshot |
|---------|------------|----------|
| **What it captures** | Visual appearance at a moment | Full page structure and content |
| **File format** | Image (PNG/JPG) | HTML + assets |
| **Interactive** | ❌ View only | ✅ Navigate, click, inspect |
| **Offline use** | ✅ Yes | ✅ Yes |
| **Use case** | Documentation, reports | Analysis, forensics |

---

## 📸 Screenshot Mode

Takes a visual capture of the domain's main page using headless browser technology.

### How It Works

1. DPULSE launches a browser instance using Selenium
2. Navigates to target domain
3. Captures full-page screenshot
4. Saves image to report folder

### Configuration

> **Important:** Proper configuration is required for screenshotting to work correctly. See [Configuration File](configuration.md) for details.

### Output

```
reports/
└── example.com_2024-01-15/
    └── screenshot.png
```

---

## 📄 HTML Snapshot (Web Copy)

Saves the webpage as an HTML file, preserving structure and interactivity.

### What It Captures

| Element | Preserved |
|---------|-----------|
| HTML code | ✅ Yes |
| DOM structure | ✅ Yes |
| Text content | ✅ Yes |
| Links | ✅ Yes |
| Forms | ✅ Yes |
| Inline styles | ✅ Yes |

### Output

```
reports/
└── example.com_2024-01-15/
    └── snapshot.html
```

---

## 📦 PageCopy Mode

Creates a complete offline copy of the page including all assets.

### What It Captures

| Asset Type | Included |
|------------|----------|
| HTML | ✅ Yes |
| CSS stylesheets | ✅ Yes |
| JavaScript files | ✅ Yes |
| Images | ✅ Yes |
| Fonts | ✅ Yes |

### Output

```
reports/
└── example.com_2024-01-15/
    └── pagecopy/
        ├── index.html
        ├── styles.css
        ├── script.js
        └── images/
```

---

## 🕰️ Wayback Machine Snapshot

Retrieves historical versions of the target domain from the Internet Archive.

### How It Works

1. Connects to Wayback Machine API
2. Queries for available snapshots within specified time period
3. Downloads selected historical versions
4. Saves all versions to report folder

### Configuration

You specify the time period during scan setup:

![Wayback Configuration](https://github.com/user-attachments/assets/dd82a133-95a8-4fa4-9dc7-ed18d2768d16)

### Output

```
reports/
└── example.com_2024-01-15/
    └── wayback_snapshots/
        ├── 2023-01-15_snapshot.html
        ├── 2023-06-20_snapshot.html
        └── 2024-01-01_snapshot.html
```

---

## When to Use Each Method

| Scenario | Recommended Method |
|----------|-------------------|
| Quick visual documentation | 📸 Screenshot |
| Preserve page for analysis | 📄 HTML Snapshot |
| Full offline copy with assets | 📦 PageCopy |
| Track changes over time | 🕰️ Wayback Snapshot |
| Legal/forensic evidence | 📸 Screenshot + 📄 HTML Snapshot |
| Website no longer exists | 🕰️ Wayback Snapshot |

---

## Output Location

All captures are saved in the scan report folder:

```
reports/
└── example.com_2024-01-15/
    ├── report.html
    ├── screenshot.png
    ├── snapshot.html
    ├── pagecopy/
    └── wayback_snapshots/
```
