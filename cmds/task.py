import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension
import json, asyncio, datetime

import urllib.request as req

# def getLiveJSON(id):
# 	# https://api.lang.live/langweb/v1/room/liveinfo?room_id=3686713
# 	url="https://api.lang.live/langweb/v1/room/liveinfo?room_id="+id
# 	request = req.Request(url, headers={
# 		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
# 		"user-uid":"2168925"
# 	})
# 	with req.urlopen(request) as response:
# 		data = response.read().decode("utf-8")
# 	return data

# 882186376555159582
class Task(Cog_Extension):
	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs)
		self.my_background_task.start()

	async def on_ready(self):
		print("on ready")

	@tasks.loop(seconds=60)
	async def my_background_task(self):
		self.channel = self.bot.get_channel(882186376555159582)
		await self.channel.send("task loop")

	@my_background_task.before_loop
	async def before_my_task(self):
		await self.bot.wait_until_ready()

def setup(bot):
	bot.add_cog(Task(bot))