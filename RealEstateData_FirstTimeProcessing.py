import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient
import SalesAnalysis as SA
import statistics


mydb = RDP.addDB()
mycursor1 = mydb.cursor(buffered=True)
mycursor2 = mydb.cursor(buffered=True)
mycursor = mydb.cursor(buffered=True)

# change the "FROM" table to the table that needs editing
client = GeocodioClient("567b6d2536413556186219244935e66bedbd9e5")
# RDP.addColumns(mycursor)
# add full address column
# mycursor.execute("UPDATE rental_property.rentaldata2 SET fullAddress=CONCAT(Address,',',City,',',StateOrProvince,',',PostalCode);")



# RDP.geocodeByLine("rental_property.rentaldata2", 250,mydb)
# RDP.geocodeByLine("rental_property.salesdata",2200,mydb)



# RDP.fullAddress(mycursor,"rental_property.salesdata",mydb)



SA.userInput()
SA.updateDownLoanMortgage("rental_property.salesdata","rental_property.user_input")
SA.updateRentEstimate(mycursor,mycursor1,mydb)
SA.results(mycursor,mydb)
