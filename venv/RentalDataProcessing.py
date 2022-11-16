import math
import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient


# create database object
def addDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        port="3306",
        database="rental_property"
    )
    return mydb

# this adds columns and types specified by user.
def addColumn(mycursor,table,column,type):
    mycursor.execute("ALTER TABLE {}     ADD COLUMN {} {};".format(table,column,type))

#add missing columns to new tables
def addColumns(mycursor,table):
    columns = (("fullAddress", "TEXT"), ("latitude", "FLOAT"), ("longitude", "FLOAT"), ("downPayment", "FLOAT"), \
               ("loan", "FLOAT"), ("monthlyMortgage", "FLOAT"), ("monthlyInsurance", "FLOAT"), \
               ("monthlyPropertyTax", "FLOAT"), ("monthlyMaintenance", "FLOAT"), ("monthlyHOA", "FLOAT"), \
               ("annualCashFlow", "FLOAT"), ("COC", "FLOAT"), ("sqftX09", "FLOAT"), ("sqftX11", "FLOAT"), \
               ("max", "FLOAT"), ("min", "FLOAT"), ("average", "FLOAT"), ("median", "FLOAT"), ("count", "INT"), \
               ("CDOM_Median", "FLOAT"), ("distanceFrom", "FLOAT"), ("mapIDX", "INT"), ("mapIDY", "INT"))
    for item in columns:
        addColumn(mycursor,table,item[0],item[1])

# fullAddress method needs to be tested.
# This adds a fullAddress column and data
def fullAddress(mycursor, table):
    mycursor.execute("UPDATE table{} SET fullAddress=CONCAT(Address,',',City,',',StateOrProvince,',',PostalCode);".format(table))
# table: name of table needs geocode
# numberOfAddresses:number of lines user would like to geocode, maximum 2500 per day
# mydb: database object
# API allows 2500 per day
def geocodeByLine(table,numberOfAddresses,mydb):
    client = GeocodioClient("567b6d2536413556186219244935e66bedbd9e5")
    mycursor_all = mydb.cursor(buffered=True)
    mycursor_byLine = mydb.cursor(buffered=True)
    mycursor_all.execute("SELECT * FROM {}".format(table))
    mycursor_byLine.execute("SELECT * FROM {}".format(table))
    i = 0
    for lines in mycursor_byLine:
        print(lines[23] is None)
        if(lines[23] is not None):
            continue
        # lines[22] is fullAddress column
        geocoded_location = client.geocode(lines[22])
        coordination = geocoded_location.coords
        mycursor_all.execute("UPDATE rental_property.rentaldata2 SET latitude={}, longitude={} WHERE MLSNumber={};".format(coordination[0], coordination[1],lines[9]))
        # mycursor.execute("UPDATE rental_property.rentaldata2 SET latitude=%f, longitude=%f WHERE MLSNumber=lines[9];"%(coordination[0], coordination[1]))
        mydb.commit()
        i += 1
        if i >= numberOfAddresses:
            break
# calculate distance in mile between two locations, using coordinates
def get_distance(lat_1, lng_1, lat_2, lng_2):
    lng_1, lat_1, lng_2, lat_2 = map(math.radians, [lng_1, lat_1, lng_2, lat_2])
    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1

    temp = (
         math.sin(d_lat / 2) ** 2
       + math.cos(lat_1)
       * math.cos(lat_2)
       * math.sin(d_lng / 2) ** 2
    )
    return 0.621371 * 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))

# calculate left and right side longitude
def longitudeRange(longitude,r):
    left = longitude - r/59.8123
    right = longitude + r/59.8123
    return([left,right])

# calculate up and down side of latitude
def latitudeRange(latitude,r):
    up = latitude - r/69.115
    down = latitude + r / 69.115


