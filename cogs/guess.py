import discord
from discord.ext import commands
import random
import time
import datetime
import json

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def guess(self, ctx):
        """猜數字小遊戲"""
        
        #check if the author of the text is the same person.
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("請選擇難度(1:簡單/2:一般/3:困難)")
        difficulty = await self.bot.wait_for("message", check = check)
        difficulty = difficulty.content
        
        match difficulty:
            case "1":
                difficulty = "簡單"
                min, max, chances, timeGiven, giveHint = easy()
            case "2":
                difficulty = "一般"
                min, max, chances, timeGiven, giveHint = normal()
            case "3":
                difficulty = "困難"
                min, max, chances, timeGiven, giveHint = hard()
            case _:
                await ctx.send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} ERROR] 錯誤選項，遊戲結束')
                return 0
        
        chancesLeft = chances
        
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家選擇了{difficulty}')
        
        ans = guessGameAnswer(min, max)
        
        gameModeInfo = f'你選擇了{difficulty}模式，以下是此模式的數值\n'
        gameModeInfo += f'終極密碼範圍:\t{str(min)}~{str(max)}\n'
        gameModeInfo += f'機會:\t{str(chances)}次\n'
        gameModeInfo += f'每次猜數字時間限制:\t{str(timeGiven)}秒\n'
        gameModeInfo += f'跟正確答案差距{str(giveHint)}時會給予「**很接近囉**」的提示\n'
        gameModeInfo += f'進行遊戲？「Y/n」'
        await ctx.send(gameModeInfo)
        
        playerChoice = await self.bot.wait_for("message", check = check)
        playerChoice = playerChoice.content.lower()
        
        if playerChoice != 'y':
            await ctx.send(f'玩家拒絕了遊戲進行')
            print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已拒絕遊戲進行')
            return 0
        
        starttime = float(time.time())
        
        while True:
        
            await ctx.send(f'猜數字({str(min)}~{str(max)}, 輸入0結束遊戲)')
            
            # wait for giving number by the self.bot
            try:
                msg = await self.bot.wait_for("message", check = check, timeout = timeGiven)
            except asyncio.TimeoutError:
                await ctx.send(f'想太久了吧！你沒時間了\n正確答案是{str(ans)}')
                print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已超時')

            if msg.content.isdigit():
                msg = int(msg.content)
            else:
                await ctx.send('已接受遊戲中斷請求')
                print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已放棄')
                break
            
            if msg > max or msg < min:
                await ctx.send('已接受遊戲中斷請求')
                print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已放棄')
                return 0
            
            endtime = float(time.time())
            
            # Give Player a hint
            if msg != ans and abs(msg - ans) <= giveHint and chancesLeft != 1:
                await ctx.send('**很接近囉**')
            
            # Detect if the Player guesses the right number
            if chancesLeft == chances and msg == ans:
                await ctx.send('恭喜! 第一次就猜中!')
                break
            elif chancesLeft >= 1 and msg == ans:
                await ctx.send('恭喜! 答對了!')
                break
            elif chancesLeft > 1 and msg < ans:
                chancesLeft -= 1
                await ctx.send(f'猜大一些\n你還剩{str(chancesLeft)}次機會')
                min = msg
            elif chancesLeft > 1 and msg > ans:
                chancesLeft -= 1
                await ctx.send(f'猜小一些\n你還剩{str(chancesLeft)}次機會')
                max = msg
            elif chancesLeft == 1:
                await ctx.send(f'你沒機會了\n正確答案是{str(ans)}')
                break
            else:
                break

        if msg >= min and msg <= max:
            await ctx.send('花了{:.2f}秒'.format(endtime - starttime))

async def setup(bot):
    await bot.add_cog(Guess(bot))



with open("./data/variables.json", "r", encoding='utf-8') as f:
    data = json.load(f)
    f.close()

# 簡單模式
def easy():
    min, max = data["easy"]["min"], data["easy"]["max"]
    chances = data["easy"]["chances"]
    timeGiven = data["easy"]["timeGiven"]
    giveHint = data["easy"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

# 一般模式
def normal():
    min, max = data["normal"]["min"], data["normal"]["max"]
    chances = data["normal"]["chances"]
    timeGiven = data["normal"]["timeGiven"]
    giveHint = data["normal"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

# 困難模式
def hard():
    min, max = data["hard"]["min"], data["hard"]["max"]
    chances = data["hard"]["chances"]
    timeGiven = data["hard"]["timeGiven"]
    giveHint = data["hard"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

def guessGameAnswer(min, max):
    
    old_ans = data["old_ans"]

    ans = random.randint(min, max)
    RandomTimes = 0
    
    while ans == old_ans:
        ans = random.randint(min, max)
        RandomTimes += 1
    
    if RandomTimes == 0:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 答案:{ans}')
    else:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 答案:{ans} (重骰{RandomTimes}次)')
    
    old_ans = ans
    
    data["old_ans"] = old_ans
    with open("./data/variables.json", "w", encoding='utf-8') as f:
        json.dump(data, f)
        f.close()
    
    return ans