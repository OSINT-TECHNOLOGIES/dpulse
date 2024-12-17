import configparser
import os
from colorama import Fore, Style

def create_config():
    basic_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 8.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.1.2; SM-G955F Build/N2G48H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
    ]

    config = configparser.ConfigParser()
    config['LOGGING'] = {'log_level': 'info'}
    config['CLI VISUAL'] = {'preview_color': 'red', 'font': 'slant'}
    config['DORKING'] = {'dorking_delay (secs)': '2', 'delay_step': '5'}
    config['USER-AGENTS'] = {}
    for i, agent in enumerate(basic_user_agents):
        config['USER-AGENTS'][f'agent_{i + 1}'] = agent
    config['PROXIES'] = {'proxies_file_path': 'NONE'}


    with open('service//config.ini', 'w') as configfile:
        config.write(configfile)

def check_cfg_presence():
    cfg_presence = os.path.isfile('service//config.ini')
    return cfg_presence

def read_config():
    config = configparser.ConfigParser()
    config.read('service//config.ini')
    log_level = config.get('LOGGING', 'log_level')
    cli_preview_color = config.get('CLI VISUAL', 'preview_color')
    wm_font = config.get('CLI VISUAL', 'font')
    dorking_delay = config.get('DORKING', 'dorking_delay (secs)')
    delay_step = config.get('DORKING', 'delay_step')
    user_agents = [value for key, value in config['USER-AGENTS'].items()]
    proxies_file_path = config.get('PROXIES', 'proxies_file_path')

    config_values = {
        'logging_level': log_level,
        'preview_color': cli_preview_color,
        'wm_font': wm_font,
        'dorking_delay (secs)': dorking_delay,
        'delay_step': delay_step,
        'user_agents': user_agents,
        'proxies_file_path': proxies_file_path
    }

    return config_values

def print_and_return_config():
    config = configparser.ConfigParser()
    config.read('service//config.ini')
    print(Fore.LIGHTMAGENTA_EX + "\n[CURRENT CONFIG CONTENT START]" + Style.RESET_ALL)
    for section in config.sections():
        print('\n')
        print(Fore.GREEN + f"[{section}]" + Style.RESET_ALL)
        for key in config[section]:
            print(Fore.GREEN + f"{key} = {config[section][key]}" + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + "\n\n[CURRENT CONFIG CONTENT END]" + Style.RESET_ALL)
    return config
