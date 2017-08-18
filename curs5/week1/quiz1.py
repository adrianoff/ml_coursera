import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np

milk = pd.read_csv('monthly-milk-production.csv',';', index_col=['month'], parse_dates=['month'], dayfirst=True)
print milk.head()

plot = milk.plot(figsize=(12,6))
plot.get_figure().savefig("output.png")

import statsmodels.api as sm
rezult = sm.tsa.stattools.adfuller(milk['milk'])
print rezult

milk['adjmilk'] = milk.milk / milk.index.days_in_month
print sum(milk.adjmilk)