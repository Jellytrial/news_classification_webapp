"""Text classification using Naive Bayes classifier
"""
import math
import sys
import morpholog


def getwords(doc):
    words = [s.lower() for s in morpholog.split(doc)]
    return tuple(w for w in words)


class NaiveBayes:
    def __init__(self):
        self.vocabularies = set()  # set of words
        self.wordcount = {}  # {category: { words: n, ...}}
        self.catecount = {}  # {category: n}

    # Training phase: word count up
    def wordcountup(self, word, cate):
        self.wordcount.setdefault(cate, {})
        self.wordcount[cate].setdefault(word, 0)
        self.wordcount[cate][word] += 1
        self.vocabularies.add(word)  # remove duplicates

    # training phase: category count up
    def catecountup(self, cate):
        self.catecount.setdefault(cate, 0)
        self.catecount[cate] += 1

    # training
    def train(self, doc, cate):
        word = getwords(doc)
        for w in word:
            self.wordcountup(w, cate)
        self.catecountup(cate)

    # Estimation phase: classification
    def classifier(self, doc):
        best = None  # best category
        maximum = -sys.maxsize
        word = getwords(doc)

        # Calculate logarithm of probability for each category
        for cate in list(self.catecount.keys()):
            prob = self.score(word, cate)
            if prob > maximum:
                maximum = prob
                best = cate
        return best

    # calculate score
    def score(self, word, cate):
        score = math.log(self.priorprob(cate))
        for w in word:
            score += math.log(self.wordprob(w, cate))

        return score

    # occurrence probability of category
    def priorprob(self, cate):
        return float(self.catecount[cate] / sum(self.catecount.values()))

    # number of a word appears in a certain category
    def incategory(self, word, cate):
        if word in self.wordcount[cate]:
            return float(self.wordcount[cate][word])
        return 0.0

    # Conditional probability P(word|cate)
    def wordprob(self, word, cate):
        prob = (self.incategory(word, cate) + 1.0) / \
               (sum(self.wordcount[cate].values()) +
                len(self.vocabularies) * 1.0)
        return prob

    # model evaluation score
    def value_score(self, doc, cate):
        acc_count = 0
        total_len = len(cate)
        for i in range(total_len):
            pred = self.classifier(doc[i])[0]
            if pred == cate[i]:
                acc_count += 1
        value_score = acc_count / total_len
        return value_score
