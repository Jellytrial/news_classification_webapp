from sklearn.externals import joblib
import codecs
from naivebayes import NaiveBayes

data = []
f = codecs.open("trans_word.csv", "r", "utf-8")
for line in f:
    line = line.rstrip()
    temp = line.split()
    data.append(temp)
f.close()

nb = NaiveBayes()
nb.train(data)

joblib.dump(nb, 'trained_nb.m')
