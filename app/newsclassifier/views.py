from django.http import HttpResponse
from django.shortcuts import render
import nbclass
import traindata
import geturldoc
import urllib
import sys

# Create your views here.
# make naivebayes classifier
news_classifier = nbclass.NaiveBayes()

# train gunosy news data
traindata.gunosy_category(news_classifier)


def news_classification(request):

    d = {
        'url': request.GET.get('url')
    }
    if d['url']:
        try:
            html_text = geturldoc.get_news_text(request.GET.get('url'))
            print(html_text)
            d['category'] = news_classifier.classifier(html_text)
            print('succed classfy')
            # score = news_classifier.score(html_text, d['category'])
            # print(score)
        except ValueError as instance:
            print(instance, file=sys.stderr)
            d['category'] = False
        except urllib.error.HTTPError as instance:
            print(instance, file=sys.stderr)
            d['category'] = False
        except urllib.error.URLError as instance:
            print(instance, file=sys.stderr)
            d['category'] = False

    return render(request, 'index.html', d)
