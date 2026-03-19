# Installation and Quick Start

---

## System Requirements

DPULSE is built on Python and designed to run across various environments. To ensure stability and full functionality, your system must meet the following criteria:

| Requirement | Details |
|-------------|---------|
| **Operating System** | Linux (recommended), macOS, or Windows |
| **Python Version** | Python **3.11** |
| **Network** | Stable, high-speed internet connection |

> **Note:** Python versions except 3.11 are not supported. According to this fact, recommended installation methods use virtual environments so you don't worry about dependencies and other projects conflicts.

### Required Tools

- **Docker** — recommended for isolation and ease of use
- **uv** — recommended for local Python 3.11 and dependencies installation using virtual environment
- **Git** — required for cloning the repository

---

## Installation Methods

We provide two methods to install DPULSE. **Docker is the recommended method** as it eliminates environment conflicts and uses containers for isolation. You can use **uv** installation method if you want to install DPULSE locally. This method provides installation with further virtual environment activation when you start DPULSE, so dependencies and versions conflicts won't appear.

---

### 🐳 Method 1: Docker (Recommended)

Using Docker ensures you have all necessary system libraries pre-installed without polluting your host machine.

**Step 1:** Pull the official image

```
# If you're using default Docker client
docker pull docker.io/osinttechnologies/dpulse:latest

# In case you are using Podman, which is Docker alternative in some OS:
podman pull docker.io/osinttechnologies/dpulse:latest
```

**Step 2:** Run the container

| Platform | Command |
|----------|---------|
| **Linux / macOS** | `docker run --rm -it -v "$PWD":/data -w /data osinttechnologies/dpulse:latest` |
| **Windows (PowerShell)** | `docker run --rm -it -v "${PWD}:/data" -w /data osinttechnologies/dpulse:latest` |
| **Linux / macOS (Podman)** | `podman run --rm -it -v "$PWD":/data:Z -w /data osinttechnologies/dpulse:latest` |

---

### 📦 Method 2: uv

If you prefer running DPULSE natively, use **uv** package. It handles virtual environments, correct Python version installation and dependency lock automatically.

```
# 1. Clone the repository
git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
cd dpulse

# 2.1. Run Linux/macOS installer
chmod +x install.sh
./install.sh

# 2.2. Run Windows installer
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

These installers will automatically:
- install `uv` if it is missing
- install Python 3.11 which is strongly required for running DPULSE
- create a virtual environment
- install all required dependencies

After this procedure you can easily start DPULSE:
```
uv run dpulse
```
---

## Conducting Your First Scan

Once DPULSE is running, follow this workflow to perform a reconnaissance task.

---

### 1️⃣ Main Menu

Upon launch, the CLI interface will appear. To start a standard investigation, select **Option 1**.

![Main Menu](https://github.com/user-attachments/assets/900a1e55-a6b4-4746-96c6-27e6bd9fd6a6)

---

### 2️⃣ Target Input

DPULSE operates strictly with **domain names**, not full URLs.

| Input Type | Example | Valid? |
|------------|---------|--------|
| Domain name | `example.com` | ✅ Yes |
| Full URL | `https://www.example.com/page` | ❌ No |

> **Note:** If you accidentally enter a URL, DPULSE will attempt to extract the domain, but manual input is preferred for accuracy.

![Target Input](https://github.com/user-attachments/assets/cc5676d5-e11c-4aeb-b0b4-dd4c23fa228a)

---

### 3️⃣ Scan Configuration (Modifiers)

You will be asked to configure the scan parameters. Available options:

| Modifier | Description |
|----------|-------------|
| **Case Comment** | Brief description for internal records (e.g., "Investigation #42") |
| **PageSearch** | Deep crawling to find sensitive files (PDFs, configs) and exposed secrets |
| **Keywords** | Custom keywords to search within downloaded documents (requires PageSearch) |
| **Dorking Mode** | Google Dorking to find admin panels, IoT devices, sensitive directories |
| **API Usage** | Third-party integrations (VirusTotal, SecurityTrails, HudsonRock) |
| **Snapshotting** | Capture website's visual state via screenshots, HTML copy, or Wayback Machine |

![Modifiers Selection](https://github.com/user-attachments/assets/61f12480-61ee-4202-a477-28c3342f7994)

---

### 4️⃣ Results

Once the scan is complete, DPULSE will:

- Generate a report and put it into a named folder (ex. "report_hackthissiteorg_(19-03-2026, 17h53m16s)"
- Save case metadata to the local database

![Scan Complete](https://github.com/user-attachments/assets/4e16f1e6-df60-441c-b730-79ea69134bb7)

You can now open the generated report file to view the gathered intelligence.

---
