import discord
from discord.ext import commands
from discord.flags import Intents
import json
import random
import os
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

with open('setting.json', mode='r', encoding='utf8') as jsonFile:
	jsonData = json.load(jsonFile)

bot = commands.Bot(command_prefix='!',intents = intents)

@bot.event
async def on_ready():
	print("Bot is online")

# load,reload,unload commands
@bot.command()
async def load(ctx, extension):
	await bot.load_extension(f'cmds.{extension}')
	await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
	await bot.unload_extension(f'cmds.{extension}')
	await ctx.send(f'Unloaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
	await bot.reload_extension(f'cmds.{extension}')
	await ctx.send(f'Reloaded {extension} done.')

async def load_extensions():
	for filename in os.listdir('./cmds'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cmds.{filename[:-3]}')

async def main():
	async with bot:
		await load_extensions()
		await bot.start(jsonData['TOKEN'])

asyncio.run(main())

# if __name__ == "__main__":
# 	bot.run(jsonData['TOKEN'])
