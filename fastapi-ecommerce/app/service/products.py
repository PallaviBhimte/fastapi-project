import json
from pathlib import Path
from typing import List, Dict

# Path to the JSON file containing product data
DATA_FILE = Path(__file__).parent.parent / "data" / "dummy.json"

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

# Save products to the JSON file
def save_product(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

# Add a new product to the data source        
def add_product(product: Dict) -> Dict:
    products = get_all_products()
    
    # Check for duplicate SKU before adding the product
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError(f"SKU {product['sku']} already exists.")
    
    # Append new product to the list and save it
    products.append(product)
    save_product(products)
    return product
        
