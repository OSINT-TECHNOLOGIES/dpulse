# DPULSE - Domain Public Data Collection Service 

<p align="center">
  <img src="https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/fed8d368-7309-4aaa-a82e-2f0b277122de">
</p>

<p align="center">
<b><i>CONVENIENT, FAST AND USER-FRIENDLY COLLECTOR OF DOMAIN INFORMATION FROM OPEN SOURCES</i></b>
</p>

<p align="center">
<img alt="GitHub License" src="https://img.shields.io/github/license/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red"> <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&label=total%20commits&color=red"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/OSINT-TECHNOLOGIES/dpulse?style=for-the-badge&color=red">
</p>







**We are happy to announce that DPULSE is getting closer to its v1.0 release!**

**We will publish a few more release candidates, where all existing bugs will be fixed and we will focus on improving the existing components of the program during release candidates phase!**

> [!CAUTION]
> DPULSE was created as a research tool, and it is not intended for criminal activities. Use DPULSE only on allowed domains and for legal purposes!

> [!TIP]
> You can visit [DPULSE wiki](https://github.com/OSINT-TECHNOLOGIES/dpulse/wiki) in order to get more technical information about this project
> 
> You can also contact the developer via e-mail: osint.technologies@gmail.com

> [!NOTE]  
> This program solution is not final and some details are potentially to be changed!
> 
> Current version: 0.9rc3 (Codename: Heartbeat)

## What is DPULSE and how can I use it?

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. Using this software you can extract useful information such as:
1) WHOIS information about domain
2) List of subdomains
3) Mentions of the domain's owner organization in some social networks, as well as organization profiles in social networks.
4) IP addresses
5) Public documents
6) Domain-related Google queries

All these results are compiled into an easy-to-read PDF report by category. Specified Google Dorking automatization is also on board!

## Program examples
**Programm menu**

![example](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/7adc438e-9f67-4919-b307-c9923e556498)

**Scanning and PDF creation report process**

![example1](https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/da3d3710-e4a5-420d-bcdc-bb43a70c92c5)


## How to start DPULSE and get some results 

Before you start working with DPULSE, you need to install all dependencies and required packages according to the instructions below. There are two ways how to install them:
> Using **pip install -r requirements.txt** command in CLI.

> Using **python setup.py install** command in CLI

Moreover, you need to manually install WKHTMLTOPDF package in DPULSE directory. This package is necessary for creating PDF reports and programm won't start unless WKHTMLTOPDF is not installed. You can find WKHTMLTOPDF download link in the project requirements paragraph down below

After preliminary setup, everything will be ready for getting started.

Then you can start DPULSE using your terminal where you write only one command:
> python dpulse.py

This will open DPULSE menu when you can select 1st point and follow the steps required by the program. After the program finishes, a PDF report with the domain name that you entered before starting will be created in the program's root folder.

## Project's requirements 

**Additional programs:**

wkhtmltopdf is required for DPULSE in order to create PDF report just right in Python. You can download it here (https://wkhtmltopdf.org/downloads.html) and you need to install it in DPULSE root directory

**Python libraries:**

| Library  | Version | 
| ---------- | ------------- | 
| Jinja2  | ==3.1.2 | 
| MarkupSafe | ==2.1.3 |
| beautifulsoup4 | ==4.12.2 |
| bs4 | ==0.0.1 |
| certifi | ==2023.11.17 |
| charset-normalizer | ==3.3.2 |
| idna | ==3.6 |
| pdfkit | ==1.0.0 |
| requests | ==2.31.0 |
| soupsieve | ==2.5 |
| urllib3 | ==2.1.0 |
| python-whois | ==0.9.4 |
| dnspython | ==2.4.2 |
| builtwith | ==1.3.4 |
| MechanicalSoup | ==1.3.0 |
| lxml | ==5.2.1 |
| colorama | ==0.4.6 |
