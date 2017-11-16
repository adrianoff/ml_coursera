# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import sys

reload(sys)
sys.setdefaultencoding('utf8')



data = pd.read_csv('./data/data.csv')
del data['Unnamed: 0']
data['label'] = data.grade.apply(lambda x: 0 if x < 4 else 1)
corpus = data[['text', 'label']]


vectorizer = TfidfVectorizer(
    #ngram_range=(1, 3), max_df=1.0, analyzer='word', use_idf=True,
    #norm='l2'
)

vectorizer = CountVectorizer()

#print corpus['text'].values.astype('U')[:100]
#exit()

corpus = corpus['text']
# print corpus.shape
# print corpus[3]
# exit()

X_vect = vectorizer.fit_transform(corpus.values.astype('U'))
freqs = [(word, X_vect.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
#sort from largest to smallest
words = sorted(freqs, key = lambda x: -x[1])

for word in words[:50]:
     print word[0].decode()

# feature_array = np.array(vectorizer.get_feature_names())
# tfidf_sorting = np.argsort(X_vect.toarray()).flatten()[::-1]
# n = 10
# top_n = feature_array[tfidf_sorting][:n]
#
# for word in top_n:
#     print word.decode()