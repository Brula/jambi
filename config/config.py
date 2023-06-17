from dataclasses import dataclass

import yaml

@dataclass
class Config:
    env: str
    database_connection_string: str

current_config: Config

def load_config(env: str):
    with open(f"config/yaml/config_{env}.yaml") as stream:
        config_yaml = yaml.safe_load(stream)
        global current_config
        current_config = Config(env=config_yaml['env'], database_connection_string=config_yaml['database_connection_string'])
