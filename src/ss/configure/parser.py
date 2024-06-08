import yaml

def parse(yaml_data) -> dict:
    return yaml.load(yaml_data, Loader=yaml.FullLoader)
