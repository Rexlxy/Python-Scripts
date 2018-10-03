from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
def reminder(receiver, myself, msg):
	try:
		receiver.send(msg)
		myself.send("已发送提醒，内容：" + msg)
	except:
		myself.send("发送提醒失败")

# 一次性任务
flag_date = 0
# 循环任务
flag_interval = 1
# 定时任务
# 定时任务 小时 分钟 接收人 信息
flag_cron = 2

# def scheduleReminder(receiver, myself, msg, ):
# 	if flag == flag_date:
# 		pass
# 	elif flag == flag_interval:
# 		pass
# 	elif flag == flog_cron:
# 		pass
# 	else:
# 		myself.send("任务类型有误")
# 		


# 定时信息 小时 分钟 接收人 信息
def addReminder(instruction, scheduler, friendList):
	inputs = instruction.split(' ', 4)
	input_hour = inputs[1]
	try:
		# 转化成中国小时
		cn_hour  = (int(input_hour) + 16) % 24
		input_minute = inputs[2]
		input_receiver = inputs[3]
		input_msg = inputs[4]
		myself = friendList['自己']
		# get the actual receiver object
		receiver = friendList[input_receiver]
		print('找到接收人')
		if receiver is None:
			print('接收人不存在')
			myself.send("接收人不存在！")
			return False
		scheduler.add_job(func = reminder, args = (receiver, myself, input_msg,), trigger = 'cron', minute = input_minute, hour = cn_hour, start_date = datetime.now())
		print('完成添加任务')
		myself.send("设置完毕, " + input_hour + "点 " + input_minute + "分 " + "接收人：" + input_receiver + " 信息：" + input_msg)
	except:
		return False
	
	return True

# 定时信息 小时 分钟 信息
def addReminder2(instruction, scheduler, friendList, receiver):
	inputs = instruction.split(' ', 3)
	input_hour = inputs[1]
	try:
		# 转化成中国小时
		cn_hour  = (int(input_hour) + 16) % 24
		input_minute = inputs[2]
		input_msg = inputs[3]
		myself = friendList['自己']
		scheduler.add_job(func = reminder, args = (receiver, myself, input_msg,), trigger = 'cron', minute = input_minute, hour = cn_hour, start_date = datetime.now())
		print('完成添加任务')
		receiver.send("设置完毕, " + input_hour + "点 " + input_minute + "分 信息：" + input_msg)
	except:
		return False
	
	return True