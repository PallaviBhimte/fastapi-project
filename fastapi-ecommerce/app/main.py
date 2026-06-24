from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products

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
            description = "UUID of the products",
            example = "c47ea2457-c4a9-4bfg-9dd5-6464r0ebe343"
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