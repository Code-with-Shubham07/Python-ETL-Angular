import yaml
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def load_config(relative_path: str):
    config_path = PROJECT_ROOT / relative_path
    with config_path.open("r") as f:
        return yaml.safe_load(f)
    
def setup_logger(log_file: str = "logs.txt", level=logging.INFO):
    log_path = PROJECT_ROOT / log_file
    logging.basicConfig(
        filename=str(log_path),
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
