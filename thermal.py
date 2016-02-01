import os
import MySQLdb # need to install 
import time

#DB constants 
HOST = None
USERNAME = None
PSSWRD = None
DB_NAME = None
DB_TABLENAME = None

#Constants
DEBUG = True
SETUP_FILE = "/home/pi/thermalSetup.txt"
FILE_DIR = "/sys/bus/w1/devices/"

#Setup variables init
nodeName = None
zoneID = []
sensorID = []
frequency = 2 # t in seconds

def databaseConnect(host, username, password, dbName):
	db = MySQLdb.connect(host, username, password, dbName)
	return db

# Read in Setup file
def getProperties():
	with open(SETUP_FILE) as setup:
		for line in setup:
			#Ignore redundant parts of file
			line = line.replace(" ", "")
			line = line.replace("\n", "")
			if "=" not in line: continue
			if line.startswith("#"): continue

			if line.startswith("ID"):
				tempSensor = line[3:]
				sensorID.append(tempSensor)
				continue
			elif line.startswith("ZONE"):
				tempZone = line[5:]
				zoneID.append(tempZone)
				continue
			elif line.startswith("NODENAME"):
				nodeName = line[9:]
				continue
			elif line.startswith("POLLRATE"):
				frequency = float(line[9:])
				continue
			elif line.startswith("HOST"):
				HOST = line[5:]
				continue
			elif line.startswith("USERNAME"):
				USERNAME = line[9:]
				continue
			elif line.startswith("PASSWORD"):
				PASSWRD = line[9:]
				continue
			elif line.startswith("DB"):
				DB_NAME = line[3:]
				continue
			elif line.startswith("TABLE"):
				DB_TABLENAME = line[6:]
				continue
			else:
				continue

# Returns in *C
def readTemp(sensor):
    fileLocation = FILE_DIR + sensor + '/w1-slave'
    file = open(fileLoaction, 'r')
    rawTemp = file.read()
    file.close()
    
    temperatureData = rawTemp.split()[-1]
    temperature = float(temperatureData[2:])/1000
    
    return temperature

#Print debug information
def printDebug():
	print("Node Name: %s \n Sensor Poll Rate: %f", nodeName, frequency)
	for i in range(len(zoneID)):
		print("Zones loaded: %s Sensors loaded: %s", zoneID[i], sensor[i])

#Main logic
def main():
	while True:
			alignmentCounter = 0

			for id in sensorID:
				zone = zoneID(alignmentCounter)
				temperature = readTemp(id)
				sql = ("INSERT INTO" + DB_TABLENAME + "(node_name, sensor_id, temperature, zone) VALUES (%s, %s, %s, %s)", (nodeName, id, temperature, zone))

				try:
					cur.execute(*sql)
					database.commit()
				except:
					database.rollback()
					print("Failed to commit to Database")
					
				alignmentCounter += 1

				if DEBUG == True:
					print (zone + " " + id + " " + str(temperature))

				time.sleep(frequency)
					
	cur.close()
	database.close()
	
if __name__ == "__main__":
	#Interface setup
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	
	getProperties()
	
	#Connect to database
	database = databaseConnect(HOST, USERNAME, PSSWRD, DB_NAME)
	cur = db.cursor()
	
	main()

