from extractor import SQLiteExtractor

def run_extraction():
    extractor = SQLiteExtractor()
    extractor.run_extraction()
    print("Extraction completed! Check 'data/output/' folder and logs.txt")

if __name__ == "__main__":
    run_extraction()
