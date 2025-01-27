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

In order to ensure the functioning of API services individually for each DPULSE user, API keys storage database was created. Similar to report storage database, it is lightweight .db extension database with simple structure shown below: 

![apistordb](https://github.com/user-attachments/assets/02233813-781e-4bf8-be7c-76ec7627be06)

Since every API key is individual for each user, you can see fillers instead of actual keys when you start DPULSE for the first time, so until you replace filler with a real API key, you can't start using API in scans. You can enter your actual API keys using DPULSE CLI. You can see full process on the screenshot below:

![apiproc](https://github.com/user-attachments/assets/effb27ab-dd4b-4470-b90c-34c6f9a43d8c)

For the first time you will see red-colored API key field, which means that scan is not available with this API. After changing filler for actual key, you will see that color changed, which indicates that you can use your API key for scanning. Be advised that every free API service provided with some limitations (you can see them in DPULSE CLI for all supported API), so keep in mind that frequent usage of free API plans is not possible. 

In case if you want to fully replace API keys, you can use reference API keys database. You can see menu point for this action on the screenshot above. This action will delete your actual API keys database, copy reference database and rename it. This action is very optional because you can change your API keys by just using first menu point in API Keys DB Manager (according to the screenshot above)

