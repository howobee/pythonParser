import requests
import re
from bs4 import BeautifulSoup
import csv

base_url  = 'https://www.avito.ru/moskva/noutbuki?'
page_part ='p='
query_part ='&q=asus'
url='https://www.avito.ru/moskva/noutbuki?p=1&q=asus'
def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                        data['price'],
                        data['metro'],
                        data['url']))
res = requests.get(url)

soup = BeautifulSoup(res.text, 'lxml')

pages = soup.find('div',class_='js-pages').find_all('a')[-1].get('href')
total_pages = pages.split('=')[1].split('&')[0]

for i in range(1, 2):
    url_gen = base_url+page_part+str(i)+query_part
    r = requests.get(url_gen)
    soupBeut= BeautifulSoup(r.text, 'lxml')
    ads = soupBeut.find_all('div', class_='item_table-wrapper')
    for ad in ads:      
        title=ad.find('a', class_='snippet-link').get('title')      
        url='https://www.avito.ru'+ad.find('a', class_='snippet-link').get('href')      
        priceText=ad.find('span', class_='snippet-price').getText()     
        price=re.sub(r'\W+', '', priceText)     
        metro = 'м.'+ad.find('span', class_='item-address-georeferences-item__content').getText()
        data = {'title': title,
                'price': price,
                'metro': metro,
                'url': url}
        write_csv(data)

def get_html(url):
    res = requests.get(url)
    return res.text


        
