from scipy import stats
import pandas as pd
import numpy as np

print stats.binom_test(67, 100, 0.75)

df = pd.read_table('pines.txt')
print df.describe()

tree_cnt = stats.binned_statistic_2d(df['sn'], df['we'], np.ones(df.shape[0]), statistic='count', bins=5)
observed_freq = np.reshape(tree_cnt.statistic, (25, 1))
print sum(observed_freq)

print stats.chisquare(observed_freq)
