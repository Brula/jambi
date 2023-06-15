import yaml

def load_config(env: str):
    with open(f"config/yaml/config_{env}.yaml") as stream:
        print(yaml.safe_load(stream))
