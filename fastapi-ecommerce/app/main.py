from fastapi import FastAPI

app = FastAPI()

# Static Route: Calling this 40 times will give the message 40 times.
@app.get('/')
def root():
    return {"message": "Welcome to FastAPI."}

# Dynamic Route - Calling product data based on the ID.
@app.get('/products/{id}')
def get_products(id:int):
    products = ['Brush', 'Laptop', 'Mouse', 'Monitor']
    return products[id]

# whatever ID you pass, you'll get the data according to that.