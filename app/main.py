from fastapi import FastAPI, Query
from typing import List

from controllers.amazon_parser_controller import AmazonParserController
from models.product import Product

description = """
Amazon web scraper that extract products' name, price, rating and if it's a bestseller

## List Products
You can list and filter the products from a page by:

* Score Rating greater than a specific value.
* Products Full Name.
* Filter only bestsellers (contains a 'bestseller' tag). 

"""

app = FastAPI(
    title='AmazonScraper',
    description=description
)
controller = AmazonParserController('pages/content.html')


@app.get('/list_products', response_model=List[Product])
def list_products(bestseller: bool = Query(False, description="Filter only bestsellers when 'true', otherwise show all"),
                  name: str = Query(None, description="Filter by matching the exact name of an item"),
                  rating_value: float = Query(None, description="Filter products with a rating value greater than this")):
    """Returns a list with all products in the page"""
    return controller.list_products(bestseller_filter=bestseller, rating_value_filter=rating_value, name_filter=name)
