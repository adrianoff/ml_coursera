import numpy as np
import pandas as pd
from math import sqrt
from statsmodels.stats.weightstats import _tconfint_generic

df = pd.read_table('water.txt')

print len(df['mortality'])

mean_mortality = df['mortality'].mean()
mortality_mean_std = df['mortality'].std(ddof=1)/sqrt(len(df['mortality']))
interval95 = _tconfint_generic(mean_mortality, mortality_mean_std, len(df['mortality']) - 1, 0.05, 'two-sided')
print "95%% confidence interval mortality ALL", round(interval95[0], 4), round(interval95[1], 4)


mean_mortality = df['mortality'][df.location == 'South'].mean()
mortality_mean_std = df['mortality'][df.location == 'South'].std(ddof=1)/sqrt(len(df['mortality'][df.location == 'South']))
interval95_South = _tconfint_generic(mean_mortality, mortality_mean_std, len(df['mortality'][df.location == 'South']) - 1, 0.05, 'two-sided')
print "95%% confidence interval mortality SOUTH", round(interval95_South[0], 4), round(interval95_South[1], 4)


mean_mortality = df['mortality'][df.location == 'North'].mean()
mortality_mean_std = df['mortality'][df.location == 'North'].std(ddof=1)/sqrt(len(df['mortality'][df.location == 'North']))
interval95_North = _tconfint_generic(mean_mortality, mortality_mean_std, len(df['mortality'][df.location == 'South']) - 1, 0.05, 'two-sided')
print "95%% confidence interval mortality NORTH", round(interval95_North[0], 4), round(interval95_North[1], 4)


mean_hardness = df['hardness'][df.location == 'South'].mean()
hardness_mean_std = df['hardness'][df.location == 'South'].std(ddof=1)/sqrt(len(df['hardness'][df.location == 'South']))
interval95_South_hardness = _tconfint_generic(mean_hardness, hardness_mean_std, len(df['hardness'][df.location == 'South']) - 1, 0.05, 'two-sided')
print "95%% confidence interval hardness SOUTH", round(interval95_South_hardness[0], 4), round(interval95_South_hardness[1], 4)


mean_hardness = df['hardness'][df.location == 'North'].mean()
hardness_mean_std = df['hardness'][df.location == 'North'].std(ddof=1)/sqrt(len(df['hardness'][df.location == 'North']))
interval95_North_hardness = _tconfint_generic(mean_hardness, hardness_mean_std, len(df['hardness'][df.location == 'South']) - 1, 0.05, 'two-sided')
print "95%% confidence interval hardness NORTH", round(interval95_North_hardness[0], 4), round(interval95_North_hardness[1], 4)

pass
