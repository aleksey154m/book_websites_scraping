import requests
from bs4 import BeautifulSoup
import re
import regex
from time import sleep


def get_description_twirpx(title_or_ISBN):
    my_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Accept-Encoding': 'gzip, deflate, br,',
                  'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36 OPR/67.0.3575.31'}

    url = r'https://www.twirpx.com'
    # Download the page using requests
    try:
        # Start session and ger SART code for furhter scraping
        sess = requests.Session()
        html_source = sess.get(url, headers=my_headers)
        bs = BeautifulSoup(html_source.text, 'html5lib')
        SART_code = bs.find('div', {'id': 'div_search_box'}).find('form').find('input', {'name': "__SART"}).get('value')
        sleep(2)

        # Get web with book list and withdraw description
        data = {'SearchQuery': title_or_ISBN, 'SearchScope': 'site',
                'SearchUID': '0', 'SearchCID': '0', 'SearchECID': '0',
                '__SART': SART_code}

        url_for_book_list = 'https://www.twirpx.com/search/'
        list_html_source = sess.post(url_for_book_list, headers=my_headers, data=data)
        bs = BeautifulSoup(list_html_source.text, 'html5lib')
        book_id = bs.find('div', {'data-file-status': 'approved'}).get('data-object-id')
        sleep(2)

        # Get description from book webpage if exist any
        url_for_book_descr = f'https://www.twirpx.com/file/{book_id}/'
        descr_html_source = sess.get(url_for_book_descr, headers=my_headers)
        bs = BeautifulSoup(descr_html_source.text, 'html5lib')
        description = str(bs.find('div', {'itemprop': 'description'}))

        # Clear book description
        description = regex.sub('<div class="bb-sep">|<br/>[ ]*', '\n', description, flags=re.IGNORECASE)
        description = regex.sub('<.*?>', '', description, flags=re.IGNORECASE)
        description = regex.sub('(\\n)+', '\n', description, flags=re.IGNORECASE)
        description = regex.sub(r'^\s+|\s+$', '', description)
        sleep(2)

        return description

    except Exception as e:
        print(f"There is no description on www.twirpx for {title_or_ISBN}")
        print(f"error {e}")
        return None
