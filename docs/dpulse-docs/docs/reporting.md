# Reporting System

DPULSE-CLI provides a comprehensive reporting system designed for detailed results presentation, analysis, and long-term storage. Reports are generated automatically after each scan and contain all gathered intelligence in an organized, interactive format. DPULSE-CLI supports HTML report as the primary and most feature-rich report format among OSINT and cybersecurity tools.

### Why HTML?

- **Universal compatibility** — opens in any web browser
- **Interactive elements** — tables, charts, graphs, navigation
- **No dependencies** — doesn't require third-party applications
- **Easy sharing** — ideal for customers, teams, presentations
- **Dynamic content** — sortable tables, filters, search

---

### Report Structure

HTML report is divided into logical sections accessible via sidebar navigation:

| Section | Icon | Description |
|---------|------|-------------|
| **General Information** | ℹ️ | Scan overview, status indicators, timestamps |
| **Scan Statistics** | 📊 | Summary metrics with interactive charts |
| **Infrastructure Graph** | 🕸️ | Interactive domain visualization |
| **WHOIS Information** | 🪪 | Domain registration details |
| **DNS & SSL Info** | 🔐 | DNS records and certificate data |
| **Social Media** | 📱 | Discovered social links and analysis |
| **Subdomains** | 🌐 | Subdomain enumeration results |
| **IP Addresses** | 🔢 | Resolved IPs with analysis tools |
| **Technology Stack** | ⚙️ | Detected services and frameworks |
| **Security Analysis** | 🛡️ | Ports, vulnerabilities, pre-pentest data |
| **Technical Files** | 📄 | robots.txt, sitemap.xml content |
| **Dorking Results** | 🔍 | Google Dorking findings (if enabled) |
| **PageSearch Results** | 📑 | Deep search findings (if enabled) |
| **API Results** | 🔌 | Third-party API data (if enabled) |

---

### General Information Section

Displays scan configuration and status:

| Field | Description |
|-------|-------------|
| **Robots.txt** | Download status (found/not found) |
| **Sitemap.xml** | Download status |
| **Sitemap Links** | Number of extracted links |
| **Google Dorking** | Enabled/disabled status |
| **PageSearch** | Enabled/disabled status |
| **Snapshotting** | Enabled/disabled status |
| **Report Created** | Timestamp of report generation |

---

### Scan Statistics Section

Provides at-a-glance metrics:

#### Overall Statistics

| Metric | Description |
|--------|-------------|
| **Subdomains Found** | Total discovered subdomains |
| **Social Media Links** | Total social media references |
| **Emails Found** | Extracted email addresses |
| **IP Addresses** | Resolved IP addresses |
| **Open Ports** | Detected open ports |
| **Vulnerabilities** | Potential security issues |

#### PageSearch Statistics (if enabled)

| Metric | Description |
|--------|-------------|
| **Accessible Subdomains** | Successfully crawled subdomains |
| **Email Addresses** | Emails found via deep search |
| **Documents** | Discovered files (PDF, DOC, etc.) |
| **Cookies** | Extracted cookies |
| **API Keys** | Exposed API keys |
| **Web Elements** | Hidden forms, inputs, comments |
| **Exposed Passwords** | Discovered credentials |

#### Interactive Charts

- **Bar Chart** — overall statistics visualization
- **Doughnut Chart** — social media platform distribution

---

### Domain Infrastructure Graph

Interactive network visualization powered by Vis.js:

#### Node Types

| Color | Type | Description |
|-------|------|-------------|
| 🟣 Purple | Domain | Central target domain |
| ⚫ Gray | Services | Detected technologies |
| 🔵 Blue | Subdomains | Discovered subdomains |
| 🩷 Pink | Socials | Social media links |
| 🩵 Teal | IPs | Resolved IP addresses |
| 🟠 Orange | Ports | Open ports |
| 🔴 Red | Vulnerabilities | Security issues |

#### Graph Controls

| Control | Function |
|---------|----------|
| **Filters** | Show/hide node types |
| **Search** | Find specific nodes with autocomplete |
| **Expand/Collapse** | Navigate node hierarchy |
| **Cluster/Uncluster** | Group nodes by type |
| **Fit View** | Auto-zoom to fit all nodes |
| **Physics Toggle** | Enable/disable force simulation |
| **Fullscreen** | Expand graph to full screen |

#### Export Options

| Format | Description |
|--------|-------------|
| **PNG** | Raster image export |
| **SVG** | Vector image export |
| **JSON** | Raw graph data |

#### Context Menu (Right-Click)

| Action | Description |
|--------|-------------|
| **Copy Label** | Copy node text to clipboard |
| **Copy All Data** | Copy complete node information |
| **Open Link** | Open URL in new tab |
| **Expand/Collapse** | Show/hide connected nodes |
| **Highlight Connected** | Emphasize related nodes |
| **Focus on Node** | Center view on node |
| **Hide Node** | Remove from view |

