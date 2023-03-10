import yaml
from pathlib import Path

def load_config():
    CONFIG_PATH = Path(__file__).parent.parent.joinpath("config.yml")

    # read config file
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)

    return config