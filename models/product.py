class Product:
    __name = None
    __bestseller = False
    __rating = 0.0
    __price = 0.0

    def __init__(self, name: str, bestseller: bool, rating: float, price: float):
        self.__name = name
        self.__bestseller = bestseller
        self.__rating = rating
        self.__price = price
