from fastapi import FastAPI
from typing import List

from controllers.amazon_parser_controller import AmazonParserController
from models.product import Product

description = """
Amazon web scraper that extract products' name, price, rating and if it's a bestseller

## List Products
You can list and filter the products from a page by:

* Score Rating greater than a specific value.
* Products Full Name.
* If it's a bestseller (contains a tag). 

"""

app = FastAPI(
    title='AmazonScraper',
    description=description
)
controller = AmazonParserController('pages/content.html')


@app.get('/list_products', response_model=List[Product])
def list_products(bestseller: bool = False, name: str = None, rating_value: float = None):
    """Returns a list with all products in the page"""
    return controller.list_products(bestseller_filter=bestseller, rating_value_filter=rating_value, name_filter=name)
