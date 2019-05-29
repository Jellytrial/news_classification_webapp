from bs4 import BeautifulSoup
from urllib import request
from nbclass import NaiveBayes
from sklearn.externals import joblib
from urllib.error import HTTPError, URLError
import csv
import time


def gunosy_category(model):
    categories = {
        'https://gunosy.com/categories/1': 'エンタメ',
        'https://gunosy.com/categories/2': 'スポーツ',
        'https://gunosy.com/categories/3': 'おもしろ',
        'https://gunosy.com/categories/4': '国内',
        'https://gunosy.com/categories/5': '海外',
        'https://gunosy.com/categories/6': 'コラム',
        'https://gunosy.com/categories/7': 'IT・科学',
        'https://gunosy.com/categories/8': 'グルメ',
    }

    page_numb = 1

    f1 = open('content.csv', 'w')
    contentWriter = csv.writer(f1)
    f2 = open('category', 'w')
    categoryWriter = csv.writer(f2)

    for url, name in categories.items():
        print(url)
        try:
            category_html = request.urlopen(url)
        except HTTPError as E:
            print(E)
            continue

        try:
            category_extract = BeautifulSoup(category_html.read(),
                                             'html.parser')
        except URLError as E:
            print(E)
            continue

        for page_index in range(1, 21):
            category_page_url = ["%s?page=%s" % (url, page_index)]
            # print(category_page_url)

            for page_url in category_page_url:
                try:
                    page_html = request.urlopen(page_url)
                except URLError as E:
                    # print('Page not found', E)
                    continue

                try:
                    page_extract = BeautifulSoup(page_html.read(),
                                                 'html.parser')
                except URLError as E:
                    print(E)
                    continue

            for index in range(0, 20):
                try:
                    title = page_extract.find_all('div',
                                                  {'class': 'list_title'})[index].a.get_text()
                    article_text = page_extract.find_all('div', {'class': 'list_lead'})[index].get_text()
                    sum_text = title + article_text
                    listdata1, listdata2 = [], []
                    listdata1.append(title)
                    listdata2.append(article_text)
                    contentWriter.writerow(listdata1 + listdata2)
                    listname = []
                    listname.append(name)
                    categoryWriter.writerow(listname)
                except AttributeError:
                    continue

                print('No.%s, extraction.train(%s, %s)' % (page_numb, sum_text,
                                                           name))
                model.train(sum_text, name)

                page_numb = page_numb + 1
                time.sleep(1)

if __name__ == "__main__":
    # get articles
    nb = NaiveBayes()
    gunosy_category(nb)
    joblib.dump(nb, 'trained_nb.m')
