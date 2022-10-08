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

def is_admin(self, ctx):
	guild_id = ctx.author.guild.id
	author_roles = ctx.author.roles
	# 689110558678581261, 703681977798230096
	if(guild_id==689110558678581261):
		for author_role in author_roles:
			if(author_role.id==702904994617098362):
				return 1
	return 0

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
		embed.set_thumbnail(url="https://i.imgur.com/PTo1ktE.png")
		for k, v in data.items():
			embed.add_field(name=k, value=v, inline=False)
		embed.set_footer(text="Made by Tony Chen")
		await ctx.send(embed=embed)

	@commands.command()
	async def cmd(self,ctx):
		source = jsonData['cmd_list']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		embed=discord.Embed(title="Bot Commands", color=0xfbff00,timestamp=TWtime.localize(datetime.datetime.now()))
		embed.set_author(name="小煜 Bot")
		embed.set_thumbnail(url="https://i.imgur.com/JJdbo1G.png")
		for k, v in data.items():
			embed.add_field(name=k, value=v, inline=False)
		embed.set_footer(text="Made by Tony Chen")
		await ctx.send(embed=embed)

	#管理員指令
	@commands.command()
	async def add_emoji_roles(self, ctx, name:str, id:str, role:str):
		guild_id = ctx.author.guild.id
		author_roles = ctx.author.roles
		emoji_str = "<:" + name + ":" + id + ">"
		if(is_admin(self,ctx)==1):
			source = jsonData['roles']
			with open(source, mode='r', encoding='utf8') as rf:
				data = json.load(rf)
			data[emoji_str] = role
			with open(source, 'w', encoding='utf8') as wf:
				json.dump(data, wf, indent = 4)
			await ctx.send("Add successed!")
		else:
			await ctx.send("操作指令權限不足!")

	@commands.command()
	async def rmv_emoji_roles(self, ctx, name:str, id:str, role:str):
		guild_id = ctx.author.guild.id
		author_roles = ctx.author.roles
		emoji_str = "<:" + name + ":" + id + ">"
		if(is_admin(self,ctx)==1):
			source = jsonData['roles']
			with open(source, mode='r', encoding='utf8') as rf:
				data = json.load(rf)
			try:
				del data[emoji_str]
				with open(source, 'w', encoding='utf8') as wf:
					json.dump(data, wf, indent = 4)
				await ctx.send("Remove successed!")
			except KeyError:
				await ctx.send(f'{emoji_str} is not in list!')
		else:
			await ctx.send("操作指令權限不足!")

	@commands.command()
	async def role_list(self,ctx):
		if(is_admin(self,ctx)==1):
			source = jsonData['roles']
			with open(source, mode='r', encoding='utf8') as rf:
				data = json.load(rf)
			embed=discord.Embed(title="Role List", color=0xfb00ff,timestamp=TWtime.localize(datetime.datetime.now()))
			embed.set_author(name="小煜 Bot")
			embed.set_thumbnail(url="https://i.imgur.com/zNvVxnT.png")
			for k, v in data.items():
				embed.add_field(name=k, value=v, inline=False)
			embed.set_footer(text="Made by Tony Chen")
			await ctx.send(embed=embed)
		else:
			await ctx.send("操作指令權限不足!")

	@commands.command()
	async def admin_cmd(self,ctx):
		if(is_admin(self,ctx)==1):
			source = jsonData['admin_cmd_list']
			with open(source, mode='r', encoding='utf8') as rf:
				data = json.load(rf)
			embed=discord.Embed(title="Admin Commends", color=0xff0000,timestamp=TWtime.localize(datetime.datetime.now()))
			embed.set_author(name="小煜 Bot")
			embed.set_thumbnail(url="https://i.imgur.com/tfganEr.png")
			for k, v in data.items():
				embed.add_field(name=k, value=v, inline=False)
			embed.set_footer(text="Made by Tony Chen")
			await ctx.send(embed=embed)
		else:
			await ctx.send("操作指令權限不足!")

async def setup(bot):
	await bot.add_cog(React(bot))