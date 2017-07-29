import numpy as np
import pandas as pd
import scipy
from sklearn import metrics
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression



df = pd.read_table('banknotes.txt')
x_train, x_test, train_labels, test_labels = train_test_split(df.drop('real', axis=1), df['real'], random_state=1, test_size=50)


lgr1 = LogisticRegression()
lgr1.fit(x_train.drop(['X4', 'X5', 'X6'], axis=1), train_labels)
predict1 = lgr1.predict(x_test.drop(['X4', 'X5', 'X6'], axis=1))

lgr2 = LogisticRegression()
lgr2.fit(x_train.drop(['X1', 'X2', 'X3'], axis=1), train_labels)
predict2 = lgr2.predict(x_test.drop(['X1', 'X2', 'X3'], axis=1))

print metrics.accuracy_score(test_labels, predict1)
print metrics.accuracy_score(test_labels, predict2)

def proportions_diff_z_test(z_stat, alternative='two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized\n"
                         "should be 'two-sided', 'less' or 'greater'")
    if alternative == 'two-sided':
        return 2 * (1 - scipy.stats.norm.cdf(np.abs(z_stat)))
    if alternative == 'less':
        return scipy.stats.norm.cdf(z_stat)
    if alternative == 'greater':
        return 1 - scipy.stats.norm.cdf(z_stat)


def proportions_diff_z_stat_rel(sample1, sample2):
    sample = zip(sample1, sample2)
    n = len(sample)

    f = sum([1 if (x[0] == 1 and x[1] == 0) else 0 for x in sample])
    g = sum([1 if (x[0] == 0 and x[1] == 1) else 0 for x in sample])

    return float(f - g) / np.sqrt(f + g - float((f - g) ** 2) / n)


def proportions_diff_confint_rel(sample1, sample2, alpha=0.05):
    z = scipy.stats.norm.ppf(1 - alpha / 2.)
    sample = zip(sample1, sample2)
    n = len(sample)

    f = sum([1 if (x[0] == 1 and x[1] == 0) else 0 for x in sample])
    g = sum([1 if (x[0] == 0 and x[1] == 1) else 0 for x in sample])

    left_boundary = float(f - g) / n - z * np.sqrt(float((f + g)) / n ** 2 - float((f - g) ** 2) / n ** 3)
    right_boundary = float(f - g) / n + z * np.sqrt(float((f + g)) / n ** 2 - float((f - g) ** 2) / n ** 3)
    return (left_boundary, right_boundary)


print proportions_diff_z_test(proportions_diff_z_stat_rel(test_labels != predict1, test_labels != predict2))
print proportions_diff_confint_rel(test_labels != predict1, test_labels != predict2)
