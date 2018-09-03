import numpy as np
import pandas as pd
import sklearn as sk
from math import exp

from sklearn.metrics import roc_auc_score

data = pd.read_csv('data-logistic.csv', index_col=None, header=None)

X1 = data[1].values
X2 = data[2].values
y  = data[0].values

C = 0.0
k = 0.1
epsilon = 1e-5

def sigmoid(y_i, x1, x2 ,w1, w2):
    return 1.0 / (1 + exp(-y_i*(w1*x1 + w2*x2)))

def sigmoid_model(x1, x2, w1, w2):
    return 1.0 / (1 + exp(-w1*x1 - w2*x2))

def step_w1(w1, w2, X1, X2, y, k, C):
    l = len(X1)
    summa = 0
    for i, x1 in enumerate(X1):
        summa = summa + (y[i]*X1[i]) * (1 - sigmoid(y[i], X1[i], X2[i], w1, w2))
    result = w1 + k * (1.0/l) * summa - k*C*w1

    return result

def step_w2(w1, w2, X1, X2, y, k, C):
    l = len(X1)
    summa = 0
    for i, x1 in enumerate(X1):
        summa = summa + (y[i]*X2[i]) * (1 - sigmoid(y[i], X1[i], X2[i], w1, w2))
    result = w2 + k * (1.0/l) * summa - k*C*w2

    return result



w1 = w2 = 0

while True:
    w1_new = step_w1(w1, w2, X1, X2, y, k, C)
    w2_new = step_w2(w1, w2, X1, X2, y, k, C)

    w_old = np.array([w1, w2])
    w_new = np.array([w1_new, w2_new])

    dist = np.linalg.norm(w_new - w_old)
    if abs(dist) < epsilon:
        break

    w1 = w1_new
    w2 = w2_new

answers = []
for i, x1 in enumerate(X1):
    answers.append(sigmoid_model(X1[i], X2[i], w1, w2))

print(roc_auc_score(y, answers))