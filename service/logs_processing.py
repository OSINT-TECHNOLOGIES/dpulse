import logging
from config_processing import read_config
from colorama import Fore, Style

config_values = read_config()
logging_level = (config_values['logging_level']).upper()

if logging_level == 'DEBUG':
    level = logging.DEBUG
elif logging_level == 'INFO':
    level = logging.INFO
elif logging_level == 'WARNING':
    level = logging.WARNING
elif logging_level == 'ERROR':
    level = logging.ERROR
elif logging_level == 'CRITICAL':
    level = logging.CRITICAL
else:
    print(Fore.RED + "You've entered wrong logging level in config file. Please verify proper mods and re-enter it" + Style.RESET_ALL)
    print(Fore.RED + "Setting config level as DEBUG for this session" + Style.RESET_ALL)
    level = logging.DEBUG

logging.basicConfig(filename="journal.log", level=level, format="%(asctime)s - %(levelname)s - %(message)s")
