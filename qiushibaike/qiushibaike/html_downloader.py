# coding: utf-8

import urllib2


class HtmlDownloader(object):

	def __init__(self):
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 \
		(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		self.headers = {'User-Agent': self.user_agent}

	def download(self, url):
		request = urllib2.Request(url, headers=self.headers)
		response = urllib2.urlopen(request)
		if response.getcode() != 200:
			return 'response failed: %s' % response.getcode()
		pagecode = response.read().decode('utf-8')
		return pagecode
