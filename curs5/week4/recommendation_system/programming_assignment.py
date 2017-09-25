from collections import Counter
import pandas as pd

view_popularity = Counter()
purchase_popularity = Counter()

#data = pd.DataFrame(columns=['views', 'purchase'])

# with open('./coursera_sessions_train.txt', 'r') as f:
#     for line in f.readlines():
#         views, purchases = line.strip().split(';')
#         for view in views.split(','):
#             if view in data.index:
#                 data.loc[view]['views'] = data.loc[view]['views'] + 1
#             else:
#                 data.loc[view] = [1, 0]
#
#             print data.count()['views']


view_popularity = Counter()
purchase_popularity = Counter()


with open('./coursera_sessions_train.txt', 'r') as f:
    for line in f.xreadlines():
        visits, purchases = line.strip().split(';')
        for visit in visits.split(','):
            view_popularity[visit] += 1
        for purchase in purchases.split(','):
            if purchase != '':
                purchase_popularity[purchase] += 1

data_views = pd.DataFrame.from_dict(view_popularity, orient='index')
data_views.columns = ['views']
data_views.views = data_views.views.astype(int)
data_purchase = pd.DataFrame.from_dict(purchase_popularity, orient='index')
data_purchase.columns = ['purchase']
data_purchase.purchase = data_purchase.purchase.astype(int)

data = pd.concat([data_views, data_purchase], axis=1)
data.purchase.fillna(0, inplace=True)
data.views.fillna(0, inplace=True)
data.views = data.views.astype(int)
data.purchase = data.purchase.astype(int)
print data.sort_values(by='views', axis=0, ascending=False).head()
