import pymongo
from datetime import datetime, timedelta
import pandas as pd
import scipy as sp
import random

# API connection to MongoDB
myclient = pymongo.MongoClient("LINK TO MONGODB DATABASE HERE")
dblist = myclient.list_database_names()
if "SIOTData" in dblist:
    print("The database exists.")
    mydb = myclient["SIOTData"]
    mycol = mydb["Air Quality Data"]

def main(toplim, botlim):
    # Execute the aggregation pipeline and retrieve the results
    results = mycol.find().sort("_id", pymongo.DESCENDING).limit(3000)
    results = list(results)
    airQData = pd.DataFrame(results)

    # Parse Data - Remove Datapoints that age is older than an hour
    airQData = airQData[airQData.timestamp >= (airQData.timestamp.max() - pd.Timedelta(hours=1).floor('H'))]

    # Find Peaks
    peaks = sp.signal.find_peaks(airQData.PM2_5, distance=10, prominence=50)
    PM2_5Peaks = airQData.PM2_5[peaks[0]]

    # Count Peaks
    countPeaks = len(PM2_5Peaks)

    # If peaks >= X number
    messages = [
            "You've got this! Quit smoking and be a healthier you!",
            "Smoking is so last season. Kick the habit!",
            "Think about all the money you'll save when you quit smoking.",
            "Your lungs will thank you for quitting smoking!",
            "You're stronger than those cigarettes. Quit today!",
            "Smoking doesn't make you cool. Quit and be the coolest!",
            "Breaking up with smoking is the best decision you'll ever make!",
            "Life is too short to smoke. Choose a smoke-free life!",
            "You're not a chimney. Time to quit smoking!",
            "Quitting smoking is a sign of true strength. Go for it!"
        ]
    
    if countPeaks >= toplim:
        return("Bro... You really need to chill out! You have smoked " + str(countPeaks) + " times in the last hour!\n" + random.choice(messages))
    elif countPeaks >= botlim:
        return("You have puffed ur vape too many times... " + str(countPeaks) + " times in the last hour to be exact >:C. \n" + random.choice(messages))
    else:
        return