import MySQLdb

class HtmlOutputer(object):
	def __init__(self):
		self.datas = []

	def collect_data(self, data):
		if data is None:
			return 'outputer: parse no data'
		self.datas.append(data)

	def output_html(self):
		fout = open('output.html','w')

		fout.write("<html>")
		fout.write("<body>")
		fout.write("<table>")

		for data in self.datas:
			fout.write("<tr>")
			fout.write("<td>%s</td>" % data['url'].encode('utf-8'))
			fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
			fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
			fout.write("</tr>")

		fout.write("</table>")
		fout.write("</body>")
		fout.write("</html>")

		fout.close()

	def output_db(self):
		conn = MySQLdb.Connect(host='127.0.0.1',port=3306,user='root',passwd='940720',db='imooc',charset='utf8')
		cursor = conn.cursor()
		row_count = 1
		for data in self.datas:
			sql = "INSERT INTO baike VALUES(%s, %s, %s)"
			cursor.execute(sql, (data['url'],data['title'],data['summary']))
			if row_count % 100 == 0:
				print "%s rows done." % row_count
			row_count += 1
		conn.commit()
		cursor.close()
		conn.close()

