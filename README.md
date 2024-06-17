# DPULSE - Domain Public Data Collection Service 

<p align="center">
  <img src="https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/fed8d368-7309-4aaa-a82e-2f0b277122de">
</p>

<p align="center">
<b><i>CONVENIENT, FAST AND USER-FRIENDLY COLLECTOR OF DOMAIN INFORMATION FROM OPEN SOURCES</i></b>
</p>

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/v1.0.2-ACTUAL%20VERSION?style=for-the-badge&label=ACTUAL%20VERSION&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/DOMAIN_OSINT-CATEGORY?style=for-the-badge&label=TOOL%20CATEGORY&color=red"> <img alt="Static Badge" src="https://img.shields.io/badge/CLI-CATEGORY?style=for-the-badge&label=interface%20type&color=red">
</p>
<p align="center">
<img alt="GitHub License" src="https://img.shields.io/github/license/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&label=total%20commits&color=red"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red">
</p>

> **Attention every DPULSE user! You DON'T NEED TO INSTALL WKHTMLTOPDF ANYWHERE if you cloned repository with last updates from June 18, 2024! When v1.0.3 will be released, we strongly recommend you to update!**

> DPULSE was created as a research tool, and it is not intended for criminal activities. Use DPULSE only on allowed domains and for legal purposes!

> You can visit [DPULSE wiki](https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki) in order to get more technical information about this project

> You can visit [DPULSE roadmap](https://github.com/users/OSINT-TECHNOLOGIES/projects/1) to get more information about development process

> You can also contact the developer via e-mail: osint.technologies@gmail.com


## About DPULSE

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. Using this software you can extract useful information such as:
1. WHOIS information 
2. Subdomains
3. Mentions of the domain's owner organization in some social networks, as well as organization profiles in social networks.
4. IP addresses
5. Public documents
6. Domain-related Google queries
7. InternetDB search results (possible vulnerabilities, open ports and so on)
8. Used web-technologies
9. Sitemap, robots.txt files, SSL certificate info
    
All these results are compiled into an easy-to-read PDF or XLSX report by category.


## How to install DPULSE


> **Attention every DPULSE user! You DON'T NEED TO INSTALL WKHTMLTOPDF ANYWHERE if you cloned repository with last updates from June 18, 2024! When v1.0.3 will be released, we strongly recommend you to update!**


### First way

Simply download zip archive from assets in releases bookmark, just right here:

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/bd2ebf09-a31c-4e27-a674-5b602808a667)

Then you just unpack the archive, open terminal in DPULSE root folder and use `pip install -r requirements.txt` to install requirements. 

### Second way

Cloning GitHub repository and requirements, you can do it using 3 simple commands:
   
  ```
  git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
  cd dpulse
  pip install -r requirements.txt
  ```

### Third way

Install using pip manager using this command: `pip install dpulse`

## DPULSE demos

### You can start DPULSE and see the main menu on the screen using `python dpulse.py` command in DPULSE root folder. 

![dpulse_start](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/2ac7f332-5482-45e4-a0c9-0cc20e0e0ac7)

### After choosing first menu point, you will be able to enter target's URL and case comment, and then you will see scanning progress

![dpulse_running](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/27a64244-03f6-4360-b872-64661e68ffb5)

### Finally, DPULSE will create report folder which contains case name (basically URL of target), date and time of scan. All report folders are contained in DPULSE root folder

![изображение](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7de73250-c9b6-4373-b21e-16bbb7a63882)


## Tasks to complete before new release
- [x] Create CSV report processing function
- [ ] Bugfixes
- [x] Find an opportunity to get rid of the manual installation of wkhtmltopdf
- [ ] IntelliSearch function to search useful strings in documents, SMs and so on
      
## DPULSE mentions in social medias

### [DPULSE first mention on X.com](https://x.com/DarkWebInformer/status/1787583156775759915?t=Ak1W9ddUPpDvLAkVyQG8fQ&s=19)

