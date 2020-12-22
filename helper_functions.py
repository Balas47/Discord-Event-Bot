

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