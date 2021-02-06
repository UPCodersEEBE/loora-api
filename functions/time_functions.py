# how to compare times in python 


import datetime


timeinput = "2022-01-01T00:00:00Z"
clock = timeinput[:-1].split("T")[1]
c = clock.split(":")


date = timeinput.split("T")[0]
d = date.split("-")


now = datetime.datetime.now()
#now = datetime.strftime(datetime.utcnow(),"%H:%M:%S") #output: 11:12:12
timein = datetime.datetime(int(d[0]),int(d[1]), int(d[2]), int(c[0]), int(c[0]), int(c[0]))
#timein = "10:12:34"

if now >  timein:
    print("Time has passed.")
if now < timein:
    print("Time has not passed yet")

