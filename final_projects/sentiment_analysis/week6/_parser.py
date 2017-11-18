###### Собственно сам парсер. #######

# -*- coding: utf-8 -*-

import requests
import bs4 as bs4
from tqdm import tqdm
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def split_uppercase(string):
    x = ''
    k = 0
    for c in string:
        if k == 0:
            x += c
        elif c.isupper() and not string[k-1].isupper():
            x += ' %s' % c
        else:
            x += c
        k += 1

    return x.strip()


site = 'https://technopoint.ru'
base_url = 'https://technopoint.ru/catalog/17a75b8e16404e77/smartfony'
pages = []

for p in range(1, 33):
    pages.append(base_url + '/?p=' + str(p) + '&i=1&stock=0&order=4')

products_link = []
print "Get Pages:\n"
for page in tqdm(pages):
    req = requests.get(page)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    links = parser.findAll('a', attrs={'data-role': 'product-cart-link'})
    for link in links:
        products_link.append(site + link['href'] + 'opinion/')


print "\n\nGet Pages With Comments:\n"
pages_with_comments = []
for link in tqdm(products_link):
    req = requests.get(link)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    ul_pagination = parser.find('ul', {"class": "pagination"})
    comments_pager_last_link = None
    if ul_pagination is not None:
        comments_pager_last_link = ul_pagination.find('li', {"class": "last"}).find('a')

    comments_pages_count = 1
    if comments_pager_last_link is not None:
        comments_pages_count = int(comments_pager_last_link["data-page"]) + 1

    for page_with_comments in range(1, comments_pages_count + 1):
        pages_with_comments.append(link + str(page_with_comments) + '/')

i = 1
print "\n\nProceed Pages With Comments:\n"
for page_with_comments in tqdm(pages_with_comments):
    req = requests.get(page_with_comments)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    opinion_items = parser.find('div', {"class": "opinion-container"}).findAll('div', {"class": "opinion-item"})
    for opinion_item in opinion_items:
        description = str(opinion_item.find('div', {"class": "descriptions"})).replace("\n", ' ')
        description = split_uppercase(unicode(description))

        grade = opinion_item["data-grade"]

        comment_file = open('./data/' + str(i) + '.txt', 'w')
        comment_file.write(page_with_comments + "\n" + grade + "\n" + description)
        comment_file.close()

        i += 1

print "\n"
print "Total comments: " + str(i)