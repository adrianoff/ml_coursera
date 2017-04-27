from sklearn import datasets, tree
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import BaggingClassifier

from sklearn.ensemble import RandomForestClassifier

digits = datasets.load_digits()

X = digits['data']
y = digits['target']

clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, X, y, cv=10)
print scores.mean()

clf_Bagging = BaggingClassifier(clf, n_estimators=100)
scores = cross_val_score(clf_Bagging, X, y, cv=10)
print scores.mean()

clf_Bagging_d = BaggingClassifier(clf, n_estimators=100, max_features=8)
scores = cross_val_score(clf_Bagging_d, X, y, cv=10)
print scores.mean()

clf = tree.DecisionTreeClassifier(max_features=8)
clf_Bagging_d2 = BaggingClassifier(clf, n_estimators=100)
scores = cross_val_score(clf_Bagging_d2, X, y, cv=10)
print scores.mean()

clf_rfc = RandomForestClassifier(n_estimators=10, max_features=8)
scores = cross_val_score(clf_rfc, X, y, cv=10)
print scores.mean()
