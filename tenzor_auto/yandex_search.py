import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions


url = 'https://yandex.ru'

def erlog(*args):
    """ Логирует ошибки программы в файл erlog.txt"""
    l = open("erlog.txt", 'a', encoding='windows-1251')
    print(str(datetime.datetime.today()), file=l)
    print(*args, file=l)
    l.close()


def ya_search(url):
    """ Ищет в Яндексе по запросу 'тензор' """
    try:
        op = webdriver.ChromeOptions()
        # op.add_argument('--disable-gpu')
        # op.add_argument('--disable-extensions')
        # op.add_argument('--no-sandbox')
        # op.add_argument('--headless')

        driver = webdriver.Chrome(options=op)
        driver.get(url)
        search_form = driver.find_element_by_xpath("//input[@id='text'][@aria-label='Запрос']")
        search_form.send_keys('тензор')
        # searching_words = driver.find_element_by_xpath("//input[@id='text'][@aria-label='Запрос']").text
        searching_words = driver.find_element_by_xpath("//span[@class='input__ahead-filler'][contain]")
        text = searching_words.te
        time.sleep(3)
        driver.quit()
    except selenium.common.exceptions.NoSuchElementException as e:
        print(" Ошибка selenium: элемент не существует")
        erlog(" Ошибка selenium: элемент не существует")
        erlog(str(e))
    except selenium.common.exceptions.InvalidArgumentException as e:
        print(" Ошибка selenium: инвалидный аргумент")
        erlog(" Ошибка selenium: инвалидный аргумент")
        erlog(str(e))
    finally:
        driver.quit()

    return text


print(ya_search(url=url))