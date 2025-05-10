# Configuration file

As you can understand, configuration file is a file that contains certain parameters which are necessary for certain DPULSE modules. Let's see what parameters are contained in this file and how to interact with it using DPULSE CLI.

## Config file content

Configuration file (config.ini) located in 'serivce' folder, which is located inside DPULSE root folder. Default config.ini file generated with your first DPULSE start and it looks like that:
```
[LOGGING]
log_level = info

[CLI VISUAL]
preview_color = red
font = slant

[DORKING]
dorking_delay (secs) = 2
delay_step = 5

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

[LOGGING] is section for log file configuration, and it's only parameter - log_level - describes log level for Python's logging library. More information about logging levels you [can find here](https://docs.python.org/3/library/logging.html#logging-levels)

[CLI VISUAL] is section for command line interface configuration. It's parameters are preview_color (determines color for big DPULSE logo on start) and font (determines font for big DPULSE logo on start). More about these parameters you [can find here](http://www.figlet.org/)

[DORKING] is section for dorking process configuration. It's parameters are dorking_delay (secs) (determines delay between dorking steps) and delay_step (determines how many requests will be in one step)

[SNAPSHOTTING] is section for snapshotting process configuration. It's parameters are installed_browser (determines your installed browser to be used in screenshot snapshotting), opera_browser_path (path to opera.exe, only in case if you want to use this browser for screenshot snapshotting), wayback_retries (determines amount of retries for getting exact Wayback snapshot in case of errors) and wayback_req_pause (determines pause in seconds between requests to Wayback archive)

[USER-AGENTS] is section for user-agents list, which is used in Google Dorking (user-agents are randomly swapped in process)

[PROXIES] is section for configuring proxies usage in Dorking, and it's only parameter - proxies_file_path - used to determine path to .txt file (path should be full with //-style slashes) which contains list of proxies (one proxy per row)

## Editing configuration file

First step in editing configuration file will be main menu of DPULSE. Here you should find 2nd menu point and select it like that:

![config1](https://github.com/user-attachments/assets/d4eda335-102c-4dc6-ab5d-206ac01202d8)

Then Setting menu will pop-out. Here you will find two menu points related to config. First is "Print current config file" and second is "Edit config file". You can see them in the image below:

![config2](https://github.com/user-attachments/assets/035e5a94-ca5f-43ca-89c7-8fca36048243)

If you select "Print current config file", you will see config file content in DPULSE CLI, just like that:

![config3](https://github.com/user-attachments/assets/a86ee852-0b2c-4c83-9a48-bca7499c4671)

If you select "Edit config file" you will see current config file's content and you will be prompted to enter section and parameter to update, and, then, some new value for that:

![config4](https://github.com/user-attachments/assets/b522f2d8-e05e-43a5-968e-b0306ad1de2e)


