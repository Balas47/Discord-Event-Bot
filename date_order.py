import time

DATE_INFO = 3
TIME_INFO = 2
MONTH_LIMITS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class EventInfo:

    def __init__(self, date, etime, description, group=""):
        """
        This class will keep track of the information necessary for an event. This
        information being the date and time for the event, and the description of
        the event. The timestamp for the creation of the reminder is stored as well
        :param date: The date for the event.
        :param time: The time the event starts.
        :param description: A description of what the event is.
        :param group: The group that the event belongs to.
        """
        self.date = date
        self.time = etime
        self.description = description
        self.group = group
        self.timestamp = time.gmtime()

        # Gets more specific details for the event
        details = date.split("/")
        if len(details) == DATE_INFO:
            self.month = int(details[0])
            self.day = int(details[1])
            self.year = int(details[2])

        else:
            # If a proper date isn't given, assume a week from now
            self.month = self.timestamp.tm_mon
            self.day = self.timestamp.tm_mday + 7

            # Ensure that a week ahead is in the proper month
            if self.day > MONTH_LIMITS[self.month - 1]:
                self.day -= MONTH_LIMITS[self.month - 1]
                self.month += 1
            self.year = self.timestamp.tm_year

            self.date = "/".join([str(self.month), str(self.day), str(self.year)])

            print("Appropriate information not given for date: The date is "
            "assumed to be a week from now")

        details = etime.split(":")
        if len(details) == TIME_INFO:
            self.hour = int(details[0])
            self.minute = int(details[1])

        else:
            # If a proper time isn't given, assume the same time
            self.hour = self.timestamp.tm_hour
            self.minute = self.timestamp.tm_min

            self.time = ":".join([str(self.timestamp.tm_hour), str(self.timestamp.tm_min)])
            
            print("Appropriate information not given for date: The time is "
            "assumed to be the current time.")

    def compare_event(self, other_event):
        """
        This funciton compares two events.
        :param other_event: The event to be compared to
        :return: True if the current event is later, false if the current event is sooner.
        """

        # Compare the year/month/day/hour/minute
        if self.year > other_event.year:
            return True
        elif self.month > other_event.month:
            return True
        elif self.day > other_event.day:
            return True
        elif self.hour > other_event.hour:
            return True
        elif self.minute > other_event.minute:
            return True

        else:
            return False

    def equal_events(self, other_event):
        """
        This function conpares two events for equality.
        :param other_event: The event to be compared to.
        :return: True if the events are equal, false otherwise.
        """
        
        # Booleans to make comparison line shorter
        year = self.year == other_event.year
        month = self.month == other_event.month
        day = self.day == other_event.day

        hour = self.hour == other_event.hour
        minute = self.minute == other_event.minute

        return year and month and day and hour and minute


    def __repr__(self):
        """
        Sets up an appropriate string representation of an event
        :return: A string to represent the EventInfo class.
        """

        my_string = "Date: " + self.date
        my_string += "\nTime: " + self.time
        my_string += "\nDescription: " + self.description
        return my_string


if __name__ == "__main__":

    # Get the time, and format the output
    the_time = time.gmtime()
    print("{month}/{day}/{year}".format(month = the_time.tm_mon, day = the_time.tm_mday,
                                        year = the_time.tm_year))
    print("{hour}:{min}:{second}".format(hour = the_time.tm_hour, min = the_time.tm_min, 
                                        second = the_time.tm_sec)) 

    print(type(the_time.tm_year))

    # Save the time as two strings for date and time
    the_date = "{month}/{day}/{year}".format(month = the_time.tm_mon, day = the_time.tm_mday,
                                        year = the_time.tm_year)
    the_time = "{hour}:{min}:{second}".format(hour = the_time.tm_hour, min = the_time.tm_min, 
                                        second = the_time.tm_sec)

    description = input("Give me some sort of description: ")

    # Testing the contructor/defaults
    event = EventInfo(the_date, the_time, description)
    other = EventInfo("", "", "THIS SHOULD BE TRUE")
    print(event.description)
    print(other.description)
    print(other.compare_event(event))
    print(other.time)