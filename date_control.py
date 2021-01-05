import time
from date_order import EventInfo

# Maximum number of recent events to hold in memory
MAX_RECENT = 100

# Indicies for reading in a file
DATE = 0
TIME = 1
SERVER = 2
DESC = 3

class EventControl:

    def __init__(self):
        """
        This class will keep track of all events, storing them in different files and
        lists as necessary based on the total number of events
        """

        self.closest = []  # Keeps track of the 1000(ish) closest events
        
        # Keeps track of the different servers that *theoretically* would use
        # the connected bot
        self.servers = ["default"] 
        self.file_limits = {}  # Keeps track of the range of dates a file contains


    def add_event(self, date, etime, des, server="default"):
        """
        Adds a new event that is to be kept track of, and puts it in its proper order in 
        the list, and potentially to a file if necessary. Uses basic insertion sort.
        :param date: The date that the event takes place.
        :param time: The time that the event takes place.
        :param des: A description of the event.
        :param server: The server that the event belongs to.
        :return: None
        """

        new_event = EventInfo(date, etime, des, server)

        # Get the current time to make sure that we are not adding an already passed event
        the_time = time.gmtime()

        the_date = "{month}/{day}/{year}".format(month = the_time.tm_mon, day = the_time.tm_mday,
                                        year = the_time.tm_year)
        the_time = "{hour}:{min}".format(hour = the_time.tm_hour, min = the_time.tm_min)

        curr_time = EventInfo(the_date, the_time, "")

        # Past events should not be added
        if curr_time.compare_event(new_event):
            print("Past events cannot be added!")
            return


        # Add the server to our list if it doesn't already exist
        if server not in self.servers:
            self.servers.append(server)
        
        # If the list of events is empty, just add it to the list
        if len(self.closest) == 0:
            self.closest.append(new_event)

        # If the event is already in the list, do nothing
        elif new_event in self.closest:
            return

        # Otherwise, put the event in the placement that it belongs
        else:

            ind = 0
            # Keep going through the list until we come across an event that occurs later
            # than the event to be added.
            while(ind < len(self.closest) and not self.closest[ind].compare_event(new_event)):
                ind += 1
            self.closest.insert(ind, new_event)

        # If the maximmum number of events has been reached, store everything, and grab a few
        if len(self.closest) >= MAX_RECENT:
            self.save_events()
            self.grab_recent()


    def save_events(self):
        """
        Saves all of the events being kept track of in various files using the following
        file format:
        mm/dd/yy, hh:mm, server_name, description
        ...
        The list of events currently being held will be cleared
        :return: None
        """
        
        # I want to save a seperate file for each server
        for groups in self.servers:

            file_name = "_".join(groups.split()) + ".event"
            
            # If the file already exists, I want to load it in
            try:
                with open(file_name, "r") as group_file:
                    full_list = group_file.readlines()

                    # Add in the event if it doesn't already exist
                    for event in full_list:
                        event = event.split(", ")
                        event = [item.strip() for item in event]
                        self.add_event(event[DATE], event[TIME], "".join(event[DESC:]), event[SERVER])

            # Otherwise I want to create that file and add in the events being stored
            except IOError:
                print("Creating file:", file_name)
                
            # Go through and get the events that belong to the current server
            server_events = []
            for i in self.closest:
                if i.group == groups:
                    server_events.append(i)
                
            # Add events to their appropriate server file
            with open(file_name, "w") as group_file:
                
                for i in range(len(server_events)):
                    self.closest.remove(server_events[i])

                    group_file.write(server_events[i].date + ", ")
                    group_file.write(server_events[i].time + ", ")
                    group_file.write(groups + ", ")
                    group_file.write(server_events[i].description + "\n")

                    # Keep track of the range of dates in the file
                    if i == 0:
                        self.file_limits[groups] = [server_events[i]]

                    elif i == len(server_events) - 1:
                        self.file_limits[groups].append(server_events[i])

    
    def grab_recent(self):
        """
        This function will loop through all of the appropriate files to grab a certain
        amount of recent events (half of the max) in order to be able to properly keep track
        of all of them. Assumes that the list of recent events is empty
        :return: None 
        """

        # The number of items to be collected from each server, in as much as possible
        collect = MAX_RECENT / 2
        collect = collect // len(self.servers)

        # Each server will have its own file
        for server in self.servers:

            filename = "_".join(server.split()) + ".event"

            try:
                # Open the file and get all of the appropriate information
                with open(filename, "r") as the_file:
                
                    # For as many events as we mean to collect
                    for i in range(int(collect)):
                    
                        # Read in the line and check that it exists
                        event = the_file.readline()
                        if event:
                            event = event.split(", ")
                            event = [item.strip() for item in event]
                            self.add_event(event[DATE], event[TIME], "".join(event[DESC:]), event[SERVER])

            except IOError:
                print(filename, "could not be opened!")


if __name__ == "__main__":
    print("For testing")

    # Setting up a test controller, and random server names
    my_events = EventControl()
    servers = ["serv1", "serv2", "serv3", "serv4", "serv5"]

    # Make sure that past events cannot be added to the events list
    my_events.add_event("1/5/2021", "10:24", "stuff and things")
    
    # Events will be added in order, but at random intervals
    # This test is expected to take a while... sleep is evil
    from random import randint, choice
    for i in range(5):

        # Sleep for a random number of seconds, and choose a random server
        time.sleep(randint(2, 10))
        server = choice(servers)

        # Get the timestamp, and save its date and time as appropriate strings
        my_time = time.gmtime()
        the_date = "{month}/{day}/{year}".format(month = my_time.tm_mon, day = my_time.tm_mday,
                                        year = my_time.tm_year)
        the_time = "{hour}:{min}".format(hour = my_time.tm_hour, min = my_time.tm_min)

        # Add the events, hopefully in order
        my_events.add_event(the_date, the_time, str(i), server)

    # Test to see if the events are saved to the appropriate server files
    my_events.save_events()
    print(my_events.closest)
    print(my_events.file_limits)

    # Test to see if the appropriate number of events are "grabbed" from the files
    my_events.grab_recent()
    print(*my_events.closest, sep="\n")