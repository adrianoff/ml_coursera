__author__ = 'xead'
from sklearn.externals import joblib
import pymorphy2


class SentimentClassifier(object):
    def __init__(self):
        self.model = joblib.load("./model/classifier.pkl")
        self.vectorizer = joblib.load("./model/vectorizer.pkl")
        self.classes_dict = {0: "negative", 1: "positive", -1: "prediction error"}

    @staticmethod
    def get_probability_words(probability):
        if probability < 0.55:
            return "neutral or uncertain"
        if probability < 0.7:
            return "probably"
        if probability > 0.95:
            return "certain"
        else:
            return ""

    def predict_text(self, text):
        #try:
        vectorized = self.vectorizer.transform([SentimentClassifier.clean_str(text)])
        return self.model.predict(vectorized)[0],\
               self.model.predict_proba(vectorized)[0].max()
        #except Exception as e:
        #    print e.message
        #    return -1, 0.8

    def predict_list(self, list_of_texts):
        try:
            vectorized = self.vectorizer.transform(list_of_texts)
            return self.model.predict(vectorized),\
                   self.model.predict_proba(vectorized)
        except Exception as e:
            print e.message
            return None

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + " " + self.classes_dict[class_prediction]

    @staticmethod
    def clean_str(string):
        morph = pymorphy2.MorphAnalyzer()

        symbols = [
            ',', '.', '-', '*', '#', ')', '(', '/', '<', '>', ':', '+', '?', '!', '"', '"', '%', '=', '\\', '}'
        ]

        string_result = ''
        for symbol in symbols:
            string_result = str(string).replace(symbol, ' ')

        words = string_result.split()
        normalized_words = []

        for word in words:
            normalized_words.append(morph.parse(unicode(word.strip()))[0].normal_form)

        string_result = unicode(' '.join(normalized_words))

        return unicode(string_result)
