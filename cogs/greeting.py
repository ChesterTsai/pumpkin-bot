import discord
from discord.ext import commands
import random

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ['安安', '你好', '嗨', 'HI', 'hi'])
    async def Hi(self, ctx):
        """跟機器人打招呼"""
        
        responses = ['安安你好',
                 '我最近感覺好讚，你呢',
                 '幹你娘閉嘴',
                 '安安阿～',
                 '嗨～',
                 '哈囉，這裡是隻再正常不過的機器人',
                 '哈囉你好嗎，衷心感謝，珍重再見',
                 '嗨，初次見面，你好']
        
        await ctx.send(f'{random.choice(responses)}')

async def setup(bot):
    await bot.add_cog(Greetings(bot))