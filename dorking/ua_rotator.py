import random
import sys
sys.path.append('service')
from config_processing import read_config
from colorama import Fore, Style

class UserAgentRotator:
    def __init__(self):
        config_values = read_config()
        self.user_agents = config_values['user_agents']

    def get_random_user_agent(self):
        print(Fore.GREEN + "Changed User-Agent to " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"{random.choice(self.user_agents)}" + Style.RESET_ALL)
        return random.choice(self.user_agents)

user_agent_rotator = UserAgentRotator()
