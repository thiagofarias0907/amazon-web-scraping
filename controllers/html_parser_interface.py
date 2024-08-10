import abc
from typing import List

import bs4

from models.product import Product


class HtmlParserInterface(metaclass=abc.ABCMeta):
    """Interface-like abstract class that claims a 'contract' that ensure which functions each must be implemented by
    children controller classes"""
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, 'list_products') and callable(__subclass.list_products) and
            hasattr(__subclass, '_find_items') and
            hasattr(__subclass, '_get_name') and
            hasattr(__subclass, '_has_bestseller_tag')  and
            hasattr(__subclass, '_get_rating') and
            hasattr(__subclass, '_get_price') or
            NotImplementedError
        )

    @abc.abstractmethod
    def list_products(self, bestseller_filter: bool = False, rating_value_filter: float = None, name_filter :str = None)  -> List[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def _find_items(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_name(self, item: bs4.BeautifulSoup) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _has_bestseller_tag(self, item: bs4.BeautifulSoup) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_rating(self, item: bs4.BeautifulSoup) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_price(self, item: bs4.BeautifulSoup) -> float:
        raise NotImplementedError

