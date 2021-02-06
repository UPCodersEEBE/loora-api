from datetime import datetime, timedelta

import calendar
import time


def time_check(timeinput):
    clock = timeinput[:-1].split("T")[1]
    c = clock.split(":")

    date = timeinput.split("T")[0]
    d = date.split("-")

    now = datetime.now()
    # now = datetime.strftime(datetime.utcnow(),"%H:%M:%S") #output: 11:12:12

    timein = datetime(
        int(d[0]), int(d[1]), int(d[2]), int(c[0]), int(c[1]), int(c[2][:2])
    )
    # timein = "10:12:34"
    compare = timein + timedelta(hours=12)

    if now > compare:
        return True
    if now < compare:
        return False


# print(time_check("2022-01-01T00:00:00Z"))

# print(time_check("2021-01-01T00:00:00Z"))
