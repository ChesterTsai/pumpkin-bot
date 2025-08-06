import json
import requests
import re
import os
import discord
import time
import datetime
from discord.ext import commands, tasks

file_location = "data/youtubedata.json"

class ytMention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytMentionLoop.start()
    
    @commands.command()
    async def ytMention(self, ctx):
        
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.channel.send('你沒有此權限')
            return
        
        #check if the author of the text is the same person.
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("請輸入Youtube帳號代碼(@XXXX)")
        handle = await self.bot.wait_for("message", check = check)
        handle = handle.content
        if handle.startswith("@"):
            handle = handle[1:]
        
        await ctx.send("請輸入頻道名稱(新影片發布時機器人稱呼你的方法)")
        channel_name = await self.bot.wait_for("message", check = check)
        channel_name = channel_name.content
        
        who_to_mention_msg = "你想要通知哪些人？"
        who_to_mention_msg += "\n\t輸入「everyone」 -> 通知所有人"
        who_to_mention_msg += "\n\t輸入「none」 -> 純文字通知"
        who_to_mention_msg += "\n\t輸入身分組ID(@該身分組並在最前面加上一個「/」後enter) -> 通知該身分組"
        await ctx.send(who_to_mention_msg)
        who_to_mention = await self.bot.wait_for("message", check = check)
        who_to_mention = who_to_mention.content
        
        await ctx.send("請接收通知的discord頻道ID")
        notifying_discord_channel = await self.bot.wait_for("message", check = check)
        notifying_discord_channel = int(notifying_discord_channel.content)
        
        writeData(handle, channel_name, who_to_mention, notifying_discord_channel)
        await ctx.send("寫入成功!")
    
    @tasks.loop(seconds=30)
    async def ytMentionLoop(self):
        data = readData()
        
        for youtube_channel in data:
            channel = f"https://www.youtube.com/@{youtube_channel}"
            channel_name = data[youtube_channel]["channel_name"]
            who_to_mention = data[youtube_channel]["who_to_mention"]
            
            match who_to_mention:
                case "everyone":
                    who_to_mention = "@everyone"
                case "none":
                    who_to_mention = ""
                case _:
                    who_to_mention = "<@&" + who_to_mention + ">"
            
            videos = requests.get(channel+"/videos").text
            shorts = requests.get(channel+"/shorts").text
            
            try:
                latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', videos).group()
                latest_shorts_url = "https://www.youtube.com/shorts/" + re.search('(?<="videoId":").*?(?=")', shorts).group()
            except:
                continue
        
            # New Video Mentioning
            if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:

                data[str(youtube_channel)]["latest_video_url"] = latest_video_url

                with open(file_location, "w", encoding='utf-8') as f:
                    json.dump(data, f, indent = 4)
                    f.close()

                discord_channel_id = data[str(youtube_channel)]["notifying_discord_channel"]
                discord_channel = self.bot.get_channel(int(discord_channel_id))

                msg = f"{who_to_mention} {channel_name}發布了新影片!\n{latest_video_url}"

                await discord_channel.send(msg)
                print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] New Video Info Sent!')
        
            # New Shorts Mentioning
            if not str(data[youtube_channel]["latest_shorts_url"]) == latest_shorts_url:

                data[str(youtube_channel)]["latest_shorts_url"] = latest_shorts_url

                with open(file_location, "w", encoding='utf-8') as f:
                    json.dump(data, f, indent = 4)
                    f.close()

                discord_channel_id = data[str(youtube_channel)]["notifying_discord_channel"]
                discord_channel = self.bot.get_channel(int(discord_channel_id))

                msg = f"{who_to_mention} {channel_name}發布了新的shorts!\n{latest_shorts_url}"

                await discord_channel.send(msg)
                print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] New Shorts Info Sent!')
        
        # time.sleep(300)

async def setup(bot):
    await bot.add_cog(ytMention(bot))

def readData():
    
    try:
        with open(file_location, "r", encoding='utf-8') as f:
            data = json.load(f)
            f.close()
    except FileNotFoundError:
        with open(file_location, 'w', encoding='utf-8') as f:
            f.write("")
            data = ""
            f.close()
    return data

def writeData(handle: str, channel_name: str, who_to_mention: str, notifying_discord_channel: int):
    data = readData()
    
    data[handle] = {
        "channel_name": channel_name,
        "who_to_mention": who_to_mention,
        "notifying_discord_channel": notifying_discord_channel
    }
    
    with open(file_location, "w", encoding='utf-8') as f:
        json.dump(data, f, indent = 4)
        f.close()