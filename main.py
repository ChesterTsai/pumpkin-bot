"""
# to generate "requirements.txt", do:
# pipreqs /path/to/project
"""

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="你"))
    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] Bot is ready')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return 0

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())