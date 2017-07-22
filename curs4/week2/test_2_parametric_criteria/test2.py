import numpy as np
import pandas as pd

import scipy
from statsmodels.stats.weightstats import *
from statsmodels.stats.proportion import proportion_confint
from sklearn.model_selection import train_test_split
from decimal import Decimal
from sklearn.linear_model import LogisticRegression

alpha = 0.05
z = scipy.stats.norm.ppf(1 - alpha / 2.)

p1 = float(10.0 / 34)
p2 = float(4.0 / 16)

left_boundary = (p1 - p2) - z * np.sqrt(p1 * (1 - p1) / 34 + p2 * (1 - p2) / 16)
right_boundary = (p1 - p2) + z * np.sqrt(p1 * (1 - p1) / 34 + p2 * (1 - p2) / 16)

#print left_boundary
#print right_boundary

n1 = 34
n2 = 16

p1 = float(10) / n1
p2 = float(4) / n2
P = float(p1 * n1 + p2 * n2) / (n1 + n2)

z_stat = (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))
p_value = 1 - scipy.stats.norm.cdf(z_stat)
#print round(p_value, 4)


df = pd.read_table('banknotes.txt')
#print df.describe()

X_train, X_test, y_train, y_test = train_test_split(df.drop('real', axis=1), df['real'], random_state=1)
#print y_train
#print type(X_train)
#print len(X_train)
#print len(X_test)

lr1 = LogisticRegression()
lr1.fit(X_train.drop(['X4', 'X5', 'X6'], axis=1), y_train)
predicts_lr1 = lr1.predict(X_test.drop(['X4', 'X5', 'X6'], axis=1))

lr2 = LogisticRegression()
lr2.fit(X_train.drop(['X1', 'X2', 'X3'], axis=1), y_train)
predicts_lr2 = lr1.predict(X_test.drop(['X1', 'X2', 'X3'], axis=1))

predicts_lr1_answers = predicts_lr1 != y_test
predicts_lr2_answers = predicts_lr2 != y_test

#print sum(predicts_lr1_answers == True)
#print sum(predicts_lr2_answers == True)

sample = zip(predicts_lr1_answers, predicts_lr2_answers)
n = len(sample)

f = sum([1 if (x[0] == 1 and x[1] == 0) else 0 for x in sample])
g = sum([1 if (x[0] == 0 and x[1] == 1) else 0 for x in sample])
z_stat = float(f - g) / np.sqrt(f + g - float((f - g) ** 2) / n)
p_value = 1 - scipy.stats.norm.cdf(z_stat)
#print p_value

def proportions_diff_confint_rel(sample1, sample2, alpha=0.05):
    z = scipy.stats.norm.ppf(1 - alpha / 2.)
    sample = zip(sample1, sample2)
    n = len(sample)

    f = sum([1 if (x[0] == 1 and x[1] == 0) else 0 for x in sample])
    g = sum([1 if (x[0] == 0 and x[1] == 1) else 0 for x in sample])

    left_boundary = float(f - g) / n - z * np.sqrt(float((f + g)) / n ** 2 - float((f - g) ** 2) / n ** 3)
    right_boundary = float(f - g) / n + z * np.sqrt(float((f + g)) / n ** 2 - float((f - g) ** 2) / n ** 3)
    return (left_boundary, right_boundary)

boundaries = proportions_diff_confint_rel(predicts_lr1_answers, predicts_lr2_answers)
#print round(boundaries[0], 4)


z = float(541.4 - 525) / (100 / np.sqrt(100))
p_value = 1 - scipy.stats.norm.cdf(z)
#print round(p_value, 4)



z = float(541.5 - 525) / (100 / np.sqrt(100))
p_value = 1 - scipy.stats.norm.cdf(z)
#print round(p_value, 4)







n1 = len(predicts_lr1_answers)
n2 = len(predicts_lr2_answers)

p1 = float(sum(predicts_lr1_answers)) / n1
p2 = float(sum(predicts_lr2_answers)) / n2
P = float(p1 * n1 + p2 * n2) / (n1 + n2)

z_stat = (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))
#print z_stat
p_value = scipy.stats.norm.cdf(z_stat)
#print p_value




z = scipy.stats.norm.ppf(1 - alpha / 2.)

p1 = float(sum(predicts_lr1_answers)) / len(predicts_lr1_answers)
p2 = float(sum(predicts_lr2_answers)) / len(predicts_lr2_answers)

left_boundary = (p1 - p2) - z * np.sqrt(p1 * (1 - p1) / len(predicts_lr1_answers) + p2 * (1 - p2) / len(predicts_lr2_answers))
right_boundary = (p1 - p2) + z * np.sqrt(p1 * (1 - p1) / len(predicts_lr1_answers) + p2 * (1 - p2) / len(predicts_lr2_answers))
print round(left_boundary, 4)
print round(right_boundary, 4)