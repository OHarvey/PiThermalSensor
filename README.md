# PiThermalSensor  
Measure Temperature from multiple DS18B20 digital temperature sensors and post data to a SQL database
## Dependancies
* SQL
* MySQLdb    

## How to get started
* Install the SQL Client to the PI: `sudo apt-get install mysql-client`
* Install MySQLdb api to the PI: `sudo apt-get install python-mysqldb`
 

## Database layout
The database that I am using for this program is a VERY simple database no unqiue fields, or primary keys. This is because it suits my needs this way. However there is no stopping you creating your own database more complex then mine. 

* database name = Anything
* Table name = Anything
* columns = `timestamp`[timestamp], `node_name`[text], `zone`[text], `sensor_id`[text], `temperature`[float]

-----------------------------------------------

## Contribute 
PLEASE SUBMIT A PULL REQUEST FOR IMPROVEMENTS! 
