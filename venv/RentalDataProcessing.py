import math
import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient
import SalesAnalysis as SA


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
    mycursor.execute("SELECT * FROM {}".format(table))
    columns = (("fullAddress", "TEXT"), ("latitude", "FLOAT"), ("longitude", "FLOAT"), ("downPayment", "FLOAT"), \
               ("loan", "FLOAT"), ("monthlyMortgage", "FLOAT"), \
               ("annualCashFlow", "FLOAT"), ("COC", "FLOAT"),\
               ("max", "FLOAT"), ("min", "FLOAT"), ("average", "FLOAT"), ("median", "FLOAT"), ("count", "INT"), \
               ("CDOM_Median", "FLOAT"))
    for item in columns:
        try:
            addColumn(mycursor,table,item[0],item[1])
        except:
            continue



# fullAddress method needs to be tested.
# This adds a fullAddress column and data
def fullAddress(mycursor, table,mydb):
    mycursor.execute("UPDATE {} SET fullAddress=CONCAT(Address,',',City,',',StateOrProvince,',',PostalCode);".format(table))
    mydb.commit()
# table: name of table needs geocode
# numberOfAddresses:number of lines user would like to geocode, maximum 2500 per day
# mydb: database object
# API allows 2500 per day
def geocodeByLine(table,numberOfAddresses,mydb):
    client = GeocodioClient("567b6d2536413556186219244935e66bedbd9e5")
    mycursor_all = mydb.cursor(buffered=True)
    mycursor_byLine = mydb.cursor(buffered=True)
    mycursor_all.execute("SELECT fullAddress, latitude,longitude,MLSNumber FROM {}".format(table))
    mycursor_byLine.execute("SELECT fullAddress,latitude,longitude,MLSNumber FROM {}".format(table))
    i = 0
    for lines in mycursor_byLine:
        print(lines[1] is not None)
        if(lines[1] is not None):
            continue
        print(lines[0])
        geocoded_location = client.geocode(lines[0])
        coordination = geocoded_location.coords
        print(coordination)
        mycursor_all.execute("UPDATE {} SET latitude={}, longitude={} WHERE MLSNumber={};".format(table,coordination[0], coordination[1],lines[3]))
        # mycursor.execute("UPDATE rental_property.rentaldata2 SET latitude=%f, longitude=%f WHERE MLSNumber=lines[9];"%(coordination[0], coordination[1]))
        print("UPDATE {} SET latitude={}, longitude={} WHERE MLSNumber={};".format(table,coordination[0], coordination[1],lines[3]))
        mydb.commit()
        i += 1
        if i >= numberOfAddresses:
            break
# calculate distance in mile between two locations, using coordinates

"""
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
"""
# calculate left and right side longitude, up and down side of latitude

"""
def longitudeRange(mycursor,longitude,latitude,r):
    mycursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(userInputTable))
    inputList = list(mycursor)[0]
    r = inputList[4]
    lessLongitude = longitude - r/59.8123
    moreLongitude = longitude + r/59.8123
    lessLatitude = latitude - r/69.115
    moreLatitude = latitude + r / 69.115
    return (lessLongitude, moreLongitude, lessLatitude, moreLatitude)
"""
def coordinatesVariables(mycursor,userInputTable):
    mycursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(userInputTable))
    inputList = list(mycursor)[0]
    r = inputList[4]
    longitudeVariable = r/59.8123
    latitudeVariable = r / 69.115
    return (latitudeVariable,longitudeVariable)