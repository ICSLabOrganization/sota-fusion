import yaml
from pathlib import Path

def load_config(mode : str = None):
    CONFIG_PATH = Path(__file__).parent.parent.joinpath("config.yml")

    # read config file
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
        if mode is None or config[mode] is None :
            raise KeyError("A mode is not assigned in load config function, please re-check the called function and touch some grass")


    return config[mode]