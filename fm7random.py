import random
import sqlite3
import re

# Open Connection
connec = sqlite3.connect("Data.db")
cursor = connec.cursor()

# Get Table Sizes and Make list variables for comparision.
cursor.execute("SELECT * FROM Cars")
carlistlimit = len(cursor.fetchall())
cursor.execute("SELECT * FROM Tracks")
tracklistlimit = len(cursor.fetchall())
cursor.execute("SELECT * FROM Tracks")
tracklist = re.sub(r"[(),']", "", str(cursor.fetchall()))
cursor.execute("SELECT * FROM NightTrack")
nightlist = re.sub(r"[(),']", "", str(cursor.fetchall()))
cursor.execute("SELECT * FROM RainTrack")
rainlist = re.sub(r"[(),']", "", str(cursor.fetchall()))
cursor.execute("SELECT * FROM WeatherType")
weatherlistlimit = len(cursor.fetchall())

# Randomize Car and Track Index
carindex = random.randrange(1, carlistlimit, 1)
trackindex = random.randrange(1, tracklistlimit, 1)

# select Car and Track from database and remove extra special characters
cursor.execute(f"SELECT CarName FROM Cars WHERE IDNo = {carindex}")
selectcar = re.sub(r"[(),']", "", str(cursor.fetchone()))
cursor.execute(f"SELECT TrackName FROM Tracks WHERE IDNo = {trackindex}")
selecttrack = re.sub(r"[(),']", "", str(cursor.fetchone()))


# Set condition based on Track selection
selectcondition = ""
selecttrack = "Ba"
if selecttrack in rainlist and selecttrack in nightlist:
    conditionrandom = random.randrange(0, 9, 1)
    if conditionrandom <= 3:
        selectcondition = "Day"
    elif conditionrandom < 6 and conditionrandom > 3:
        selectcondition = "Night"
    else:
        selectcondition = "Rain"
elif selecttrack in rainlist:
    conditionrandom = random.randrange(1, 10, 1)
    if conditionrandom > 5:
        selectcondition = "Day"
    else:
        selectcondition = "Rain"
elif selecttrack in nightlist:
    conditionrandom = random.randrange(1, 10, 1)
    if conditionrandom > 5:
        selectcondition = "Day"
    else:
        selectcondition = "Night"
elif selecttrack in tracklist:
    selectcondition = "Day"
# Should catch cases of the track selection not being in the database
else:
    print("Not sure how this happened, but the randomly selected track doesn't exist in the database")
    quit()

# If the condition is set to Rain, select the three options used for the race and their respective probabilities
selectweather = []
weatherprobability = []
if selectcondition == "Rain":
    for i in range(3):
        weatherindex = random.randrange(1, weatherlistlimit, 1)
        cursor.execute(f"SELECT Weather FROM WeatherType WHERE IDNo = {weatherindex}")
        weatherhold = re.sub(r"[(),']", "", str(cursor.fetchone()))
        selectweather.append(weatherhold) 
        # selectweather.append(random.choice(weatherlist))
        if i > 0:
            weatherprobability.append(random.randrange(0,100,20))

# Print a message based on the selected condition, including the car, track and condition (with weather options if Rain is picked)
if selectcondition == "Rain":
    prtmessage = f"Your car is the {selectcar}. The track is {selecttrack}. You may be racing in the {selectcondition}. Weather selections are {selectweather[0]}, {selectweather[1]} at {weatherprobability[0]}% probability, and {selectweather[2]} at {weatherprobability[1]}% probability"
elif selectcondition == "Night":
    prtmessage = f"Your car is the {selectcar}. The track is {selecttrack}. You will be racing at {selectcondition}."
else:
    prtmessage = f"Your car is the {selectcar}. The track is {selecttrack}. You will be racing during the {selectcondition}."
print(prtmessage)