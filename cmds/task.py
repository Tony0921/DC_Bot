import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import command
from core.classes import Cog_Extension
import json, asyncio, datetime

# 網頁請求
import urllib.request as req

# chrome webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# HTML解析
import bs4

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

def getLiveJSON(id):
	# https://api.lang.live/langweb/v1/room/liveinfo?room_id=3686713
	url="https://api.lang.live/langweb/v1/room/liveinfo?room_id="+id
	request = req.Request(url, headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
		"user-uid":"2168925"
	})
	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
		print("send!")
	return data

def langLiveNotify(live_info):
	#loaded data
	nickname = live_info['nickname']
	live_status = live_info['live_status']
	#local data
	localDataPath = jsonData['lang_live_status']
	with open(localDataPath, 'r', encoding='utf8') as rf:
		localData = json.load(rf)
	#判斷是否開台
	if localData[nickname]['live_status'] != live_status:
		localData[nickname]['live_status'] = live_status
		with open(localDataPath, 'w', encoding='utf8') as wf:
			wf.write(json.dumps(localData, indent=4))
		if live_status == 1:
			print("開台了")
			return 1
		else:
			print("關台了")
	return 0

async def getLiveTime():
	# 設定chrome
	options = Options()
	options.add_argument("--disable-notifications")
	options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
	
	# 開啟chrome
	chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
	chrome.get("https://zh-tw.facebook.com/AKB48TeamTP")
	await asyncio.sleep(3)

	# 滾動捲軸
	for x in range(1, 3):
		chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		await asyncio.sleep(3)

	scripts = "\
	var elements = document.getElementsByClassName('oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p');\
	for(let i=0;i < elements.length;i++){\
		if(elements[i].innerHTML=='顯示更多'){\
			console.log(elements[i].innerHTML);\
			elements[i].click();\
		}\
	}"

	chrome.execute_script(scripts)
	await asyncio.sleep(1)

	# HTML解析
	root = bs4.BeautifulSoup(chrome.page_source, "html.parser")
	str1 = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m'
	targets = root.find_all('span',{'class':str1})

	total_text = ""
	for target in targets:
		posts = target.find_all('div', {'dir': 'auto'})
		isLive = 0;
		
		for post in posts:
			if post.getText().startswith("#浪Live"):
				isLive = 1;
		date_text = ""
		for post in posts:
			if isLive == 1:
				tmp_text = post.getText()
				if '月' in tmp_text and '日' in tmp_text:
					date_text = tmp_text
				if post.getText().startswith('林于馨'):
					total_text += date_text + "\n"
					total_text += post.getText() +"\n"
					date_text = ""
	chrome.quit()

	return total_text

class Task(Cog_Extension):
	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs)
		self.my_background_task.start()
		self.crawler_task.start()
		

	async def on_ready(self):
		print("on ready")

	@tasks.loop(seconds=60)
	async def my_background_task(self):
		localDataPath = jsonData['lang_live_status']
		with open(localDataPath, 'r', encoding='utf8') as rf:
			localData = json.load(rf)
		for k, v in localData.items():
			newData = getLiveJSON(v['id'])
			dicData = json.loads(newData)
			live_info = dicData['data']['live_info']
			if langLiveNotify(live_info) == 1:
				liveRoomUrl = "https://www.lang.live/room/" + live_info['pretty_id']
				self.channel = self.bot.get_channel(882597035411386388)
				await self.channel.send(live_info['nickname'] + " 開台了\n" + liveRoomUrl)

	@tasks.loop(seconds=60)
	async def crawler_task(self):
		now_time = datetime.datetime.now()
		now_h = now_time.hour
		now_m = now_time.minute
		now_wd = now_time.weekday()+1
		print(now_time)
		if now_wd==3 and now_h==22 and now_m==52:
			result = await getLiveTime()
			self.channel = self.bot.get_channel(945336871804895282)
			print("web crawler success!")
			await self.channel.send(result)

	@my_background_task.before_loop
	async def before_my_task(self):
		await self.bot.wait_until_ready()

def setup(bot):
	bot.add_cog(Task(bot))