from selenium import webdriver
from time import sleep
import pytesseract
from PIL import Image


url = 'https://www.avito.ru/moskva/avtomobili/bmw_x6_2018_1900739661'

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


    #Загружаем скриншот и распознаем номер на картинки в текст
    image_phone_number = Image.open('tel_img.gif')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    phone_number =  pytesseract.image_to_string(image_phone_number)
    #Функция вовращает номер телефона строкой
    return phone_number


    





if __name__ == '__main__':
    avito_get_phonenum(url)






