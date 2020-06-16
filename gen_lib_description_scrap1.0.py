import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import regex
from time import sleep



def get_description_libgen(md5hash):
    sleep(3)
    my_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Accept-Encoding': 'gzip, deflate, br,',
                  'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36 OPR/67.0.3575.31'}

    # Download the page using requests and scrap description
    url = f'http://gen.lib.rus.ec/book/index.php?md5={md5hash}'
    try:
        html_source = requests.get(url, headers=my_headers)

        bs = BeautifulSoup(html_source.text, 'html5lib')
        description = str(bs.tbody.find_all('tr', recursive=False)[18])
        description = regex.sub('(<br/>)+', '\n', description)
        description = regex.sub('<.*?>', '', description)
        description = regex.sub(r'^\s+|\s+$', '', description)

        return description

    except Exception as e:
        print(f"error {e}")
        return None


print(get_description_libgen('29275786108C4FD681B8E6A96C62AEF2'))