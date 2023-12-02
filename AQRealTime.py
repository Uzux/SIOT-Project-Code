from discordKaliBot import SendMsg
import pymongo
from datetime import datetime, timedelta
import pandas as pd
import scipy as sp


# API connection to MongoDB
myclient = pymongo.MongoClient("mongodb+srv://uzux:pokemon9@siot.bbvtbv5.mongodb.net/")
dblist = myclient.list_database_names()
if "SIOTData" in dblist:
    print("The database exists.")
    mydb = myclient["SIOTData"]
    mycol = mydb["Air Quality Data"]

# Loop this
# while True:
# Request last 1 hour of Data from API
start = datetime.today() - timedelta(hours=1, minutes=0)
start = start.replace(microsecond=0)
end = datetime.today()
end = end.replace(microsecond=0)

# print(type(start))
# print(type(end))

# Execute the aggregation pipeline and retrieve the results
results = mycol.find().sort("_id", pymongo.DESCENDING).limit(3000)
results = list(results)
airQData = pd.DataFrame(results)

# Parse Data - Remove Datapoints that age is greater than an hour
airQData = airQData[airQData.timestamp >= (airQData.timestamp.max() - pd.Timedelta(hours=1).floor('H'))]
print(airQData)

# Find Peaks
peaks = sp.signal.find_peaks(airQData.PM2_5, distance=10, prominence=50)
PM2_5Peaks = airQData.PM2_5[peaks[0]]

# Count Peaks
countPeaks = len(PM2_5Peaks)

# If peaks >= X number
if countPeaks > 10:
    SendMsg("Bro, stop smoking")