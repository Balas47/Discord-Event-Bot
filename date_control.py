import time
from date_order import EventInfo

class EventControl:

    # Maximum number of recent events to hold in memory
    MAX_RECENT = 100

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
                    group_file.read()

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
                    for i in server_events:
                        group_file.write(i.date + ", ")
                        group_file.write(i.time + ", ")
                        group_file.write(groups + ", ")
                        group_file.write(i.description + "\n")


if __name__ == "__main__":
    print("For testing")

    # Setting up a test controller, and random server names
    my_events = EventControl()
    servers = ["serv1", "serv2", "serv3", "serv4", "serv5"]
    
    # Events will be added in order, but at random intervals
    # This test is expected to take a while... sleep is evil
    from random import randint, choice
    for i in range(100):

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