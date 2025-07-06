import discord
from discord.ext import commands
import random

class _8ball(commands.Cog):
    """問機器人一個問題"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question: str):
        """用法: 8ball [問題]"""
        
        responses = ['這是當然的',
                 '絕對是的阿',
                 '不用想了，一定是',
                 '是的，完全就是',
                 '痾...也許吧',
                 '或許你得再問一次',
                 '現在無法預測',
                 '等等再問一次，我就會告訴你答案了',
                 '不',
                 '完全不可能',
                 '我的回答是「不」',
                 '看起來非常不好']
    
        await ctx.send(f'你問的問題是: {question}\n我的回答是: {random.choice(responses)}')

async def setup(bot):
    await bot.add_cog(_8ball(bot))