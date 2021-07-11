import discord
from discord.ext import commands
import json
import random

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

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')

@bot.command()
async def pic(ctx):
    pic = discord.File(jsonData['capoo_pic'][0])
    await ctx.send(file=pic)

@bot.command()
async def rand_pic(ctx):
    random_pic = random.choice(jsonData['capoo_pic'])
    pic = discord.File(random_pic)
    await ctx.send(file=pic)

@bot.command()
async def url_pic(ctx):
    random_pic = random.choice(jsonData['url_pic'])
    await ctx.send(random_pic)

bot.run(jsonData['TOKEN'])
