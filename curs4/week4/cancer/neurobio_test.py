import pandas as pd
from scipy.stats import ttest_ind
import statsmodels as sc
import statsmodels.stats.multitest as smm
import numpy as np




data = pd.read_csv('gene_high_throughput_sequencing.csv', header = 0)
diagnos = data['Diagnosis']
gene = data.drop(['Diagnosis', 'Patient_id'], axis = 1)
normal = gene[data['Diagnosis'] == 'normal']
early_neoplasia = gene[data['Diagnosis'] == 'early neoplasia']
cancer = gene[data['Diagnosis'] == 'cancer']
p_value1 = ttest_ind(normal, early_neoplasia, equal_var = False)
p_value2 = ttest_ind(early_neoplasia, cancer, equal_var = False)
reject1, p_corrected1, alpha1_1, alpha2_1 = smm.multipletests(p_value1.pvalue, alpha = 0.025, method = 'holm')
reject2, p_corrected2, alpha1_2, alpha2_2 = smm.multipletests(p_value2.pvalue, alpha = 0.025, method = 'holm')
f_c1 = []
f_c2 = []
def fold_change(f_c, control, treatment):
    for i in gene.columns:
        if np.mean(control[i]) < np.mean(treatment[i]):
            f_c.append(np.mean(treatment[i]) / np.mean(control[i]))
        if np.mean(control[i]) > np.mean(treatment[i]):
            f_c.append(-np.mean(control[i]) / np.mean(treatment[i]))
fold_change(f_c1, normal, early_neoplasia)
fold_change(f_c2, early_neoplasia, cancer)
answ1 = 0
for k in range(len(p_corrected1)):
    if abs(f_c1[k]) > 1.5 and p_corrected1[k] < 0.025 and reject1[k] == True:
        answ1 += 1

print answ1