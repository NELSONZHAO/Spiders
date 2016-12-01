# coding:utf-8


class UrlManager(object):

	def __init__(self):
		self.new_urls = set()

	def has_new_url(self):
		return len(self.new_urls)

	def get_new_url(self):
		return self.new_urls.pop()

	def add_new_url(self, pageindex):
		new_page = "http://www.qiushibaike.com/text/page/" + str(pageindex) + "/"
		self.new_urls.add(new_page)

