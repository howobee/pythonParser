import requests
import re
from bs4 import BeautifulSoup
import csv
import os
from selenium import webdriver
from time import sleep
import pytesseract
from PIL import Image

#Функция для считывания телефонного номера 
def avito_get_phonenum(url):
    
    #Открываем браузер 
    browser = webdriver.Firefox(executable_path=r'./geckodriver.exe')
    browser.get(url)
    
    #Находим кнопку и кликаем
    button= browser.find_element_by_xpath('//a[@class="button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height"]')
    button.click()
    sleep(3)
    
    #Сохраняем скриншот дисплее браузера в файл "avito_scr.png"
    browser.save_screenshot('avito_scr.png')
    image_s_l = browser.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
    
    #Берем координаты начальной точки и размеры картинки для crop()
    location = image_s_l.location     # dict{x:value, y:value}
    size = image_s_l.size             # dict{width:value, height:value}

    # Загружаем картинку и вызываем функцию crop() для обрезки картинки
    image = Image.open('avito_scr.png')
    x = location['x']
    y = location['y']
    width = size['width']
    height = size['height']
    image.crop((x, y, x+width, y+height)).save('tel_img.gif')

    # Закрываем браузер
    browser.close()

    #Загружаем скриншот и распознаем номер на картинки в текст
    image_phone_number = Image.open('tel_img.gif')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    phone_number =  pytesseract.image_to_string(image_phone_number)
    #Функция вовращает номер телефона строкой
    return phone_number

# Фукнция для записи данных в файл в csv формате
def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                        data['price'],
                        data['metro'],
                        data['url'],
                        data['phone_number']))


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
        phone_number = avito_get_phonenum(url)
        
        data = {'title': title,
                'price': price,
                'metro': metro,
                'url': url,
                'phone_number': phone_number}
        
        write_csv(data)

        #Удаляем картинки из папки
        file1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'avito_scr.png')
        file2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tel_img.gif')
        os.remove(file1)
        os.remove(file2)
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
    
    base_url  = 'https://www.avito.ru/moskva/avtomobili?'
    page_part ='p='
    query_part ='&q=bmw'
    url='https://www.avito.ru/moskva/avtomobili?p=1&q=bmw'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, 2):
        url_gen = base_url+page_part+str(i)+query_part
        html = get_html(url_gen)
        get_page_data(html)
        time.sleep(3)


if __name__ == '__main__':
    main()



    


    
