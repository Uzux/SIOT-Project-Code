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
# 91      2023-11-09 17:16:43+00:00
# 402     2023-11-09 18:10:12+00:00
# 1049    2023-11-09 20:01:21+00:00
# 1174    2023-11-09 20:23:16+00:00
# 1471    2023-11-09 20:36:21+00:00

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
# print(smokingEvents)

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
    # x_scatter.append(smokingEvents['SEvent'][ind])
    # data2 = airQData.query('PM2_5 == @smokingEvents.SEvent[@ind]')
    # y_scatter.append(data2)
    # n_scatter.append(str(smokingEvents['Process'][ind]))

# print(x_scatter)
# print(y_scatter)

# fig, ax = plt.subplots()
# ax.scatter(x_scatter, y_scatter, color='k')
# for i, txt in enumerate(n_scatter):
#     ax.annotate(txt, (x_scatter[i],y_scatter[i]))

# labelLines(plt.gca().get_lines(), zorder=2.5, fontsize=5)
plt.show()