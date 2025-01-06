# About reporting system

DPULSE as every OSINT tool is highly dependent on reporting system. User-friendly reports are crucial for detailed results presentation and further storage. DPULSE supports the most common types of reports: HTML and XLSX. Moreover, DPULSE provides you with reports storage database, which contains some information about scan, report and extracted data and gives you opportunity for long-term reports storage in one place. Also you can move this database between different DPULSE versions, which brings a little bit better user-experience.

## HTML report

HTML report was the first supported type of report. HTML is a widely supported format that can be opened in any web browser, allowing for the creation of visually appealing reports using tables, charts, diagrams, and other elements. It supports links and hyperlinks that can be used to create navigation within the report and link to external resources, and enables creating dynamic content that can be updated in real-time. HTML is often used in web applications, making it easy to integrate reports with existing web systems. And, in general, this report format is more user-friendly, which makes it more convenient for sharing with investigation customers, OSINT teams and usage in presentations. Moreover, unlike PDF report generation, HTML is easier to handle when both developing and delievering, as it doesn't require to install 3rd party applications (like wkhtmltopdf). You can see example of DPULSE generated HTML report [here](https://github.com/OSINT-TECHNOLOGIES/dpulse/tree/rolling/report_examples/html_report_example).

## XLSX report

XLSX is a widely supported format that can be opened in most spreadsheet and office applications, including Microsoft Excel, Google Sheets, and LibreOffice Calc, making it easy to analyze and process data. It allows storing data in a structured format, supports formulas and functions that can be used to automate calculations and data analysis, and enables creating charts and diagrams to visualize data. Additionally, XLSX is often used in business applications, making it easy to integrate reports with existing systems. You can see example of DPULSE generated XLSX report [here](https://github.com/OSINT-TECHNOLOGIES/dpulse/tree/rolling/report_examples/xlsx_report_example).

## Side files

As you may have noticed in report examples on GitHub page, there are also some side files except for report file. These files may be the following:

* target's robots.txt file (if accessible) 
* target's sitemap.xml file (if accessible)
* ps_documents folder with extracted documents from domain and its subdomains (if PageSearch was selected for scan)

## Report storage database

As said above, report storage database contains key information about scan, report and extracted data. DPULSE generates this database when DPULSE is first launched or if database file was not found in the root directory, so users don't need to worry about it's manual creation. Report storage database is a simple .db file (with hard-coded report_storage.db name) with structure which shown below:

![rsdbstr](https://github.com/user-attachments/assets/491d1147-78ca-47a8-a405-5e351dc2730e)

Lets describe these fields in more detailed way:

* id - integer value that displays the number of reports generated and the order in which they are generated
* report_file_extension - string which shows main report file extension, in current DPULSE version this value could be xlsx, pdf or html
* report_content - BLOB or HTML data which contains main report file's copy
* comment - string which shows comment to your cases, which you can enter before each scan
* target - string which shows domain which you've scanned
* creation_date - string which shows when your report was generated (YYYYMMDD format)
* dorks_results - text array which contains a copy of Google Dorking results (if this mode was selected before scan)
* robots_text - text array which contains a copy of robots.txt file from scanned domain
* sitemap_text - text array which contains all sitemap.xml links file from scanned domain
* sitemap_file - text array which contains a copy of sitemap.xml file from scanned domain
* api_scan - string which indicates whether API scanning was activated or not, and if it was activated - contains used APIs

Interacting with report storage database is a very simple process. First of all, after each scan you can see several messages which indicate that your report was successfully saved in report storage database:

![rsdb1](https://github.com/user-attachments/assets/db3b22f8-1e74-4095-8ab7-99fd5837aa0a)

Also, you have separate menu item in DPULSE CLI to work with report storage database which named "Report storage DB manager":

![rsdb2](https://github.com/user-attachments/assets/519682dc-5d01-4844-8dcd-67e1914bb765)

As you can see, there are menu points for both seeing DB content and recreating reports. Lets see what DPULSE will return if we select first menu item:

![rsdb3](https://github.com/user-attachments/assets/6778cf83-e9cf-4580-b46d-7c187cbdde9d)

Report recreating process is shown below:

![rsdb4](https://github.com/user-attachments/assets/d7af9b03-703e-46b2-846b-05d99b33b900)

And that's how recreated report looks like inside:

![rsdb5](https://github.com/user-attachments/assets/799d45cb-bc51-43ca-8b06-14e236d21912)
