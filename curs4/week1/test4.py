from scipy import stats
print stats.binom_test(67, 100, 0.75)

import pandas as pd
df = pd.read_table('pines.txt')
print df.describe()

step = 40
cluster_coords = []
for sn in range(0, 200, step):
    for we in range(0, 200, step):
        cluster_coords.append([sn, we])

print cluster_coords

pines = []
first = True
for cluster in cluster_coords:
    if first:
        new_pines_cluster = df[
            (df.sn >= cluster[0]) &
            (df.we >= cluster[1]) &
            (df.sn < cluster[0]+step) &
            (df.we < cluster[1]+step)
        ]
    else:
        new_pines_cluster = df[
            (df.sn > cluster[0]) &
            (df.we > cluster[1]) &
            (df.sn <= cluster[0]+step) &
            (df.we <= cluster[1]+step)
        ]
    pines.append(len(new_pines_cluster))
    first = False

print sum(pines)
