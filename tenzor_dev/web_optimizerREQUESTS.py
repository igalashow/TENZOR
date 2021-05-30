import datetime
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

url='https://tass.ru/ekonomika/11493549'


def erlog(*args):
	l = open("erlog.txt", 'a', encoding='windows-1251')
	print(str(datetime.today()), file=l)
	print(*args, file=l)
	l.close()


def requests_get_source(url):
	"""	Получает страницу через Requests """
	try:
		ua = UserAgent()
		headers = {'User-Agent': ua.firefox}
		r = requests.get(url, headers=headers, timeout=15)
	except requests.ConnectionError as e:
		erlog(" Упс!! Ошибка соединения. Проверьте подключение к Интернет.")
		erlog(str(e))
	except requests.Timeout as e:
		erlog(" OOPS!! Timeout Error")
		erlog(str(e))
		print('Время загрузки страницы истекло')
	except requests.RequestException as e:
		erlog("OOPS!! General Error")
		erlog(str(e))
	except KeyboardInterrupt:
		erlog(" Кто-то закрыл программу")

	r.encoding = 'utf-8'
	source = r.text
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

	maxi = 0	# тег с максимальным количеством абзацев текста
	maxi_index = 0	# индекс тега с максимальным количеством абзацев текста

	# Находим родительский тег с максимальным количеством тегов <p>
	for index, tag in enumerate(parents_p):
		str_tag = str(tag)
		if str_tag.count('<p') > maxi:
			maxi = str_tag.count('<p')
			maxi_index = index

	# Полезное содержимое страницы в виде списка вебэлементов
	content = parents_p[maxi_index].find_all('p')
	return content


def formatter(content, len_line=80):
	""" Форматирует текст контента по заданным параметрам"""

	clean_content = []
	# Форматируем ссылки и убираем теги
	for tag_p in content:
		str_tag_p = str(tag_p)
		# Форматируем ссылки в вид [ссылка]
		while str_tag_p.find('<a href="') >= 0:
			index_href = str_tag_p.find('<a href="')	# находим индекс начала тега
			index_end_href = str_tag_p.find('"', index_href+9)	# находим индекс второй кавычки
			link = str_tag_p[index_href+9:index_end_href]	# вырезаем ссылку
			formatted_link = '['+link+'] '
			str_tag_p = str_tag_p.replace('<a href="'+link, formatted_link+'<a "')	# перемещаем [ссылку] за пределы тега

		# убираем все теги, оставляем только текст
		str_tag_p_clean = re.sub(r'\<[^>]*\>', '', str_tag_p)
		clean_content.append(str_tag_p_clean)

	# Отбиваем абзацы пустой строкой
	clean_list_content = []
	for paragraph in clean_content:
		clean_list_content.append(paragraph+'\n\n')

	# Создаем список всех слов статьи
	all_words = []
	for words in clean_list_content:
		words_group = words.split(sep=' ')
		all_words += words_group

	# Регулируем длину строки
	stroka = ''
	all_lines = ''
	end_p = False # флаг конца абзаца

	for word in all_words:
		# Если строка не заполнена и не было конца абзаца
		if len(stroka+word) < len_line and end_p == False:
			# плюсуем слово
			stroka += word + ' '
			# Проверяем на конец абзаца
			if word.endswith('\n\n'):
				end_p = True
				all_lines += stroka
				stroka = ''

		# Если строка не заполнена и был конец абзаца
		elif  len(stroka+word) < len_line and end_p == True:
			stroka = word + ' '
			end_p = False

		# если длина слова больше длины строки (например ссылка)
		elif len(word) >= len_line:
			all_lines += word + '\n'

		# Если не было конца абзаца
		elif end_p == False:
			all_lines += stroka + '\n'
			stroka = word+' '

	# Пишем все строки в файл
	with open('article.txt', 'w', encoding='utf-8') as f:
		print(all_lines, file=f)
try:
	content = find_content(requests_get_source(url))
	# print(content)
	formatter(content)
except Exception as e:
	erlog(str(e))
	print('Ошибка, смотри erlog.txt')
	

