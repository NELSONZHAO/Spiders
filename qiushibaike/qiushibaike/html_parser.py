# coding: utf-8
from bs4 import BeautifulSoup


class HtmlParser(object):

	def parse(self, html_doc):
		name_datas = []
		content_datas = []
		good_datas = []
		soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
		names = soup.find_all('h2')
		contents = soup.find_all('div', class_='content')
		goods = soup.find_all('div', class_='stats')
		for name in names:
			name_datas.append(name.get_text().strip())
		for content in contents:
			content_datas.append(content.get_text().strip())
		for good in goods:
			good_datas.append(good.find('i', class_='number').get_text().strip())

		return zip(name_datas, content_datas, good_datas)
