import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient
import SalesAnalysis as SA



mydb = RDP.addDB()
# mycursor1 = mydb.cursor(buffered=True)
# mycursor2 = mydb.cursor(buffered=True)
mycursor = mydb.cursor(buffered=True)

# change the "FROM" table to the table that needs editing
client = GeocodioClient("567b6d2536413556186219244935e66bedbd9e5")
# RDP.addColumns(mycursor)
# add full address column
# mycursor.execute("UPDATE rental_property.rentaldata2 SET fullAddress=CONCAT(Address,',',City,',',StateOrProvince,',',PostalCode);")



"""
i = 0
for lines in mycursor2:
    if(lines[23] is not None):
        continue
    # lines[22] is fullAddress column
    geocoded_location = client.geocode(lines[22])
    coordination = geocoded_location.coords
    mycursor1.execute("UPDATE rental_property.rentaldata2 SET latitude={}, longitude={} WHERE MLSNumber={};".format(coordination[0], coordination[1],lines[9]))
    # mycursor.execute("UPDATE rental_property.rentaldata2 SET latitude=%f, longitude=%f WHERE MLSNumber=lines[9];"%(coordination[0], coordination[1]))
    mydb.commit()
    i += 1
    if i >= 100:
        break
"""

RDP.geocodeByLine("rental_property.rentaldata2", 2400,mydb)

"""
print(RDP.get_distance(29.4216,90,29.4216,91))
print(RDP.get_distance(29.817,90,29.817,91))
print(RDP.get_distance(30.07094,90,30.07094,91))
print(RDP.get_distance(30.07094,90,30.07094,91))
print(RDP.get_distance(29,-95,30,-95))
print(RDP.get_distance(29,-76,30,-76))
"""

"""
SQL syntax for updating geocode: 

UPDATE rental_property.rentaldata2 as RD2
Join rental_property.temp as temp on  RD2.MLSNumber=temp.MLSNumber
SET RD2.latitude=temp.Latitude
WHERE RD2.latitude is null and RD2.MLSNumber=temp.MLSNumber;
"""

