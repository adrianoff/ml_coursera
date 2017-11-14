import requests
import bs4 as bs4

base_url = 'https://technopoint.ru/catalog/17a75b8e16404e77/smartfony'
pages = []

for p in range(1, 33):
    pages.append(base_url + '/?p=' + str(p) + '&i=1&stock=0&order=4')

products_link = []
for page in pages:
    req = requests.get(page)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    links = parser.findAll('a', attrs={'data-role': 'product-cart-link'})
    for link in links:
        products_link.append(base_url + link['href'] + 'opinion/')

print products_link
