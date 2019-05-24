import math
import sys
from collections import defaultdict
import morpholog


def getwords(doc):
    words = [s.lower() for s in morpholog.split(doc)]
    return tuple(w for w in words)


class NaiveBayes:

    def __init__(self):
        self.categories = set()
        self.vocabularies = set()
        self.wordcount = {}         # wordcount[cat][word]
        self.catcount = {}          # catcount[cat]
        self.denominator = {}       # denominator[cat] P(word|cat)

    def train(self, data):
        for d in data:
            cat = d[0]
            self.categories.add(cat)
        for cat in self.categories:
            self.wordcount[cat] = defaultdict(int)
            self.catcount[cat] = 0
        # count words
        for d in data:
            cat, doc = d[0], d[1:]
            self.catcount[cat] += 1
            for wc in doc:
                word, count = wc.split(":")
                count = int(count)
                self.vocabularies.add(word)
                self.wordcount[cat][word] += count

        for cat in self.categories:
            self.denominator[cat] = sum(
                self.wordcount[cat].values()) + len(self.vocabularies)

    def classifier(self, doc):
        best = None  # best category
        maximum = -sys.maxsize
        # word = getwords(doc)

        # Calculate logarithm of probability for each category
        for cat in self.catcount.keys():
            # print(cat)
            prob = self.score(doc, cat)
            # print(prob)
            if prob > maximum:
                maximum = prob
                best = cat
        return best

    # occurrence probability of category
    def priorprob(self, cat):
        return float(self.catcount[cat] / sum(self.catcount.values()))

    def score(self, doc, cat):
        score = math.log(self.priorprob(cat))
        for wc in doc:
            word, count = wc.split(":")
            count = int(count)
            for i in range(count):
                score += math.log(self.wordprob(word, cat))

        return score

    # number of a word appears in a certain category
    def incategory(self, word, cat):
        if word in self.wordcount[cat]:
            return float(self.wordcount[cat][word])
        return 0.0

    # Conditional probability P(word|cate)
    def wordprob(self, word, cat):
        prob = (self.incategory(word, cat) + 1.0) / \
            self.denominator[cat]
        return prob

    def __str__(self):
        total = sum(self.catcount.values())
        return "documents: %d, vocabularies: %d, categories: %d" % \
               (total, len(self.vocabularies), len(self.categories))
