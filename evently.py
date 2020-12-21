import discord
from discord.ext import commands

# Setting the command prefix for the bot
client = commands.Bot(command_prefix = '!')

# Prepares the first thing the bot does when logged in and ready
@client.event
async def on_ready():
    print("I'm ready, I'm ready, I'm READY!")

client.run('insert token here')