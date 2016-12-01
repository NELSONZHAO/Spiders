# coding:utf-8
import urllib2


class HtmlDownloader(object):

	def download(self, url):
		if url is None:
			return 'downloader: url is None'
		response = urllib2.urlopen(url)
		if response.getcode() != 200:
			return 'response code failed:%s' % response.getcode()
		return response.read()  # 返回一个'str'格式的内容
