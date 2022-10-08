import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

class Event(Cog_Extension):
	@commands.Cog.listener()
	async def on_member_join(self,member):
		guild = member.guild
		role = member.guild.get_role(703676601010880633)
		await member.send(f"歡迎加入 {guild} 伺服器!")
		await member.add_roles(role)		

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		await member.send(f"你離開了 {member.guild} 伺服器。")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self,info):
		source = jsonData['roles']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		if info.message_id == 866975390589255690:
			for k, v in data.items():
				if str(info.emoji) == k:
					guild = self.bot.get_guild(info.guild_id)
					role = guild.get_role(int(v))
					await info.member.add_roles(role)
					await info.member.send(f"你在 {guild.name} 取得了 {role} 身分組!")
		if info.message_id == 1028282045434175581:
			guild = self.bot.get_guild(info.guild_id)
			await info.member.send(f"{info.emoji}\n 貼圖名: {info.emoji.name}\n ID: {info.emoji.id}")
					

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, info):
		source = jsonData['roles']
		with open(source, mode='r', encoding='utf8') as rf:
			data = json.load(rf)
		if info.message_id == 866975390589255690:
			for k, v in data.items():
				print(info.emoji)
				if str(info.emoji) == k:
					guild = self.bot.get_guild(info.guild_id)
					user = guild.get_member(info.user_id)
					role = guild.get_role(int(v))
					await user.remove_roles(role)
					await user.send(f"你在 {guild.name} 移除了 {role} 身分組!")

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.content == '...':
			await msg.channel.send('你才點點點，你全家點點點= =')

		if msg.content == 'capoo' and msg.author != self.bot.user: #!!!防止無限循環
			await msg.channel.send('capoo')

		if msg.content.endswith('peko') and msg.author != self.bot.user:
			await msg.channel.send('好油喔 peko')

		if msg.content == '<:AOV:866962499604840469>':
			await msg.channel.send(f"<@&745307828167901304>, {str(msg.author)[:-5]} 糾團打傳說啦！快跟上！")
		
		if msg.content == '<:Apex:866962310874136587>':
			await msg.channel.send(f"<@&779587792669638656>, {str(msg.author)[:-5]} 正在糾團！特務們快跟上腳步！")

async def setup(bot):
	await bot.add_cog(Event(bot))