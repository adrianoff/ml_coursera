from __future__ import division, print_function
import warnings
warnings.filterwarnings('ignore')
from glob import glob
import os
import pickle
#pip install tqdm
from tqdm import tqdm_notebook
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import glob, re, ntpath

PATH_TO_DATA = ('../capstone_user_identification/')


def prepare_train_set(path_to_csv_files, session_length=10):
    files = glob.glob(path_to_csv_files + 'user*.csv')
    sites = pd.DataFrame()
    for file in files:
        sites = pd.concat([sites, pd.read_csv(file)])

    sites['count'] = 0
    sites_count = sites.groupby('site')['count'].agg('count')

    sites = pd.DataFrame(columns=['site', 'total_visits'])
    sites['site'] = sites_count.index
    sites['total_visits'] = sites_count.values
    sites.sort_values(['total_visits'], inplace=True, ascending=False)
    sites = sites.reset_index(drop=True)
    sites.index = sites.index + 1

    columns = sites.site.values
    columns = np.append(columns, 'user_id')
    train_data = pd.DataFrame(columns=columns)

    for file in files:
        df = pd.read_csv(file)
        user_id = int(re.findall(r'\d+', ntpath.basename(file))[0])

        k = 0
        s = 1
        cur_index = len(train_data.index) - 1
        for site in df.site.values:
            new_index = cur_index + k

            if new_index not in train_data.index:
                train_data.loc[new_index] = 0
                train_data.loc[new_index]['user_id'] = user_id

            train_data.loc[new_index][site] = train_data.loc[new_index][site] + 1
            s = s + 1
            if s > session_length:
                k = k + 1
                s = 1

    return train_data


train_data = prepare_train_set(os.path.join(PATH_TO_DATA, '3users/'), session_length=10)
train_data

#prepare_train_set(os.path.join(PATH_TO_DATA, '3users/'), session_length=10)