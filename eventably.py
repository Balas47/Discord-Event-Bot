import discord
from discord.ext import commands
from random import randint

DATE = 3
TIME = 2
CONFIRM = ["y", "yes", "yep"]

# Check to make sure the date is in the proper format
# More checking to be done soon
def date_check(date):
    date = date.split("/")
    
    # Check if there are 3 "numbers" given
    if len(date) != DATE:
        return False

    elif date[0].isdigit() and date[1].isdigit and date[2].isdigit:
        return True
        
    return False

# Check to make sure the time is in the proper format
# More checking to be done soon
def time_check(time):
    time = time.split(":")

    # Check if there are 2 "numbers" given
    if len(time) != TIME:
        return False

    elif time[0].isdigit() and time[1].isdigit:
        return True

    return False


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


# Determines whether or not an egg results in a chicken
@client.command()
async def egg(ctx):

    # Chance for egg
    chick = randint(0, 100)
    
    # 20% chance for a chick
    if chick < 20:
        await ctx.send("You got a chick! Take care of it :)")

    else:
        await ctx.send("No chick this time :(")


# Gets information about the event with a series of messages
@client.command()
async def event(ctx):

    # First step, get the date
    await ctx.send("Please tell me the date for the event in the format 'mm/dd/yyyy'")

    # Check that the author and the channel are the same
    def this_check(m):
        return m.author == ctx.author and m.channel == ctx.message.channel

    # Get the response
    try:
        date = await client.wait_for('message', check=this_check, timeout=15.0)
    except:
        await ctx.send("I guess not")
        return

    # Check the format
    if not date_check(date.content):
        await ctx.send("Thats not the right format, so a week from now it is")

    # Second step, get the time
    await ctx.send("Please tell me the time for the event in the format 'hh:mm'"
    "\n24 hour time :)")

    # Get the response
    try:
        the_time = await client.wait_for('message', check=this_check, timeout=15.0)
    except:
        await ctx.send("I guess not")
        return

    # Check the format
    if not time_check(the_time.content):
        await ctx.send("Thats not the right format, but I will survive...")

    # Final step, get the description
    await ctx.send("Alright, now just describe the event briefly and we are good to go!")

    # Get the response
    try:
        description = await client.wait_for('message', check=this_check, timeout=30)
    except:
        await ctx.send("We were so close :(")
        return

    # CONFIRM WITH THE USER
    # This particular format will be changed later
    await ctx.send("The Date: {}\nThe Time: {} \n".format(date.content, the_time.content))
    await ctx.send("Is this correct? (y/n)")

    try:
        confirm = await client.wait_for('message', check=this_check, timeout=15)
    except:
        await ctx.send("I will take that as a no :(")
        return

    if confirm.content.lower() in CONFIRM:
        await ctx.send("Great! We are all set!")
    else:
        await ctx.sent("I will take that as a no, try again maybe?")


client.run('insert token here')