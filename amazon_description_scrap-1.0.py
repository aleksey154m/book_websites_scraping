import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import regex
import re
from time import sleep


def scrape_web_source(url):
    sleep(2)
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # Download the page using requests
    html_source = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if html_source.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in html_source.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, html_source.status_code))
        return None

    return html_source


def get_book_description_amazon(title):
    book_enumeration_link = (r"https://www.amazon.com/s?i=stripbooks-intl-ship&k=" + quote(title) + r"&ref=nb_sb_noss&url=search-alias%3Dstripbooks-intl-ship")

    bs = BeautifulSoup(scrape_web_source(book_enumeration_link).text, 'html5lib')

    # Try to get first book link if exist any
    try:
        book_link = (bs.find_all('a', {'class': 'a-link-normal a-text-normal'})[0].get('href'))
        book_link = 'https://www.amazon.com' + book_link
        print(book_link)
        bs = BeautifulSoup(scrape_web_source(book_link).text, 'html5lib')
        description = bs.find('div', {'id': 'bookDescription_feature_div'}).noscript.div
        # Clear book description
        description = regex.sub(r'<p>|(<BR>)+', '\n', str(description), flags=re.IGNORECASE)
        description = regex.sub(r'<LI>', '\n-', description, flags=re.IGNORECASE)
        description = regex.sub(r'<.*?>', '', description)
        description = regex.sub(r'^\s+|^[ ]*', '', description)

        return description

    except Exception as e:
        print(f'No results for {title} in Books on website.')
        print(f"error {e}")
        return None
