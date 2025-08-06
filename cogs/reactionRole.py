import discord
from discord.ext import commands
import json

class reactionRole(commands.Cog):
    """
        點一下反應以加入身分組
        警告：拜託別把機器人身分組拉到最上面，給他高於自動給的身分組就好
        Warning: Please DO NOT make the bot role the highest role,
        only make it higher than the reaction role
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addRole(self, ctx):

        if not ctx.message.author.guild_permissions.administrator:
            await ctx.channel.send('你沒有此權限')
            return
        
        #check if the author of the text is the same person.
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("請輸入要加入反應的訊息ID")
        messageID = await self.bot.wait_for("message", check = check)
        messageID = messageID.content
        
        await ctx.send("請輸入貼圖ID")
        emoji_id = await self.bot.wait_for("message", check = check)
        emoji_id = int(emoji_id.content)
        
        await ctx.send("請輸入身分組名稱")
        role_name = await self.bot.wait_for("message", check = check)
        role_name = role_name.content
        
        writeData(messageID, emoji_id, role_name)
        await ctx.send("寫入成功!")
    
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

def readData():
    
    try:
        with open("./data/reactionRole.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            f.close()
    except FileNotFoundError:
        with open("./data/reactionRole.json", 'w', encoding='utf-8') as f:
            f.write("")
            data = ""
            f.close()
    return data

def writeData(messageID :str, emoji_id :int, role_name :str):
    data = readData()
    
    data[messageID] = {
        "emoji_id": emoji_id,
        "role_name": role_name
    }
    
    with open("./data/reactionRole.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()