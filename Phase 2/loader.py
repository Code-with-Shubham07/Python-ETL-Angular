from neo4j import GraphDatabase
import pandas as pd, os, logging, sys
from datamodel import graph_model
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)                
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from common_utils import load_config, setup_logger
    
class Neo4jLoader:
    def __init__(self):
        setup_logger("Phase 2/logs.txt")
        load_dotenv()
        cfg = load_config("Phase 2/config.yaml")
        
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")

        if not uri or not user or not password:
            raise ValueError("Neo4j credentials missing. Please check your .env file.")
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.cfg = cfg
        self.path = cfg.get("output_path", ".")

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as s:
            for label, cols in graph_model["nodes"].items():
                id_field = cols[0]

                cypher = f"""
                CREATE CONSTRAINT IF NOT EXISTS
                FOR (n:{label})
                REQUIRE n.{id_field} IS UNIQUE
                """
                s.run(cypher)
                logging.info(f"Created constraint for :{label}({id_field})")

    def load_nodes(self, batch_size=1000):
        with self.driver.session() as s:
            for label, cols in graph_model["nodes"].items():

                fname = os.path.join(self.path, f"{label.lower()}_cleaned.csv")
                if not os.path.exists(fname):
                    logging.warning(f"File not found: {fname}")
                    continue

                df = pd.read_csv(fname)
                records = df.where(pd.notnull(df), None).to_dict("records")

                total = len(records)
                if total == 0:
                    logging.info(f"No records for {label}")
                    continue
                id_field = cols[0]

                cypher = f"""
                UNWIND $rows AS row
                MERGE (n:{label} {{ {id_field}: row.{id_field} }})
                SET n += row
                """

                for i in range(0, total, batch_size):
                    batch = records[i:i+batch_size]
                    s.run(cypher, rows=batch)
                    logging.info(f"{label}: inserted batch {i} - {i+len(batch)-1}")

                logging.info(f"{label}: inserted {total} nodes")


    def load_relationships(self):
        with self.driver.session() as s:
            for rel_name, (src_label, dst_label, condition) in graph_model["relationships"].items():
                src_field, dst_field = condition.split('=')
                cypher = f"""
                MATCH (a:{src_label}), (b:{dst_label})
                WHERE a.{src_field} = b.{dst_field}
                MERGE (a)-[:{rel_name.split('-')[1]}]->(b)
                """
                s.run(cypher)
                logging.info(f"Created relationship {rel_name}")

if __name__ == "__main__":
    loader = Neo4jLoader()
    loader.create_constraints()
    loader.load_nodes(batch_size=1000)
    loader.load_relationships()
    loader.close()
    print("Data loaded into Neo4j successfully")
