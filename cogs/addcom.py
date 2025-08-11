import discord
from discord.ext import commands, tasks
import json

file_location = "data/customCmd.json"

class addcom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addcom(self, ctx, cmdName, cmdRespon):
        guildID = ctx.guild.id
        writeData(guildID, cmdName, cmdRespon)
        await ctx.send(f"成功新增指令:\t!{cmdName}")
        
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

def writeData(guildID: int, cmdName: str, cmdRespon: str):
    data = readData()
    
    data[guildID] = {
        cmdName : cmdRespon
    }
    
    with open(file_location, "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()