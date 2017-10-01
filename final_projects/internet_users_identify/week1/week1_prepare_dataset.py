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
import glob

PATH_TO_DATA = ('../capstone_user_identification/')


def prepare_train_set(path_to_csv_files, session_length=10):
    files = glob.glob(path_to_csv_files + 'user*.csv')
    sites = pd.DataFrame()
    for file in files:
        sites = pd.concat([sites, pd.read_csv(file)])

    print(sites.groupby('site').head(100))

prepare_train_set(os.path.join(PATH_TO_DATA, '3users/'), session_length=10)