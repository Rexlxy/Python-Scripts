from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time

# 解析得到的网页
def parsePage(page):
	output = ""
	soup = BeautifulSoup(page, 'html.parser')
	result = soup.find_all("div", {"class":"search-result"})[0]
	# 标题信息
	headOne = result.find_all('h1')
	if not headOne:
		return "搜索失败 检查地铁站名是否正确"
	headOne = headOne[0]
	output = output + headOne.get_text() +":\n"
	lineList = result.find_all('table')[0]
	allTr = lineList.find_all('tr')
	for tr in allTr:
		# 如果是车站
		station = tr.find_all('td', {"class":"station-name"})
		if station:
			output = output + "地铁站：" + station[0].get_text() + "\n"
		else:
			line = tr.find_all('td', {"class":"line-name"})
			# 如果是线路
			if line:
				output = output + "线路：" + line[0].get_text() + "\n"
			else:
				changeStation = tr.find_all('td', {"class":"change-station"})
				# 如果是换乘站
				if changeStation:
					output = output + "换乘站:" + changeStation[0].get_text() + "\n"
				else:
					print("Nothing found")
	# 统计信息
	result_info = result.find_all('div', {"class":"result-info"})[0]
	return output + result_info.get_text()

def searchSubway(origin, destination):
	browser = webdriver.PhantomJS()
	#browser = webdriver.Chrome("C:/chromedriver.exe")
	browser.get('http://bj.bendibao.com/ditie/hc/')
	# 起点输入框
	start_input = browser.find_element_by_class_name('start')
	start_input.send_keys(origin)
	# 终点输入框
	end_input = browser.find_element_by_class_name("end")
	end_input.send_keys(destination)
	# 按下搜索按钮
	search_button = browser.find_element_by_class_name('btn')
	search_button.click()
	return parsePage(browser.page_source)


print("成功加载地铁导航模块!")


