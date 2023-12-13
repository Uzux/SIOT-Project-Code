from operator import contains
from turtle import width
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines
import re
from datetime import datetime, timedelta

# Read AQ Data
airQData = pd.read_csv(r"SIOTData Before Intervention (9 days).csv")
airQData = airQData.drop(columns=['PM2.5', 'device', '_id'], axis=1) # There is another column called PM2_5

# Find peaks (Smoking Events)
peaks = sp.signal.find_peaks(airQData.PM2_5, distance=10, prominence=50)
PM2_5Peaks = airQData.PM2_5[peaks[0]]
# PM10Peaks = airQData.PM10[peaks[0]]

tsAirQPeaks = pd.to_datetime(airQData.timestamp[peaks[0]], utc=True)

# Read ManicTime Data
manicTData = pd.read_csv(r"ManicTimeData_2023-12-09.csv")

manicTData.Start = pd.to_datetime(manicTData.Start, utc=True)
manicTData.End = pd.to_datetime(manicTData.End, utc=True)

# Find application that was open during smoking event
smokingEvents = pd.DataFrame()
tsPeaks = []
for peak in tsAirQPeaks:
    if not manicTData.query(('Start < @peak < End')).empty:
        data = manicTData.query(('Start < @peak < End'))

        smokingEvents =  pd.concat([smokingEvents, data])
        tsPeaks.append(peak)

# Inserting Smoking event for later analysis
smokingEvents.insert(2, "SEvent", tsPeaks)

# Granulating browser activities
# for ind in smokingEvents.index:
#     m = re.search('- (.+?) - Google Chrome', str(smokingEvents['Name'][ind]))
#     if m:
#         arrName = str(m.group(0)).split("- ")
#         arrName.reverse()
#         smokingEvents['Process'][ind] = str(arrName[1] + "- " + arrName[0])

# Find unique processes and count their frequency
uniqueProcesses = smokingEvents['Process'].value_counts()
print(uniqueProcesses)

smokingEvents = smokingEvents.reset_index()
print(smokingEvents)

# Plotting Data
plt.plot(pd.to_datetime(airQData.timestamp), airQData.PM2_5)
plt.title("Finding Peaks")

[plt.axvline(p, c='C3', linewidth=0.3) for p in tsAirQPeaks]
# [plt.axvline(p, c='C3', linewidth=0.3, label='') for p in smokingEvents]

x_scatter = []
y_scatter = []
n_scatter = []

for ind in smokingEvents.index:
    plt.axvline(smokingEvents['SEvent'][ind], c='b', linewidth=0.1, label=str(smokingEvents['Process'][ind]))
plt.show()