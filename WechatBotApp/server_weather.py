from urllib.request import urlopen
from bs4 import BeautifulSoup

def getWeather(city):
	url = ""
	if city == "北京":
		url = "http://www.weather.com.cn/weather/101010100.shtml"
	elif city == "扬州":
		url = "http://www.weather.com.cn/weather/101190601.shtml"
	elif city == "昆山":
		url = "http://www.weather.com.cn/weather/101190404.shtml"
	else:
		return "无服务"
	html = urlopen(url)
	bsObj = BeautifulSoup(html,'html.parser')
	seven_days = bsObj.find_all("ul", {"class":"t clearfix"})[0]
	list = seven_days.find_all("li")
	output = city + "天气：\n"
	for item in list[:2]:
		output += generateOneDayWeather(item)
	return output	

def generateOneDayWeather(item):
	# day of a week
	output = item.find("h1").get_text()
	# output.replace("（", "(")
	# output.replace("）", ")")
	output += " "
	# weather
	output = output + item.find("p", {"class":"wea"}).get_text() + " "
	# temperature
	withTag = item.find("p", {"class":"tem"}).get_text()
	# withTag.replace('<span>', '')
	# withTag.replace('</span>', '')
	#withTag = withTag.replace(' ', '')
	withTag = withTag.replace('\n', '')
	output = output + withTag + '\n'
	return output

print("成功加载天气模块!")
# print(getWeather("北京"))
# print(getWeather("昆山"))