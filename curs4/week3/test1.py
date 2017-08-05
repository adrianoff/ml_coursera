import pandas as pd
import numpy as np

df = pd.read_table('illiteracy.txt')
print df.corr()
print df.corr(method='spearman')