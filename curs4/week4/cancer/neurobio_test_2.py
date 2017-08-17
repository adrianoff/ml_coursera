import pandas as pd
import scipy
import numpy as np
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

df = pd.read_csv('gene_high_throughput_sequencing.csv')

group_normal = df[df['Diagnosis'] == 'normal']
group_early_neoplasia = df[df['Diagnosis'] == 'early neoplasia']
group_cancer = df[df['Diagnosis'] == 'cancer']

del group_normal['Patient_id']
del group_normal['Diagnosis']
del group_early_neoplasia['Patient_id']
del group_early_neoplasia['Diagnosis']
del group_cancer['Patient_id']
del group_cancer['Diagnosis']

p1=[]
for i in range(len(group_normal.columns)):
    p1.append(ttest_ind(group_normal[group_normal.columns[i]], group_early_neoplasia[group_early_neoplasia.columns[i]], equal_var = False)[1])


p2=[]
for i in range(len(group_early_neoplasia.columns)):
    p2.append(ttest_ind(group_early_neoplasia[group_early_neoplasia.columns[i]], group_cancer[group_cancer.columns[i]], equal_var = False)[1])

reject1, p_corrected1, a1, a2 = multipletests(p1, alpha=0.025, method='holm')
reject2, p_corrected2, a3, a4 = multipletests(p2, alpha=0.025, method='holm')

q = np.where(np.array(reject1) == True)
print len(q[0])
z = np.where(np.array(reject2) == True)
print len(z[0])



norneo_fc = []
for i in q[0]:
    C = np.mean(group_normal.iloc[:,i])
    T = np.mean(group_early_neoplasia.iloc[:,i])
    if T > C:
        norneo_fc.append(T / C)
    else:
        norneo_fc.append(C / T)

neocan_fc = []
for i in z[0]:
    C = np.mean(group_early_neoplasia.iloc[:,i])
    T = np.mean(group_cancer.iloc[:,i])
    if T > C:
        neocan_fc.append(T / C)
    else:
        neocan_fc.append(C / T)


answer3 = np.where(np.array(norneo_fc) > 1.5)
print len(answer3[0])
answer4 = np.where(np.array(neocan_fc) > 1.5)
print len(answer4[0])


def write_answer_3(num):
  with open("genes3.txt", "w") as f:
    f.write(str(num))
write_answer_3(len(answer3[0]))

def write_answer_4(num):
  with open("genes4.txt", "w") as f:
    f.write(str(num))
write_answer_4(len(answer4[0]))


reject3, p_corrected3, a5, a6 = multipletests(p1,
                                            alpha = 0.025,
                                            method = 'fdr_bh')
reject4, p_corrected4, a7, a8 = multipletests(p2,
                                            alpha = 0.025,
                                            method = 'fdr_bh')


x = np.where(np.array(reject3) == True)
print len(x[0])
y = np.where(np.array(reject4) == True)
print len(y[0])



norneo_fc1 = []
for i in x[0]:
    C = np.mean(group_normal.iloc[:,i])
    T = np.mean(group_early_neoplasia.iloc[:,i])
    if T > C:
        norneo_fc1.append(T / C)
    else:
        norneo_fc1.append(C / T)

neocan_fc1 = []
for i in y[0]:
    C = np.mean(group_early_neoplasia.iloc[:,i])
    T = np.mean(group_cancer.iloc[:,i])
    if T > C:
        neocan_fc1.append(T / C)
    else:
        neocan_fc1.append(C / T)

answer5 = np.where(np.array(norneo_fc1) > 1.5)
print len(answer5[0])
answer6 = np.where(np.array(neocan_fc1) > 1.5)
print len(answer6[0])


def write_answer_5(num):
  with open("genes5.txt", "w") as f:
    f.write(str(num))
write_answer_5(len(answer5[0]))

def write_answer_6(num):
  with open("genes6.txt", "w") as f:
    f.write(str(num))
write_answer_6(len(answer6[0]))