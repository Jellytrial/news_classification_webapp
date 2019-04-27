import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


def get_news_text(url):
    if url is None or url is '':
        return None
    try:
        html = urllib.request.urlopen(url)
    except HTTPError:
        return None
    except URLError:
        return None

    try:
        soup = BeautifulSoup(html.read(), 'lxml')
    except AttributeError:
        return None

    # get text
    text = soup.find('h1').get_text()
    print(text)
    return text
