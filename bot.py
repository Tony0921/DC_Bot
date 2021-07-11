import discord
from discord.ext import commands
import json
import random
import os

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	print("Bot is online")

@bot.event
async def on_member_join(member):
	print(f'{member}join!')
	channel = bot.get_channel(int(jsonData['Main_channel']))
	await channel.send(f'{member}join!')

@bot.event
async def on_member_remove(member):
	print(f'{member}leave!')
	channel = bot.get_channel(int(jsonData['Main_channel']))
	await channel.send(f'{member}leave!')

# load,reload,unload commands
@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cmds.{extension}')
	await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cmds.{extension}')
	await ctx.send(f'Unloaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
	bot.reload_extension(f'cmds.{extension}')
	await ctx.send(f'Reloaded {extension} done.')

for filename in os.listdir('./cmds'):
	if filename.endswith('.py'):
		bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
	bot.run(jsonData['TOKEN'])
