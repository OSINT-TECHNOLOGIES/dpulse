# Automatic Google Dorking Scan Mode

Automatic Google Dorking scan is an extended domain research function that uses prepared query databases to discover hidden resources, sensitive files, and exposed interfaces on the target domain.

> **Note:** Dorking scan is optional — you can enable or disable it during pre-scan preparation steps.

---

## How Dorking Scan Works

1. Takes the target domain
2. Applies pre-built dork queries from selected database
3. Searches Google for matches
4. Returns discovered URLs and resources

---

## Prepared Dorking Databases

DPULSE-CLI includes four specialized dorking databases:

| Database | Dorks Count | Purpose |
|----------|-------------|---------|
| **IoT Dorking** | 20 | Find IoT devices, cameras, sensors |
| **Files Dorking** | 30 | Discover documents and file types |
| **Admin Panels Dorking** | 72 | Locate admin interfaces and login pages |
| **Web Elements Dorking** | 25 | Find directories, configs, sensitive paths |

---

### 🔌 IoT Dorking (20 dorks)

Discovers IoT devices, cameras, and network services:

| Category | Examples |
|----------|----------|
| **Common IoT ports** | `:8080`, `:1883`, `:8883`, `:554`, `:81` |
| **Service ports** | `:5000`, `:9000`, `:10000` |
| **Device keywords** | `device`, `camera`, `sensor`, `firmware` |
| **Interface keywords** | `control`, `status`, `monitor`, `stream` |
| **Other** | `debug`, `service`, `api`, `video` |

<details>
<summary>View all IoT dorks</summary>

```
inurl:":8080" site:{}
inurl:":1883" site:{}
inurl:":8883" site:{}
inurl:":554" site:{}
inurl:":81" site:{}
inurl:":5000" site:{}
inurl:":9000" site:{}
inurl:":10000" site:{}
inurl:debug site:{}
inurl:device site:{}
inurl:control site:{}
inurl:status site:{}
inurl:service site:{}
inurl:monitor site:{}
inurl:stream site:{}
inurl:video site:{}
inurl:camera site:{}
inurl:sensor site:{}
inurl:api site:{}
inurl:firmware site:{}
```

</details>

---

### 📁 Files Dorking (30 dorks)

Discovers various file types indexed by search engines:

| Category | File Types |
|----------|------------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.xlsx`, `.xls`, `.ppt`, `.pptx` |
| **Data files** | `.txt`, `.csv`, `.xml`, `.json` |
| **Web files** | `.html`, `.php`, `.asp`, `.aspx`, `.js`, `.css` |
| **Media** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.mp3`, `.mp4`, `.avi` |
| **Archives** | `.zip`, `.rar` |
| **Sensitive** | `.sql`, `.db`, `.conf`, `.ini` |

<details>
<summary>View all Files dorks</summary>

```
filetype:pdf site:{}
filetype:doc site:{}
filetype:docx site:{}
filetype:xlsx site:{}
filetype:xls site:{}
filetype:ppt site:{}
filetype:pptx site:{}
filetype:txt site:{}
filetype:csv site:{}
filetype:xml site:{}
filetype:json site:{}
filetype:html site:{}
filetype:php site:{}
filetype:asp site:{}
filetype:aspx site:{}
filetype:js site:{}
filetype:css site:{}
filetype:jpg site:{}
filetype:jpeg site:{}
filetype:png site:{}
filetype:gif site:{}
filetype:mp3 site:{}
filetype:mp4 site:{}
filetype:avi site:{}
filetype:zip site:{}
filetype:rar site:{}
filetype:sql site:{}
filetype:db site:{}
filetype:conf site:{}
filetype:ini site:{}
```

</details>

---

### 🔐 Admin Panels Dorking (72 dorks)

Discovers admin interfaces for various CMS and frameworks:

| Platform | Dorks Count |
|----------|-------------|
| WordPress | 4 |
| Joomla | 3 |
| Drupal | 3 |
| phpMyAdmin | 3 |
| Magento | 3 |
| vBulletin | 3 |
| osCommerce | 2 |
| PrestaShop | 3 |
| OpenCart | 2 |
| Zen Cart | 2 |
| MediaWiki | 2 |
| Moodle | 2 |
| Concrete5 | 2 |
| TYPO3 | 2 |
| Plone | 2 |
| Django | 1 |
| Ruby on Rails | 2 |
| Craft CMS | 2 |
| ExpressionEngine | 2 |
| Kentico | 2 |
| Umbraco | 2 |
| Sitecore | 2 |
| DotNetNuke | 2 |
| SharePoint | 2 |
| Plesk | 2 |
| Generic admin | 15 |

<details>
<summary>View all Admin Panels dorks</summary>

