import pandas as pd
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as smm

df = pd.read_csv('gene_high_throughput_sequencing.csv')

df_normal = df[df['Diagnosis'] == 'normal']
df_neoplasia = df[df['Diagnosis'] == 'early neoplasia']
df_cancer = df[df['Diagnosis'] == 'cancer']


def Fct(c, t):
    if t > c:
        r = t/c
    else:
        r = -c/t
    return r

ttest_ind_neoplasia_cancer = []
for column in df_neoplasia.iloc[:, 2:].columns.values:
    ttest_ind_neoplasia_cancer.append(ttest_ind(df_neoplasia[column], df_cancer[column], equal_var=False))

pvalues_neoplasia_cancer = [test.pvalue for test in ttest_ind_neoplasia_cancer]
print len(pvalues_neoplasia_cancer)

reject, p_corrected, _, _ = smm.multipletests(pvalues_neoplasia_cancer, alpha=0.025, method='fdr_bh')
df_temp = pd.DataFrame()
df_temp['reject'] = reject
df_temp['p_corrected'] = p_corrected
df_temp['p_values'] = pvalues_neoplasia_cancer

print df_temp.reject.value_counts()

df_temp_2 = pd.DataFrame()
df_temp_2['p_corrected'] = df_temp[(df_temp.p_corrected < 0.025) & (df_temp.reject == True)]['p_corrected']
df_temp_2['p_values'] = df_temp[(df_temp.p_corrected < 0.025) & (df_temp.reject == True)]['p_values']


fct1 = []
for index, row in df_temp_2.iterrows():
    fct1.append(Fct(row['p_values'], row['p_corrected']))

c1 = 0
for item in fct1:
    if abs(item) > 1.5:
        c1 = c1 + 1

print c1