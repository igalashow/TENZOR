import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from bs4 import BeautifulSoup


url = 'https://yandex.ru'

def erlog(*args):
    """ Логирует ошибки программы в файл erlog.txt"""
    l = open("erlog.txt", 'a', encoding='windows-1251')
    print(*args)
    print(str(datetime.datetime.today()), file=l)
    print(*args, file=l)
    l.close()


def test_ya_search():
    """ Ищет в Яндексе по запросу 'тензор' """
    try:
        op = webdriver.ChromeOptions()
        # op.add_argument('--disable-gpu')
        # op.add_argument('--disable-extensions')
        # op.add_argument('--no-sandbox')
        # op.add_argument('--headless')

        driver = webdriver.Chrome(options=op)
        driver.get('https://yandex.ru')
        source = driver.page_source
        search_form = driver.find_element_by_xpath("//input[@id='text'][@aria-label='Запрос']")
        assert search_form

        # ввод в поисковую строку слова 'тензор'
        search_form.send_keys('тензор')
        # нажимаем Enter
        search_form.send_keys(Keys.ENTER)
        time.sleep(3)

        # определяем tensor.ru в пятерке поиска
        # issue = driver.find_elements_by_xpath("//h2[@class]/descendant::a[@href]")#/following-sibling::a[@href]")
        driver.quit()
        soup = BeautifulSoup(source, 'html.parser')
        for ahref in issue[:5]:
            str_ahref = str(ahref.get_attribute('outerHTML'))
            print(str_ahref)

    except selenium.common.exceptions.NoSuchElementException as e:
        erlog(" Ошибка selenium: элемент не существует")
        erlog(str(e))
    except selenium.common.exceptions.InvalidArgumentException as e:
        erlog(" Ошибка selenium: инвалидный аргумент")
        erlog(str(e))
    finally:
        driver.quit()

    return


test_ya_search()