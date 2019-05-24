import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


def get_news_text(url):
    if url is None or url is '':
        return None
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as E:
        print(E)
        return None
    except URLError as E:
        print(E)
        return None

    try:
        soup = BeautifulSoup(html.read(), 'lxml')
    except AttributeError as E:
        print(E)
        return None

    # get text
    text = soup.find('h1').get_text()
    print(text)
    return text
