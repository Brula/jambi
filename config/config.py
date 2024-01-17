from dataclasses import dataclass

import yaml

@dataclass
class Config:
    env: str
    database_connection_string: str
    output_folder: str
    template_folder: str
    pages_table_name: str

def load_config(env: str) -> Config:
    with open(f"config/yaml/config_{env}.yaml") as stream:
        config_yaml = yaml.safe_load(stream)
        return Config(
            env=config_yaml['env'],
            database_connection_string=config_yaml['database_connection_string'],
            output_folder=config_yaml['output_folder'],
            template_folder=config_yaml['template_folder'],
            pages_table_name=config_yaml['pages_table_name']
        )
