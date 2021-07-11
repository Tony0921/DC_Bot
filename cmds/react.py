import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import datetime
import pytz

TWtime = pytz.timezone('Asia/Taipei')

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

	@commands.command()
	async def cmd(self,ctx):
		embed=discord.Embed(title="Bot Commands", color=0xfbff00,timestamp=TWtime.localize(datetime.datetime.now()))
		embed.set_author(name="Xioa_Yu Bot")
		embed.set_thumbnail(url="https://icon-library.com/images/command-line-512.png")
		embed.add_field(name="!pic", value="特定圖片", inline=False)
		embed.add_field(name="!rand_pic", value="圖庫隨機圖片", inline=False)
		embed.add_field(name="!url_pic", value="網址圖庫隨機圖片", inline=False)
		embed.add_field(name="!sayd [you want to say]", value="機器人幫你說", inline=False)
		embed.add_field(name="!clean [num]", value="清除n筆訊息", inline=False)
		embed.set_footer(text="Made by Tony Chen")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(React(bot))