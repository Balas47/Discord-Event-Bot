import time
ALL_INFO = 3
MONTH_LIMITS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class EventInfo:

    def __init__(self, date, etime, description):
        """
        This class will keep track of the information necessary for an event. This
        information being the date and time for the event, and the description of
        the event. The timestamp for the creation of the reminder is stored as well
        :param date: The date for the event.
        :param time: The time the event starts.
        :param description: A description of what the event is.
        """
        self.date = date
        self.time = etime
        self.description = description
        self.timestamp = time.gmtime()

        # Gets more specific details for the event
        details = date.split("/")
        if len(details) == ALL_INFO:
            self.month = details[0]
            self.day = details[1]
            self.year = details[2]

        else:
            # If a proper date isn't given, assume a week from now
            self.month = self.timestamp.tm_mon
            self.day = self.timestamp.tm_mday + 7

            # Ensure that a week ahead is in the proper month
            if self.day > MONTH_LIMITS[self.month - 1]:
                self.day -= MONTH_LIMITS[self.month - 1]
                self.month += 1
            self.year = self.timestamp.tm_year
            print("Appropriate Information Not Given For Date: A week from now will"
            "be considered the date")

        details = etime.split(":")
        if len(details) == ALL_INFO:
            self.hour = details[0]
            self.minute = details[1]
            self.seconds = details[2]

        else:
            # If a proper time isn't given, assume the same time
            self.hour = self.timestamp.tm_hour
            self.minute = self.timestamp.tm_min
            self.seconds = self.timestamp.tm_sec
            print("Appropriate Information Not Given For Date")

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

    event = EventInfo(the_date, the_time, description)
    print(event.description)