import discord
from discord.ext import commands, tasks
from random import randint
from helper_functions import date_check, time_check, find_channel
from date_control import EventControl, EventInfo
import time

CONFIRM = ["y", "yes", "yep"]

# Setting the command prefix for the bot
client = commands.Bot(command_prefix = '!')
control_events = EventControl()


##########################################################################################
# EVENTS ARE DEFINED IN THIS SECTION
##########################################################################################


# Prepares the first thing the bot does when logged in and ready
@client.event
async def on_ready():
    print("I'm ready, I'm ready, I'm READY!")

    # Start the background tasks
    get_events.start()


# Do things when a message is deleted
@client.event
async def on_message_delete(message):

    # Don't do anything for the bots own message
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


##########################################################################################
# COMMANDS ARE DEFINED IN THIS SECTION
##########################################################################################


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

    server = ctx.guild.name  # Get the name of the server

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
    # This format might be changed later
    await ctx.send("The Date: {}\nThe Time: {} \nThe Description: {}".format(date.content, the_time.content, description.content))
    await ctx.send("Is this correct? (y/n)")

    try:
        confirm = await client.wait_for('message', check=this_check, timeout=15)
    except:
        await ctx.send("I will take that as a no :(")
        return

    if confirm.content.lower() in CONFIRM:
        await ctx.send("Great! We are all set!")

        # Add in the event
        control_events.add_event(date.content, the_time.content, description.content, date.guild.name)

        # For testing purposes, print out the event
        print(*control_events.closest, sep="\n")
        print("List of servers:", control_events.servers, "\n")

    else:
        await ctx.sent("Thats too bad, try again maybe?")


##########################################################################################
# COMMANDS ARE DEFINED IN THIS SECTION
##########################################################################################


# This task will occasionally check the most recent event(s) to alert the appropriate server
@tasks.loop(minutes = 1.0)
async def get_events():

    # Create a temporary event to compare to
    the_time = time.gmtime()

    the_date = "{month}/{day}/{year}".format(month = the_time.tm_mon, day = the_time.tm_mday,
                                        year = the_time.tm_year)
    the_time = "{hour}:{min}".format(hour = the_time.tm_hour, min = the_time.tm_min)

    curr_time = EventInfo(the_date, the_time, "")

    # Store events to be removed later
    to_remove = []

    # Loop through the most recents events to check if the task time has come
    for event in control_events.closest:

        # The event and the current time should be equal
        if curr_time.equal_events(event):

            alert = find_channel(client.guilds, event.group)
            
            # Try to send a reminder to the announcements channel
            await alert.send("REMINDER FOR THE FOLLOWING EVENT!")
            await alert.send(event.description)

            to_remove.append(event)

    # Remove all events that have now been used up
    for item in to_remove:
        control_events.closest.remove(item)

    # Grab events if the closest list is now empty
    if len(control_events.closest) == 0:
        control_events.grab_recent()



client.run('insert token here')