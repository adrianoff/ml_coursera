import pandas as pd
import numpy as np
from sklearn.cluster import MeanShift

# old = open('checkins.dat', 'r+')
# new = open('checkins.csv', 'w')
#
# for idx, line in enumerate(old):
#     if idx == 1:
#         continue
#
#     values = line.split('|')
#
#     ignore_this_line = False
#     new_line_list = []
#     for item in values:
#         trimmed_values = item.strip()
#         if trimmed_values == '':
#             ignore_this_line = True
#             break
#         new_line_list.append(trimmed_values)
#
#     if ignore_this_line == False:
#         try:
#             new_line_list[5] = new_line_list[5].replace(' ', 'T')
#         except Exception:
#             continue
#         new.write(','.join([str(i) for i in new_line_list]) + "\n")
#
# old.close()
# new.close()

data = pd.read_csv('checkins.csv')
data = data[:100000]

X = data[['latitude', 'longitude']]

ms = MeanShift(bandwidth=0.1)
y = ms.fit_predict(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

#print("number of estimated clusters : %d" % n_clusters_)
large_clusters = set()
clusters_centers = []
i = 0
for label in np.unique(y):
    if (np.sum(y == label) > 15):
        large_clusters.add(label)
        clusters_centers.append(X[y == label].mean(axis=0))
        i += 1

clusters_centers = np.array(clusters_centers)
print len(clusters_centers)
print i

for center in clusters_centers:
    print center[0], ',', center[1]
