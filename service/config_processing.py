import configparser
import os

def create_config():
    config = configparser.ConfigParser()
    config['LOGGING'] = {'log_level': 'info'}
    config['CLI VISUAL'] = {'preview_color': 'red'}

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

    config_values = {
        'logging_level': log_level,
        'preview_color': cli_preview_color
    }

    return config_values
