import yaml

def parse(yaml_data: str) -> dict:
    return yaml.load(yaml_data, Loader=yaml.FullLoader)
