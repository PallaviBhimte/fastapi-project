from fastapi import FastAPI, HTTPException, Query
from service.products import get_all_products

# Create FastAPI application
app = FastAPI()

# Route path GET endpoint
@app.get('/')
def root():
    return {"message": "Welcome to FastAPI."}

# # Get all products
# @app.get("/products")
# def get_products():
#     return get_all_products()

# Get list of products from name-based Search filter
@app.get("/products")
def list_products(
    name:str = Query(
        default = None, 
        min_length = 1, 
        max_length = 50, 
        description = "Search by Product Name (case insensitive)"
    )
):
    # Load all products from data
    products = get_all_products()

    if name:
        # clean name
        search_term = name.strip().lower()

        # Filter & list products after matching search term and product name
        products = [p for p in products if search_term in p.get("name", "").lower()]

        # Raise error if no products match the search term
        if not products:
            raise HTTPException(
                status_code = 404,
                detail = f"No product found matching name = {name}"
            )
        
        # Count final results after filtering
        total = len(products)

    return {"total": total, "items": products}