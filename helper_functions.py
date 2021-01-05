DATE = 3
TIME = 2

CHANNEL = "announcements"

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


# Goes through the servers that the bot is in to find the text channel to 
# send the event reminder to.
def find_channel(servers, goal_name):

    # Go through the guilds to find the right one
    for guild in servers:

        # If the guild has been found, find the appropriate text channel (announcements)
        if guild.name == goal_name:

            for channel in guild.text_channels:

                # If the channel was found, return the actual channel object
                if channel.name == CHANNEL:
                    return channel