```
site:{} intitle:"WordPress Login"
site:{} inurl:/wp-admin/
site:{} intext:"Войти в WordPress"
site:{} intitle:"Dashboard" "WordPress"
site:{} intitle:"Joomla! Administrator Login"
site:{} inurl:/administrator/
site:{} intitle:"Joomla! 3.x" "Login"
site:{} intitle:"Drupal login"
site:{} inurl:/user/login
site:{} intitle:"Drupal 8" "Login"
site:{} intitle:"phpMyAdmin"
site:{} inurl:/phpmyadmin/
site:{} intitle:"phpMyAdmin 4.x"
site:{} intitle:"Magento Admin"
site:{} inurl:/admin/
site:{} intitle:"Magento 2" "Admin"
site:{} intitle:"vBulletin Admin CP"
site:{} inurl:/admincp/
site:{} intitle:"vBulletin 4.x" "Admin"
site:{} intitle:"osCommerce Administration"
site:{} intitle:"osCommerce 2.x" "Admin"
site:{} intitle:"PrestaShop Back Office"
site:{} inurl:/admin-dev/
site:{} intitle:"PrestaShop 1.7" "Back Office"
site:{} intitle:"OpenCart Admin Panel"
site:{} intitle:"OpenCart 3.x" "Admin"
site:{} intitle:"Zen Cart Admin"
site:{} intitle:"Zen Cart 1.5" "Admin"
site:{} intitle:"MediaWiki" "Special:UserLogin"
site:{} inurl:/mediawiki/index.php/Special:UserLogin
site:{} intitle:"Moodle" "Log in to the site"
site:{} inurl:/login/index.php
site:{} intitle:"Concrete5" "Sign In"
site:{} inurl:/index.php/dashboard/
site:{} intitle:"TYPO3" "Backend Login"
site:{} inurl:/typo3/
site:{} intitle:"Plone" "Log in"
site:{} inurl:/login_form
site:{} intitle:"Django" "Site administration"
site:{} inurl:/rails/admin/
site:{} intitle:"Ruby on Rails" "Admin"
site:{} intitle:"Craft CMS" "Control Panel"
site:{} inurl:/admin/
site:{} intitle:"ExpressionEngine" "Control Panel"
site:{} inurl:/admin.php
site:{} intitle:"Kentico" "CMS Desk"
site:{} inurl:/cmsdesk/
site:{} intitle:"Umbraco" "Backoffice"
site:{} inurl:/umbraco/
site:{} intitle:"Sitecore" "Launchpad"
site:{} inurl:/sitecore/
site:{} intitle:"DotNetNuke" "Host"
site:{} inurl:/host/
site:{} intitle:"SharePoint" "Sign In"
site:{} inurl:/_layouts/15/
site:{} intitle:"Plesk" "Login"
site:{} inurl:login.php?user=admin
site:{} inurl:dashboard
site:{} intitle:"admin login"
site:{} intitle:"administrator login"
site:{} "admin panel"
site:{} inurl:panel
site:{} inurl:cp
site:{} inurl:controlpanel
site:{} inurl:backend
site:{} inurl:management
site:{} inurl:administration
site:{} intitle:"admin access"
site:{} intitle:"control panel"
site:{} "admin login" +directory
site:{} "administrator login" +password
site:{} inurl:/plesk-login/
```

</details>

---

### 🌐 Web Elements Dorking (25 dorks)

Discovers sensitive directories and exposed paths:

| Category | Keywords |
|----------|----------|
| **Directories** | `index of`, `backup`, `old`, `temp` |
| **Upload/Download** | `upload`, `download` |
| **Configuration** | `config`, `setup`, `install` |
| **Data storage** | `database`, `log` |
| **Debug & API** | `debug`, `api` |
| **Sensitive** | `secret`, `private`, `secure`, `password` |
| **Authentication** | `auth`, `token`, `session` |
| **Admin** | `admin`, `login`, `dashboard`, `panel` |

<details>
<summary>View all Web Elements dorks</summary>

```
site:{} intext:"index of"
site:{} inurl:admin
site:{} inurl:login
site:{} inurl:dashboard
site:{} inurl:wp-content
site:{} inurl:backup
site:{} inurl:old
site:{} inurl:temp
site:{} inurl:upload
site:{} inurl:download
site:{} inurl:config
site:{} inurl:setup
site:{} inurl:install
site:{} inurl:database
site:{} inurl:log
site:{} inurl:debug
site:{} inurl:api
site:{} inurl:secret
site:{} inurl:private
site:{} inurl:secure
site:{} inurl:password
site:{} inurl:auth
site:{} inurl:token
site:{} inurl:session
site:{} inurl:panel
```

</details>

---

## Creating Custom Dorking Database

DPULSE-CLI allows you to create your own custom Google Dorking database for specialized research needs.

---

### Step 1: Open Custom DB Generator

Navigate through DPULSE-CLI menus to access the custom Dorking DB generator:

![Dorking Menu](https://github.com/user-attachments/assets/fc8fe1ba-1845-46d1-a9b9-d09d3dc03ce6)

---

### Step 2: Create Your Database

Follow the interactive prompts:

| Prompt | Description |
|--------|-------------|
| **Database name** | Enter name without extension (e.g., `my_custom_dorks`) |
| **Dork ID** | Starts at 1, auto-increments |
| **Dork query** | Your custom dork query |

> **Important:** Use `{}` as a placeholder for the domain. DPULSE-CLI will replace it with the actual target domain during scan.

**Example dork format:**
```
site:{} inurl:secret-endpoint
```

![Custom Dork Generator](https://github.com/user-attachments/assets/8f3e8ca5-feec-4bf5-add8-048f54931b67)

---

### Step 3: Use Your Database

After creation, your new `.db` file appears in the `dorking` folder and can be selected for scans:

![Custom DB Result](https://github.com/user-attachments/assets/0cd4facc-215b-4e56-ab56-aa23cb5136db)

**Database structure preview:**

![Database Inside](https://github.com/user-attachments/assets/023467c2-008b-451f-8e14-88b7e54a8c3c)

---

## When to Use Dorking Scan

| Scenario | Recommendation |
|----------|----------------|
| Looking for exposed files | ✅ Use Files Dorking |
| Finding admin panels | ✅ Use Admin Panels Dorking |
| IoT device discovery | ✅ Use IoT Dorking |
| General reconnaissance | ✅ Use Web Elements Dorking |
| Quick scan | ❌ Skip Dorking (adds time) |
| Stealth required | ❌ Skip Dorking (leaves traces in Google) |

> **Warning:** Google may rate-limit or block requests if too many dork queries are executed quickly. DPULSE includes delays to minimize this risk.
