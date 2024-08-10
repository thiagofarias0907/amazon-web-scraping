from fastapi import FastAPI
from controllers import main

app = FastAPI()

@app.get('/list_products')
def list_products(best_seller=False):
    """Returns a list with all products in the page"""
    return main.list_products(best_seller=best_seller)
