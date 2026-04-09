import os
from main import IntelligenceEngine

def test_load():
    try:
        engine = IntelligenceEngine()
        engine.clean_data()
        print(f"Success: Loaded {len(engine.df)} rows")
        stats = engine.get_descriptive_stats()
        print("Descriptive Stats calculated successfully")
        print(stats)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_load()
