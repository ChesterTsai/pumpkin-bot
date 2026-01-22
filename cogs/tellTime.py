from discord.ext import commands, tasks
import discord
import datetime
import time

class tellTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tellTimeLoop.start()

    @commands.command()
    async def subTime(self, ctx):
        """訂閱機器人報時"""
        channelID = ctx.channel.id
        writeData(channelID)
        await ctx.send("已訂閱機器人報時")

    @commands.command()
    async def unsubTime(self, ctx):
        """取消訂閱機器人報時"""
        channelID = ctx.channel.id
        removeData(channelID)
        await ctx.send("已取消訂閱機器人報時")

    @tasks.loop(seconds = 1)
    async def tellTimeLoop(self):
        subbedChannel = readData()
        print(subbedChannel)
        if str(datetime.datetime.now().strftime("%m,%d,%H,%M,%S")) == "01,01,00,00,00":
            msg = f'今年已經過了100%，新年快樂！'
            await self.bot.change_presence(activity=discord.CustomActivity(name=msg))
            for channelID in subbedChannel:
                if channelID.isdigit():
                    return
                await self.bot.get_channel(int(channelID)).send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] {msg}')
            time.sleep(1)
        if int(time.time()) % 315576 == 0:
            msg = f'今年已經過了{int((time.time() / 315576) % 100)}%'
            await self.bot.change_presence(activity=discord.CustomActivity(name=msg))
            for channelID in subbedChannel:
                if channelID.isdigit():
                    return
                await self.bot.get_channel(int(channelID)).send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] {msg}')
            time.sleep(1)

    @tellTimeLoop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(tellTime(bot))

def readData():
    try:
        f = open("./data/subTime.txt", "r", encoding="utf-8")
        tmp = f.read()
        data = tmp.split("\n")
        f.close()
    except FileNotFoundError:
        f = open("./data/subTime.txt", "w", encoding='utf-8')
        f.write("")
        data = ""
        f.close()
    return data

def writeData(channelID: int):
    data = readData()

    for i in data:
        if i == str(channelID):
            return

    f = open("./data/subTime.txt", "a", encoding='utf-8')
    f.write(str(channelID) + '\n')
    f.close()

def removeData(channelID: int):
    data = readData()
    if str(channelID) in data:
        data.remove(str(channelID))
    data = [x for x in data if x.strip()]
    newData = ""
    for i in data:
        newData = newData + i + "\n"
    f = open("./data/subTime.txt", "w", encoding='utf-8')
    f.write(str(newData))
    f.close()
