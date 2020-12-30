import time
import date_order

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
            while(ind < len(self.closest) and self.closest[i].compare_event(new_event)):
                index += 1
            self.closest.insert(ind, new_event)

if __name__ == "__main__":
    print("For testing")