# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression




train_all = pd.read_csv("./data/train.csv")
train_all['description'] = train_all['description'].fillna("")
train_all['title'] = train_all['title'].fillna("")


train_all['deal_class'] = train_all['deal_probability'].apply(lambda x: "1" if x >=0.5 else "0")
train_all['text'] = train_all['title'] + " " + train_all['description']
data = train_all[['text', 'deal_class']]




cv = StratifiedKFold(data.deal_class, n_folds=3, shuffle=True, random_state=1)

pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer='word')),
    ('classifier', LogisticRegression())
])

pipeline_params = {
    'classifier__penalty': ['l2'],
    'vectorizer__ngram_range': [(1, 3)]
}

grid = GridSearchCV(pipeline, pipeline_params, cv=cv, refit=True, verbose=100, n_jobs=4)

grid.fit(data.text.values, data.deal_class)
best = grid.best_estimator_
print(
    "Accuracy (TfidfVectorizer + LogisticRegression): {}, params {}" . format(grid.best_score_, grid.best_params_)
)
print (grid.best_score_)