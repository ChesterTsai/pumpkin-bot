import discord
from discord.ext import commands
import datetime
import time

class shutdown(commands.Cog):
    """關閉機器人，僅機器人維護者可以使用此命令"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def shutdown(self, ctx, reason: str = ''):
        """用法：shutdown [原因]"""
        
        # See if "Admin.txt" exists, if not, create one.
        try:
            f = open('./data/Admin.txt', 'r', encoding='utf-8')
            tmp = f.read()
            ADMIN_ID_LIST = tmp.split('\n')
            f.close()
        except FileNotFoundError:
            await ctx.send("建立機器人維護者資料...")
            with open('./data/Admin.txt', 'w', encoding='utf-8') as f:
                f.write("")
                f.close()
            await ctx.send("建立完成")
        
        
        # actual function
        if str(ctx.message.author.id) not in ADMIN_ID_LIST:
            await ctx.send('去你媽的沒權限還想把我關掉')
            return 0
        
        await self.bot.change_presence(status=discord.Status.offline)
        if reason == '':
            outputMessage = f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 睡了！晚安'
        else:
            outputMessage = f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 基於原因:[{reason}]，所以我要睡了！晚安'
        await ctx.send(outputMessage)
        time.sleep(3)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(shutdown(bot))