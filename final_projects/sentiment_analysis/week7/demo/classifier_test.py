# -*- coding: utf-8 -*-
__author__ = 'adrianoff'


from sentiment_classifier import SentimentClassifier

clf = SentimentClassifier()

pred = clf.get_prediction_message("Это отличный смартфон, просто чудесный")

print pred