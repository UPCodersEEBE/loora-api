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
    clock = timeinput[:-1].split("T")[1]
    c = clock.split(":")

    date = timeinput.split("T")[0]
    d = date.split("-")

    now = datetime.now()

    timein = datetime(
        int(d[0]), int(d[1]), int(d[2]), int(c[0]), int(c[1]), int(c[2][:2])
    )

    if action == "alive":
        compare = timein + timedelta(hours=12)

    elif action == "ping":
        compare = timein + timedelta(minutes=10)

    if now > compare:
        return True
    else:
        return False
