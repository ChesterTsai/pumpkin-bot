import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """輸出機器人的延遲"""
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(ping(bot))