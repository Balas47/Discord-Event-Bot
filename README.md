# EVENTABLY
## Everyones favorite event tracker bot

Eventably is a discord bot that can be used to keep track of simple events. With a date, a time, and a description, the bot will store the information needed to send a reminder of the event to your discord server when the time is right.

## Requirements

- In order to use the bot you need a discord bot token, which can be retrieved through discords developer portal.

- I recommend that at least Python 3 should be installed onto your machine, along with the discord.py Python API. Documentation for installing and using discord.py can be found here: https://github.com/Rapptz/discord.

- A discord server where the bot has administrator privliges. The server should have a text channel called "announcements", this is the channel that the bot will look for in order to send event reminders to. If the channel is not there, the bot will not be able to send out the event reminders.

## Commands

There are some commands that can be used with this bot (with some more to come... maybe). Reminder, in order to use a command simply send !COMMAND from within the server.

- !help: This command sends you a link to this page :)

- !event: This is the command where you can start giving the bot information about your event, with some safeguards in hand. First the bot will ask for a date, which should be given in the mm/dd/yyyy format (1/5/2021 instead of January 5, 2021 for example). If a date in a different format is given, or if something that was not a date was given (say if you tell it that the date is "greg"), then the bot will assume that the event will be taking place a week from that date. Then, the bot will ask for a time, which should be given in the hh:mm format (12:30 for example). If a time in a different format is given, or if something that was not a time was given (see the example given for the date), then the bot will assume that the event will be taking place at the time that the !event command was sent. Finally, the bot will ask for a description of the event, which is what will be used by the bot when the reminder is sent out. Once all of that information is in, the bot will present it to you, and ask for confirmation, in which case you send "y" if everything is correct. The event will then be stored, and a reminder will be sent to the servers announcement channel when the time for the event has been reached. 

- !egg: This is an "easter" egg of sorts. It has a 20% change of generating an egg... these eggs have no consequence as of now.

## Other features

There are some small things that the bot does as well.

- When members joins or leaves the server, that message will be printed out to the terminal.

- When a message is deleted, the bot will let you know that it was aware of what happened.

- Every minute, the bot will check if an event reminder needs to be sent out. This means that event times can be something odd like 3:27, and the evet will still be sent out at the appropriate time, within a minute at least. 

- By default, the bot keeps track of 100 events. All of the events are ordered from most recent to further away. If there are more than 100 events, then the bot will store all events in various file, one file for each server that the bot is a member of. Saving to, and getting events from files are done automatically by the bot. If the list of events it is keeping track of reaches 0, then the bot will attempt to grab events from files. If the bot is keeping track of more than 100 files, then it will automatically dump all of the events to various files. 

## Some things to be aware of

- If the bot goes down, it does not (as of writing this) automatically grab a list of servers that it used to belong to. This means that if the bot goes down, the event command needs to be called from every server that it belonged to. Once this is done, then the bot will be able to access all of the events that it was keeping track of beforehand.

- When trying to add an event, if the event date/time would have already passed, the event will not be kept track of. However, the bot will not send a message regarding this, the message will be printed out onto the terminal. 