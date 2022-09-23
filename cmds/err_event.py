import discord
from discord.ext import commands
from core.classes import Cog_Extension

import time

class Err_event(Cog_Extension):
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		#error log
		t = time.localtime()
		result = time.strftime("%Y/%m/%d %H:%M:%S ", t)
		f = open("./private_files/err_log.txt", "a")
		f.write(result + str(error) + "\n")
		f.close()
		
		if hasattr(ctx.command, 'on_error'): #若有自己的錯誤處理就跳過
			return

		if isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("參數遺失")
		elif isinstance(error, commands.errors.CommandError):
			await ctx.send("沒有這個指令啦！")
		else:
			await ctx.send(f"""```diff\n-Error.-\n{error}.\n```""")

async def setup(bot):
	await bot.add_cog(Err_event(bot))