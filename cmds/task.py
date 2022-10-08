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

def getLiveStatus(live_info):
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
	options.add_argument("--headless")
	options.add_argument("--disable-notifications")
	options.add_argument("--no-sandbox")
	options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
	options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
	
	# 開啟chrome
	chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
	chrome.get("https://zh-tw.facebook.com/AKB48TeamTP")
	await asyncio.sleep(5)

	# 滾動捲軸
	for x in range(1, 2):
		chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		await asyncio.sleep(3)

	scripts = "\
	var elements = document.getElementsByClassName('qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq cxfqmxzd pbevjfx6 innypi6y');\
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
	str1 = 'gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas m2nijcs8 hxfwr5lz k1z55t6l oog5qr5w tes86rjd pbevjfx6 ztn2w49o'
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
					liveTime = post.getText()
					# print(date_text)
					# print(liveTime)
					total_text += date_text + "\n" + liveTime + "\n"
					date_text = ""
	chrome.quit()

	return total_text

class Task(Cog_Extension):
	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs)
		self.my_background_task.start()
		# self.crawler_task.start()

	async def on_ready(self):
		print("on ready")

	def cog_unload(self):
		print("task unload")
		self.my_background_task.cancel()

	@tasks.loop(seconds=60)
	async def my_background_task(self):
		#langLiveNotify
		localDataPath = jsonData['lang_live_status']
		with open(localDataPath, 'r', encoding='utf8') as rf:
			localData = json.load(rf)
		for k, v in localData.items():
			newData = getLiveJSON(v['id'])
			dicData = json.loads(newData)
			live_info = dicData['data']['live_info']
			if getLiveStatus(live_info) == 1:
				liveRoomUrl = "https://www.lang.live/room/" + live_info['pretty_id']
				self.channel = self.bot.get_channel(882597035411386388)
				await self.channel.send(live_info['nickname'] + " 開台了\n" + liveRoomUrl)

		#getLiveTime
		now_time = datetime.datetime.now()
		now_h = now_time.hour
		now_m = now_time.minute
		now_wd = now_time.weekday()+1
		print(now_time)
		timeSetting = jsonData['getLiveTime']
		with open(timeSetting, 'r', encoding='utf8') as rf:
			_time = json.load(rf)
		if now_wd==_time['wd'] and now_h==_time['h'] and now_m==_time['m']:
			result = await getLiveTime()
			print(result)
			self.channel = self.bot.get_channel(945336871804895282)
			print("web crawler success!")
			if result != "":
				await self.channel.send(result)

	@my_background_task.before_loop
	async def before_my_task(self):
		await self.bot.wait_until_ready()

async def setup(bot):
	await bot.add_cog(Task(bot))