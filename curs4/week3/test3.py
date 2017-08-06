import pandas as pd
import numpy as np

from scipy.stats import wilcoxon
from statsmodels.sandbox.stats.multicomp import multipletests

df = pd.read_table('AUCs.txt')
df = df.drop(df.columns[[0]], axis=1)
p_values = []
for i, lhs_column in enumerate(df.columns):
    for j, rhs_column in enumerate(df.columns):
        if i >= j:
            continue

        _, p = wilcoxon(df[lhs_column], df[rhs_column])
        p_values.append(p)
        #print lhs_column, rhs_column, wilcoxon(df[lhs_column], df[rhs_column])

print multipletests(p_values, alpha=0.05, method='holm')
print multipletests(p_values, alpha=0.05, method='fdr_bh') 