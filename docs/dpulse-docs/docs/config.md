# Configuration file

As you can understand, configuration file is a file that contains certain parameters which are necessary for certain DPULSE modules. Let's see what parameters are contained in this file and how to interact with it using DPULSE CLI.

## Config file content

Configuration file (config.ini) located in 'serivce' folder, which is located inside DPULSE root folder. Default config.ini file generated with your first DPULSE start and it looks like that:
```
[HTML_REPORTING]
template = modern
delete_txt_files = n

[LOGGING]
log_level = info

[CLI VISUAL]
preview_color = red
font = slant

[DORKING]
dorking_delay (secs) = 2
delay_step = 5
full_path_to_browser = path\to\browser\for\dorking
browser_mode = nonheadless

[SNAPSHOTTING]
installed_browser = firefox
opera_browser_path = None
wayback_retries = 3
wayback_req_pause = 2

[USER-AGENTS]
agent_1 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
agent_2 = Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
agent_3 = Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
agent_4 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36
agent_5 = Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
agent_6 = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
agent_7 = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
agent_8 = Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36
agent_9 = Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36
agent_10 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36
agent_11 = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36
agent_12 = Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
agent_13 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
agent_14 = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
agent_15 = Mozilla/5.0 (Linux; Android 8.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36
agent_16 = Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36
agent_17 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
agent_18 = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
agent_19 = Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
agent_20 = Mozilla/5.0 (Linux; Android 7.1.2; SM-G955F Build/N2G48H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36

[PROXIES]
proxies_file_path = NONE
```

As you can see, config file built with sections, which represent separated DPULSE functions. Lets describe these sections and parameters:

| SECTION    | PARAMETER    | POSSIBLE VALUES     | COMMENT    |
| ------------- | ------------- | ------------- | ------------- |
| [HTML_REPORTING] | template | modern / legacy | Determines which HTML report template should be used while creating report itself. Modern contains more features like analytics, graphs and interactive features, while legacy is not supported anymore but may be convenient choice for someone |
| [HTML_REPORTING] | delete_txt_files | y / n | Modern HTML report template contains text boxes for the content of robots.txt and sitemap.xml files, so maybe you won't need them as .txt files. Y parameter makes DPULSE delete this files from report folder, and N parameter leave everything as is |
| [LOGGING] | log_level | See [here](https://docs.python.org/3/library/logging.html#logging-levels) | Determines how much technical info about program's execution will be logged in journal.log file |
| [CLI_VISUAL] | preview_color | See [here](https://pypi.org/project/colorama/) | Determines the color of DPULSE ASCII art's color |
| [CLI_VISUAL] | font | - | - |
| [DORKING] | dorking_delay (secs) | Any integer value >=0 | Determines how much time browser will be on pause between dorks |
| [DORKING] | delay_step | Any integer value >0 | Determines the amount of dorks browser should handle before activating delay |
| [DORKING] | full_path_to_browser | Full path to your browser's executable file with \ symbol as a separator | Determines which browser will be used for Dorking |
| [DORKING] | browser_mode | headless / nonheadless | Sets which browser mode will be used during Dorking process (headless means that browser window won't be opened, so nonheadless means that browser window will be opened every new dork, and actually it gives better results with TOS and Captcha bypassing) |
| [SNAPSHOTTING] | installed_browser | Cell 1, Row 2 | Cell 1, Row 2 |
| [SNAPSHOTTING] | opera_browser_path | Full path to your Opera.exe / None | Enter your Opera.exe path only if you decided to use Opera for screenshot snapshotting, in other cases - leave it as None |
| [SNAPSHOTTING] | wayback_retries | Any integer value >0 | Determines how many retries DPULSE will make before abandoning inaccessible Wayback link |
| [SNAPSHOTTING] | wayback_req_pause | Any integer value >0 | Determines how many seconds DPULSE will wait between different retries to an inaccessible Wayback link |
| [USER-AGENTS] | agent_N | Any default user-agent string | User-agent are used to try bypassing TOS and Captcha when Dorking domain |
| [PROXIES] | proxies_file_path | Full path to your proxies .txt file | Determines path to .txt file with "//" symbols as a separator which contains list of proxies (one proxy per row) |

## Editing configuration file

First step in editing configuration file will be main menu of DPULSE. Here you should find 2nd menu point and select it like that:

![config1](https://github.com/user-attachments/assets/d4eda335-102c-4dc6-ab5d-206ac01202d8)

Then Setting menu will pop-out. Here you will find two menu points related to config. First is "Print current config file" and second is "Edit config file". You can see them in the image below:

![config2](https://github.com/user-attachments/assets/035e5a94-ca5f-43ca-89c7-8fca36048243)

If you select "Print current config file", you will see config file content in DPULSE CLI, just like that:

![config3](https://github.com/user-attachments/assets/a86ee852-0b2c-4c83-9a48-bca7499c4671)

If you select "Edit config file" you will see current config file's content and you will be prompted to enter section and parameter to update, and, then, some new value for that:

![config4](https://github.com/user-attachments/assets/b522f2d8-e05e-43a5-968e-b0306ad1de2e)


