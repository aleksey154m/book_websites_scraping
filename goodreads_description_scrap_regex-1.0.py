import requests
from urllib.parse import quote
from time import sleep
import regex
import re


def get_description(xml_response):
    pattern_descr = regex.compile(r'(?<=<description><!\[CDATA\[).*(?=]]><\/description>)', flags=re.IGNORECASE)
    pattern_clear = regex.compile('(<br />[ ]*)+', flags=re.IGNORECASE)
    description = regex.findall(pattern_descr, xml_response.text)
    if not description:
        return None
    description = regex.sub(pattern_clear, '\n', description[0])
    description = regex.sub('<.*?>', '', description)
    return description


def get_description_goodreads_title_author(title=None, author=None):
    try:
        sleep(2)
        title_q = quote(title)
        url = f'https://www.goodreads.com/book/title.xml?key=Oy45h0CWmvHA7gDifDH6eQ&title={title_q}'
        # If author present chage url link
        if author:
            author_q = quote(author)
            url = url + f'&author={author_q}'
        xml_response = requests.get(url)
        description = get_description(xml_response)

        return description

    except Exception as e:
        print(f'No results for {title, author} in Books.')
        print(f"error {e}")
        return None


def get_description_goodreads_isbn(isbn):
    try:
        sleep(2)
        url = f'https://www.goodreads.com/book/isbn/{isbn}?key=Oy45h0CWmvHA7gDifDH6eQ'
        xml_response = requests.get(url)
        description = get_description(xml_response)

        return description

    except Exception as e:
        print(f'No results for {isbn} in Books.')
        print(f"error {e}")
        return None
