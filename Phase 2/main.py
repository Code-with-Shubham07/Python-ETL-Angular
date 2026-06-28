from transformer import clean_and_filter
from loader import Neo4jLoader

if __name__ == "__main__":
    print("=== Starting Phase 2 ===")

    print("-> Filtering and Cleaning data...")
    clean_and_filter()
    print("Filtered data saved.")

    print("-> Loading data into Neo4j...")
    loader = Neo4jLoader()
    loader.load_nodes()
    loader.load_relationships()
    loader.close()
    print("Data loaded successfully into Neo4j")