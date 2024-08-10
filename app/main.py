from fastapi import FastAPI
from controllers.main import Controller

app = FastAPI(title='AmazonScraper')
controller = Controller('pages/content.html')


@app.get('/list_products')
def list_products(bestseller: bool = False, name: str = None, rating_value: float = None):
    """Returns a list with all products in the page"""
    return controller.list_products(bestseller_filter=bestseller, rating_value_filter=rating_value, name_filter=name)
