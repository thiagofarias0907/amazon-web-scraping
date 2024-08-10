from pydantic import BaseModel

class Product(BaseModel):
    name: str
    bestseller: bool = False
    rating: float = 0.0
    price: float = 0.0
