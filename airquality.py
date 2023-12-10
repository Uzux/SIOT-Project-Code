import time
from datetime import datetime
import requests
from bson.json_util import dumps
import simple_sds011

sleepInterval = 5

# Endpoint and API Key
url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-makfy/endpoint/data/v1/action/"
API_KEY = "kw6ke7m5ErHviy5VqxjPBIFchx1ffMNL8JuOI9vC9i9locwXtpcNw79bD2ljiq1V"

# PM Sensor Setup
pm = simple_sds011.SDS011('/dev/ttyUSB0')
pm.mode = simple_sds011.MODE_PASSIVE

def getSensorData():
    documentToAdd = {}

    # Get data from sensor
    result = pm.query()
    pmTwoFive = result["value"]["pm2.5"]
    pmTen = result["value"]["pm10.0"]
    
    # Get time now
    datetimeNow = datetime.today().replace(microsecond=0)
    
    # JSON format for data
    documentToAdd = {
        "device": "Raspberry Pi",
        "timestamp": datetimeNow,
        "PM2_5": pmTwoFive,
        "PM10": pmTen,
    }
    print(documentToAdd)
    return documentToAdd

def insertOne(document):
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': API_KEY, 
    }

    # Desinate where the data goes on MongoDB
    payload = dumps({
        "dataSource": "SIOT",
        "database": "SIOTData",
        "collection": "Air Quality Data",
        "document": document
    })
    response = requests.request("POST", url + "insertOne", headers=headers, data=payload)
    if response.status_code >= 200 and response.status_code < 300:
        print("Successfully Inserted")
    else:
        print("Response: (" + str(response.status_code) + ") msg =" + str(response.text))
        print("Error insertOne")
    response.close

while True:
    document = getSensorData()
    insertOne(document)
    if document["PM2_5"] >= 100:
        time.sleep(300/document["PM2_5"])
    else:
        time.sleep(sleepInterval)