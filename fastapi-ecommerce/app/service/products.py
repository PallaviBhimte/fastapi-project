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

# Remove a product by its unique ID
def remove_product(id: str) -> str:
    products = get_all_products()
    
    # Find and remove the product with the matching ID
    for idx, p in enumerate(products):
        if p["id"] == str(id):
            deleted = products .pop(idx)
            save_product(products)
            return {"message": "Product deleted successfully.", "data": deleted}     

# Update product by its unique ID
def change_product(product_id:str, update_data: dict):
    products = get_all_products()
    
    # Find the product with the matching ID and update its fields
    for index, product in enumerate(products):
        
        # Check if the product ID matches the provided ID
        if product["id"] == str(product_id):
            
            # Update product fields with new data, exclude None values
            for key, value in update_data.items():
                if value is None:
                    continue
                if isinstance(value, dict) and isinstance(product.get(key), dict):
                    product[key].update(value)
                else:
                    product[key] = value
            products[index] = product
            save_product(products)
            return product
    raise ValueError(f"Product not found.")