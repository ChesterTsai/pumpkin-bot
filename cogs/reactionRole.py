import discord
from discord.ext import commands
import json

class reactionRole(commands.Cog):
    """點一下反應以加入身分組"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addRole(self, ctx, messageID :str, emoji_id :int, role_name :str):
        """用法：addRole [訊息ID] [貼圖ID] [身分組名稱]"""
        if ctx.message.author.guild_permissions.administrator:
            writeData(messageID, emoji_id, role_name)
            await ctx.send("寫入成功!")
        else:
            await ctx.channel.send('你沒有此權限')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):        
        data = readData()
        
        for messageID in data:
            if int(messageID) != payload.message_id:
                continue
            member = payload.member
            guild = member.guild # payload.member.guild
            emoji = payload.emoji.id
            
            if emoji != data[messageID]["emoji_id"]:
                continue
            role_name = data[messageID]["role_name"]
            role = discord.utils.get(guild.roles, name = role_name)
            await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        data = readData()
        
        for messageID in data:
            if int(messageID) != payload.message_id:
                continue
            guild = await(self.bot.fetch_guild(payload.guild_id))
            emoji = payload.emoji.id
            
            if emoji != data[messageID]["emoji_id"]:
                continue
            
            role_name = data[messageID]["role_name"]
            role = discord.utils.get(guild.roles, name = role_name)
            
            member = await(guild.fetch_member(payload.user_id))
            if member is None:
                pass
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(reactionRole(bot))


def writeData(messageID :str, emoji_id :int, role_name :str):
    with open("./data/reactionRole.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()
    
    data[messageID] = {
        "emoji_id": emoji_id,
        "role_name": role_name
    }
    
    with open("./data/reactionRole.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()

def readData():
    with open("./data/reactionRole.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()
    return data