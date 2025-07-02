import discord
from discord.ext import commands
import random
import time
import datetime

class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def dice(self, ctx):
        """骰骰子小遊戲"""
        
        gameMsg, gameResult = diceResult(ctx.author.mention)
        
        await ctx.send(gameMsg)
        
        if gameResult != "playerLose":
            return 0
        
        # If Player Loses
        
        starttime = float(time.time())
        endtime = float(time.time())
        
        while endtime - starttime < 10:
            def check(msg):
                return msg.author == ctx.author

            msg = await self.bot.wait_for("message", check=check, timeout=(10 - (endtime - starttime)))

            endtime = float(time.time())
            if endtime - starttime < 10:
                await ctx.channel.purge(limit = 1)
                await ctx.send(f'你還在被禁言中,剩餘{10 - int(endtime - starttime)}秒')

async def setup(bot):
    await bot.add_cog(dice(bot))



def diceResult(mentionAuthor):
    
    min, max = 1, 6
    gameMsg = ""
    gameResult = ""

    playerDiceA = random.randint(min, max)
    botDiceA = random.randint(min, max)
    playerDiceB = random.randint(min, max)
    botDiceB = random.randint(min, max)

    playerDiceSum = playerDiceA + playerDiceB
    botDiceSum = botDiceA + botDiceB

    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家點數:{playerDiceSum}, 機器人點數:{botDiceSum}')
    
    gameMsg += f'{mentionAuthor}, 你骰到{playerDiceA}點和{playerDiceB}點' + "\n"
    gameMsg += f'而我骰到{botDiceA}點和{botDiceB}點' + "\n"

    if playerDiceSum > botDiceSum:
        gameMsg += f'{mentionAuthor}, 你贏了! 恭喜'
        gameResult = "playerWin"
    elif playerDiceSum == botDiceSum:
        gameMsg += f'{mentionAuthor}, 我們平手囉!'
        gameResult = "tie"
    else:
        gameMsg += f'{mentionAuthor}, 你輸了! 接受懲罰吧'
        gameResult = "playerLose"
    
    return (gameMsg, gameResult)