---

### WHOIS Information Section

Domain registration details:

| Field | Description |
|-------|-------------|
| **Domain** | Short domain name |
| **Full URL** | Complete URL with protocol |
| **IP Address** | Resolved IP |
| **Registrar** | Domain registrar |
| **Created** | Registration date |
| **Expires** | Expiration date |
| **Organization** | Registered organization |
| **Contacts** | Administrative emails |

---

### DNS & SSL Information Section

#### DNS Records

| Record Type | Description |
|-------------|-------------|
| **Name Servers** | NS records |
| **MX Records** | Mail exchange servers |

#### SSL Certificate

| Field | Description |
|-------|-------------|
| **Issuer** | Certificate authority |
| **Subject** | Certificate owner |
| **Valid From** | Issue date |
| **Valid Until** | Expiration date |
| **Common Name** | Certificate CN |
| **Serial Number** | Unique identifier |

---

### Social Media Section

#### Supported Platforms

| Platform | Icon | Description |
|----------|------|-------------|
| Facebook | 📘 | Pages, profiles, posts |
| Twitter / X | 🐦 | Profiles, tweets |
| Instagram | 📸 | Profiles, posts |
| Telegram | ✈️ | Channels, groups |
| TikTok | 🎵 | Profiles, videos |
| LinkedIn | 💼 | Company pages, profiles |
| VKontakte | 🔵 | Pages, groups |
| YouTube | ▶️ | Channels, videos |
| Odnoklassniki | 🟠 | Profiles, groups |
| WeChat | 💬 | Official accounts |

#### Social Media Analysis Table

Interactive DataTable with:

| Feature | Description |
|---------|-------------|
| **Search** | Filter by keyword |
| **Platform Filter** | Show specific platform |
| **Select All/Deselect** | Bulk selection |
| **Verify Links** | Check if links are accessible |
| **Archive.org** | Open selected in Wayback Machine |
| **Export CSV** | Download selected data |

---

### Subdomains Section

Interactive table with subdomain data:

#### Table Features

| Feature | Description |
|---------|-------------|
| **Search** | Filter subdomains |
| **Sorting** | Sort by any column |
| **Pagination** | Navigate large datasets |
| **Selection** | Select for bulk actions |

#### Bulk Actions

| Action | Description |
|--------|-------------|
| **Check Selected** | Verify subdomain accessibility |
| **Export CSV** | Download selected data |
| **Open All** | Open in new tabs |
| **Check SSL** | Verify SSL certificates |
| **Security Headers** | Analyze HTTP headers |
| **DNS Lookup** | Resolve DNS records |
| **WHOIS Info** | Get registration data |

---

### IP Addresses Section

Interactive table with IP analysis:

#### Table Features

| Column | Description |
|--------|-------------|
| **IP Address** | Resolved address |
| **Associated Subdomain** | Source subdomain |
| **Status** | Active/inactive |
| **Geolocation** | Country, city (when available) |

#### Bulk Actions

| Action | Description |
|--------|-------------|
| **Geolocate** | Get geographic location |
| **Export CSV** | Download data |
| **Shodan Lookup** | Search in Shodan |
| **VirusTotal** | Check reputation |
| **AbuseIPDB** | Check abuse reports |
| **Reverse DNS** | Get hostnames |
| **WHOIS** | Get IP registration data |

---

### Technology Stack Section

#### Detected Categories

| Category | Examples |
|----------|----------|
| **Web Servers** | Nginx, Apache, IIS |
| **CMS** | WordPress, Joomla, Drupal |
| **Programming Languages** | PHP, Python, Java |
| **Web Frameworks** | Django, Laravel, Rails |
| **Analytics** | Google Analytics, Yandex Metrica |
| **JavaScript Frameworks** | React, Vue, Angular |
| **Tags** | Technology identifiers |
| **CPE** | Common Platform Enumeration entries |

#### Technology Analysis Table

| Action | Description |
|--------|-------------|
| **Check CVEs** | Search for known vulnerabilities |
| **Filter by Category** | Show specific tech type |
| **Export CSV** | Download data |

---

### Security Analysis Section

#### Pre-Pentest Information

| Category | Description |
|----------|-------------|
| **Open Ports** | Discovered network ports |
| **Hostnames** | Related hostnames |
| **Potential Vulnerabilities** | Detected CVEs and issues |

#### Ports Analysis Table

| Feature | Description |
|---------|-------------|
| **Port Number** | Detected port |
| **Service** | Identified service |
| **Status** | Open/filtered/closed |
| **Filter by Service** | HTTP, SSH, FTP, DB, Mail, Remote |
| **Generate Nmap** | Create Nmap command for selected ports |
| **Export CSV** | Download data |

#### Vulnerabilities Analysis Table

