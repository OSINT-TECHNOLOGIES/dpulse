# Installation and Quick Start

## System Requirements

DPULSE is built on Python and designed to run across various environments. To ensure stability and full functionality, your system must meet the following criteria:

*   **Operating System:** Linux (recommended), macOS, or Windows.
*   **Python Version:** Python **3.10**, **3.11**, or **3.12**.
    *   *Note:* Older versions (3.9 and below) are not supported due to dependency conflicts.
*   **Network:** A stable, high-speed internet connection is crucial. Modules like *Dorking Scan* and *PageSearch* rely on active scraping; unstable connections may lead to timeouts or incomplete results.
*   **Dependencies:**
    *   **Docker** (Recommended for isolation and ease of use).
    *   **Poetry** (Recommended for local Python installation).
    *   **Git** (Required for cloning the repository).

---

## Installation Methods

We provide three methods to install DPULSE. **Docker is the recommended method** as it eliminates environment conflicts.

### Method 1: Docker (Recommended)

Using Docker ensures you have all necessary system libraries pre-installed without polluting your host machine.

1.  **Pull the official image:**
    ```bash
    docker pull osinttechnologies/dpulse:latest
    ```

2.  **Run the container:**
    *   **Linux / macOS:**
        ```bash
        docker run --rm -it -v "$PWD":/data -w /data osinttechnologies/dpulse:latest
        ```
    *   **Windows (PowerShell):**
        ```powershell
        docker run --rm -it -v "${PWD}:/data" -w /data osinttechnologies/dpulse:latest
        ```

---

### Method 2: Poetry

If you prefer running DPULSE natively, use [Poetry](https://python-poetry.org/). It handles virtual environments and dependency locking automatically.

1.  **Clone the repository:**
    *   For the **Stable** version:
        ```bash
        git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
        cd dpulse
        ```
    *   For the **Rolling** (Dev) version:
        ```bash
        git clone --branch rolling --single-branch https://github.com/OSINT-TECHNOLOGIES/dpulse.git
        cd dpulse
        ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Run DPULSE:**
    ```bash
    poetry run python dpulse.py
    ```

---

### Method 3: Standard PIP (Legacy)

This method is available but **not recommended** due to potential version conflicts with other Python packages on your system.

1.  **Clone the repository and enter the directory:**
    ```bash
    git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
    cd dpulse
    ```

2.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run DPULSE:**
    ```bash
    python dpulse.py
    ```

> **Note:** The deprecated `.bat` and `.sh` installer scripts have been removed in favor of standard package managers to ensure security and reliability.

---

## Conducting Your First Scan

Once DPULSE is running, follow this workflow to perform a reconnaissance task.

### 1. Main Menu
Upon launch, the CLI interface will appear. To start a standard investigation, select **Option 1**.

![Main Menu](https://github.com/user-attachments/assets/5b45d4f0-9fad-4e17-8d74-96989037a66a)

### 2. Target Input
DPULSE operates strictly with **domain names** (e.g., `example.com`), not full URLs (e.g., `https://www.example.com/page`).

*   **Input:** Enter the target domain when prompted.
*   **Correction:** If you accidentally enter a URL, DPULSE will attempt to extract the domain, but manual input is preferred for accuracy.

![Target Input](https://github.com/user-attachments/assets/cc5676d5-e11c-4aeb-b0b4-dd4c23fa228a)

### 3. Scan Configuration (Modifiers)
You will be asked to configure the scan parameters. You can customize the depth and scope of the research:

*   **Case Comment:** A brief description for your internal records (e.g., "Investigation #42").
*   **PageSearch:** Enables deep crawling of the domain to find sensitive files (PDFs, configs) and exposed secrets.
    *   *Keywords:* If PageSearch is active, you can specify keywords to search for within downloaded documents.
*   **Dorking Mode:** Activates Google Dorking to find admin panels, IoT devices, or sensitive directories.
*   **API Usage:** Toggles third-party integrations (VirusTotal, SecurityTrails, HudsonRock).
*   **Snapshotting:** Enables capturing the target website's visual state via screenshots or Wayback Machine.

![Modifiers Selection](https://github.com/user-attachments/assets/9470350f-edf3-4692-b9bd-7c327cea2017)

### 4. Results
Once the scan is complete, DPULSE will generate a report in the `./reports` directory and save the case metadata to the local database.

![Scan Complete](https://github.com/user-attachments/assets/4e16f1e6-df60-441c-b730-79ea69134bb7)

You can now open the generated report file to view the gathered intelligence.
