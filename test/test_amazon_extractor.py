import unittest

from controllers.main import Controller


class AmazonExtractorTestCase(unittest.TestCase):

    complete_page_controller = Controller('test_pages/complete_page.html')
    fewer_items_page_controller = Controller('test_pages/fewer_items_page.html')
    without_items_page_controller = Controller('test_pages/items_not_found.html')

    bestseller_item_controller = Controller('test_pages/bestseller_item.html')
    regular_item_controller = Controller('test_pages/regular_item.html')

    without_review_item_controller = Controller('test_pages/without_review_item.html')

    # complete_page = open('test_pages/complete_page.html', 'r', encoding='utf-8')
    # parsed_complete_page_soup = bs4.BeautifulSoup(complete_page.read(), 'html.parser')
    #
    # fewer_items_page = open('test_pages/fewer_items_page.html', 'r', encoding='utf-8')
    # parsed_fewer_items_page_soup = bs4.BeautifulSoup(complete_page.read(), 'html.parser')

    def test_number_of_items_parsed(self):
        """Should match the right number of items in each page"""
        self.assertEqual(24, len(self.complete_page_controller._find_items()), "Main html page parser must match 24 items")
        self.assertEqual(9, len(self.fewer_items_page_controller._find_items()), "'Fewer Items' html page parser must match 9 items")
        self.assertEqual(0, len(self.without_items_page_controller._find_items()), "'Items Not Found' html page parser must match 0 item")

    def test_number_of_products_extracted(self):
        """Should match the number of products extracted that must be returned for each page"""
        self.assertEqual(24, len(self.complete_page_controller.list_products()), "Main html page must return 24 products")
        self.assertEqual(9, len(self.fewer_items_page_controller.list_products()), "'Fewer Items' must return 9 products")
        self.assertEqual(0, len(self.without_items_page_controller.list_products()), "'Items Not Found' must return 0 products")

    def test_has_rating(self):
        """Should match true when the item's innerHtml has the bestseller tag, false otherwise"""
        without_rating_item = self.without_review_item_controller.soup
        self.assertFalse(self.without_review_item_controller.has_rating(without_rating_item))

        with_rating_item = self.regular_item_controller.soup
        self.assertTrue(self.regular_item_controller.has_rating(with_rating_item))

    def test_rating_value(self):
        self.fail()

    def test_rating_value_when_none(self):
        self.fail()

    def test_price_whole_value(self):
        self.fail()

    def test_price_decimal_value(self):
        self.fail()

    def test_price_float(self):
        self.fail()

    def test_has_best_seller_tag(self):
        """Should match true when the item's innerHtml has the bestseller tag, false otherwise"""
        best_seller_item = self.bestseller_item_controller.soup
        self.assertTrue(self.bestseller_item_controller.has_bestseller_tag(best_seller_item))

        regular_item = self.regular_item_controller.soup
        self.assertFalse(self.regular_item_controller.has_bestseller_tag(regular_item))

    def test_is_best_seller(self):
        self.fail()

    def test_name(self):
        self.fail()

    def test_name_encoding_cleaning(self):
        self.fail()

    def test_first_item_values(self):
        self.fail()

    def test_last_item_values(self):
        self.fail()

    def test_third_item_values(self):
        self.fail()

    def test_page_number(self):
        self.fail()

    def test_has_next_page(self):
        self.fail()

    def test_number_of_best_seller_items(self):
        self.fail()

    def test_number_of_regular_items(self):
        self.fail()

    def test_without_items(self):
        self.fail()



if __name__ == '__main__':
    unittest.main()
