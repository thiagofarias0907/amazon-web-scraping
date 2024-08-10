import bs4

import re

from exceptions.ParsingFailureException import ParsingFailureException
from models.product import Product


class Controller:
    """
    Main controller class for extracting data from the Amazon Website products' list

    Assumptions:
     - Using the html file provided, not needed to use a real request with url and request lib
     - Expecting that price and values are in the same currency
     - Extracting only the final and best price value (main value shown for each item) after discounts
    """

    def __init__(self, content_path):
        self.content_path = content_path
        self.soup = self.__parse_html()

    def list_products(self, bestseller_filter: bool = False, rating_value_filter: float = None, name_filter :str = None):
        """Main function that control the procedure to parse and list the products given the filters"""
        products = []
        parsed_items = self._find_items()
        for item in parsed_items:
            name = self._get_name(item)
            if (name_filter is not None) and (name_filter != name):
                continue

            bestseller = self._has_bestseller_tag(item)
            if bestseller_filter and not bestseller:
                continue

            rating = self._get_rating(item)
            if (rating_value_filter is not None) and rating <= rating_value_filter:
                continue

            price = self._get_price(item)
            product = Product(name=name, price=price, bestseller=bestseller, rating=rating)
            products.append(product)
        return products

    def __read_file(self):
        """Read a html file content. It will throw FileNotFound and other reading exception"""
        html_content = None
        with open(self.content_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content

    def __parse_html(self):
        """Parse the html content with BeautifulSoup"""
        return bs4.BeautifulSoup(self.__read_file(), 'html.parser')

    def _find_items(self) -> list:
        """Find the items list"""
        items = list(self.soup.select('span .s-result-item.s-asin'))
        return items

    @staticmethod
    def _has_rating(item: bs4.BeautifulSoup) -> bool:
        """Checks if the rating row exists for the given item inner html"""
        match_css_select = item.select('div .a-row.a-size-small')
        if (match_css_select is None) or (len(match_css_select) == 0):
            return False
        else:
            return True

    @staticmethod
    def _has_bestseller_tag(item: bs4.BeautifulSoup) -> bool:
        """Check if the bestseller tag exists for the given item"""
        match = item.select('span .a-badge-text')
        if (match is None) or (len(match) == 0):
            return False

        match_text = re.sub("\\n\s+", ' ', match[0].text.strip())
        return match_text == 'Mais vendido'

    def _get_rating(self, item: bs4.BeautifulSoup):
        """Extract the rating value for the given item"""
        if not self._has_rating(item):
            return 0.0

        match_css_select = item.select('div .a-row.a-size-small')
        match_text = re.search("([\\d,]+).*de.*\\d+", match_css_select[0].text.strip())

        if (match_text is None) or (len(match_text.groups()) == 0):
            raise ParsingFailureException(id="get_rating", content=match_css_select[0].text)

        return float(match_text.group(1).replace(',', '.'))

    @staticmethod
    def _get_name(item) -> str:
        """Extract the item's name"""
        match = item.select('.a-size-base-plus.a-color-base.a-text-normal')
        if (match is None) or (len(match) == 0):
            return False
        match_text = re.sub("\\n\s+", ' ', match[0].text.strip())
        return match_text

    def _get_price(self, item) -> float:
        """Extract the item's price"""
        return self._get_whole_price_value(item) + self._get_decimal_fraction_price_value(item) / 100

    @staticmethod
    def _get_whole_price_value(item) -> int:
        """Extract the whole / integer part of the price. It expects positive or 0 values only"""
        match = item.select('span .a-price-whole')
        if (match is None) or (len(match) == 0):
            return False
        match_text = re.sub("\\D+", '', match[0].text.strip())
        return int(match_text)

    @staticmethod
    def _get_decimal_fraction_price_value(item) -> int:
        """Extract the item price's decimal fraction"""
        match = item.select('span .a-price-fraction')
        if (match is None) or (len(match) == 0):
            return False
        match_text = re.sub("\\D+", '', match[0].text.strip())
        return int(match_text)
