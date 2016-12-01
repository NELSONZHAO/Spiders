# coding: utf-8
import MySQLdb

class HtmlOutputer(object):

	def __init__(self):
		self.alldata = []

	def collect_data(self, data):
		for d in data:
			self.alldata.append(d)
	
	def savedb(self):
		# print 'There is a new requirement about database...'
		conn = MySQLdb.Connect(host='127.0.0.1', port=3306, user='root', passwd='940720', db='imooc', charset='utf8')
		cursor = conn.cursor()
		sql = 'INSERT qiushi(username,content,likes) VALUES(%s, %s, %s)'
		for d in self.alldata:
			cursor.execute(sql, (d[0].encode('utf-8'), d[1].encode('utf-8'), d[2].encode('utf-8')))
		conn.commit()
		cursor.close()
		conn.close()


