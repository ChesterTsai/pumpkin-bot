import discord
from discord.ext import commands

class clear(commands.Cog):
    """清除訊息，僅管理員可以使用"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def clear(self, ctx, amount: int = 5):
        """用法: clear (要清除的訊息數量，預設為5)"""
        if ctx.message.author.guild_permissions.administrator:
            amount += 1
            await ctx.channel.purge(limit = amount)
        else:
            await ctx.channel.send('你沒有此權限')

async def setup(bot):
    await bot.add_cog(clear(bot))