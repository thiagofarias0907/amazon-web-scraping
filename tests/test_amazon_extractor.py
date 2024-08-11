import unittest
from unittest.mock import patch

from controllers.amazon_parser_controller import AmazonParserController
import os

test_dir = os.path.dirname(__file__)

class AmazonExtractorTestCase(unittest.TestCase):
    complete_page_controller = AmazonParserController(os.path.join(test_dir,'pages/complete_page.html'))
    fewer_items_page_controller = AmazonParserController(os.path.join(test_dir,'pages/fewer_items_page.html'))
    without_items_page_controller = AmazonParserController(os.path.join(test_dir,'pages/items_not_found.html'))

    bestseller_item_controller = AmazonParserController(os.path.join(test_dir,'pages/bestseller_item.html'))
    regular_item_controller = AmazonParserController(os.path.join(test_dir,'pages/regular_item.html'))

    without_review_item_controller = AmazonParserController(os.path.join(test_dir,'pages/without_review_item.html'))

    def test_number_of_items_parsed(self):
        """Should match the right number of items in each page"""
        self.assertEqual(24, len(self.complete_page_controller._find_items()),
                         "Main html page parser must match 24 items")
        self.assertEqual(9, len(self.fewer_items_page_controller._find_items()),
                         "'Fewer Items' html page parser must match 9 items")
        self.assertEqual(0, len(self.without_items_page_controller._find_items()),
                         "'Items Not Found' html page parser must match 0 item")

    def test_number_of_products_extracted(self):
        """Should match the number of products extracted that must be returned for each page"""
        self.assertEqual(24, len(self.complete_page_controller.list_products()),
                         "Main html page must return 24 products")
        self.assertEqual(9, len(self.fewer_items_page_controller.list_products()),
                         "'Fewer Items' must return 9 products")
        self.assertEqual(0, len(self.without_items_page_controller.list_products()),
                         "'Items Not Found' must return 0 products")

    def test_has_rating(self):
        """Should match true when the item's innerHtml has the bestseller tag, false otherwise"""
        without_rating_item = self.without_review_item_controller.soup
        self.assertFalse(self.without_review_item_controller._has_rating(without_rating_item))

        with_rating_item = self.regular_item_controller.soup
        self.assertTrue(self.regular_item_controller._has_rating(with_rating_item))

    def test_rating_value(self):
        """Should get the item's rating value"""
        with patch('controllers.amazon_parser_controller.AmazonParserController._has_rating') as mock_controller_has_rating:
            mock_controller_has_rating.return_value = True
            item_controller = AmazonParserController(os.path.join(test_dir,'pages/regular_item.html'))
            self.assertEqual(4.7, item_controller._get_rating(item_controller.soup))

    def test_rating_value_when_none(self):
        """Should return 0.0 when item's rating value does not exist"""

        with patch('controllers.amazon_parser_controller.AmazonParserController._has_rating') as mock_controller_has_rating:
            mock_controller_has_rating.return_value = False
            item_controller = AmazonParserController(os.path.join(test_dir,'pages/without_review_item.html'))
            self.assertEqual(0.0, item_controller._get_rating(item_controller.soup))

    def test_price_whole_value(self):
        """Should extract the whole part digits of the price"""

        regular_item = self.regular_item_controller.soup
        self.assertEqual(1719, self.regular_item_controller._get_whole_price_value(regular_item))

        bestseller_item = self.bestseller_item_controller.soup
        self.assertEqual(248, self.bestseller_item_controller._get_whole_price_value(bestseller_item))

    def test_price_decimal_value(self):
        """Should extract the decimal / fractional part digits of the price"""

        regular_item = self.regular_item_controller.soup
        self.assertEqual(0, self.regular_item_controller._get_decimal_fraction_price_value(regular_item))

        bestseller_item = self.bestseller_item_controller.soup
        self.assertEqual(89, self.bestseller_item_controller._get_decimal_fraction_price_value(bestseller_item))

    def test_price_float(self):
        """Should return the complete price value as float"""

        regular_item = self.regular_item_controller.soup
        self.assertEqual(1719.0, self.regular_item_controller._get_price(regular_item))

        bestseller_item = self.bestseller_item_controller.soup
        self.assertEqual(248.89, self.bestseller_item_controller._get_price(bestseller_item))

    def test_has_best_seller_tag(self):
        """Should match true when the item's innerHtml has the bestseller tag, false otherwise"""

        best_seller_item = self.bestseller_item_controller.soup
        self.assertTrue(self.bestseller_item_controller._has_bestseller_tag(best_seller_item))

        regular_item = self.regular_item_controller.soup
        self.assertFalse(self.regular_item_controller._has_bestseller_tag(regular_item))

    def test_name(self):
        """Should extract the item's name"""
        regular_item = self.regular_item_controller.soup
        self.assertEqual("SMARTPHONE XIAOMI POCO X3 PRO 6GB RAM 128GB ROM - GLOBAL Cor:Frost Blue",
                         self.regular_item_controller._get_name(regular_item))

        best_seller_item = self.bestseller_item_controller.soup
        self.assertEqual("Relógio Xiaomi Mi Band 6 Original - Versão Global -",
                         self.bestseller_item_controller._get_name(best_seller_item))

    def test_first_item_values(self):
        """Should parse the first item's values correctly"""
        first_product = self.complete_page_controller.list_products()[0]
        self.assertEqual("Smartphone Poco X3 PRO 256gb 8gb RAM – Phantom Black - Preto", first_product.name)
        self.assertEqual(1975.0, first_product.price)
        self.assertEqual(4.8, first_product.rating)
        self.assertTrue(first_product.bestseller)

    def test_last_item_values(self):
        """Should parse the last item's values correctly"""
        first_product = self.complete_page_controller.list_products()[23]
        self.assertEqual("Novo Apple iPad - 10,2 polegadas, Wi-Fi, 32 GB - Space Gray - 8ª geração", first_product.name)
        self.assertEqual(2538.57, first_product.price)
        self.assertEqual(4.9, first_product.rating)
        self.assertFalse(first_product.bestseller)

    def test_third_item_values(self):
        """Should parse the third item's values correctly"""
        first_product = self.complete_page_controller.list_products()[2]
        self.assertEqual(
            "Fire TV Stick Lite com Controle Remoto Lite por Voz com Alexa (sem controles de TV) | Streaming em Full HD | Modelo 2020",
            first_product.name)
        self.assertEqual(349.0, first_product.price)
        self.assertEqual(4.8, first_product.rating)
        self.assertFalse(first_product.bestseller)

    def test_number_of_best_seller_items(self):
        """Should return 5 items with bestseller attribute as True"""
        products = self.complete_page_controller.list_products()
        counter = 0
        for product in products:
            if product.bestseller:
                counter = counter + 1
        self.assertEqual(5, counter)

    def test_number_of_regular_items(self):
        """Should return 19 items with false bestseller attribute"""
        products = self.complete_page_controller.list_products()
        counter = 0
        for product in products:
            if not product.bestseller:
                counter = counter + 1
        self.assertEqual(19, counter)

    def test_without_items(self):
        """Should return 0 items when it's a page without results"""
        self.assertEqual(0, len(self.without_review_item_controller.list_products()))


if __name__ == '__main__':
    unittest.main()
