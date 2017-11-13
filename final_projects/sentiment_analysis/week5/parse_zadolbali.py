import requests
import bs4
from multiprocessing import Pool
import codecs

def parse_page(url):
    text = requests.get(url).text
    parser = bs4.BeautifulSoup(text, 'lxml')
    x = parser.findAll('div', attrs={'class':'text'})
    return [res.text for res in x]

p = Pool(10)
url_list = ['http://zadolba.li/201604' + '0' * int(n < 10) + str(n) for n in range(1, 18)]
    
if __name__ == '__main__':    
    map_results = p.map(parse_page, url_list)
    reduce_results = reduce(lambda x,y: x + y, map_results)
    with codecs.open('parsing_results.txt', 'w', 'utf-8') as output_file:
        print >> output_file, u'\n'.join(reduce_results)