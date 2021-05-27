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

op = webdriver.ChromeOptions()
# op.add_argument('headless')
# op.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=op)
driver.get(url)

source = driver.page_source

driver.quit()

soup = BeautifulSoup(source, 'html.parser')

# удаляем пустые теги
empty_tags = soup.findAll(lambda tag: not tag.contents or 
len(tag.get_text(strip=True)) <= 0)
[empty_tag.extract() for empty_tag in empty_tags]

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
