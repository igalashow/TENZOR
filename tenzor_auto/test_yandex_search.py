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

def check_tenzor(links):
    """ Проверяет наличие tensor.ru в первой пятёрке поисковой выдачи """
    flag = False
    for link in links[:5]:
        if 'tensor.ru' in link:
            flag = True
    return flag

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

        # тест 1: проверка наличия поля поиска
        assert search_form

        # ввод в поисковую строку слова 'тензор'
        search_form.send_keys('тензор')

        # нажимаем Enter
        search_form.send_keys(Keys.ENTER)
        time.sleep(3)

        # парсинг ссылок из поисковой выдачи
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        tags_h2 = soup.find_all('h2')
        a_tags = []
        for tag in tags_h2:
            a = tag.find('a')
            if a:
                a_tags.append(a)
                a = None

        # очистка от тегов, остаются только ссылки
        links = []
        for tag in a_tags:
            str_a = str(tag)
            while str_a.find('href="') >= 0:
                index_href = str_a.find('href="')  # находим индекс начала тега
                index_end_href = str_a.find('"', index_href + 6)  # находим индекс второй кавычки
                link = str_a[index_href + 6:index_end_href]  # вырезаем ссылку
                links.append(link)
                str_a = str_a.replace('href="','"')  # удаляем атрибут href

        # Зачистка от рекламы яндекса
        for index, link in enumerate(links):
            if 'yabs.yandex.ru' in link:
                links.remove(link)
                links.insert(index, ' ')

        # тест 4: проверка на tensor.ru в первой пятерке поисковой выдачи
        assert check_tenzor(links)


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