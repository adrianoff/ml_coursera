from __future__ import division, print_function

import numpy as np
import pandas as pd

from glob import glob
import os
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

PATH_TO_DATA = "../capstone_user_identification/"


def prepare_train_set2(path_to_csv_files, session_length=10):
    site_dict = {}
    site_id = 1
    user_id = 1
    sessions = []
    i = 0  # session row initialization

    for session_file in tqdm(glob(path_to_csv_files + '/*.csv')):
        sessions.append([0] * session_length + [user_id])
        df = pd.read_csv(session_file, usecols=[1], squeeze=True)
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

#train_data, site_freq_users = prepare_train_set2(os.path.join(PATH_TO_DATA, '150users/'), session_length=10)
#print (train_data.shape)
#print (len(site_freq_users))

train_data_toy, site_freq_users_toy = prepare_train_set2(os.path.join(PATH_TO_DATA, '3users/'), session_length=10)
X_toy, y_toy = train_data_toy.iloc[:, :-1], train_data_toy.iloc[:, -1]
X_toy_matrix = X_toy.as_matrix()

print (X_toy)
print (y_toy)


def matrix_to_sparse_matrix(matrix):
    from scipy.sparse import csr_matrix

    matrix_shape = matrix.shape
    NMZ = np.prod(np.array(matrix_shape))
    data = np.array([1] * NMZ)
    indptr = np.arange(0, NMZ + matrix.shape[1], matrix.shape[1])
    return csr_matrix((data, matrix.reshape(-1), indptr), dtype=int)[:, 1:]

X_sparse_toy = matrix_to_sparse_matrix(X_toy_matrix)
print (X_sparse_toy.todense())
pass