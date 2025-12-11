# DPULSE - Domain Public Data Collection Service 

<p align="center">
  <img src="https://github.com/user-attachments/assets/949c332b-790e-49da-81a3-a7cf21e9ddf2">
</p>

<p align="center">
<b><i>CONVENIENT, FAST AND USER-FRIENDLY COLLECTOR OF DOMAIN INFORMATION FROM OPEN SOURCES</i></b>
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/v1.3.4-CURRENT%20STABLE%20VERSION?style=for-the-badge&label=CURRENT%20STABLE%20VERSION&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/v1.4-red?style=for-the-badge&logo=f&label=CURRENT%20ROLLING%20VERSION">
<img alt="Static Badge" src="https://img.shields.io/badge/DOMAIN_OSINT-CATEGORY?style=for-the-badge&label=TOOL%20CATEGORY&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/CLI-CATEGORY?style=for-the-badge&label=interface%20type&color=red">
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/supports-virustotal_api (key required)-red?style=for-the-badge"> <img alt="Static Badge" src="https://img.shields.io/badge/supports-securitytrails_api (key required)-red?style=for-the-badge"> <img alt="Static Badge" src="https://img.shields.io/badge/supports-hudsonrock_api (no key required)-red?style=for-the-badge"> 
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
     
2. ***PageSearch scan:*** extended subdomains deep search function, which starts in addition to basic scan and which can find:
   - more e-mail addresses
   - API keys
   - exposed passwords
   - cookies
   - hidden forms of data and other web page elements
   - documents, config files, databases files (and PageSearch can download them!)
   - specified words by user in PDF files

3. ***Dorking scan:*** extended domain research function with prepared Google Dorking databases for different purposes, such as:
   - IoT dorking
   - files dorking
   - admin panels dorking
   - web elements dorking
   - Moreover, this mode allows you to create your own custom Google Dorking database

4. ***API scan:*** extended domain research function with prepared functions for 3rd party APIs usage. Currently DPULSE supports these API:
    - VirusTotal API (for brief domain information gathering)
    - SecurityTrails API (deep subdomains and DNS enumeration)
    - HudsonRock API (for querying a database with exposed computers which were compromised through global info-stealer campaigns)

5. ***Web-pages snapshoting:*** extended functionality which allows to save web-pages copies in different forms:
    - Screenshot snapshotting (saves target domain's page in form of screenshot)
    - HTML snapshotting (saves target domain'spage in form of HTML file)
    - Wayback Machine snapshotting (saves every version of target domain's page within a user-defined time period)

Finally, DPULSE compiles all found data into an easy-to-read HTML or XLSX report by category. It also saves all information about scan in local report storage database, which can be restored later.

# How to install and run DPULSE

## _Recommended ways_

DPULSE repository is using Poetry to manage dependencies and the tool itself integrated with Docker. So it's very easy to install and use DPULSE on every system without dependencies and software conflicts. 

### <ins>First way (using Docker)</ins>

WIP

### <ins>Second way (using Poetry)</ins>

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

### <ins>Third way (old and classic, using pip)</ins>

Nowadays pip usage is a slightly outdated way of distributing dependencies and software itself. This way might be connected with dependencies and versioning conflicts, but you can try it.

Use this set of commands to install DPULSE stable versions:

  ```
  git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
  cd dpulse
  pip install -r requirements.txt
  ```

Use this set of commands to install DPULSE rolling versions:

  ```
  git clone --branch rolling --single-branch https://github.com/OSINT-TECHNOLOGIES/dpulse.git
  cd dpulse
  pip install -r requirements.txt
  ```

After installation, you simply start DPULSE using `python dpulse.py`. Be adviced that as was said before, it's not guaranteed to work for your first try, but this method might work for you.

# DPULSE demo and use-cases

### You can start DPULSE and see the main menu on the screen using one of the recommended commands in DPULSE root folder. Don't forget to install all requirements before starting DPULSE

![dpulse_start](https://github.com/user-attachments/assets/9ec0ab73-2206-4d38-bae6-e88656e17f95)

### After choosing first menu point, you will be able to enter target's URL and case comment, and then you will see scanning progress

![dpulse_bs](https://github.com/user-attachments/assets/b0ad7827-6dac-4f82-a369-4447a0e1c878)

### Finally, DPULSE will create report folder which contains case name (basically URL of target), date and time of scan. All report folders are contained in DPULSE root folder

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7de73250-c9b6-4373-b21e-16bbb7a63882)


# Tasks to complete before new release
- [x] CLI rework (more fancy and user-friendly)
- [ ] Report storage database rework (more information to store)
- [ ] HTML report rework (modern style and look; functionality expansion)

# DPULSE mentions in social medias

## Honorable mentions:

### [The very first mention on cybersecurity related website (DarkWebInformer)](https://darkwebinformer.com/dpulse-tool-for-complex-approach-to-domain-osint/)

### [The very first mention from cybercrime intelligence company (HudsonRock)](https://www.linkedin.com/feed/update/urn:li:share:7294336938495385600/)

### [The very first mention on cybersecurity educational website (Ethical Hackers Academy)](https://ethicalhacksacademy.com/blogs/cyber-security-tools/dpulse)

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





