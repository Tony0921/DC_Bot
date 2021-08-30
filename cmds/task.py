import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio,datetime
import urllib.request as req

# class Task(Cog_Extension):
#     def __init__(self, *args, **kwargs):
#         super().__init__( *args, **kwargs)

#         async def langliveNotify():
#             await self.bot.wait_until_ready()
#             while not self.bot.is_closed():

#                 pass


def setup(bot):
	bot.add_cog(Task(bot))