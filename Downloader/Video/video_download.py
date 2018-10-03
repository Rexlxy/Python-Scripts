import urllib.request
import datetime
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import random
import http.client
import downloader
import configparser

# try to connect to the url, return the beautiful soup object
# exit if failing for 5 times
def getBSObject(url):
	for i in range(4):
		try:
			req = urllib.request.Request(url, headers=headers)
			page = urllib.request.urlopen(req).read()
			break
		except http.client.IncompleteRead as e:
			print('Exception: http.client.IncompleteRead, URL: ', url)
			sleepTime = random.randint(0,3)
			print("sleeping (seconds): ", sleepTime)
			continue
	
	bs = BeautifulSoup(page ,'html.parser')
	return bs


# enter one video page, find the url and download
def downloadVideo(url, folderName, index):
	filename = folderName+ "/" + str(index) + ".mp4"
	# get beautiful soup object
	bs = getBSObject(url)
	
	try:
		div = bs.find("div", {"id":"player"})
		title = bs.find('title').get_text()
		script = div.find('script')
		s = str(script)
	except:
		print("Can't find tag: ", filename)
		return 
	
	# find valid urls by RegEx
	results = gl_regEx.findall( s)
	print('-----------------------------------------------------------------------')
	print("Trying to download:" + filename)
	print('Page link:' + url)
	for result in results:
		
		# 预处理
		s = result.replace('\\', '' )
		print('Downloading.....')
		starttime = datetime.datetime.now()
		try:
			downloader.multithread_download(s, filename)
		except:
			print("Invalid link, retrying...")
			continue
		endtime = datetime.datetime.now()
		print("Finished in (seconds): ", (endtime-starttime).seconds)
		return

	print("No url works:" + filename)

# download videos on one page
def downloadOnePage(url, folderName):
	# get beautiful soup object
	bs = getBSObject(url)
	
	try:
		block = bs.find('div', {'class':'sectionWrapper'})
		# other pages are different from the first page in structure.
		if block is None:
			block = bs.find('ul', {'class':'videos search-video-thumbs freeView'})
		list = block.findAll('li', {'class':'js-pop videoblock videoBox'})
	except:
		print("Can't find tag: " + folderName)
		return 

	index = 0;
	for item in list:
		a = item.find('a')
		# print(a)
		link = 'XXXXXXXXX' + a['href']
		# title = a['title']
		# print('page link:' + link)
		downloadVideo(link, folderName, index)
		index += 1;
		sleepTime = random.randint(0,5)
		print("Random Sleep(seconds): ", sleepTime)
	print("### All downloaded: " + folderName)
	

# download videos from the search result url with specified number 
# of pages
def myProgram(url, folderName, start, end):
	page = start;
	if not os.path.exists(folderName):
		os.makedirs(folderName)
	preffix = folderName + '/'
	# go through pages
	while page <= end:
		folderName = preffix + 'page' + str(page)
		# create folder
		if not os.path.exists(folderName):
			os.makedirs(folderName)
		
		if page==1:
			suffix = ''
		else:
			suffix = "&page=" + str(page) 
		print("///////////////////////////////////////////////////////////////////////")
		print("### Downloading page: " + str(page))
		downloadOnePage(url+suffix, folderName)
		page += 1
	print("Terminated!")


# 主程序
gl_regEx = re.compile(r'videoUrl":"(.+?)"') # compiled regular expression
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


#读取配置文件
cf = configparser.ConfigParser()
cf.read("config.ini")
url = cf.get("parameter", "url")
folderName = cf.get("parameter", "folderName")
start = int(cf.get("parameter", "start"))
end = int(cf.get("parameter", "end"))
 
myProgram(url, folderName, start, end)
