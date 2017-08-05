import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.weightstats import *
from statsmodels.stats.proportion import proportion_confint

df = pd.read_table('water.txt')
print df.corr()
print df.corr(method='spearman')

print df[df.location == 'South'].corr()
print df[df.location == 'North'].corr()


table = [[203, 718], [239, 515]]
print stats.chi2_contingency(table)


alpha = 0.05
z = stats.norm.ppf(1 - alpha / 2.)

p1 = float(239) / (239+515)
p2 = float(203) / (203+718)

left_boundary = (p1 - p2) - z * np.sqrt(p1 * (1 - p1) / (239+515) + p2 * (1 - p2) / (203+718))
right_boundary = (p1 - p2) + z * np.sqrt(p1 * (1 - p1) / (239+515) + p2 * (1 - p2) / (203+718))

print (left_boundary, right_boundary)

n1 = (239+515)
n2 = (203+718)
p1 = float(239) / n1
p2 = float(203) / n2
P = float(p1 * n1 + p2 * n2) / (n1 + n2)

z_stat = (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))
print 2 * (1 - stats.norm.cdf(np.abs(z_stat)))


table = [[197, 111, 33], [382, 685, 331], [110, 342, 333]]
print '*:' , stats.chi2_contingency(table)

def vcramer(table):
    chi, p, _, _ = stats.chi2_contingency(table, correction=False)
    n = table.sum()
    r,c = table.shape
    return np.sqrt(chi/(n*(min(r,c)-1.))), p

#print vcramer(table)
chi, p, _, _ = stats.chi2_contingency(table)
n = sum([197, 111, 33]) + sum([382, 685, 331]) + sum([110, 342, 333])
cramer = np.sqrt(chi/(n*(min(3, 3)-1.)))
print cramer