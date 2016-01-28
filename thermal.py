import os
import MySQLdb # need to install 
import time

#Interface setup
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#DB constants TODO get from setup file
HOST = 'enter ip/host name'
USERNAME = 'enter username'
PSSWRD = 'enter password'
DB_NAME = ' enter database name'
DB_TABLENAME = "enter table name"

#Constants
DEBUG = True
SETUP_FILE = "/home/pi/thermalSetup.txt"
FILE_DIR = "/sys/bus/w1/devices/"

#Setup variables init
nodeName = ""
zoneID = []
sensorID = []
frequency = 2 # t in seconds

#Connect to database
db = MySQLdb.connect(host=HOST, user=USERNAME, passwd=PSSWRD, db=DB_NAME)
cur = db.cursor()

# Read in Setup file
with open(SETUP_FILE) as setup:
    for line in setup:
        #Ignore redundant parts of file
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        if "=" not in line: continue
        if line.startswith("#"): continue

        if "ID" in line:
            tempSensor = line[3:]
            sensorID.append(tempSensor)
            continue
        elif "ZONE" in line:
            tempZone = line[5:]
            zoneID.append(tempZone)
            continue
        elif "NODENAME" in line:
            nodeName = line[9:]
            continue
        elif "POLLRATE" in line:
            frequency = float(line[9:])
            continue
        else:
            continue

#Print debug information
if DEBUG == True:
    print("Node Name: %s \n Sensor Poll Rate: %f", nodeName, frequency)
    for i in range(len(zoneID)):
        print("Zones loaded: %s Sensors loaded: %s", zoneID[i], sensor[i])

# Returns in C
def readTemp(sensor):
    fileLocation = FILE_DIR + sensor + '/w1-slave'
    file = open(fileLoaction, 'r')
    rawTemp = file.read()
    file.close()
    
    temperatureData = rawTemp.split()[-1]
    temperature = float(temperatureData[2:])/1000
    
    return temperature

#Main loop TODO add a exit clause
while True:
    alignmentCounter = 0

    for id in sensorID:
        zone = zoneID(alignmentCounter)
        temperature = readTemp(id)
        sql = ("INSERT INTO" + DB_TABLENAME + "(node_name, sensor_id, temperature, zone) VALUES (%s, %s, %s, %s)", (nodeName, id, temperature, zone))

        try:
            cur.execute(*sql)
            db.commit()
        except:
            db.rollback()
            print("Failed to commit to Database")
            
        alignmentCounter += 1

        if DEBUG == True:
            print (zone + " " + id + " " + str(temperature))

        time.sleep(frequency)
            
cur.close()
db.close()
