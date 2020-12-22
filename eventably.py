import discord
from discord.ext import commands
from random import randint

# Setting the command prefix for the bot
client = commands.Bot(command_prefix = '!')


# Prepares the first thing the bot does when logged in and ready
@client.event
async def on_ready():
    print("I'm ready, I'm ready, I'm READY!")


# Do things when a message is deleted
@client.event
async def on_message_delete(message):

    # Don't do anything for the bots own messages
    if message.author == client.user:
        return
    
    # Send an "omnious" message to that channel
    await message.channel.send("I saw something...")
    print("The following message was deleted")
    print(message.content)
    print("It was written by:", message.author)


# Keep track of members that have joined
@client.event
async def on_member_join(member):
    print(member.name, "has joined the server")


# Keep track of members that have left
@client.event
async def on_member_remove(member):
    print(member.name, "has left the server")


@client.command()
async def egg(ctx):

    # Chance for egg
    chick = randint(0, 100)
    
    # 20% chance for a chick
    if chick < 20:
        await ctx.send("You got a chick! Take care of it :)")

    else:
        await ctx.send("No chick this time :(")

client.run('insert token here')