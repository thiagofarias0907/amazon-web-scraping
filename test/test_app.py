import urllib

from app.main import app
from fastapi.testclient import TestClient
import unittest
import json

client = TestClient(app)


class AmazonExtractorTestCase(unittest.TestCase):

    def test_read_complete_list(self):
        """Should return all products"""

        with open('jsons/complete.json', 'r', encoding='utf8') as expected_file:
            expected_response = json.loads(expected_file.read())
            response = client.get("/list_products")
            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, response.json())

            response = client.get("/list_products?bestseller=false")
            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, response.json())

    def test_read_bestsellers_list(self):
        """Should list only bestsellers"""

        response = client.get("/list_products?bestseller=true")
        self.assertEqual(200, response.status_code)
        with open('jsons/bestsellers.json', 'r', encoding='utf8') as expected_file:
            expected_response = json.loads(expected_file.read())
            self.assertEqual(expected_response, response.json())

    def test_read_item_name_list(self):
        """Should list only name matching product"""
        name_parsed = urllib.parse.quote('Novo Apple iPad - 10,2 polegadas, Wi-Fi, 32 GB - Space Gray - 8ª geração')
        response = client.get("/list_products?name=" + name_parsed)
        self.assertEqual(200, response.status_code)
        with open('jsons/single_item.json', 'r', encoding='utf8') as expected_file:
            expected_response = json.loads(expected_file.read())
            self.assertEqual(expected_response, response.json())

    def test_read_rating_over_4_8_list(self):
        """Should list only products with rating values over 4.8"""
        response = client.get("/list_products?rating_value=4.8")
        self.assertEqual(200, response.status_code)
        with open('jsons/rating_over_4_8.json', 'r', encoding='utf8') as expected_file:
            expected_response = json.loads(expected_file.read())
            self.assertEqual(expected_response, response.json())

    def test_read_rating_over_4_7_and_bestseller_list(self):
        """Should list only the three products matching the filters rating over 4.7 and bestseller"""
        response = client.get("/list_products?rating_value=4.7&bestseller=true")
        self.assertEqual(200, response.status_code)
        with open('jsons/double_filter.json', 'r', encoding='utf8') as expected_file:
            expected_response = json.loads(expected_file.read())
            self.assertEqual(expected_response, response.json())


if __name__ == '__main__':
    unittest.main()
