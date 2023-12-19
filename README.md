<p align="center">
  <img src="https://github.com/OSINT-TECHNOLOGIES/dpulse/assets/77023667/f7d560fa-ce29-4795-b9f8-527916e3bbbe">
</p>

# DPULSE - Domain Public Data Collection Service 

DPULSE - Domain Public Data Collection Service 

Current version: 0.1b (Codename: Heartbeat)

[!] This program solution is not final and some details are potentially to be changed [!]

**If you want to contact the developer about DPULSE - write here:** osint.technologies@gmail.com

## What is DPULSE and how can I use it?

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. Using this software you can extract useful information such as:
1) WHOIS information about domain
2) List of subdomains
3) Mentions of the domain's owner organization in some social networks, as well as organization profiles in social networks.
4) IP addresses
5) Public documents
6) Domain-related Google queries

All these results are compiled into an easy-to-read PDF report by category. Specified Google Dorking automatization is also on board!

## How to start DPULSE and get some results 

Before you start working with DPULSE, you need to install all dependencies and required packages according to the instructions below. After preliminary setup, everything will be ready for getting started.

You can start DPULSE using your terminal where you write only one command: python dpulse.py -sd "url" -ra "n"

- url is a short form of domain link, ex: stackoverflow.com, google.com, facebook.com and so on

- n is a digit which specifies amount of Google Dorking results which will be printed in PDF report.

## Project's requirements 

**Additional programs:**

wkhtmltopdf is required for DPULSE in order to create PDF report just right in Python. You can download it here (https://wkhtmltopdf.org/downloads.html) and you need to install it in DPULSE root directory

**Python libraries:**

Jinja2==3.1.2 

MarkupSafe==2.1.3

beautifulsoup4==4.12.2

bs4==0.0.1

certifi==2023.11.17

charset-normalizer==3.3.2

fake-useragent==1.2.1

idna==3.6

pdfkit==1.0.0

requests==2.31.0

soupsieve==2.5

urllib3==2.1.0

useragent==0.1.1

whois==0.9.27

In general you can install these requirements (except of wkhtmltopdf, which need to be downloaded and installed manually) using pip and requirements.txt file which you can find in this repository.
