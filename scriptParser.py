import requests
import re
from bs4 import BeautifulSoup
import csv
import time

# Фукнция для записи данных в файл в csv формате
def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                        data['price'],
                        data['metro'],
                        data['url']))


#Функция для парсинга html и создания данных
def get_page_data(html):
    
    soup = BeautifulSoup(html, 'lxml')
    ads =  soup.find_all('div', class_='item_table-wrapper')
    for ad in ads:
        #title pcice url metro 
        try:
            title=ad.find('a', class_='snippet-link').get('title')      
        except:
            title=''
        try:
            url='https://www.avito.ru'+ad.find('a', class_='snippet-link').get('href')      
        except:
            url=''
        try:
            priceText=ad.find('span', class_='snippet-price').getText()     
            price=re.sub(r'\W+', '', priceText)     
        except:
            price=''
        try:    
            metro = 'м.'+ad.find('span', class_='item-address-georeferences-item__content').getText()

        except:
            metro=''

        data = {'title': title,
                'price': price,
                'metro': metro,
                'url': url}
        
        write_csv(data)
#Функция для cocтавления HTTP запроса и получения ответа от сервера
def get_html(url):
    res = requests.get(url)    
    return res.text

#Функция для получение количества страниц
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div',class_='js-pages').find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


#Главная функция
def main():
    
    url='https://www.avito.ru/moskva/noutbuki?p=1&q=asus'
    base_url='https://www.avito.ru/moskva/noutbuki?'
    page_part='p='
    query_part = '&q=asus'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages):
        url_gen = base_url+page_part+str(i)+query_part
        html = get_html(url_gen)
        get_page_data(html)
        time.sleep(3)


if __name__ == '__main__':
    main()



    


    
