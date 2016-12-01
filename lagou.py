# coding:utf-8
# 说明:该文档用来爬取拉勾网全国站中Python领域的招聘岗位,继而对数据进行统计分析
# 思路:1.爬取(企业名字,企业类别,企业现状,职位,地点,薪资,经验,学历,优势);2.分析;3.可视化

import urllib2
from bs4 import BeautifulSoup
import MySQLdb

class UrlManager(object):
	def __init__(self):
		self.urls = set()

	def add_new_url(self, page):
		new_url = 'http://www.lagou.com/zhaopin/Python/%s/' % page
		self.urls.add(new_url)

	def have_url(self):
		return self.urls

	def get_new_url(self):
		return self.urls.pop()


class Downloader(object):
	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

	def download(self, url):
		request = urllib2.Request(url, headers=self.headers)
		response = urllib2.urlopen(request)
		return response.read()


class Parser(object):
	def parse(self, html):
		detail_data = []
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		# find all nodes that includes the information
		nodes = soup.find_all('li', class_='con_list_item')
		# get information from nodes
		for node in nodes:
			detail_data.append(self.get_detail(node))
		return detail_data

	def get_detail(self, node):
		# find company name
		company = node.find('div', class_='company_name').find('a').string.encode('utf-8')
		# find industry
		industry = node.find('div', class_='industry').string.strip().split('/')
		company_cls = industry[0].encode('utf-8')
		company_type = industry[1].encode('utf-8')
		# find advantage
		advantage = '/'.join([i.encode('utf-8') for i in node.find('div', class_='li_b_r').get_text().split()])
		# find job name
		job = node.find('h2').string.encode('utf-8')
		# find job place
		place = node.find('em').string.encode('utf-8')
		# find money
		money = node.find('span', class_='money').string.encode('utf-8')
		# requirement
		requirement = node.find('div', class_='li_b_l').get_text().strip().split('/')
		# find experience
		experience = requirement[0].encode('utf-8')
		# find education
		education = requirement[1].encode('utf-8')
		return [company, company_cls, company_type, advantage, job, place, money, experience, education]


class Output(object):
	def __init__(self):
		self.total = []

	def collect(self, data):
		self.total = self.total + data

	def show(self):
		for i in self.total:
			print i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]
		print 'There are %s jobs' % len(self.total)

	def intodb(self):
		conn = MySQLdb.Connect(user='root',passwd='940720',host='127.0.0.1',port=3306, db='spiders', charset='utf8')
		cursor = conn.cursor()
		sql = 'INSERT lagou_python_hangzhou(company, cls, type, advantage, job, place, money, experience, education) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
		for i in self.total:
			cursor.execute(sql, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))
		conn.commit()
		cursor.close()
		conn.close()


class MainSpider(object):
	def __init__(self):
		self.urlmanager = UrlManager()
		self.downloader = Downloader()
		self.parser = Parser()
		self.output = Output()

	def crawl(self):
		# page
		page = 1
		# add new_url into urlmanager
		self.urlmanager.add_new_url(page)
		# if there is a new url in current url manager, then execute 'while'
		while self.urlmanager.have_url():
			try:
				new_url = self.urlmanager.get_new_url()  # get a new url
				html = self.downloader.download(new_url)  # download the content of the url
				data = self.parser.parse(html)  # parse the html
				self.output.collect(data)  # collect parsed data
				print '%s pages have done.' % page
				page += 1
				self.urlmanager.add_new_url(page)
			except:
				print 'crawl failed!'

			if page == 6: break
		self.output.show()
		# self.output.intodb()
		print 'data has saved.'

if __name__ == "__main__":
	spider = MainSpider()
	spider.crawl()