import pandas as pd, os, logging, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)             
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from common_utils import load_config, setup_logger 
    
def clean_and_filter():
    setup_logger("Phase 2/logs.txt")
    cfg = load_config("Phase 2/config.yaml")
    os.makedirs(cfg['output_path'], exist_ok=True)

    for name, path in cfg['data_paths'].items():
        df = pd.read_csv(path)
        logging.info(f"Loaded {name} ({len(df)} rows)")

        if name in cfg['select_columns']:
            cols = [c for c in cfg['select_columns'][name] if c in df.columns]
            df = df[cols]
            logging.info(f"Filtered {name} -> {cols}")

        df.replace(['NULL', 'null', 'NaN', ''], pd.NA, inplace=True)
        df.dropna(how='all', inplace=True)

        out = os.path.join(cfg['output_path'], f"{name}_cleaned.csv")
        df.to_csv(out, index=False)
        logging.info(f"Saved {out} ({len(df)} rows)")

if __name__ == "__main__":
    clean_and_filter()   
