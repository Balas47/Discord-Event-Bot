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
        
        # If the list of events is empty, just add it to the list
        if len(self.closest) == 0:
            self.closest.append(new_event)

        # Otherwise, put the event in the placement that it belongs
        else:

            ind = 0
            # Keep going through the list until we come across an event that occurs later
            # than the event to be added.
            while(ind < len(self.closest) and not self.closest[ind].compare_event(new_event)):
                ind += 1
            self.closest.insert(ind, new_event)


    def save_events(self):
        """
        Saves all of the events being kept track of in various files using the following
        file format:
        mm/dd/yy, hh:mm, server_name, description
        ...
        :return: None
        """
        
        # I want to save a seperate file for each server
        for groups in servers:

            file_name = groups + ".event"
            
            # If the file already exists, I want to load it in
            try:
                with open(file_name, "r") as group_file:
                    full_list = group_file.readlines()

                    for event in full_list:
                        event = event.split(", ")
                        self.add_event(event[DATE], event[TIME], str(event[DESC:]), event[SERVER])

            # Otherwise I want to create that file and add in the events being stored
            except:
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


if __name__ == "__main__":
    print("For testing")

    # Setting up a test controller, and random server names
    my_events = EventControl()
    servers = ["serv1", "serv2", "serv3", "serv4", "serv5"]
    
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