# DPULSE - Domain Public Data Collection Service 

<p align="center">
  <img src="https://github.com/user-attachments/assets/e49c764a-5039-4a54-b002-6b625f0b371b">
</p>

<p align="center">
<b><i>CONVENIENT, FAST AND USER-FRIENDLY COLLECTOR OF DOMAIN INFORMATION FROM OPEN SOURCES</i></b>
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/v1.2-CURRENT%20STABLE%20VERSION?style=for-the-badge&label=CURRENT%20STABLE%20VERSION&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/None-red?style=for-the-badge&logo=f&label=CURRENT%20ROLLING%20VERSION">
<img alt="Static Badge" src="https://img.shields.io/badge/DOMAIN_OSINT-CATEGORY?style=for-the-badge&label=TOOL%20CATEGORY&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/CLI-CATEGORY?style=for-the-badge&label=interface%20type&color=red">
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/supports-virustotal_api-red?style=for-the-badge"> <img alt="Static Badge" src="https://img.shields.io/badge/supports-securitytrails_api-red?style=for-the-badge">

</p>

> Attention! DPULSE is a research tool. It is not intended for criminal activities! Use DPULSE only on allowed domains and for legal purposes!

> Please, before creating an issue or DMing developer about DPULSE, make sure that your problem or question is not covered with [DPULSE documentation](https://dpulse.readthedocs.io)

# Repository map

## What to visit?

| What do you want to see? | Link |
| --- | --- |
| I want to read project documentation | [See DPULSE Readthedocs Page](https://dpulse.readthedocs.io) |
| I want to see developer's contacts | [See "Contact developer" page on Readthedocs](https://dpulse.readthedocs.io/en/latest/contact_dev/#) |
| I want to see project roadmap and future development plans | [See DPULSE roadmap](https://github.com/users/OSINT-TECHNOLOGIES/projects/1) |

## What to download?

| Your expectations | Version and link for you |
| --- | --- |
| I want to use only tested and stable version of DPULSE | [DPULSE stable ZIP archive](https://github.com/OSINT-TECHNOLOGIES/dpulse/archive/refs/heads/main.zip) |
| I don't mind to use DPULSE with latest changes and I'm OK with bugs and issues  | [DPULSE rolling ZIP archive](https://github.com/OSINT-TECHNOLOGIES/dpulse/archive/refs/heads/rolling.zip) |
| I want to use only one specific version of DPULSE  | [See DPULSE releases page](https://github.com/OSINT-TECHNOLOGIES/dpulse/releases) |
| I want to see more detailed installation instructions | [See DPULSE installation guides](https://github.com/OSINT-TECHNOLOGIES/dpulse?tab=readme-ov-file#how-to-install-and-run-dpulse)


# About DPULSE

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. In general, it provides you with a certain set of functions, such as:

1. ***Basic scan:*** extracts general information about domain, such as
   - WHOIS information
   - subdomains
   - e-mail addresses
   - IP addresses
   - social medias links/posts/profiles
   - SSL certificate info
   - possible vulnerabilities
   - open ports
   - CPEs, used web-technologies and so on
   - It also can download sitemap.xml and robots.txt files from a domain
     
2. ***PageSearch standard scan:*** extended subdomains deep search function, which starts in addition to basic scan and which can find:
   - more e-mail addresses
   - API keys
   - exposed passwords
   - cookies
   - hidden forms of data and other web page elements
   - documents, config files, databases files (and PageSearch can download them!)
   - specified words by user in PDF files

3. ***PageSearch Sitemap inspection scan:*** sitemap links crawler which starts in addition to basic scan and which can find even more e-mails

4. ***Dorking scan:*** extended domain research function with prepared Google Dorking databases for different purposes, such as:
   - IoT dorking
   - files dorking
   - admin panels dorking
   - web elements dorking
   - Moreover, this mode allows you to create your own custom Google Dorking database

6. ***API scan:*** extended domain research function with prepared functions for 3rd party APIs usage. Currently DPULSE supports these API:
    - VirusTotal API (for brief domain information gathering)
    - SecurityTrails API (deep subdomains and DNS enumeration)

Finally, DPULSE compiles all found data into an easy-to-read HTML or XLSX report by category. It also saves all information about scan in local report storage database, which can be restored later.

# How to install and run DPULSE

## _Recommended ways_

Since DPULSE repository is using Poetry* to manage dependencies, it is higly recommended to install and start DPULSE using Poetry, especially on Linux systems where a lot of Python packages which DPULSE requires are preinstalled.

_* Poetry is a tool for dependency management and packaging in Python. It can be simply installed everywhere using `pip install poetry` command, but more instructions you can find on [Poetry official documentation page](https://python-poetry.org/docs/#ci-recommendations)_

### <ins>First way (the simplest way)</ins>

Just download DPULSE using fast-access links at the top of the README:

![изображение](https://github.com/user-attachments/assets/bd1d9627-950b-40d4-91c4-6751476d7b65)

Then just unpack downloaded archive, open terminal in DPULSE root folder and use `pip install -r requirements.txt` command to install requirements. Then type `python dpulse.py` in terminal, and that's where program starts.

If `pip install -r requirements.txt` doesn't work, then just use `poetry install` command. After that, start DPULSE with `poetry run python dpulse.py`

### <ins>Second way (the most correct way)</ins>

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

## _Other ways_

### <ins>Third way (using pip manager)</ins>

You also can install DPULSE using pip manager. It'll install DPULSE and necessery dependencies in one command: `pip install dpulse`. Then you just locate DPULSE root folder and type `python dpulse.py` to start program.

## _Installers usage_

DPULSE has two pre-written installation scripts, both for Windows (installer.bat) and for Linux (installer.sh). You can use them to clone repository and install dependencies or only for dependencies installation. Keep in mind that installer.bat (Windows installer) requires installed Git to clone repository.

### <ins>Windows installer usage</ins>

You can start installer.bat from terminal by typing `./installer.bat` in terminal. Then you choose menu item which you want to start.

If you have problems with starting installer.bat, you should try to start it in admin terminal.

### <ins>Linux installer usage</ins>

To start installer.sh in Linux you should follow these steps in your terminal:

  ```
  sudo chmod +x installer.sh
  sudo bash installer.sh
  ```
Then you choose menu item which you want to start.

If you have problems with starting installer.sh, you should try to use `dos2unix installer.sh` or `sed -i 's/\r//' installer.sh` commands.

# DPULSE demo and use-cases

### You can start DPULSE and see the main menu on the screen using one of the recommended commands in DPULSE root folder. Don't forget to install all requirements before starting DPULSE

![dpulse_start](https://github.com/user-attachments/assets/9ec0ab73-2206-4d38-bae6-e88656e17f95)

### After choosing first menu point, you will be able to enter target's URL and case comment, and then you will see scanning progress

![dpulse_bs](https://github.com/user-attachments/assets/b0ad7827-6dac-4f82-a369-4447a0e1c878)

### Finally, DPULSE will create report folder which contains case name (basically URL of target), date and time of scan. All report folders are contained in DPULSE root folder

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7de73250-c9b6-4373-b21e-16bbb7a63882)


# Tasks to complete before new release
- [ ] Add web pages snapshoting (with screenshots)
- [ ] Add web pages snapshoting (with web pages copying as HTML objects)
- [ ] Add web pages snapshoting (with Wayback Machine)
      
# DPULSE mentions in social medias

## Mention on OSINT/Infosec related websites:

### [Mention on osinttools.io](https://osinttools.io/tools/dpulse/)

## X.com mentions:

### [by @DarkWebInformer](https://x.com/DarkWebInformer/status/1787583156775759915?t=Ak1W9ddUPpDvLAkVyQG8fQ&s=19)

### [by @0xtechrock](https://x.com/0xtechrock/status/1804470459741978974?t=us1EVJEECNZdSmSe5CQjQA&s=19)

### [by @OSINTech_](https://x.com/OSINTech_/status/1805902553885888649)

### [by @cyb_detective](https://x.com/cyb_detective/status/1821337404763959487?t=vbyRUeXM2C6gf47l7XvJnQ&s=19)

### [by @DailyOsint](https://x.com/DailyOsint/status/1823013991951523997?t=Fr-oDCZ2pFmFJpUT3BKl5A&s=19)

### [by @UndeadSec](https://x.com/UndeadSec/status/1827692406797689032)

### [by @akaclandestine](https://x.com/akaclandestine/status/1875980998418002151?t=Ac-fZ9oe2FLKkTTCClss8g&s=19)

### [by @hdH4dg8](https://x.com/hdH4dg8/status/1876106586869104906?t=Awfas25ukXkblPRt4krSzA&s=19)

### [by @wy88215534](https://x.com/wy88215534/status/1876522251828494794?t=cmwoNCDZv0kMEDMKokcVFA&s=19)

## Facebook mentions:

### [by Inteligência Cibernética](https://www.facebook.com/osintbrasil/posts/pfbid037ibycZcBWe2MjtV4HiWvRWxyKei8TJ5Ycfxai4TDNHXuwrYkDGuyjDsPow8WUNbyl)

### [by Suboxone hackers society](https://www.facebook.com/groups/1277175496530786/posts/1578570389724627/)

## LinkedIn mentions:

### [by Maory Schroder](https://fr.linkedin.com/posts/maory-schroder_osint-cybers%C3%A9curit%C3%A9-pentest-activity-7227562302009491456-sXoZ?trk=public_profile)

### [by Maxim Marshak](https://www.linkedin.com/pulse/bormaxi8080-osint-timeline-64-27062024-maxim-marshak-jojbf)

### [by DailyOSINT](https://www.linkedin.com/posts/daily-osint_osint-reconnaissance-infosec-activity-7228779678096850946-H-zC)

### [by 7HacX](https://www.linkedin.com/posts/7hacx_domain-osint-whois-activity-7228763157912002560-26Wc)

## Telegram mentions:

### [by Cyber Detective](https://t.me/cybdetective/2706)

### [by Hackers Factory](https://t.me/dilagrafie/3673)

### [by C.I.T Security](https://t.me/citsecurity/8578)

### [by Adityaa_oky](https://t.me/adityaa_oky/960)

### [by Реальний OSINT](https://t.me/realOSINT/462)





