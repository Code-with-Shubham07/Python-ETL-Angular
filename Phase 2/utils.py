import yaml
import logging
import os

def load_config(config_name="config.yaml"):
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, config_name)

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    

def setup_logger():
    logging.basicConfig(
        filename="logs.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    