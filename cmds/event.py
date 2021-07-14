import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

class Event(Cog_Extension):
	@commands.Cog.listener()
	async def on_member_join(self,member):
		print(f'{member}join!')
		channel = self.bot.get_channel(int(jsonData['Main_channel']))
		await channel.send(f'{member}join!')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		print(f'{member}leave!')
		channel = self.bot.get_channel(int(jsonData['Main_channel']))
		await channel.send(f'{member}leave!')
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.content == '...':
			await msg.channel.send('你才點點點，你全家點點點= =')

		# if msg.content == 'peko' and msg.author != self.bot.user: #!!!防止無限循環
		# 	await msg.channel.send('peko')

		if msg.content == 'capoo' and msg.author != self.bot.user: #!!!防止無限循環
			await msg.channel.send('capoo')

		if msg.content.endswith('peko') and msg.author != self.bot.user:
			await msg.channel.send('好油喔 peko')
		

def setup(bot):
	bot.add_cog(Event(bot))