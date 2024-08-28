# Simple Amazon Web Scraping

## Description
Simple Web Scraper API using BeautifulSoup and FastApi. It uses a file (*content.html*) containing the html page of a search result from the Amazon Website. This project was made with a TDD approach, using the html files in the `tests/pages` folder.

**Main classes:**
 - app > endpoint definition
 - html_parser_interface > an example of using abstract classes to emulate an interface in python
 - amazon_parser* > main class with the parser / scraping functions 

**Tests:**
 - test_app.py > api unit tests
 - test_amazon_extractor > scraping unit tests 

## Setting up your development environment

### Installing the libraries
At the same directory as this file, run:
  - `pip install pipenv`
  - `pipenv install`

### Running the API for development
Initialize your app using `pipenv`:

- `pipenv shell`

Then run the following commands:

- `uvicorn app.main:app --reload`

And your app will be running on http://localhost:8000/

Tip:

Access http://localhost:8000/docs to use the built-in interface.

### Running the test files
 - `python -m unittest discover Tests`
