import json
from pathlib import Path
from typing import List, Dict

# Path to the JSON file containing product data
DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:    
    # Check if data file exists before reading
    if not DATA_FILE.exists():
        return []
    
    # Open and load JSON data from the file
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

# Wrapper function to fetch all products from data source
def get_all_products() -> List[Dict]:
    return load_products()

