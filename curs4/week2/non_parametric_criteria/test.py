import numpy as np
import pandas as pd
import itertools

from scipy import stats
from statsmodels.stats.descriptivestats import sign_test
from statsmodels.stats.weightstats import zconfint


# Question 4
data = np.array([49, 58, 75, 110, 112, 132, 151, 276, 281, 362])
m0 = 200.0
print stats.wilcoxon(data - m0)

# Question 5
data1 = np.array([22, 22, 15, 13, 19, 19, 18, 20, 21, 13, 13, 15])
data2 = np.array([17, 18, 18, 15, 12, 4, 14, 15, 10])
print stats.mannwhitneyu(data1, data2)

# Question 6
data = pd.read_table('challenger.txt')


def get_bootstrap_samples(data, n_samples):
    indices = np.random.randint(0, len(data), (n_samples, len(data)))
    samples = data[indices]
    return samples


def stat_intervals(stat, alpha):
    boundaries = np.percentile(stat, [100 * alpha / 2., 100 * (1 - alpha / 2.)])
    return boundaries

np.random.seed(0)
temp0 = data[data.Incident == 0].Temperature.values
temp1 = data[data.Incident == 1].Temperature.values
temp1_mean_scores = map(np.mean, get_bootstrap_samples(temp1, 1000))
temp0_mean_scores = map(np.mean, get_bootstrap_samples(temp0, 1000))

delta_median_scores = map(lambda x: x[0] - x[1], zip(temp0_mean_scores, temp1_mean_scores))
print "95% confidence interval for the difference between medians",  stat_intervals(delta_median_scores, 0.05)


# Question 7
np.random.seed(0)
data = pd.read_table('challenger.txt')
temp0 = data[data.Incident == 0].Temperature.values
temp1 = data[data.Incident == 1].Temperature.values


def permutation_t_stat_ind(sample1, sample2):
    return np.mean(sample1) - np.mean(sample2)


def get_random_combinations(n1, n2, max_combinations):
    index = range(n1 + n2)
    indices = set([tuple(index)])
    for i in range(max_combinations - 1):
        np.random.shuffle(index)
        indices.add(tuple(index))
    return [(index[:n1], index[n1:]) for index in indices]


def permutation_zero_dist_ind(sample1, sample2, max_combinations=None):
    joined_sample = np.hstack((sample1, sample2))
    n1 = len(sample1)
    n = len(joined_sample)

    if max_combinations:
        indices = get_random_combinations(n1, len(sample2), max_combinations)
    else:
        indices = [(list(index), filter(lambda i: i not in index, range(n))) \
                   for index in itertools.combinations(range(n), n1)]

    distr = [joined_sample[list(i[0])].mean() - joined_sample[list(i[1])].mean() \
             for i in indices]
    return distr


def permutation_test(sample, mean, max_permutations=None, alternative='two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized\n"
                         "should be 'two-sided', 'less' or 'greater'")

    t_stat = permutation_t_stat_ind(sample, mean)

    zero_distr = permutation_zero_dist_ind(sample, mean, max_permutations)

    if alternative == 'two-sided':
        return sum([1. if abs(x) >= abs(t_stat) else 0. for x in zero_distr]) / len(zero_distr)

    if alternative == 'less':
        return sum([1. if x <= t_stat else 0. for x in zero_distr]) / len(zero_distr)

    if alternative == 'greater':
        return sum([1. if x >= t_stat else 0. for x in zero_distr]) / len(zero_distr)

print "p-value: %f" % permutation_test(temp0, temp1, max_permutations=10000)