## System requirements

DPULSE is a Python-based tool, so its basic requirement is installed Python. The most stable and tested versions are Python 3.10, 3.11 and 3.12. Other versions may decrease stability or even lead to problem with starting DPULSE because of used dependencies. It is also strongly recommended to have a high-speed and stable internet connection for stable work of such functions as Dorking scan and PageSearch which actively use web resources scraping. Also you need to install some Python packages using requirements.txt file or Poetry dependencies manager

## Installing DPULSE

You can install DPULSE in several ways, use the way you like the most. But since DPULSE repository is using Poetry to manage dependencies, it is higly recommended to install and start DPULSE using Poetry, especially on Linux systems where a lot of Python packages which DPULSE requires are preinstalled. More information about Poetry you can find on [Poetry official documentation page](https://python-poetry.org/docs/#ci-recommendations)

### Install and start DPULSE. Way №1 (using Poetry)

Use this set of commands to install DPULSE stable versions:

  ```
  git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
  cd dpulse
  poetry install
  ```

Use this set of commands to install DPULSE rolling versions:

  ```
  git clone --branch rolling --single-branch https://github.com/OSINT-TECHNOLOGIES/dpulse.git
  cd dpulse
  poetry install
  ```

After installation, you simply start DPULSE using `poetry run python dpulse.py`

### Install and start DPULSE. Way №2 (without using Poetry)

Just download DPULSE using fast-access links at the top of the README:

![image](https://github.com/user-attachments/assets/9ec2d2d7-706f-4385-9594-54e0cc72c695)

Decide what version you want to download and use basing on your expectations like stability, support, functionality and so on

Then just unpack downloaded archive, open terminal in DPULSE root folder and use `pip install -r requirements.txt` command to install requirements. Then type `python dpulse.py` in terminal, and that's where program starts.

If `pip install -r requirements.txt` doesn't work, then just use `poetry install` command. After that, start DPULSE with `poetry run python dpulse.py`

### Install and start DPULSE. Way №3 (using pip manager)

You also can install DPULSE using pip manager. It'll install DPULSE and necessery dependencies in one command: `pip install dpulse`. Then you just locate DPULSE root folder and type `python dpulse.py` to start program.

### Installers usage

DPULSE has two pre-written installation scripts, both for Windows (installer.bat) and for Linux (installer.sh). You can use them to clone repository and install dependencies or only for dependencies installation. Keep in mind that installer.bat (Windows installer) requires installed Git to clone repository.

#### Windows installer usage

You can start installer.bat from terminal by typing `./installer.bat` in terminal. Then you choose menu item which you want to start.

If you have problems with starting installer.bat, you should try to start it in admin terminal.

#### Linux installer usage

To start installer.sh in Linux you should follow these steps in your terminal:

```
sudo chmod +x installer.sh
sudo bash installer.sh
```

Then you choose menu item which you want to start.

If you have problems with starting installer.sh, you should try to use `dos2unix installer.sh` or `sed -i 's/\r//' installer.sh` commands.

### Conduct your first scan

#### Meet DPULSE main menu

After you successfully start DPULSE, you will see its main menu which contains some menu points. In order to conduct your first scan, you should select 1st point:

![image](https://github.com/user-attachments/assets/5b45d4f0-9fad-4e17-8d74-96989037a66a)

#### Correctly input your target

After selecting 1st menu point, you'll be asked to enter your target's domain name as shown below:

![image2](https://github.com/user-attachments/assets/cc5676d5-e11c-4aeb-b0b4-dd4c23fa228a)

DPULSE works only with domain names. Enter domain name when you are asked to determine target resource. When it is necessary, DPULSE will transform domain name in URL.

A domain name is a unique web address that can be acquired through domain registration. It’s the website’s equivalent to a physical address. It consists of a name and an extension, and it helps users easily find your website and eliminates the need to memorize the site’s Internet Protocol (IP) address. In the context of the internet, a domain name identifies a realm of administrative autonomy, authority, or control. Domain names are often used to identify services provided through the internet, such as websites, email services, and more. 

| URL  | Domain name |
| ------------- | ------------- |
| Example: https://www.bing.com/  | Example: bing.com  |
| String that provides the complete address of a web page  | Human-friendly text form of an IP address  |
| Contains the following parts: method, protocol, hostname, port, and path of the file  | Part of the URL and is mostly used for branding of the organization  |

#### Select the modifiers

After you've enter correct domain name of your target, you'll be asked to set some modifiers for your scan. These contain:

* Case comment: some brief description of what you are scanning and what do you want to find (actually you can enter anything here)
* Report file extension: type of your report file, as you can see it can be XLSX or HTML report
* PageSearch usage: determines if PageSearch will be used during scan
* PageSearch keywords (if previous modifier was set to Y): keywords which DPULSE will try to find in found PDF documents
* Dorking mode: determines which Dorking database will be used during scan, but can be declined with N flag
* Third-party APIs usage: determines which API will be used during scan, but can be declined with N flag
* Snapshotting usage: determines which type of snapshotting will be used during scan, but can be declined with N flag

Example of modifiers selection is shown below:

![image_mods](https://github.com/user-attachments/assets/9470350f-edf3-4692-b9bd-7c327cea2017)

#### Get the report!

After your first scan will be successfully ended, you will see this post-scan messages:

![image_report](https://github.com/user-attachments/assets/4e16f1e6-df60-441c-b730-79ea69134bb7)

This means that scan was ended, report was generated and scan results were written in report storage database. Congratulations, you successfully conducted your first scan using DPULSE!


