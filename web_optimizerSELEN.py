from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import selenium.common.exceptions
import os

url='https://meduza.io/feature/2021/05/23/armiya-mertvetsov-zaka-snaydera-ograblenie-kazino-vo-vremya-apokalipsisa'

def erlog(*args):
	l = open("erlog.txt", 'a', encoding='windows-1251')
	print(str(datetime.today()), file=l)
	print(*args, file=l)
	l.close()




op = webdriver.ChromeOptions()
# op.add_argument('headless')
# op.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=op)
driver.get(url)

# main_page = driver.find_element_by_tag_name("html")
# source = main_page.get_attribute("innerHTML")
source = driver.page_source
# parentTag = driver.find_element_by_xpath("//p/parent::*")
# count_of_p = len(parentTag)
# prognoz = driver.find_element_by_xpath("//tr/td/table/tbody/tr/td/b[text()='ИНФОРМАЦИЯ О НЕБЛАГОПРИЯТНЫХ МЕТЕОРОЛОГИЧЕСКИХ УСЛОВИЯХ (НМУ) В НИЖЕГОРОДСКОЙ ОБЛАСТИ']/following::tr[4]")
# st_clean = prognoz.text

driver.quit()

soup = BeautifulSoup(source, 'html.parser')

# удаляем пустые теги
empty_tags = soup.findAll(lambda tag: not tag.contents or 
len(tag.get_text(strip=True)) <= 0)
[empty_tag.extract() for empty_tag in empty_tags]

# while soup.find('div', {'class' : 'sub_menu'}):
	# soup.find('div', {'class' : 'sub_menu'}).decompose()
# while soup.find('h1'):
	# soup.find('h1').decompose()
# st = soup.find_parents('p')
# st = soup.select("div > p")				#извлекаем текст из тела страницы
# print(st)
# for div in soup.find_all('div'):
	# if div.contents == "p":
		# #do whatever you want with div.parent which is the element you want.
		# print(div)

# def p_inside(tag):
	# return (tag.name == 'p')

p_tags = soup.find_all('p')
parents_p = [p.parent for p in p_tags]
# print(parent_p)
print(len(parents_p))

maxi = 0	# тэг с максимальным количеством абзацев текста
maxi_index = 0	# индекс тега с максимальным количеством абзацев текста

for index, tag in enumerate(parents_p):
	# print(tag)
	str_tag = str(tag)
	print(str_tag.count('<p'))
	if str_tag.count('<p') > maxi:
		maxi = str_tag.count('<p')
		maxi_index = index
print('максимально абзацев: ', maxi)
print(parents_p[maxi_index])

# Полезное содержимое страницы
content = soup.find_all('p')
print(content[6])

	
	# st_c = re.sub(r'\<[^>]*\>', '', str(st))				# убираем всё, что в теговых скобках, оставляем только текст
	# st_clean = re.sub('[\r\t\n]', '', st_c)
	# st_clean = re.sub('Подробнее', '', st_clean)
	# print(st)