| Feature | Description |
|---------|-------------|
| **CVE ID** | Vulnerability identifier |
| **Severity** | Critical/High/Medium/Low |
| **Description** | Vulnerability details |
| **Filter by Severity** | Show specific risk level |
| **Remediation Guide** | Generate fix recommendations |
| **Export Report** | Download vulnerability report |

##### Severity Badges

| Level | Color | Description |
|-------|-------|-------------|
| **Critical** | 🔴 Red (pulsing) | Immediate action required |
| **High** | 🟠 Orange | High priority fix |
| **Medium** | 🟡 Yellow | Should be addressed |
| **Low** | 🟢 Green | Minor issue |

---

### Technical Files Section

Collapsible sections containing:

| File | Description |
|------|-------------|
| **robots.txt** | Crawler directives from target |
| **sitemap.xml** | Site structure XML |
| **Sitemap Links** | Extracted URLs from sitemap |

---

### Optional Sections

These sections appear only when corresponding scan modes are enabled:

#### Dorking Results

Contains Google Dorking query results in preformatted text.

#### PageSearch Results

Contains deep search process output showing:

- Crawled subdomains
- Discovered files
- Extracted credentials
- Found keywords

#### API Results

##### VirusTotal Results

- Domain reputation
- Detected samples
- Malicious URLs

##### SecurityTrails Results

- Historical DNS data
- Deep subdomain enumeration
- DNS record changes

##### HudsonRock Results

- Compromised credentials
- Infostealer data
- Breach intelligence

---

### Interactive Features

#### Theme Toggle

| Theme | Description |
|-------|-------------|
| **Light** | Default bright theme |
| **Dark** | Dark mode for low-light viewing |

#### Export Options

| Option | Description |
|--------|-------------|
| **Print** | Browser print dialog |
| **PDF** | Generate PDF document |

#### Navigation

| Feature | Description |
|---------|-------------|
| **Sidebar TOC** | Collapsible table of contents |
| **Progress Bar** | Reading progress indicator |
| **Back to Top** | Quick navigation links |
| **Skip Link** | Accessibility jump to content |

#### Keyboard Accessibility

| Key | Action |
|-----|--------|
| **Tab** | Navigate between elements |
| **Enter** | Activate buttons, expand nodes |
| **Arrow Keys** | Navigate graph nodes |
| **Escape** | Close fullscreen, menus |

---

## Side Files

Additional files saved alongside reports:

| File/Folder | Description |
|-------------|-------------|
| **robots.txt** | Downloaded robots.txt (if accessible) |
| **sitemap.xml** | Downloaded sitemap (if accessible) |
| **ps_documents/** | Extracted documents from PageSearch |
| **screenshots/** | Domain screenshots (if snapshotting enabled) |
| **snapshots/** | HTML/PageCopy snapshots |
| **wayback_snapshots/** | Wayback Machine archives |

---

## Report Storage Database

DPULSE maintains a local SQLite database for report management.

### Database Details

| Property | Value |
|----------|-------|
| **Filename** | `report_storage.db` |
| **Format** | SQLite |
| **Created** | Automatically on first launch |
| **Location** | DPULSE-CLI root directory |
| **Portable** | Yes — can be moved between installations |

### Database Schema

| Field | Type | Description |
|-------|------|-------------|
| **id** | Integer | Auto-increment report ID |
| **report_file_extension** | String | Report format (html, xlsx) |
| **report_content** | BLOB/HTML | Complete report copy |
| **comment** | String | User-defined case comment |
| **target** | String | Scanned domain |
| **creation_date** | String | Report date (YYYYMMDD) |
| **dorks_results** | Text | Google Dorking results |
| **robots_text** | Text | robots.txt content |
| **sitemap_text** | Text | Sitemap links |
| **sitemap_file** | Text | sitemap.xml content |
| **api_scan** | String | Used APIs indicator |

![Database Structure](https://github.com/user-attachments/assets/491d1147-78ca-47a8-a405-5e351dc2730e)

### Database Manager

Access via DPULSE-CLI menu:

![Report Storage DB Manager](https://github.com/user-attachments/assets/519682dc-5d01-4844-8dcd-67e1914bb765)

#### Available Actions

| Action | Description |
|--------|-------------|
| **View Content** | Display all stored reports |
| **Recreate Report** | Regenerate report from database |
| **Delete Entry** | Remove report from database |

#### Viewing Database Content

![Database Content](https://github.com/user-attachments/assets/6778cf83-e9cf-4580-b46d-7c187cbdde9d)

#### Recreating Reports

![Report Recreation](https://github.com/user-attachments/assets/d7af9b03-703e-46b2-846b-05d99b33b900)

#### Recreated Report Example

![Recreated Report](https://github.com/user-attachments/assets/799d45cb-bc51-43ca-8b06-14e236d21912)
