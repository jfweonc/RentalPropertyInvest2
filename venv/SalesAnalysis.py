import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient

def userInput():
    mydb=RDP.addDB()
    mycursor=mydb.cursor(buffered=True)
    downPercent=input("downpayment %:")
    down=float(downPercent)
    interestPercent=input("interest rate:")
    interest=float(interestPercent)
    loanTerms=input("loan needs to be paid over how many years?")
    loanTerm=float(loanTerms)
    mycursor.execute("INSERT INTO rental_property.user_input VALUES ({},{},{})".format(down,interest,loanTerm))
    print(down,interest,loanTerm)
    mydb.commit()
"""
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
"""