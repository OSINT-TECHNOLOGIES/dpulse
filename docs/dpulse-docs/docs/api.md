# Third-party API scan mode

Currently DPULSE supports two third-party APIs: 

* SecurityTrails API (securitytrails.com) for deep subdomains and DNS enumeration
* VirusTotal API (virustotal.com) for brief domain information gathering

## SecurityTrails API 

SecurityTrails API is used to gather information about a specified domain. It retrieves various types of DNS records, subdomains, and other details. SecurityTrails API in DPULSE returns these details about target domain:

* Alexa rank
* Apex domain
* Hostname
* A/MX/NS/SOA/TXT records
* All subdomains list
* Alive (pingable) subdomains list

## VirusTotal API

VirusTotal API is used to interact with the VirusTotal service programmatically and analyze files and URLs using multiple antivirus engines and website scanners, providing insights into whether they are malicious. VirusTotal API in DPULSE returns these details about target domain:

* Categories
* Detected samples
* Undetected samples
* Detected URLs

## API Keys database

