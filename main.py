import discord
from discord.ext import commands
from discord.ext import tasks
import time
import datetime
import asyncio

import shutdownMsg
import randomRespons
import guessGame
import diceGame
import moraGame

with open('token.txt') as f:
    TOKEN = f.readline()
    f.close()
client = commands.Bot(command_prefix = '$', intents = discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="你"))
    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] Bot is ready')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return 0

@client.command()
async def shutdown(ctx, reason = ''):
    """關閉機器人，僅機器人維護者可以使用此命令"""
    
    try:
        f = open('Admin.txt', 'r', encoding='utf-8')
        tmp = f.read()
        ADMIN_ID_LIST = tmp.split('\n')
        f.close()
    except FileNotFoundError:
        await ctx.send("建立機器人維護者資料...")
        with open('Admin.txt', 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
    
    if str(ctx.message.author.id) not in ADMIN_ID_LIST:
        await ctx.send('去你媽的沒權限還想把我關掉')
        return 0
    
    await client.change_presence(status=discord.Status.offline)
    await ctx.send(shutdownMsg.shutdown(reason))
    time.sleep(3)
    await client.close()

@client.command()
async def ping(ctx):
    """輸出機器人的延遲"""
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount = 5):
    """清除訊息，僅管理員可以使用，用法: clear [要清除的訊息數量，預設為5]"""
    if ctx.message.author.guild_permissions.administrator:
        amount += 1
        await ctx.channel.purge(limit = amount)
    else:
        await ctx.channel.send('你沒有此權限')

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    """問機器人一個問題，用法: 8ball [問題]"""
    
    await ctx.send(randomRespons._8ball(question))

@client.command(aliases = ['安安', '你好', '嗨', 'HI', 'hi'])
async def Hi(ctx):
    """跟機器人打招呼"""
    await ctx.send(randomRespons.Hi())

@client.command()
async def choice(ctx, *, choic):
    """選擇困難症，讓機器人幫你選擇，用法: choice (問題一) (問題二) [問題三] [問題四]..."""
    await ctx.send(randomRespons.choice(choic))

@client.command()
async def guess(ctx):
    """猜數字小遊戲"""
    starttime = float(time.time())
    
    #check if the author of the text is the same person.
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    await ctx.send("請選擇難度(1:簡單/2:一般/3:困難)")
    difficulty = await client.wait_for("message", check = check)
    difficulty = difficulty.content
    
    match difficulty:
        case "1":
            difficulty = "簡單"
            min, max, chances, totalTimeGiven, giveHint = guessGame.easy()
        case "2":
            difficulty = "一般"
            min, max, chances, totalTimeGiven, giveHint = guessGame.normal()
        case "3":
            difficulty = "困難"
            min, max, chances, totalTimeGiven, giveHint = guessGame.hard()
        case _:
            await ctx.send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 錯誤選項，遊戲結束')
            return 0
    
    ans = guessGame.guessGameAnswer(min, max)
    
    chancesLeft = chances
    
    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家選擇了{difficulty}')
    
    while True:
    
        await ctx.send(f'猜數字({str(min)}~{str(max)}, 輸入0結束遊戲)')
        
        # wait for giving number by the client
        try:
            msg = await client.wait_for("message", check = check, timeout = 4.0)
        except asyncio.TimeoutError:
            await ctx.send(f'想太久了吧！你沒時間了\n正確答案是{str(ans)}')
            print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已超時')

        if msg.content.isdigit():
            msg = int(msg.content)
        else:
            await ctx.send('已接受遊戲中斷請求')
            print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已放棄')
            break

        endtime = float(time.time())
        
        if msg > max or msg < min:
            await ctx.send('已接受遊戲中斷請求')
            print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已放棄')
            return 0
        
        
        if msg != ans and abs(msg - ans) <= giveHint and chancesLeft != 1:
            await ctx.send('**很接近囉**')
        if endtime - starttime > totalTimeGiven:
            await ctx.send(f'你沒時間了\n正確答案是{str(ans)}')
            break
        elif chancesLeft == chances and msg == ans:
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

    if msg >= 1 and msg <= 100:
        await ctx.send('花了{:.2f}秒'.format(endtime - starttime))

@client.command()
async def dice(ctx):
    """骰骰子小遊戲"""
    
    gameMsg, gameResult = diceGame.dice(ctx.author.mention)
    
    await ctx.send(gameMsg)
    
    if gameResult != "playerLose":
        return 0
    
    # If Player Loses
    
    starttime = float(time.time())
    endtime = float(time.time())
    
    while endtime - starttime < 10:
        def check(msg):
            return msg.author == ctx.author

        msg = await client.wait_for("message", check=check, timeout=(10 - (endtime - starttime)))

        endtime = float(time.time())
        if endtime - starttime < 10:
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'你還在被禁言中,剩餘{10 - int(endtime - starttime)}秒')

@client.command()
async def mora(ctx):
    """猜拳小遊戲"""

    playAgain = True

    while playAgain == True:
    
        await ctx.send(f'輸入1:剪刀/2:石頭/3:布, 輸入其他結束遊戲')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        msg = await client.wait_for("message", check=check)
        
        gameMsg, gameResult = moraGame.mora(msg.content)
        
        await ctx.send(gameMsg)
        
        if gameResult != "Tie":
            playAgain = False

client.run(TOKEN)