import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import regex
from time import sleep


def scrape_web_source(url):
    sleep(3)
    my_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
                  'Accept-Encoding': 'gzip, deflate, br,',
                  'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36 OPR/67.0.3575.31'}

    # Download the page using requests
    try:
        html_source = requests.get(url, headers=my_headers)
        html_source = html_source.content.decode('utf-8')

        return html_source

    except Exception as e:
        print(f"error {e}")
        return None


def get_description_livelib(title_or_ISBN):
    book_enumeration_link = (r"https://www.livelib.ru/find/" + quote(title_or_ISBN))
    bs = BeautifulSoup(scrape_web_source(book_enumeration_link), 'html5lib')

    try:
        # Try to get first book link if exist any
        no_res = bs.find('span', {'class': 'not-found-text'})
        if no_res:
            print(f'По запросу «{title_or_ISBN}» ничего не найдено.')
            return None

        book_link = (bs.find('a', {'class': 'title'}).get('href'))

        # Try to get book description if exist
        book_link = r"https://www.livelib.ru" + book_link
        bs = BeautifulSoup(scrape_web_source(book_link), 'html5lib')
        raw_description = bs.find('p', {'itemprop': 'description'}).get_text()
        # Clear book description
        raw_description = regex.sub('(\\n)+[ ]*', '\n', raw_description)
        raw_description = regex.sub(r'^\s+|\s+$', '', raw_description)
        description = raw_description

        return description

    except Exception as e:
        print(f'No description for {title_or_ISBN} on book page.')
        print(f"error {e}")
        return None
