from sklearn.externals import joblib
import traindata
import naivebayes as nb


nbclass = nb.NaiveBayes(100)
traindata.gunosy_category(nbclass)
joblib.dump(nb, 'trained_nb.m')
