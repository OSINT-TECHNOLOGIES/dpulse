# Configuration File

DPULSE-CLI uses a central configuration file to control behaviour of all modules. All settings are stored in human readable INI format. Configuration is created automatically on first DPULSE launch with safe default values.

---

## General Information

| Property | Value |
|---|---|
| Filename | `config.ini` |
| Location | `/service/config.ini` |
| Format | INI |
| Created | Automatically on first launch |
| Editable | ✅ Via CLI or manually |

> 💡 You can always reset configuration to default values by deleting `config.ini` file. DPULSE-CLI will recreate it on next launch.

---

## Configuration Reference

All parameters grouped by functional sections.


---

### 📄 [HTML_REPORTING]

Report generation settings.

| Parameter | Possible values | Default | Description | Recommendation |
|---|---|---|---|---|
| `template` | `modern` / `legacy` | `modern` | HTML report template. Modern template contains all interactive features, graphs and tables. Legacy template is deprecated and kept only for compatibility. | ✅ Always use `modern` |
| `delete_txt_files` | `y` / `n` | `n` | If enabled, DPULSE will delete separate `robots.txt` and `sitemap.xml` files from report folder. These files are already embedded inside HTML report. | Use `y` if you don't need separate copies |


---

### 📝 [LOGGING]

Logging settings.

| Parameter | Possible values | Default | Description |
|---|---|---|---|
| `log_level` | `debug` / `info` / `warning` / `error` / `critical` | `info` | Verbosity level of `journal.log` file. |

> 💡 Set to `debug` only if you are reporting a bug or troubleshooting issues.


---

### 🎨 [CLI_VISUAL]

Interface appearance settings.

| Parameter | Possible values | Default | Description |
|---|---|---|---|
| `preview_color` | `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` | `red` | Color of DPULSE ASCII banner on launch. |
| `font` | Any figlet font name | `slant` | Font used for ASCII banner. |


---

### 🔍 [DORKING]

Google Dorking module settings. This is one of the most important sections for reliable dorking.

| Parameter | Possible values | Default | Description | Recommendation |
|---|---|---|---|---|
| `dorking_delay (secs)` | Integer >= 0 | `2` | Delay in seconds between dork queries. | ✅ Minimum 2 seconds. Lower values will almost certainly result in captcha. |
| `delay_step` | Integer > 0 | `5` | Number of dorks after which additional delay is applied. | Recommended 5-10 |
| `full_path_to_browser` | Full path to browser executable | None | Path to browser that will be used for dorking. | ✅ Use Chrome or Firefox. Edge works too. |
| `browser_mode` | `headless` / `nonheadless` | `nonheadless` | Browser mode. Headless mode runs browser in background. |

> ⚠️ Very important note: Headless mode is detected by Google 100% of the time. You will get captcha after 2-3 dorks. **Always use nonheadless mode**. This is the only working method to bypass Google captcha and rate limits.


---

### 📸 [SNAPSHOTTING]

Screenshot and snapshot module settings.

| Parameter | Possible values | Default | Description |
|---|---|---|---|
| `installed_browser` | `firefox` / `chrome` / `edge` / `opera` | `firefox` | Browser that will be used for taking screenshots and snapshots. |
| `opera_browser_path` | Full path / `None` | `None` | Full path to Opera executable. Required only if you selected Opera as browser. |
| `wayback_retries` | Integer > 0 | `3` | Number of retries for Wayback Machine requests. |
| `wayback_req_pause` | Integer > 0 | `2` | Delay in seconds between Wayback Machine retries. |


---

### 🕵️ [USER-AGENTS]

List of user agent strings used for all requests. DPULSE-CLI selects random user agent from this list for each request.

| Parameter | Description |
|---|---|
| `agent_1` ... `agent_20` | User agent strings |

> 💡 You can add your own user agents, or modify existing ones. You can add up to 99 agents.


---

### 🔌 [PROXIES]

Proxy support settings.

| Parameter | Description |
|---|---|
| `proxies_file_path` | Full path to text file with proxies, one proxy per line. Set to `NONE` to disable proxies. |

> Proxy format: `http://user:pass@host:port` or `socks5://user:pass@host:port`


---

## Editing Configuration

You don't need to edit config.ini file manually. DPULSE-CLI has built-in configuration editor available directly from CLI.


---

### Step 1: Open Settings Menu

From main menu select **Option 2: Settings**:

![Main Menu Settings](https://github.com/user-attachments/assets/d4eda335-102c-4dc6-ab5d-206ac01202d8)


---

### Step 2: Select Action

Settings menu contains two options:

| Option | Action |
|---|---|
| **Print current config file** | Display full current configuration in CLI |
| **Edit config file** | Open interactive configuration editor |

![Settings Menu](https://github.com/user-attachments/assets/035e5a94-ca5f-43ca-89c7-8fca36048243)


---

### View Current Configuration

Select first option to see all current parameters and values:

![Config Preview](https://github.com/user-attachments/assets/a86ee852-0b2c-4c83-9a48-bca7499c4671)


---

### Edit Configuration

Select second option to open interactive editor:

1. Enter section name you want to edit
2. Enter parameter name
3. Enter new value

![Config Editor](https://github.com/user-attachments/assets/b522f2d8-e05e-43a5-968e-b0306ad1de2e)

> ✅ Changes are applied immediately and will be used for all next scans. You don't need to restart DPULSE.


---

## Reset Configuration

If you want to reset all settings to default values:

1. Close DPULSE-CLI
2. Delete file `/service/config.ini`
3. Launch DPULSE-CLI again

Configuration file will be recreated with all default values.

---
