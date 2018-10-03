# -*- coding: utf-8 -*-
from wxpy import *
import datetime
import time
from subwayNav import searchSubway
from server_weather import getWeather
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from map_api import navigateInfo2
from server_schedule import addReminder
from server_schedule import addReminder2
def loginInfo(me):
	#localtime = time.asctime( time.localtime(time.time()))
	localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	greeting = "机器人开始使用, 时间: "
	me.send(greeting + localtime + "\n" + getWeather("北京"))

#生成日期信息
def dateMsg():
	today = datetime.today()
	return str(today.year) + "年" + str(today.month) + "月" + str(today.day) + "日\n"

SLEEP = False
bot = Bot()

loginInfo(bot.file_helper)

# 添加好友 key value
def addFriend(instruction, friendList):
	inputs = instruction.split(' ',  2)
	friendKey = inputs[1]
	friendValue = inputs[2]
	friends = bot.friends().search(friendValue)
	if len(friends) == 0:
		print('添加好友失败:', friendKey)
		friendList['自己'].send('无法找到好友：' + friendValue)
	else:
		friendList[friendKey] = friends[0]
		print('添加好友成功:', friendKey)
		return friends[0]


# 添加群聊 key value
def addGroup(instruction, friendList):
	inputs = instruction.split(' ',  2)
	GroupKey = inputs[1]
	GroupValue = inputs[2]
	groups = bot.groups().search(GroupValue)
	if len(groups) == 0:
		print('添加群聊失败:', GroupValue)
		friendList['自己'].send('无法找到群聊：' + GroupValue)
	else:
		friendList[GroupKey] = groups[0]
		print('添加群聊成功:', GroupKey)
		return groups[0]

print("获取好友列表中...")
#get friends
friendList = {'自己':bot.file_helper}
zhounan = addFriend("添加好友 周楠 q(0.0)p", friendList)
haoming = addFriend("添加好友 王昊明 王昊明", friendList)
liyuan = addFriend("添加好友 龟哥 龟哥", friendList)
qiwei = addFriend("添加好友 启威 启威狗", friendList)
group = addGroup("添加群聊 家人群 我们爱小鹿", friendList)
westWood = addGroup("添加群聊 281 Westwood 281", friendList)
print("获取好友完毕！")

def showFriends(friendList):
	output = ''
	for key,value in friendList.items():
		output = output + key + '|'
	friendList['自己'].send('当前好友：' + output)

#爸妈群发送天气
def test():
	westWood.send("Test")

def groupWeather():
	group.send(dateMsg() + getWeather("扬州") + getWeather("昆山"))

def morningGroup():
	groupWeather()

def morningZhounan():
	zhounan.send(dateMsg() + getWeather("北京"))

def goodNight():
	zhounan.send("星星：晚上好楠楠，早点睡觉哦！")

def afterWork():
	zhounan.send("星星：下班路上小心哦，晚上吃点东西")





print("添加任务中...")
scheduler = BackgroundScheduler()
scheduler.add_job(morningZhounan, 'cron', minute = "0", hour = "7", start_date= datetime.now())
scheduler.add_job(morningGroup, 'cron', minute = "0", hour = "7", start_date= datetime.now())
scheduler.add_job(goodNight, 'cron', minute = "0", hour = "21", start_date= datetime.now())
scheduler.add_job(afterWork, 'cron', minute = "0", hour = "18", start_date= datetime.now())
#scheduler.add_job(test, 'cron', minute = "29", hour = "14", start_date= datetime.now())
scheduler.start()
print("任务添加完毕")

#响应群
@bot.register([Group], TEXT)
def reply(msg):
	if msg.is_at:
		if "天气怎么样" in msg.text:
			group.send(getWeather("扬州")+getWeather("昆山"))
		elif "导航" in msg.text:
			components = msg.text.split()
			o = components[2]
			d = components[3]
			c = components[4]
			group.send(navigateInfo2(o, d, c))

