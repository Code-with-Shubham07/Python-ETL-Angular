import sqlite3
import pandas as pd
import logging
import yaml
import os

class SQLiteExtractor:
    def __init__(self, config_path="config.yaml"):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_full_path = os.path.join(current_dir, config_path)
        self.config = self.load_config(config_full_path)

        project_root = os.path.dirname(current_dir)
        self.db_path = os.path.join(project_root, self.config["database_path"])
        self.output_path = os.path.join(project_root, self.config["output_path"])
        self.log_file = os.path.join(current_dir, self.config["log_file"])
        self.tables = self.config["tables_to_extract"]

        self.setup_logging()

    def load_config(self, path):
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def extract_table(self, table_name):
        logging.info(f"Starting extraction for table: {table_name}")
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            os.makedirs(self.output_path, exist_ok=True)
            output_file = os.path.join(self.output_path, f"{table_name}.csv")
            df.to_csv(output_file, index=False)
            conn.close()
            logging.info(f"Extracted and saved {table_name} successfully.")
        except Exception as e:
            logging.error(f"Error extracting {table_name}: {e}")

    def run_extraction(self):
        for table in self.tables:
            self.extract_table(table)
