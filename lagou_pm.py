# coding: utf-8
# 说明:爬取拉勾网中全国范围内所有含有产品经理关键词的职位
# 思路:1.循环;2.获取json;3.解析并存储json

import urllib2
import json
import time
import random
import MySQLdb


# 获取json
def crawl():
	# 设置爬虫基本参数
	headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
	loginheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, sdch',
				'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
				'Connection': 'keep-alive',
				'Host': 'www.lagou.com',
				'User-Agent': headers}
	pn = 1
	url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&first=true&kd=产品经理&pn='
	# 查看结果数量确定循环总页数
	init_url = url + str(pn)
	response = urllib2.urlopen(init_url)
	page = response.read()
	jsondata = json.loads(page, encoding='utf-8')
	resultsize = jsondata['content']['positionResult']['totalCount']
	pagesize = jsondata['content']['positionResult']['resultSize']
	pages = resultsize / pagesize + 1
	print 'There are %s pages.' % pages
	# 循环取页面数据(每页15个)
	while pn <= 2:
		new_url = url + str(pn)
		request = urllib2.Request(new_url, headers=loginheaders)
		result = urllib2.urlopen(request).read()
		jsonresult = json.loads(result, encoding='utf-8')
		data = jsonresult['content']['positionResult']['result']
		# print '-' * 30
		print '%s/%s pages have done.' % (pn, pages)
		pn += 1
		info = parse(data)
		savefile(info)
		#savedb(info)
		time.sleep(10 * random.random() / 2)


# 解析json
def parse(data):
	pagedata = []
	for d in data:
		companyid = str(d['companyId']).encode('utf-8')  # 企业编号
		companyfullname = d['companyFullName'].encode('utf-8')  # 企业全名
		companyshortname = d['companyShortName'].encode('utf-8')  # 企业简名
		financestage = d['financeStage'].encode('utf-8')  # 企业发展阶段
		companysize = d['companySize'].encode('utf-8')  # 企业规模
		industry = d['industryField'].encode('utf-8')  # 企业的领域
		city = d['city'].encode('utf-8')  # 城市
		if d['district'] != None:
			district = d['district'].encode('utf-8')  # 企业的城市区域
		else: district = 'null'
		if d['businessZones'] != None:
			businesszones = '/'.join(d['businessZones']).encode('utf-8')  # 企业区(可为空值)
		else: businesszones = 'null'
		positionname = d['positionName'].encode('utf-8')  # 职务名称
		positionid = str(d['positionId']).encode('utf-8')  # 职位编号
		education = d['education'].encode('utf-8')  # 教育水平要求
		experience = d['workYear'].encode('utf-8')  # 经验要求
		jobnature = d['jobNature'].encode('utf-8')  # 岗位性质(实习or全职)
		if d['companyLabelList'] != None:
			labels = '/'.join(d['companyLabelList']).encode('utf-8')  # 企业标签
		else: labels = 'null'
		salary = d['salary'].encode('utf-8')  # 工资
		advantage = d['positionAdvantage'].encode('utf-8')  # 福利待遇
		pagedata.append([companyid, companyfullname, companyshortname, financestage, companysize, industry,
						city, district, businesszones, positionname, positionid, education, experience, jobnature, labels,
						salary, advantage])
	return pagedata


# 存储结果
def savefile(info):
	# 结果写入txt文档
	with open('lagou_pm_country.txt', 'a') as f:
		for item in info:
			f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
					(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
					 item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16]))
	print 'Write done.'


"""# 写入数据库
def savedb(info):
	# 将结果存入数据库中
	conn = MySQLdb.Connect(host='127.0.0.1', port=3306, user='root', passwd='940720', db='spiders', charset='utf8')
	cursor = conn.cursor()
	sql = 'INSERT lagou_datamining_country(companyid, companyfullname, companyshortname, financestage, companysize, industry,' \
		  'city, district, businesszones, positionname, positionid, education, experience, jobnature, labels,' \
		  'salary, advantage) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	for item in info:
		cursor.execute(sql, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
							 item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16]))
	conn.commit()
	cursor.close()
	conn.close()
	print 'write into database...'"""

if __name__ == "__main__":
	crawl()