#响应自己
@bot.register([bot.self],TEXT, except_self=False)
def auto_reply(msg):
	global SLEEP
	global friendList
	global scheduler
	if "off" == msg.text:
		bot.file_helper.send("关闭睡眠模式")
		SLEEP = False
	if SLEEP:
		bot.file_helper.send("睡眠模式中\n")
	elif "on" == msg.text:
		bot.file_helper.send("开启睡眠模式")
		SLEEP = True
	elif "check status" in msg.text:
		bot.file_helper.send("Check:运行正常\n SLEEP:" , SLEEP)	
	elif "天气怎么样" in msg.text:
		bot.file_helper.send(getWeather("北京"))
	elif "小猪" in msg.text:
		result = None
		result = bot.file_helper.send_file('pigs.mp4')
		while result is None:
			print("1  ")
	elif "导航" in msg.text:
		components = msg.text.split()
		o = components[1]
		d = components[2]
		c = components[3]
		bot.file_helper.send(navigateInfo2(o, d, c))
	elif "地铁线路 " in msg.text:
		components = msg.text.split()
		o = components[1]
		d = components[2]
		bot.file_helper.send(searchSubway(o, d))
	elif "给爸妈发送天气" in msg.text:
		group.send(dateMsg() + getWeather("扬州") + getWeather("昆山"))
	elif "给周楠发送天气" in msg.text:
		friendList['周楠'].send(getWeather('北京'))
	elif "定时信息" in msg.text:
		if not addReminder(msg.text, scheduler, friendList):
			friendList['自己'].send("设置失败，检查定时信息格式:  定时信息 小时 分钟 接收人 信息")

	elif "添加好友" in msg.text:
		addFriend(msg.text, friendList)
	elif "添加群聊" in msg.text:
		addGroup(msg.text, friendList)
	elif "全部好友" in msg.text:
		showFriends(friendList)
	else:
		bot.file_helper.send("收到:" + msg.text)

#龟哥
@bot.register([liyuan], TEXT)
def auto_reply(msg):
	if "圣人惠" in msg.text:
		liyuan.send_image('image/image.jpg')
	elif "天气怎么样" in msg.text:
		liyuan.send(getWeather("Beijing"))
	elif "小猪" in msg.text:
		liyuan.send_video('pigs.mp4')
	elif "定时信息" in msg.text:
		if not addReminder2(msg.text, scheduler, friendList, friendList['龟哥']):
			friendList['龟哥'].send("设置失败，检查定时信息格式:  定时信息 小时 分钟 信息")
	elif "导航 " in msg.text:
		components = msg.text.split()
		o = components[1]
		d = components[2]
		c = components[3]
		liyuan.send(navigateInfo2(o, d, c))

#启威
@bot.register([qiwei], TEXT)
def auto_reply(msg):
	if "霞之丘诗羽" in msg.text:
		i = 0
		while i < 5:
			qiwei.send_image('image2.jpg')
			i = i + 1




#周楠
@bot.register([zhounan], TEXT)
def auto_reply(msg):
	global SLEEP
	if SLEEP:
		zhounan.send("睡着啦，醒来回复你哦")
	elif "导航 " in msg.text:
		components = msg.text.split()
		o = components[1]
		d = components[2]
		c = components[3]
		zhounan.send(navigateInfo2(o, d, c))
	elif "你" in msg.text and "是猪" in msg.text:
		zhounan.send("来自星星机器人: 你才是猪，周楠是小猪仔")
	elif "天气怎么样" in msg.text:
		zhounan.send(getWeather("北京"))
	elif "嘻嘻" in msg.text:
		zhounan.send("傻笑楠楠")
	elif "地铁线路 " in msg.text:
		components = msg.text.split()
		o = components[1]
		d = components[2]
		zhounan.send(searchSubway(o, d))

#embed()
bot.join()
