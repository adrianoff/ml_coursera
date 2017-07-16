import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
from statsmodels.stats.weightstats import DescrStatsW

df = pd.read_table('diamonds.txt')
X_train, X_test, y_train, y_test = train_test_split(df.drop('price', axis=1), df['price'], random_state=1)

lr = LinearRegression()
lr.fit(X_train, y_train)

rf = RandomForestRegressor(random_state=1)
rf.fit(X_train, y_train)

predicts_lr = lr.predict(X_test)
predicts_rf = rf.predict(X_test)

mod_lr = np.abs(y_test - predicts_lr)
mod_rf = np.abs(y_test - predicts_rf)

print "n: ", len(mod_lr)

print "mod_lr: ", np.mean(mod_lr)
print "mod_rf: ", np.mean(mod_rf)

print stats.ttest_rel(mod_lr, mod_rf)
print "95%% confidence interval: [%f, %f]" % DescrStatsW(mod_lr-mod_rf).tconfint_mean()