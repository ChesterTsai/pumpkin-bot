import discord
from discord.ext import commands
import random

class Choice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def choice(self, ctx, *, choices: str):
        """選擇困難症，讓機器人幫你選擇，用法: choice (問題一),(問題二),[問題三],[問題四]..."""
        responses = choices.split(',')
        await ctx.send(f'{random.choice(responses)} 是最棒的答案')

async def setup(bot):
    await bot.add_cog(Choice(bot))