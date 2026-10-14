import discord
from discord.ext import commands
import random
import time
import math

DICE_MIN, DICE_MAX = 1, 6
MUTE_SECONDS = 10

PLAYER_WIN = "playerWin"
TIE = "tie"
PLAYER_LOSE = "playerLose"

class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mutedUntil = {}  # 使用者ID -> 禁言到期時間 (time.monotonic)

    def muteRemaining(self, userId):
        """回傳剩餘禁言秒數，沒被禁言或已到期則回傳 0"""
        until = self.mutedUntil.get(userId)
        if until is None:
            return 0
        remaining = until - time.monotonic()
        if remaining <= 0:
            self.mutedUntil.pop(userId, None)
            return 0
        return remaining

    async def isMuted(self, ctx):
        return self.muteRemaining(ctx.author.id) > 0

    async def bot_check(self, ctx):
        # 全域檢查：被禁言的人不能執行任何指令
        # discord.py 會自動註冊/移除這個名稱的方法；True = 放行，所以要把 isMuted 取反
        return not await self.isMuted(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        remaining = self.muteRemaining(message.author.id)
        if remaining <= 0:
            return

        try:
            await message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass
        await message.channel.send(f'你還在被禁言中,剩餘{math.ceil(remaining)}秒')
    
    @commands.command()
    async def dice(self, ctx):
        """骰骰子小遊戲"""
        
        gameMsg, gameResult = diceResult(ctx.author.mention)
        
        await ctx.send(gameMsg)
        
        if gameResult != PLAYER_LOSE:
            return 0
        
        # If Player Loses: 禁言 MUTE_SECONDS 秒
        now = time.monotonic()
        # 順便清掉已到期、之後不會再發言的紀錄
        self.mutedUntil = {uid: t for uid, t in self.mutedUntil.items() if t > now}
        self.mutedUntil[ctx.author.id] = now + MUTE_SECONDS

async def setup(bot):
    await bot.add_cog(dice(bot))



def diceResult(mentionAuthor):
    
    gameMsg = ""
    gameResult = ""

    playerDiceA = random.randint(DICE_MIN, DICE_MAX)
    botDiceA = random.randint(DICE_MIN, DICE_MAX)
    playerDiceB = random.randint(DICE_MIN, DICE_MAX)
    botDiceB = random.randint(DICE_MIN, DICE_MAX)

    playerDiceSum = playerDiceA + playerDiceB
    botDiceSum = botDiceA + botDiceB
    
    gameMsg += f'{mentionAuthor}, 你骰到{playerDiceA}點和{playerDiceB}點' + "\n"
    gameMsg += f'而我骰到{botDiceA}點和{botDiceB}點' + "\n"

    if playerDiceSum > botDiceSum:
        gameMsg += f'{mentionAuthor}, 你贏了! 恭喜'
        gameResult = PLAYER_WIN
    elif playerDiceSum == botDiceSum:
        gameMsg += f'{mentionAuthor}, 我們平手囉!'
        gameResult = TIE
    else:
        gameMsg += f'{mentionAuthor}, 你輸了! 接受懲罰吧'
        gameResult = PLAYER_LOSE
    
    return (gameMsg, gameResult)