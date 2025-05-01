from datetime import datetime
from datetime import datetime

def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

def get_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date


def get_time_of_day():
    current_time = datetime.datetime.now().time()
    if 4 <= current_time.hour < 12:
        return "morning"
    elif 12 <= current_time.hour < 18:
        return "afternoon"
    elif 18 <= current_time.hour <= 23:
        return "evening"
    else:
        return "night"

def wish_time_of_day(): 
    time_of_day = get_time_of_day()
    if time_of_day == "morning":
        print("Good Morning!")
    elif time_of_day == "afternoon":
        print("Good Afternoon!")
    elif time_of_day == "evening":
        print("Good Evening!")
    
    else:
        print("It's late, you should go take some rest!")
