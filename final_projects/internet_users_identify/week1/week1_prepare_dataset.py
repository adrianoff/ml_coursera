from __future__ import division, print_function
import warnings
warnings.filterwarnings('ignore')
from glob import glob
import os
import pickle
#pip install tqdm

from tqdm import tqdm

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import glob, re, ntpath
import sys

PATH_TO_DATA = ('../capstone_user_identification/')


def prepare_train_set2(path_to_csv_files, session_length=10):
    site_dict = {}
    site_id = 1
    user_id = 1
    sessions = []
    i = 0  # session row initialization

    for file in tqdm(glob.glob(path_to_csv_files + '/*.csv')):
        sessions.append([0] * session_length + [user_id])
        df = pd.read_csv(file, usecols=[1], squeeze=True)
        j = 0  # session column initialization

        for k, site in enumerate(df):
            # Fill site dictionary
            if site in site_dict:
                site_dict[site] = (site_dict[site][0], site_dict[site][1] + 1)
            else:
                site_dict[site] = (site_id, 1)
                site_id += 1

            # Fill sessions list
            sessions[i][j] = site_dict[site][0]
            j += 1
            if k == (len(df) - 1):
                i += 1
                j = 0
                user_id += 1
                continue
            if (j // session_length) == 1:
                sessions.append([0] * session_length + [user_id])
                i += 1
                j = 0

    # Convert sessions list to dataframe
    columns = ['site1', 'site2', 'site3', 'site4', 'site5',
               'site6', 'site7', 'site8', 'site9', 'site10', 'user_id']
    sessions_df = pd.DataFrame(np.array(sessions), columns=columns)

    return sessions_df, site_dict

def prepare_train_set(path_to_csv_files, session_length=10):
    files = glob.glob(path_to_csv_files + 'user*.csv')
    sites = pd.DataFrame()
    for session_file in files:
        sites = pd.concat([sites, pd.read_csv(session_file)])

    sites['count'] = 0
    sites_count = sites.groupby('site')['count'].agg('count')

    sites = pd.DataFrame(columns=['site_id', 'total_visits'])
    sites['total_visits'] = sites_count.values
    sites.index = sites_count.index
    sites.sort_values(['total_visits'], inplace=True, ascending=False, kind='heapsort')
    sites['site_id'] = [j for j in range(1, len(sites.index)+1)]

    columns = ['site' + str(i) for i in range(1, session_length + 1)]
    columns.append('user_id')

    train_data = pd.DataFrame(columns=columns, dtype='int')
    train_data_arr = {}
    train_data_arr_keys = []

    sites_list = sites.to_dict()

    l = 0
    for session_file in files:
        l += 1

        sys.stdout.write(session_file + " " + str(l) + "\n")
        sys.stdout.flush()

        df = pd.read_csv(session_file)
        user_id = int(re.findall(r"\d+", ntpath.basename(session_file))[0])

        k = 0
        s = 1
        cur_index = len(train_data_arr)

        for site in df.site.values:
            new_index = cur_index + k

            if new_index not in train_data_arr_keys:
                train_data_arr_keys.append(new_index)

                train_data_arr[new_index] = 0
                train_data_arr[new_index]['user_id'] = user_id

            train_data_arr[new_index]['site' + str(s)] = sites_list['site_id'][site]

            s += 1
            if s > session_length:
                k += 1
                s = 1

    train_data = train_data.from_dict(train_data_arr, dtype=int)
    # train_data.fillna(0, inplace=True)
    # train_data = train_data.transpose()
    # train_data = train_data[columns]
    # train_data = train_data.astype(np.int)

    return train_data, sites

train_data, site_freq_users = prepare_train_set2(os.path.join(PATH_TO_DATA, '150users/'), session_length=10)

print (train_data.shape)
#print (site_freq_users.shape)

#prepare_train_set(os.path.join(PATH_TO_DATA, '3users/'), session_length=10)
