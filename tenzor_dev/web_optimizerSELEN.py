from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import selenium.common.exceptions
import os

url = 'https://meduza.io/feature/2021/05/23/armiya-mertvetsov-zaka-snaydera-ograblenie-kazino-vo-vremya-apokalipsisa'

def erlog(*args):
	l = open("erlog.txt", 'a', encoding='windows-1251')
	print(str(datetime.today()), file=l)
	print(*args, file=l)
	l.close()

def selenium_get_source(url):
	"""	Получает страницу через Selenium WebDriver	"""

	op = webdriver.ChromeOptions()
	# op.add_argument('--disable-gpu')
	# op.add_argument('--disable-extensions')
	# op.add_argument('--headless')

	driver = webdriver.Chrome(options=op)
	driver.get(url)
	source = driver.page_source
	driver.quit()
	return source

def find_content(source):
	""" Находит полезный контент на странице """

	soup = BeautifulSoup(source, 'html.parser')

	# удаляем пустые теги
	empty_tags = soup.findAll(lambda tag: not tag.contents or
	len(tag.get_text(strip=True)) <= 0)
	[empty_tag.extract() for empty_tag in empty_tags]

	# находим все теги абзацев <p>
	p_tags = soup.find_all('p')
	# Находим все родительские теги для <p>
	parents_p = [p.parent for p in p_tags]

	maxi = 0	# тэг с максимальным количеством абзацев текста
	maxi_index = 0	# индекс тега с максимальным количеством абзацев текста

	# Находим родительский тег с максимальным количеством тегов <p>
	for index, tag in enumerate(parents_p):
		str_tag = str(tag)
		if str_tag.count('<p') > maxi:
			maxi = str_tag.count('<p')
			maxi_index = index

	# Полезное содержимое страницы в виде списка вебэлементов по абзацам
	content = parents_p[maxi_index].find_all('p')
	return content
	
# st_c = re.sub(r'\<[^>]*\>', '', str(st))				# убираем всё, что в теговых скобках, оставляем только текст
# st_clean = re.sub('[\r\t\n]', '', st_c)
# st_clean = re.sub('Подробнее', '', st_clean)
# print(st)

content = find_content(selenium_get_source(url))
print(content)
