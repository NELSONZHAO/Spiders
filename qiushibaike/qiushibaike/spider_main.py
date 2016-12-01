# coding:utf-8
from qiushibaike import url_manager
from qiushibaike import html_downloader
from qiushibaike import html_parser
from qiushibaike import html_outputer


class SpiderMain(object):
	def __init__(self):
		self.urls = url_manager.UrlManager()  # url管理器
		self.downloader = html_downloader.HtmlDownloader()  # 下载器
		self.parser = html_parser.HtmlParser()  # 解析器
		self.outputer = html_outputer.HtmlOutputer()  # 输出器

	def crawl(self):
		count = 1  # 记录爬取了多少页
		self.urls.add_new_url(count)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()  # 获取新的url
				html_doc = self.downloader.download(new_url)  # 下载新的url内容
				print "%d pages has done." % count
				data = self.parser.parse(html_doc)  # 解析网页内容
				self.outputer.collect_data(data)  # 将数据进行存储
			except Exception:
				print "crawl failed"

			if count == 10:
				break
			count += 1
			self.urls.add_new_url(count)

		self.outputer.savedb()
		print "All works have done."

if __name__ == "__main__":
	spider = SpiderMain()
	spider.crawl()
