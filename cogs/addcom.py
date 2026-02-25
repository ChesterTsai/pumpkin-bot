import discord
from discord.ext import commands, tasks
import json

file_location = "data/customCmd.json"

class addcom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addcom(self, ctx, cmdName, *, cmdRespon):
        """新增/修改指令，用法：addcom [指令名] [指令內容]"""
        guildID = str(ctx.guild.id)
        if str(cmdName).startswith("!"):
            cmdName = cmdName[1:]
        writeData(guildID, cmdName, cmdRespon)
        await ctx.send(f"成功新增指令:\t!{cmdName}")

    @commands.command()
    async def delcom(self, ctx, cmdName):
        """刪除指令，用法：delcom [指令名]"""
        guildID = str(ctx.guild.id)
        if str(cmdName).startswith("!"):
            cmdName = cmdName[1:]
        removeData(guildID, cmdName)
        await ctx.send(f"成功移除指令:\t!{cmdName}")

    @commands.command()
    async def comlist(self, ctx):
        """查看此群的自訂指令"""
        data = readData()
        msg = f"此群的自訂指令列表:\n"
        for guildID in data:
            if ctx.guild.id != int(guildID):
                continue
            for cmdName in data[guildID]:
                msg += f"\t!{cmdName} : {data[guildID][cmdName]}\n"
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        data = readData()

        for guildID in data:
            if msg.guild.id != int(guildID):
                continue
            if not msg.content.startswith("!"):
                continue
            for cmdName in data[guildID]:
                if msg.content[1:] != cmdName:
                    continue
                await msg.channel.send(data[guildID][cmdName])
        

async def setup(bot):
    await bot.add_cog(addcom(bot))

def readData():
    
    try:
        with open(file_location, "r", encoding='utf-8') as f:
            data = json.load(f)
            f.close()
    except FileNotFoundError:
        with open(file_location, 'w', encoding='utf-8') as f:
            f.write("{}")
            data = {}
            f.close()
    return data

def writeData(guildID: str, cmdName: str, cmdRespon: str):
    data = readData()
    
    try:
        bool(data[guildID])
        data[guildID][cmdName] = cmdRespon
    except KeyError:
        data.update({guildID : {cmdName : cmdRespon}})
    
    with open(file_location, "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()

def removeData(guildID: str, cmdName: str):
    data = readData()
    
    del data[guildID][cmdName]
    if not bool(data[guildID]):
        del data[guildID]
    
    with open(file_location, "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()
