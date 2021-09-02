import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import command
from core.classes import Cog_Extension
import json, asyncio, datetime

import urllib.request as req

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

class Task(Cog_Extension):
	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs)
		self.my_background_task.start()

	async def on_ready(self):
		print("on ready")

	@tasks.loop(seconds=60)
	async def my_background_task(self):
		self.channel = self.bot.get_channel(882597035411386388)
		# await self.channel.send("task loop")
		localDataPath = jsonData['lang_live_status']
		with open(localDataPath, 'r', encoding='utf8') as rf:
			localData = json.load(rf)
		for k, v in localData.items():
			# embed.add_field(name=k, value=v, inline=False)
			newData = getLiveJSON(v['id'])
			dicData = json.loads(newData)
			live_info = dicData['data']['live_info']
			if langLiveNotify(live_info) == 1:
				liveRoomUrl = "https://www.lang.live/room/" + live_info['pretty_id']
				await self.channel.send(live_info['nickname'] + " 開台了\n" + liveRoomUrl)

	@my_background_task.before_loop
	async def before_my_task(self):
		await self.bot.wait_until_ready()

def setup(bot):
	bot.add_cog(Task(bot))