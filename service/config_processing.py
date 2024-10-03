import configparser
import os

def create_config():
    config = configparser.ConfigParser()
    config['LOGGING'] = {'log_level': 'info'}
    config['CLI VISUAL'] = {'preview_color': 'red', 'font': 'slant'}
    config['DORKING'] = {'dorking_delay (secs)': '2', 'delay_step': '5'}

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

    config_values = {
        'logging_level': log_level,
        'preview_color': cli_preview_color,
        'wm_font': wm_font,
        'dorking_delay (secs)': dorking_delay,
        'delay_step': delay_step
    }

    return config_values
