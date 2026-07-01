from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products, add_product, remove_product, change_product
from schema.product import Product, ProductUpdate

from datetime import datetime
from uuid import uuid4, UUID

# Create FastAPI application
app = FastAPI()

# Route path GET endpoint
@app.get('/')
def root():
    return {"message": "Welcome to FastAPI."}

# Get list of products from name-based Search filter
@app.get("/products")
def list_products(
    name:str = Query(
        default = None, 
        min_length = 1, 
        max_length = 50, 
        description = "Search by Product Name (case insensitive)"
    ),
    sort_by_price:bool = Query(
        default = False,
        description = " Sort products by price"
    ),
    order:str = Query(
        default = "asc",
        description = "Sort order when sort_by_price = true (asc, desc)"
    ),
    limit:int = Query(
        default = 10,
        ge = 1,
        le = 100,
        description = "Number of items to return"
    ),
    offset:int = Query(
        default = 0,
        ge = 0,
        description = "Pagination offset"
    )
):
    # Load all products from data
    products = get_all_products()

    if name:
        # clean name
        search_term = name.strip().lower()

        # Filter & list products after matching search term and product name
        products = [p for p in products if search_term in p.get("name", "").lower()]

    # Raise exception if no products match the search term
    if not products:
        raise HTTPException(
            status_code = 404,
            detail = f"No product found matching name = {name}"
        )
    
    # Sort products by price in ascending or descending order
    if sort_by_price:
        # if order is desc then reverse = True, order is asc then revesrse = False
        reverse = order == "desc"
        products = sorted(products, key = lambda p:p.get("price", 0), reverse=reverse)

    # Count final results after filtering
    total = len(products)

    # Pagination using offset and limit
    products = products[offset:offset+limit]

    return {"total": total, "limit":limit, "items": products}

# Get product by its unique ID
@app.get("/products/{product_id}")
def get_product_by_id(
        product_id: str = Path(
            ...,
            min_length = 36,
            max_length = 36,
            description = "UUID of the products"
        )
):
    # Load all products from data
    products = get_all_products()

    # find an return matching products
    for product in products:
        if product["id"] == product_id:
            return product
    
    # return 404 if product does not exist
    raise HTTPException(status_code = 404, detail = "Product not found!")

# Create product endpoint (201 Created)
@app.post("/products", status_code = 201)
def create_product(product: Product):
    # Convert Product model to dictionary and add additional fields
    product_dict = product.model_dump(mode = "json")
    
    # Add unique ID and timestamp to the product data
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat()
    
    # Add product to the data source and handle error
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
    
    # Return received product data
    return product.model_dump(mode = "json")

# Delete product endpoint
@app.delete("/products/{product_id}")
def delete_product(
    product_id:UUID = Path(..., description = "UUID of the product to delete")
):
    # Remove product and handle exceptions
    try:
        res = remove_product(str(product_id))
        return res
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

# Update product endpoint
@app.put("/products/{product_id}")
def update_product(
    product_id:UUID = Path(..., description = "Product UUID"),
    payload: ProductUpdate = ...,
):  
    # Update product and handle exceptions
    try:
        update_product = change_product(str(product_id), payload.model_dump(mode = "json", exclude_unset = True))
        return update_product
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))