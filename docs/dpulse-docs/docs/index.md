# Welcome to DPULSE documentation

Convenient, fast and user-friendly collector of domain information from open-sources
 
## What is DPULSE

DPULSE is a software solution for conducting OSINT research in relation to a certain domain. In general, it provides you with a certain set of functions, such as:

1. ***Basic scan:*** extracts general information about domain such as WHOIS information, subdomains, e-mail addresses, IP addresses, social medias links/posts/profiles, SSL certificate info, possible vulnerabilities, open ports, CPEs, used web-technologies and so on. It also can download sitemap.xml and robots.txt files from a domain
     
2. ***PageSearch scan:*** extended subdomains deep search function, which starts in addition to basic scan and which can find more e-mail addresses, API keys, exposed passwords, cookies, hidden forms of data and other web page elements, documents, config files, databases files (and PageSearch can download them!), specified words by user in PDF files

3. ***Dorking scan:*** extended domain research function with prepared Google Dorking databases for different purposes, such as IoT dorking, files dorking, admin panels dorking, web elements dorking. Moreover, this mode allows you to create your own custom Google Dorking database

4. ***API scan:*** extended domain research function with prepared functions for 3rd party APIs usage. Currently DPULSE supports VirusTotal API (for brief domain information gathering) and SecurityTrails API (deep subdomains and DNS enumeration)

5. ***Snapshotting:*** extended domain research function which copys domain's home page content in various ways: by screenshotting it (screenshot snapshot), by HTML copying (HTML snapshot) and by finding and downloading previous versions (Wayback Machine snapshot)

Finally, DPULSE compiles all found data into an easy-to-read HTML or XLSX report by category. It also saves all information about scan in local report storage database, which can be restored later.
