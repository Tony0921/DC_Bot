import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio,datetime

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

		async def interval():
			await self.bot.wait_until_ready()
			self.channal = self.bot.get_channel(882186376555159582)
			while not self.bot.is_closed():
				await self.channel.send("do something")
				await asyncio.sleep(5)

		self.bg_task = self.bot.loop.create_task(interval())

def setup(bot):
	bot.add_cog(Task(bot))