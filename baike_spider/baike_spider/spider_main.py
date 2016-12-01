# coding:utf-8
from baike_spider import url_manager
from baike_spider import html_downloader
from baike_spider import html_parser
from baike_spider import html_outputer


class SpiderMain(object):
	def __init__(self):
		self.urls = url_manager.UrlManager()  # url管理器
		self.downloader = html_downloader.HtmlDownloader()  # 下载器
		self.parser = html_parser.HtmlParser()  # 解析器
		self.outputer = html_outputer.HtmlOutputer()  # 输出器

	def crawl(self, root_url):
		count = 1  # 计数
		self.urls.add_new_url(root_url)	 # 向url管理器中加入根url开始爬取
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()  # 从url管理器中获取一个新的url
				print 'crawl %d:%s' % (count, new_url)  # 提示输出
				html_cont = self.downloader.download(new_url)  # 下载url内容
				new_urls, new_data = self.parser.parse(new_url, html_cont)  # 解析url内容并返回新的url与data
				self.urls.add_new_urls(new_urls)  # 把新的url加入url管理器
				self.outputer.collect_data(new_data)  # 收集新的数据

				if count == 1000:  # 输出100条结果
					break
				count = count + 1
			except Exception, e:
				# print e
				print 'crawl failed'

		# 调用输出方法进行输出
		# self.outputer.output_html()
		self.outputer.output_db()


if __name__ == "__main__":
	root_url = "http://baike.baidu.com/view/21087.htm"
	obj_spider = SpiderMain()
	obj_spider.crawl(root_url)
