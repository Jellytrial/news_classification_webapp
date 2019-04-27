import codecs
import sys
import math
from naivebayes import NaiveBayes
from sklearn.externals import joblib


number = []
f = open("trans_word.csv")
for line in f:
    line = line.rstrip()
    number.append(line.split()[0])
f.close()
num = len(number)
print(num)


def crossValidation(data, N=num, randomize=False):

    if randomize:
        from random import shuffle
        shuffle(data)

    # Cross Validation
    accuracyList = []
    for n in range(N):
        # split train and test data
        trainData = [d for i, d in enumerate(data) if i % N != n]
        testData = [d for i, d in enumerate(data) if i % N == n]
        # print(len(trainData), len(testData))
        # train data
        nb = NaiveBayes(100)
        nb.train(trainData)

        # save trained model
        joblib.dump(nb, 'trained_nb.m')

        # accuracy of test data
        hit = 0
        numTest = 0
        for d in testData:
            correct = d[0]
            words = d[1:]
            predict = nb.classify(words)
            if correct == predict:
                hit += 1
            numTest += 1
        accuracy = float(hit) / float(numTest)
        accuracyList.append(accuracy)

    average = sum(accuracyList) / float(N)
    average_f = round(average, 4)
    return average


if __name__ == "__main__":
    data = []
    f = codecs.open("trans_word.csv", "r", "utf-8")
    for line in f:
        line = line.rstrip()
        temp = line.split()
        data.append(temp)
    f.close()
    # Cross Validation
    average = crossValidation(data, N=num, randomize=True)
    average_f = round(average, 4)
    print(average_f)
