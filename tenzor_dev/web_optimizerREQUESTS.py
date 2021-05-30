import datetime
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urlparse
import os
from config import LEN_LINE, RECOMMEND, WHITE_LIST, BLACK_LIST


def erlog(*args):
	""" Логирует ошибки программы в файл erlog.txt"""
	l = open("erlog.txt", 'a', encoding='windows-1251')
	print(str(datetime.datetime.today()), file=l)
	print(*args, file=l)
	l.close()


class WebOptimizer():
	""" Оптимизатор читаемости текстового контента на сайтах"""

	# def read_config(self):
	# 	""" Считывает файл настроек config.py"""
	# 	if os.path.isfile('config.py'):
	# 		with open('config.py', 'r') as config:
	#
	# 	else:
	# 		pass



	def recommendation(self, url):
		""" Вставляет рекомендацию в начало файла """
		for domen in WHITE_LIST:
			if domen in url:
				return '!Это рекомендуемый источник!\n\n'
		for domen in BLACK_LIST:
			if domen in url:
				return '!Это НЕ рекомендуемый источник!\n\n'

	def url_to_path(self, url):
		""" Формирует путь сохранения файла из URL """
		url_parse_result = urlparse(url)
		file_path = str(url_parse_result.netloc + url_parse_result.path)
		return file_path


	def save_file(self, file_path, filename='index.txt'):
		""" Сохраняет файл по url_to_path """
		if not os.path.isfile(file_path+'/'+filename):
			os.makedirs(file_path)
			with open(file_path+'/'+filename, 'w', encoding='utf-8') as f:
				print(formatted_text, file=f)
			print(f'Файл с текстом статьи создан по адресу:\n'
				  f'[текущая папка]/{file_path}')
		else:
			print(f'Файл с текстом этой статьи уже существует по адресу:\n'
				  f'[текущая папка]/{file_path}')


	def requests_get_source(self, url):
		"""	Получает страницу через Requests """
		try:
			ua = UserAgent()
			headers = {'User-Agent': ua.firefox}
			r = requests.get(url, headers=headers, timeout=15)

		except requests.exceptions.InvalidURL as e:
			print('Введен некорректный URL!')
			erlog("Введен некорректный URL!")
			erlog(str(e))
		except requests.exceptions.InvalidSchema as e:
			print('Некорректная схема URL!')
			erlog("Некорректная схема URL!")
			erlog(str(e))
		except requests.ConnectionError as e:
			erlog(" Упс!! Ошибка соединения. Проверьте подключение к Интернет.")
			erlog(str(e))
		except requests.Timeout as e:
			erlog(" OOPS!! Timeout Error")
			erlog(str(e))
			print('Время загрузки страницы истекло')
		except requests.exceptions.RequestException as e:
			erlog("OOPS!! General Error")
			erlog(str(e))
		except KeyboardInterrupt:
			erlog(" Кто-то закрыл программу")

		r.encoding = 'utf-8'
		source = r.text
		return source


	def find_content(self, source):
		""" Находит полезный контент на странице """
		try:
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

			# Полезное содержимое страницы в виде списка вебэлементов, включая заголовки
			content = parents_p[maxi_index].find_all(['p', 'h1', 'h2', 'h3', 'h4'])
		except:
			print('Вероятно, сайт не содержит полезной информации ;)')
		return content


	def formatter(self, content, len_line=80, recommend=False):
		""" Форматирует текст контента по заданным параметрам """

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

		clean_list_content = []
		# Если включен режим - добавляем в начало рекомендацию
		if recommend == True:
			clean_list_content.append(wo.recommendation(url))
		# Отбиваем абзацы и заголовки пустой строкой
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
		all_lines += stroka
		return all_lines

while True:
	try:
		wo = WebOptimizer()

		url = input('Введите URL статьи: ')

		source = wo.requests_get_source(url)
		content = wo.find_content(source)
		formatted_text = wo.formatter(content, LEN_LINE, RECOMMEND)

		# Пишем все строки в файл
		file_path = wo.url_to_path(url)
		wo.save_file(file_path)

	except Exception as e:
		erlog(str(e))
		print('Ошибка, смотри erlog.txt')
	

