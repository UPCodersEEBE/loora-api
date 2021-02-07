from datetime import datetime, timedelta

import calendar
import time

# compares an input time with the current time. The action configures what is the
# accepted difference from the input and current time.
# Some formatting is needed due to the time formatting from the device
# if the action to check is "alive" (this means ultrasound detection), the offset
# is 12 hours
# if the action to check is "ping" the offset is set to 10 minutes
def time_check(timeinput, action):
    timein = format_time(timeinput)
    now = datetime.now()

    if action == "alive":
        compare = timein + timedelta(hours=4)
        if datetime.now().hour > 21 and datetime.now().hour < 10:
            return False

    elif action == "ping":
        compare = timein + timedelta(minutes=10)

    if now > compare:
        return True
    else:
        return False

def format_time(timeinput):
    clock = timeinput[:-1].split("T")[1]
    c = clock.split(":")

    date = timeinput.split("T")[0]
    d = date.split("-")

    return datetime(
        int(d[0]), int(d[1]), int(d[2]), int(c[0]), int(c[1]), int(c[2][:2])
    )

def arduino_new_time(action):
    now = datetime.now()
    if action == "alive":
        now -= timedelta(hours=3)
    elif action == "ping":
        now += timedelta(hours=2)
    return str(now).replace(" ","T")+"Z"
