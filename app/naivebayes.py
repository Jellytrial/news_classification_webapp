import math
import sys
from collections import defaultdict


class NaiveBayes:

    def __init__(self, data):
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

    def classify(self, doc):

        best = None
        max = -sys.maxsize
        for cat in self.catcount.keys():
            p = self.score(doc, cat)
            if p > max:
                max = p
                best = cat
        return best

    def wordProb(self, word, cat):

        return float(self.wordcount[cat][word] + 1) / \
               float(self.denominator[cat])

    def score(self, doc, cat):
        total = sum(self.catcount.values())
        score = math.log(float(self.catcount[cat]) / total)

        for wc in doc:
            word, count = wc.split(":")
            count = int(count)

            for i in range(count):
                score += math.log(self.wordProb(word, cat))
        return score

    def __str__(self):
        total = sum(self.catcount.values())
        return "documents: %d, vocabularies: %d, categories: %d" % \
               (total, len(self.vocabularies), len(self.categories))
