# DPULSE - Domain Public Data Collection Service 

<p align="center">
  <img src="https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/fed8d368-7309-4aaa-a82e-2f0b277122de">
</p>

<p align="center">
<b><i>CONVENIENT, FAST AND USER-FRIENDLY COLLECTOR OF DOMAIN INFORMATION FROM OPEN SOURCES</i></b>
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/v1.0.5-ACTUAL%20STABLE%20VERSION?style=for-the-badge&label=ACTUAL%20STABLE%20VERSION&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/DOMAIN_OSINT-CATEGORY?style=for-the-badge&label=TOOL%20CATEGORY&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/CLI-CATEGORY?style=for-the-badge&label=interface%20type&color=red">
</p>
<p align="center">
<img alt="GitHub License" src="https://img.shields.io/github/license/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red">
</p>

> DPULSE was created as a research tool, and it is not intended for criminal activities. Use DPULSE only on allowed domains and for legal purposes!

> You can visit [DPULSE wiki](https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki/DPULSE-WIKI) in order to get more technical information about this project

> You can visit [DPULSE roadmap](https://github.com/users/OSINT-TECHNOLOGIES/projects/1) to get more information about development process

> You can also contact the developer via e-mail: osint.technologies@gmail.com


# About DPULSE

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. Using this software you can extract useful information such as:
1. PageSearch function [BETA] which gives opportunity to extract public documents, find keywords (temporarily only in PDF files) and more
2. WHOIS information 
3. Subdomains
4. Mentions of the domain's owner organization in some social networks, as well as organization profiles in social networks.
5. IP addresses
6. Automated Google Dorking related to domain
7. InternetDB search results (possible vulnerabilities, open ports and so on)
8. Used web-technologies
9. Sitemap, robots.txt files, SSL certificate info
  
All this data is compiled into an easy-to-read PDF or XLSX report by category.


# How to install and run DPULSE

## _Recommended ways_

Since DPULSE repository is using Poetry* to manage dependencies, it is higly recommended to install and start DPULSE using Poetry, especially on Linux systems where a lot of Python packages which DPULSE requires are preinstalled.

_* Poetry is a tool for dependency management and packaging in Python. It can be simply installed everywhere using `pip install poetry` command, but more instructions you can find on [Poetry official documentation page](https://python-poetry.org/docs/#ci-recommendations)_

### First way (recommended on every OS, using Poetry)

Use this set of commands to use recommended way of DPULSE installation:

  ```
  git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
  cd dpulse
  poetry install
  ```
Then you simply start DPULSE using `poetry run python dpulse.py`

### Second way (recommended on Windows systems, without using Poetry)

Simply download zip archive from assets in releases bookmark, just right here:

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/bd2ebf09-a31c-4e27-a674-5b602808a667)

Then you just unpack the archive, open terminal in DPULSE root folder and use `pip install -r requirements.txt` command to install requirements. Then type `python dpulse.py` in terminal, and that's where program starts.

You also can use this installation way with some different approach using this set of commands:

  ```
  git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
  cd dpulse
  pip install -r requirements.txt
  ```

## _Other ways_

### Third way (using pip)

You also can install DPULSE using pip manager. It'll install DPULSE and necessery dependencies in one command: `pip install dpulse`. Then you just locate DPULSE root folder and type `python dpulse.py` to start program.

## _Installers usage_

DPULSE has two pre-written installation scripts, both for Windows (installer.bat) and for Linux (installer.sh). You can use them to clone repository and install dependencies or only for dependencies installation. Keep in mind that installer.bat (Windows installer) requires installed Git to clone repository.

### Windows installer usage

You can start installer.bat from terminal by typing `./installer.bat` in terminal. Then you choose menu item which you want to start.

If you have problems with starting installer.bat, you should try to start it in admin terminal.

### Linux installer usage

To start installer.sh in Linux you should follow these steps in your terminal:

  ```
  sudo chmod +x installer.sh
  sudo bash installer.sh
  ```
Then you choose menu item which you want to start.

If you have problems with starting installer.bat, you should try to use `dos2unix installer.sh` or `sed -i 's/\r//' installer.sh` commands.

# DPULSE demos

### You can start DPULSE and see the main menu on the screen using one of the recommended commands in DPULSE root folder. Don't forget to install all requirements before starting DPULSE

![dpulse_start](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/2ac7f332-5482-45e4-a0c9-0cc20e0e0ac7)

### After choosing first menu point, you will be able to enter target's URL and case comment, and then you will see scanning progress

![dpulse_running](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/27a64244-03f6-4360-b872-64661e68ffb5)

### Finally, DPULSE will create report folder which contains case name (basically URL of target), date and time of scan. All report folders are contained in DPULSE root folder

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7de73250-c9b6-4373-b21e-16bbb7a63882)


# Tasks to complete before new release
- [x] Create CSV report processing function
- [ ] Bugfixes
- [x] Find an opportunity to get rid of the manual installation of wkhtmltopdf
- [ ] IntelliSearch function to search useful strings in documents, SMs and so on
      
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





