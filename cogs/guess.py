import discord
from discord.ext import commands
import random
import time
import datetime
import json
import asyncio
import os
from pathlib import Path

# guess.py 在 cogs/ 底下，variables.json 在專案根目錄的 data/ 裡
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "variables.json"

# 難度選項 -> (顯示名稱, variables.json 裡的 key)
DIFFICULTIES = {
    "1": ("簡單", "easy"),
    "2": ("一般", "normal"),
    "3": ("困難", "hard"),
}

def now():
    return datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

def writeData(text):
    # 先寫到暫存檔再替換，避免寫到一半當機而弄壞 variables.json
    tmpPath = DATA_PATH.with_name(DATA_PATH.name + ".tmp")
    with open(tmpPath, "w", encoding='utf-8') as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmpPath, DATA_PATH)

class guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 只在載入 cog 時讀一次設定；修改 variables.json 後請 reload 這個 cog
        with open(DATA_PATH, "r", encoding='utf-8') as f:
            self.data = json.load(f)
        self.saveLock = asyncio.Lock()
        self.playing = set()  # 正在玩的 (使用者ID, 頻道ID)

    async def pickAnswer(self, lo, hi):
        """抽出與上一題不同的答案，並記錄起來"""
        old_ans = self.data.get("old_ans")

        if old_ans is not None and lo < hi and lo <= old_ans <= hi:
            # 從「扣掉 old_ans 的範圍」直接抽，不需要重骰迴圈
            ans = random.randint(lo, hi - 1)
            if ans >= old_ans:
                ans += 1
        else:
            ans = random.randint(lo, hi)

        self.data["old_ans"] = ans
        await self.saveData()
        return ans

    async def saveData(self):
        # 檔案寫入丟到 thread，避免卡住 event loop；用 lock 避免多場遊戲同時寫檔
        async with self.saveLock:
            text = json.dumps(self.data, indent = 4)
            await asyncio.to_thread(writeData, text)

    @commands.command()
    async def guess(self, ctx):
        """猜數字小遊戲"""

        playerKey = (ctx.author.id, ctx.channel.id)
        if playerKey in self.playing:
            await ctx.send("你已經在進行一場遊戲了")
            return 0

        self.playing.add(playerKey)
        try:
            await self.playGame(ctx)
        finally:
            self.playing.discard(playerKey)

    async def playGame(self, ctx):
        """實際的遊戲流程"""
        
        #check if the author of the text is the same person.
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("請選擇難度(1:簡單/2:一般/3:困難)")
        reply = await self.bot.wait_for("message", check = check)

        choice = DIFFICULTIES.get(reply.content.strip())
        if choice is None:
            await ctx.send(f'[{now()} ERROR] 錯誤選項，遊戲結束')
            return 0

        difficulty, key = choice
        cfg = self.data[key]
        lo, hi = cfg["min"], cfg["max"]
        chances = cfg["chances"]
        timeGiven = cfg["timeGiven"]
        giveHint = cfg["giveHint"]
        
        chancesLeft = chances
        
        
        ans = await self.pickAnswer(lo, hi)
        
        gameModeInfo = f'你選擇了{difficulty}模式，以下是此模式的數值\n'
        gameModeInfo += f'終極密碼範圍:\t{str(lo)}~{str(hi)}\n'
        gameModeInfo += f'機會:\t{str(chances)}次\n'
        gameModeInfo += f'每次猜數字時間限制:\t{str(timeGiven)}秒\n'
        gameModeInfo += f'跟正確答案差距{str(giveHint)}時會給予「**很接近囉**」的提示\n'
        gameModeInfo += f'進行遊戲？「Y/n」'
        await ctx.send(gameModeInfo)
        
        playerChoice = await self.bot.wait_for("message", check = check)
        playerChoice = playerChoice.content.strip().lower()
        
        if playerChoice != 'y':
            await ctx.send(f'玩家拒絕了遊戲進行')
            return 0
        
        starttime = time.monotonic()
        finished = False  # 遊戲是否正常結束（答對或機會用完）
        endtime = starttime

        while True:

            await ctx.send(f'猜數字({str(lo)}~{str(hi)}, 輸入0結束遊戲)')

            # wait for giving number by the player
            try:
                reply = await self.bot.wait_for("message", check = check, timeout = timeGiven)
            except asyncio.TimeoutError:
                await ctx.send(f'想太久了吧！你沒時間了\n正確答案是{str(ans)}')
                break

            text = reply.content.strip()

            if text == "0":
                await ctx.send('已接受遊戲中斷請求')
                break

            # isdecimal() 與 int() 接受的字元一致；isdigit() 會放行「²」之類而讓 int() 出錯
            num = int(text) if text.isdecimal() else None

            if num is None or num > hi or num < lo:
                await ctx.send(f'請輸入{str(lo)}~{str(hi)}之間的整數（輸入0結束遊戲）')
                continue

            endtime = time.monotonic()

            # Give Player a hint
            if num != ans and abs(num - ans) <= giveHint and chancesLeft != 1:
                await ctx.send('**很接近囉**')

            # Detect if the Player guesses the right number
            if chancesLeft == chances and num == ans:
                await ctx.send('恭喜! 第一次就猜中!')
                finished = True
                break
            elif num == ans:
                await ctx.send('恭喜! 答對了!')
                finished = True
                break
            elif chancesLeft > 1 and num < ans:
                chancesLeft -= 1
                await ctx.send(f'猜大一些\n你還剩{str(chancesLeft)}次機會')
                lo = num
            elif chancesLeft > 1 and num > ans:
                chancesLeft -= 1
                await ctx.send(f'猜小一些\n你還剩{str(chancesLeft)}次機會')
                hi = num
            else:
                # chancesLeft == 1 且猜錯
                await ctx.send(f'你沒機會了\n正確答案是{str(ans)}')
                finished = True
                break

        if finished:
            await ctx.send('花了{:.2f}秒'.format(endtime - starttime))

async def setup(bot):
    await bot.add_cog(guess(bot))
