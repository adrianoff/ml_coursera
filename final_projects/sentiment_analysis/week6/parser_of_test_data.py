import bs4 as bs4
import pandas as pd

f = open('./data/test.csv')
test_text = f.read()

parser = bs4.BeautifulSoup(test_text, 'lxml')
reviews = parser.findAll('review')
reviews_text = []
for review in reviews:
    reviews_text.append(unicode(review.text))

data = pd.DataFrame()
data['text'] = reviews_text
data.to_csv('./data/test_data_to_predict.csv', encoding='utf-8')
