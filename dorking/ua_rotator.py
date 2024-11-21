import random
import sys
sys.path.append('service')
from config_processing import read_config

class UserAgentRotator:
    def __init__(self):
        config_values = read_config()
        self.user_agents = config_values['user_agents']

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

user_agent_rotator = UserAgentRotator()
