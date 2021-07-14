import discord
from discord.ext import commands
from discord.ext.commands.core import command
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
	async def sayd(self,ctx, *,msg):
		await ctx.message.delete()
		await ctx.send(msg)

	@commands.command()
	async def clean(self, ctx, num:int):
		await ctx.channel.purge(limit=num+1)
		await ctx.send(f"""```diff\n-Delete {num} message.\n```""")

	@commands.command()
	async def pic(self, ctx, name:str):
		source = jsonData['pic_lib']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		try:
			await ctx.send(data[name])
		except KeyError:
			await ctx.send(f'{name} is not in library!')

	@commands.command()
	async def add_pic(self, ctx , name:str, url:str):
		source = jsonData['pic_lib']
		if url.startswith('https://'):
			with open(source, mode='r', encoding='utf8') as rf:
				data = json.load(rf)
			data[name] = url
			with open(source, 'w', encoding='utf8') as wf:
				json.dump(data, wf)
			await ctx.send("Add successed!")
		else:
			await ctx.send("Unsuccessed!")

	@commands.command()
	async def rmv_pic(self, ctx, name:str):
		source = jsonData['pic_lib']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		try:
			del data[name]
			with open(source, 'w', encoding='utf8') as wf:
				json.dump(data, wf)
			await ctx.send("Remove successed!")
		except KeyError:
			await ctx.send(f'{name} is not in library!')

	@commands.command()
	async def rmv_pic_all(self, ctx):
		source = jsonData['pic_lib']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		data = {}
		with open(source, 'w', encoding='utf8') as wf:
			json.dump(data, wf)
		await ctx.send("Library is clear!")

	@commands.command()
	async def pic_lib(self, ctx):
		source = jsonData['pic_lib']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		embed=discord.Embed(title="圖片庫", color=0x00d9ff,timestamp=TWtime.localize(datetime.datetime.now()))
		embed.set_author(name="小煜 Bot")
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Picture_icon_BLACK.svg/1200px-Picture_icon_BLACK.svg.png")
		for k, v in data.items():
			embed.add_field(name=k, value=v, inline=False)
		embed.set_footer(text="Made by Tony Chen")
		await ctx.send(embed=embed)

	@commands.command()
	async def cmd(self,ctx):
		embed=discord.Embed(title="Bot Commands", color=0xfbff00,timestamp=TWtime.localize(datetime.datetime.now()))
		embed.set_author(name="小煜 Bot")
		embed.set_thumbnail(url="https://icon-library.com/images/command-line-512.png")
		embed.add_field(name="!pic [name]", value="URL圖庫圖片", inline=False)
		embed.add_field(name="!add_pic [name] [URL]", value="新增URL圖片", inline=False)
		embed.add_field(name="!rmv_pic [name]", value="刪除URL圖片", inline=False)
		embed.add_field(name="!rmv_pic_all", value="刪除圖庫所有圖片", inline=False)
		embed.add_field(name="!pic_lib", value="查看圖庫", inline=False)
		# embed.add_field(name="!rand_pic", value="圖庫隨機圖片", inline=False)
		# embed.add_field(name="!url_pic", value="網址圖庫隨機圖片", inline=False)
		embed.add_field(name="!sayd [you want to say]", value="機器人幫你說", inline=False)
		embed.add_field(name="!clean [num]", value="清除n筆訊息", inline=False)
		embed.set_footer(text="Made by Tony Chen")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(React(bot))