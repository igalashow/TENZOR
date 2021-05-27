import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

url='https://meduza.io/feature/2021/05/23/armiya-mertvetsov-zaka-snaydera-ograblenie-kazino-vo-vremya-apokalipsisa'

def erlog(*args):
	l = open("erlog.txt", 'a', encoding='windows-1251')
	print(str(datetime.today()), file=l)
	print(*args, file=l)
	l.close()



try:
	ua = UserAgent()
	headers = {'User-Agent': ua.firefox}
	r = requests.get(url, headers=headers, timeout=15)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text, 'html.parser')
	
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
	
	pp = soup.find_all('p')
	parent_p = [p.parent for p in pp]
	# print(parent_p)
	print(len(parent_p))
	
	maxi = 0	# тэг с максимальным количеством абзацев текста
	maxi_index = 0	# индекс тега с максимальным количеством абзацев текста
	
	for index, tag in enumerate(parent_p):
		# print(tag)
		str_tag = str(tag)
		print(str_tag.count('<p>'))
		if str_tag.count('<p>') > maxi:
			maxi = str_tag.count('<p>')
			maxi_index = index
	print('максимально абзацев: ', maxi)
	print(parent_p[maxi_index])
	
	# Полезное содержимое страницы
	content = soup.find_all('p')
	print(content[0])
	# # divs = [a for a in soup.find(p_inside)]
	# divs = soup.find(p_inside)
	# print(divs)
		
	# divs =  soup.select('div > p')
	# print(len(divs))
	# print(divs)
	
	# st_c = re.sub(r'\<[^>]*\>', '', str(st))				# убираем всё, что в теговых скобках, оставляем только текст
	# st_clean = re.sub('[\r\t\n]', '', st_c)
	# st_clean = re.sub('Подробнее', '', st_clean)
	# print(st)
	
	
except requests.ConnectionError as e:
	erlog(" Упс!! Ошибка соединения. Проверьте подключение к Интернет. Technical Details given below.")
	erlog(str(e))
except requests.Timeout as e:
	erlog(" OOPS!! Timeout Error")
	erlog(str(e))
except requests.RequestException as e:
	erlog("OOPS!! General Error")
	erlog(str(e))
except KeyboardInterrupt:
	erlog(" Кто-то закрыл программу")
	
