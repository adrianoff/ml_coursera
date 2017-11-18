
# -*- coding: utf-8 -*-

import bs4 as bs4
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf8')

path = './data'
files = [f for f in listdir(path) if isfile(join(path, f))]

texts = []
grades = []
links = []
full_contents = []

for file_name in tqdm(files):
    f = open(path + '/' + file_name)
    content = f.read()
    link, grade, html = content.split("\n")

    parser = bs4.BeautifulSoup(html, 'lxml')
    lis = parser.findAll('li')

    comment_text = ''
    try:
        if int(grade) in [4, 5]:
            comment_text += lis[0].find('span', {'class': 'description-text'}).text
        else:
            comment_text += lis[1].find('span', {'class': 'description-text'}).text
    except AttributeError:
        pass

    try:
        comment_text += ' ' + lis[2].find('span', {'class': 'description-text'}).text
    except (IndexError, AttributeError) as e:
        pass

    texts.append(comment_text)
    links.append(link)
    grades.append(grade)
    full_contents.append(content)

    f.close()


data = pd.DataFrame()
data['grade'] = grades
data['link'] = links
data['text'] = texts
data['content'] = full_contents

data.to_csv('./data.csv', encoding='utf-8')