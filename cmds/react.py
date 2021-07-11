import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

class React(Cog_Extension):

	@commands.command()
	async def pic(self,ctx):
		pic = discord.File(jsonData['capoo_pic'][0])
		await ctx.send(file=pic)

	@commands.command()
	async def rand_pic(self,ctx):
		random_pic = random.choice(jsonData['capoo_pic'])
		pic = discord.File(random_pic)
		await ctx.send(file=pic)

	@commands.command()
	async def url_pic(self,ctx):
		random_pic = random.choice(jsonData['url_pic'])
		await ctx.send(random_pic)

	@commands.command()
	async def sayd(self,ctx, *,msg):
		await ctx.message.delete()
		await ctx.send(msg)

	@commands.command()
	async def clean(self, ctx, num:int):
		await ctx.channel.purge(limit=num+1)

def setup(bot):
	bot.add_cog(React(bot))