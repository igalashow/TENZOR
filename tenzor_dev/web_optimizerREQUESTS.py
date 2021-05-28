import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

url='https://zona.media/article/2021/05/20/dymovsky'

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


content = find_content(requests_get_source(url))
print(content)

	# st_c = re.sub(r'\<[^>]*\>', '', str(st))				# убираем всё, что в теговых скобках, оставляем только текст
	# st_clean = re.sub('[\r\t\n]', '', st_c)
	# st_clean = re.sub('Подробнее', '', st_clean)
	# print(st)
	
	

