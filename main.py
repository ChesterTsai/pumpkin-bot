"""
# to generate "requirements.txt", do:
# pipreqs /path/to/project
"""
#https://discord.com/api/oauth2/authorize?bot_id=915579282439434280&permissions=8&scope=bot

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import datetime
import asyncio
import random
import time

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = '', intents = discord.Intents.all(), case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name=f'今年已經過了{int((time.time() / 315576) % 100)}%'))
    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] Bot is ready')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return 0

async def loadCogOnStartUp():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command(hidden=True)
async def load(ctx, cog: str):
    """load a newly added cog"""
    
    # See if "Admin.txt" exists, if not, create one.
    try:
        f = open('./data/Admin.txt', 'r', encoding='utf-8')
        tmp = f.read()
        ADMIN_ID_LIST = tmp.split('\n')
        f.close()
    except FileNotFoundError:
        await ctx.send("建立機器人維護者資料...")
        with open('./data/Admin.txt', 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
        await ctx.send("建立完成")
    
    if str(ctx.message.author.id) not in ADMIN_ID_LIST:
        await ctx.send("錯誤，不是機器人維護者")
        return 0
    
    await bot.load_extension(f"cogs.{cog}")
    await ctx.send("已載入")

@bot.command(hidden=True)
async def reload(ctx, cog: str):
    """reload certain cog"""
    
    # See if "Admin.txt" exists, if not, create one.
    try:
        f = open('./data/Admin.txt', 'r', encoding='utf-8')
        tmp = f.read()
        ADMIN_ID_LIST = tmp.split('\n')
        f.close()
    except FileNotFoundError:
        await ctx.send("建立機器人維護者資料...")
        with open('./data/Admin.txt', 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
        await ctx.send("建立完成")
    
    if str(ctx.message.author.id) not in ADMIN_ID_LIST:
        await ctx.send("錯誤，不是機器人維護者")
        return 0
    
    await bot.reload_extension(f"cogs.{cog}")
    await ctx.send("已刷新")

@bot.command(hidden=True)
async def unload(ctx, cog: str):
    """unload certain cog"""
    
    # See if "Admin.txt" exists, if not, create one.
    try:
        f = open('./data/Admin.txt', 'r', encoding='utf-8')
        tmp = f.read()
        ADMIN_ID_LIST = tmp.split('\n')
        f.close()
    except FileNotFoundError:
        await ctx.send("建立機器人維護者資料...")
        with open('./data/Admin.txt', 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
        await ctx.send("建立完成")
    
    if str(ctx.message.author.id) not in ADMIN_ID_LIST:
        await ctx.send("錯誤，不是機器人維護者")
        return 0
    
    await bot.unload_extension(f"cogs.{cog}")
    await ctx.send("已取消載入")

async def main():
    async with bot:
        await loadCogOnStartUp()
        await bot.start(TOKEN)

asyncio.run(main())
