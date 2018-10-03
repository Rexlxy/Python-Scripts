# -*- coding: utf-8 -*-
import json
import requests
import string
# api_url = 'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=39.934,116.329&output=json&pois=1&ak=LljGnSTnZKu0TmSvIqmhw5zwwEt8KrAN&callback=showLocation'

ak = "LljGnSTnZKu0TmSvIqmhw5zwwEt8KrAN"

# url = "http://api.map.baidu.com/geocoder/v2/?location=32.780835,119.457959&output=json&pois=1&ak="+ak

#地理位置 》经纬度
def getLocation(address):
	api_url = "http://api.map.baidu.com/geocoder/v2/?address="+address+"&output=json&ak=" + ak
	result = getResult(api_url)
	location = result['result']['location']
	lat = str(round(location['lat'],6))
	lng = str(round(location['lng'],6))
	return lat+","+lng

#经纬度 》 地理位置 "39.934,116.32"
def getAddress(location):
	api_url = "http://api.map.baidu.com/geocoder/v2/?location="+location+"9&output=json&pois=1&ak="+ak
	result = getResult(api_url)
	return result['result']['formatted_address']

def getResult(url):
	response = requests.get(url)
	result = json.loads(response.content.decode('utf-8'))
	return result

def getDuration(seconds):
	output = ""
	hours = seconds/3600
	minutes = (seconds%3600)/60
	if hours == 0:
		output = str(int(minutes))+"分钟"
	else:
		output = str(int(hours))+"小时"+ str(int(minutes))+"分钟"
	return output

def navigateInfo(origin, destination, city): 
	url = "http://api.map.baidu.com/direction/v1?mode=transit&origin="+origin+"&destination="+destination+"&origin_region="+city+"&destination_region="+city+"&output=json&ak="+ak
	result = getResult(url)
	output = ""
	routes = result['result']['routes']
	index = 1
	for k in routes:
		#print("方案"+str(index)+":")
		output = output + "方案"+str(index)+":\n"
		index += 1
		steps = k['scheme'][0]['steps']
		#print("耗时:"+getDuration(k['scheme'][0]['duration']))
		output = output + "耗时:"+getDuration(k['scheme'][0]['duration']) + "\n"
		for s in steps:
			
			# print("distance:"+str(s[0]['distance'])+"米")
			# typeInt = s[0]['type']
			# if typeInt == 1:
			# 	print("火车")
			# elif typeInt == 2:
			# 	print("飞机")
			# elif typeInt == 3:
			# 	print("公交")
			# elif typeInt == 4:
			# 	print("驾车")
			# elif typeInt == 5:
			# 	print("步行")
			# elif typeInt == 6:
			# 	print("大巴")
			instruction = s[0]['stepInstruction']
			instruction = instruction.replace('<font color="#313233">', '')
			instruction = instruction.replace('</font>', '')
			instruction = instruction.replace('<font color="#7a7c80">', '')
			#print("*"+instruction)
			output = output + "*" + instruction + '\n'
		output = output + "------------------\n"
		#print("---------------------------------------\n")

	return output

def navigateInfo2(origin, destination, city): 
	origin = getLocation(city+origin)
	destination = getLocation(city+destination)
	url = "http://api.map.baidu.com/direction/v2/transit?origin="+origin+"&destination="+destination+"&ak="+ak
	result = getResult(url)
	output = ""
	routes = result['result']['routes']
	index = 1
	for route in routes:
		#print("方案"+str(index)+":")
		output = output + "方案"+str(index)+":\n"
		index += 1
		steps = route['steps']
		#print("耗时:"+getDuration(k['scheme'][0]['duration']))
		output = output + "耗时:"+getDuration(route['duration']) + "\n"
		for s in steps:
			
			# print("distance:"+str(s[0]['distance'])+"米")
			# typeInt = s[0]['type']
			# if typeInt == 1:
			# 	print("火车")
			# elif typeInt == 2:
			# 	print("飞机")
			# elif typeInt == 3:
			# 	print("公交")
			# elif typeInt == 4:
			# 	print("驾车")
			# elif typeInt == 5:
			# 	print("步行")
			# elif typeInt == 6:
			# 	print("大巴")
			instruction = s[0]['instructions']
			instruction = instruction.replace('<font color="#313233">', '')
			instruction = instruction.replace('</font>', '')
			instruction = instruction.replace('<font color="#7a7c80">', '')
			#print("*"+instruction)
			output = output + "*" + instruction + '\n'
		output = output + "---------------------------------\n"
		#print("---------------------------------------\n")

	return output

print("成功加载百度地图Api模块!")
# print(navigateInfo2("外滩","东方明珠","上海"))
# print(getLocation("扬州江都"))
# print(getAddress(getLocation("扬州江都")))

# 
# 
# if response.status_code == 200:
# 	result = json.loads(response.content.decode('utf-8'))
# 	print("Here's your info: ")
# 	print(result['result']['formatted_address'])
	#print(result['result']['routes'][0]['scheme'][0]['steps'])
	# for k, v in result.items():
	# 	print('{0}:{1}'.format(k, v))
# else:
#     print("None")

# address = '北京市'
# url= 'http://api.map.baidu.com/geocoder?output=json&key=f247cdb592eb43ebac6ccd27f796e2d2&address='+str(address)
# response = requests.get(url)
# answer = response.json()
# lon = float(answer['result']['location']['lng'])
# lat = float(answer['result']['location']['lat'])