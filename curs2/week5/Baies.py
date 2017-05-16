from sklearn.datasets import load_digits
from sklearn.datasets import load_breast_cancer
from sklearn.cross_validation import cross_val_score

from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB



digits = load_digits()
breast_cancer = load_breast_cancer()

estimator = BernoulliNB()
scores = cross_val_score(estimator, X=breast_cancer['data'], y=breast_cancer['target'])
print scores.mean()

estimator = MultinomialNB()
scores = cross_val_score(estimator, X=breast_cancer['data'], y=breast_cancer['target'])
print scores.mean()

estimator = GaussianNB()
scores = cross_val_score(estimator, X=breast_cancer['data'], y=breast_cancer['target'])
print scores.mean()



estimator = BernoulliNB()
scores = cross_val_score(estimator, X=digits['data'], y=digits['target'])
print scores.mean()

estimator = MultinomialNB()
scores = cross_val_score(estimator, X=digits['data'], y=digits['target'])
print scores.mean()

estimator = GaussianNB()
scores = cross_val_score(estimator, X=digits['data'], y=digits['target'])
print scores.mean()