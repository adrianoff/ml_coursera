import pandas as pd
import math
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms


df = pd.read_table('botswana.tsv')
#print df.head()
#print df.describe()
#print df.religion.value_counts()

#print df.dropna().describe()
#print df.agefm.value_counts()
#df.fillna(value=nan, inplace=True)

df['nevermarr'] = df['agefm'].apply(lambda x : 1 if math.isnan(x) else 0)
del df['evermarr']
df.agefm.fillna(value=0, inplace=True)

df.loc[df['nevermarr'] == 1, 'heduc'].fillna(value=-1, inplace=True)
print 'Question 3: ',  df.heduc.isnull().sum()

df['idlnchld_noans'] = df['idlnchld'].apply(lambda x : 1 if math.isnan(x) else 0)
df['heduc_noans'] = df['heduc'].apply(lambda x : 1 if math.isnan(x) else 0)
df['usemeth_noans'] = df['usemeth'].apply(lambda x : 1 if math.isnan(x) else 0)

df.idlnchld.fillna(value=-1, inplace=True)
df.heduc.fillna(value=-2, inplace=True)
df.usemeth.fillna(value=-1, inplace=True)

df.knowmeth.dropna()
df.electric.dropna()
df.tv.dropna()
df.radio.dropna()
df.bicycle.dropna()

str_regression = 'ceb ~ '
first = True
for column in df.columns:
    if column != 'ceb':
        plus = ' + '
        if first:
            plus = ''
        str_regression = str_regression + plus + column
        first = False

print str_regression

m1 = smf.ols(str_regression, data=df)
fitted = m1.fit()
#print fitted.summary()

#print 'Breusch-Pagan test: p=%f' % sms.het_breushpagan(fitted.resid, fitted.model.exog)[1]


str_regression = 'ceb ~ '
#df.drop('religion', axis=1, inplace=True)
#df.drop('radio', axis=1, inplace=True)
#df.drop('tv', axis=1, inplace=True)
first = True
for column in df.columns:
    if column in ['religion', 'radio', 'tv']:
        continue
    if column != 'ceb':
        plus = ' + '
        if first:
            plus = ''
        str_regression = str_regression + plus + column
        first = False

m2 = smf.ols(str_regression, data=df)
fitted2 = m2.fit(cov_type='HC1')
#print fitted2.summary()

print "F=%f, p=%f, k1=%f" % m1.fit().compare_f_test(m2.fit())

df.drop('usemeth_noans', axis=1, inplace=True)
df.drop('usemeth', axis=1, inplace=True)
str_regression = 'ceb ~ '
first = True
for column in df.columns:
    if column in ['religion', 'radio', 'tv']:
        continue
    if column in ['usemeth_noans', 'usemeth']:
        continue
    if column != 'ceb':
        plus = ' + '
        if first:
            plus = ''
        str_regression = str_regression + plus + column
        first = False

m3 = smf.ols(str_regression, data=df)
fitted3 = m3.fit(cov_type='HC1')
#fitted3 = m3.fit()
#print 'Breusch-Pagan test: p=%f' % sms.het_breushpagan(fitted3.resid, fitted3.model.exog)[1]


#print m1.fit().compare_f_test(m3.fit())
print fitted3.summary()