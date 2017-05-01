import numpy as np
from sklearn import metrics
from sklearn.datasets import load_boston
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
import math


def gbm_predict(X):
    return [sum([coeff * algo.predict([x])[0]
                 for algo, coeff in zip(base_algorithms_list, coefficients_list)]) for x in X]

# def gbm_predict(X):
#     ziped = zip(base_algorithms_list, coefficients_list)
#
#     summa = np.array([])
#     for x in X:
#         for algo, coeff in ziped:
#             algo_predict = algo.predict([x])[0]
#             new_item = coeff * algo_predict
#             summa = np.append(summa, new_item)
#
#     return summa


def l_derivative(p, z):
    return p - z


boston = load_boston()
n = len(boston.data)
X = boston.data
y = boston.target
X_train = np.array(X[:int(0.75*n)])
X_test = np.array(X[int(0.75*n):])
y_train = np.array(y[:int(0.75*n)])
y_test = np.array(y[int(0.75*n):])

# print X_test.shape
# print y_test.shape
# print X_train.shape
# print y_train.shape
#
# max_depth = 5
# random_state = 42
# const_coef = 0.9
#
# base_algorithms_list = list()
# coefficients_list = list()
# y_current = np.array(y_train)
#
# for i in range(50):
#     clf = DecisionTreeRegressor(max_depth=5, random_state=42)
#     clf.fit(X_train, y_current)
#     base_algorithms_list.append(clf)
#     coefficients_list.append(0.9)
#     y_current = y_train - gbm_predict(X_train)
#
# print math.sqrt(mean_squared_error(y_test, gbm_predict(X_test)))
#
#
# base_algorithms_list = list()
# coefficients_list = list()
# y_current = np.array(y_train)
#
# for i in range(50):
#     clf = DecisionTreeRegressor(max_depth=5, random_state=42)
#     clf.fit(X_train, y_current)
#     base_algorithms_list.append(clf)
#     coefficients_list.append(0.9 / (1.0 + i))
#     y_current = y_train - gbm_predict(X_train)
#
# print np.sqrt(metrics.mean_squared_error(y_test, gbm_predict(X_test)))


gb_metrics = np.array([])
for i in range(100, 10000, 200):
    clf = GradientBoostingRegressor(n_estimators=i, max_depth=3)
    clf.fit(X_train, y_train)

    gb_metrics = np.append(gb_metrics, np.sqrt(metrics.mean_squared_error(y_test, clf.predict(X_test))))

