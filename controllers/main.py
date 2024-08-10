import bs4

import re

class Controller:

    def __init__(self, content_path):
        self.content_path = content_path
        self.soup = self.__parse_html()
        # e_commerce_html = open('pages/content.html', 'r', encoding='utf-8')
        # # Parse html
        # self.soup = bs4.BeautifulSoup(e_commerce_html.read(), 'html.parser')

    def list_products(self):
        """Documentation here"""
        # print(self.soup.find('span', {'class': 'a-badge-text'}).text)

        # This should return the list of products
        return []

    def __read_file(self):
        """Read a html file content. It will throw FileNotFound and other reading exception"""
        # todo: Might need to create a webpage reader using uri + requests, unless this projects still aims to read a file from a cloud storage

        html_content = open(self.content_path, 'r', encoding='utf-8')
        return html_content.read()

    def __parse_html(self):
        """Parse the html content with BeautifulSoup"""
        return bs4.BeautifulSoup(self.__read_file(), 'html.parser')

    def _find_items(self):
        """Find the items list"""
        return self.soup.select('span .s-result-item')

    @staticmethod
    def has_rating(item: bs4.BeautifulSoup) -> bool:
        return len(item.select('div .a-row.a-size-small')) > 0

    @staticmethod
    def has_bestseller_tag(item: bs4.BeautifulSoup) -> bool:
        match = item.select('span .a-badge-text')
        if (match is None) or (len(match) == 0):
            return False
        match_text = re.sub("\\n\s+",' ', match[0].text.strip())
        return match_text == 'Mais vendido'

