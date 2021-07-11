import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is online")

@bot.event
async def on_member_join(member):
    print(f'{member}join!')
    channel = bot.get_channel(863469068082216981)
    await channel.send(f'{member}join!')

@bot.event
async def on_member_remove(member):
    print(f'{member}leave!')
    channel = bot.get_channel(863469068082216981)
    await channel.send(f'{member}leave!')

bot.run('ODYzNzU5MjY1NjEyNTYyNDky.YOrkgA.ydTXU91EJmEWlJcc_ZEXoKWPcn0')
