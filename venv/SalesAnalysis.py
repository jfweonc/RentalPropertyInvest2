import mysql.connector
import RentalDataProcessing as RDP
import requests
import json
from geocodio import GeocodioClient



#
def userInput():
    mydb=RDP.addDB()
    mycursor=mydb.cursor(buffered=True)
    downPercent=input("downpayment %:")
    down=float(downPercent)
    interestPercent=input("interest rate:")
    interest=float(interestPercent)
    loanTerms=input("loan needs to be paid over how many years?")
    loanTerm=float(loanTerms)
    radiusOfProperties=input("radius:")
    radius=float(radiusOfProperties)
    year_range=input("yearRange:")
    yearRange=float(year_range)
    sqFt_RangePercent=input("sqFtRangePercent")
    sqFtRangePercent=float(sqFt_RangePercent)
    mycursor.execute("INSERT INTO rental_property.user_input VALUES ({},{},{},NULL,{},{},{})"\
                     .format(down,interest,loanTerm,radius,yearRange,sqFtRangePercent))
    print(down,interest,loanTerm,radius,yearRange,sqFtRangePercent)
    mydb.commit()

def updateDownLoanMortgage(salesTable, userInputTable):
    mydb=RDP.addDB()
    mycursor=mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(userInputTable))
    inputList = list(mycursor)[0]
    downPercent = inputList[0]
    interest = inputList[1] / 12
    term = inputList[2] * 12
    factor = monthlyLoanFactor(interest, term)
    mycursor.execute("UPDATE {} SET downPayment=ListPrice*{}".format(salesTable,downPercent))
    print(downPercent)
    mydb.commit()
    mycursor.execute("UPDATE {} SET loan=ListPrice - downPayment".format(salesTable))
    mydb.commit()
    mycursor.execute("UPDATE {} SET monthlyMortgage=loan*{}".format(salesTable,factor))
    mydb.commit()

def monthlyLoan (loan,r,n):
    mortgage = loan * r * pow((1 + r), n) / (pow((1 + r), n) - 1)
    return mortgage

def monthlyLoanFactor(r,n):
    factor = r * pow((1 + r), n) / (pow((1 + r), n) - 1)
    return factor
def monthlyMortgage(userInputTable,mycursor,salesTable,mydb):
    mycursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(userInputTable))
    inputList = list(mycursor)[0]
    downPercent = inputList[0]
    interest = inputList[1] / 12
    term = inputList[2] * 12
    factor = monthlyLoanFactor(interest, term)
    print(1)
    mycursor.execute("UPDATE {} SET monthlyMortgage=loan*{}".format(salesTable,factor))
    mydb.commit()
    print(1)



def rentEstimate(latitudeVariable,yearVariable,sqFtVariablePercent,table):
    mycursor.execute("SELECT TS.MLSNumber,TS.latitude,TS.longitude,TS.YearBuilt,TS.SqFtTotal,TR.latitude,TR.longitude,\
        AVG(TR.ListPrice) as averageRent, MAX(TR.ListPrice) as maxRent, \
        MIN(TR.ListPrice) as minRent, COUNT(TR.ListPrice) as propertyCount, AVG(TR.CDOM_Median) as rentalCDOM\
        FROM rental_property.salesdata as TS, rental_property.rentaldata2 as TR\
        WHERE (TR.latitude between (TS.latitude-{}) and (TS.latitude+{})) \
            AND (TR.YearBuilt between (TS.YearBuilt-{}) and (TS.YearBuilt+{}))\
            AND (TR.SqFtTotal between (TS.SqFtTotal*(1-{})) and (TS.SqFtTotal*(1+{})))\
        GROUP BY TS.MLSNumber;".format(latitudeVariable,latitudeVariable,yearVariable,\
                                       yearVariable,sqFtVariablePercent,sqFtVariablePercent))
    for items in mycursor:
        mycursor1.execute("UPDATE {} SET average={}, count={}, CDOM_Median={} WHERE MLSNumber={}\
        ;".format(table,items[7],items[10],items[11],items[0]))
        print("UPDATE {} SET average={}, count={}, CDOM_Median={} WHERE MLSNumber={}\
        ;".format(table,items[7],items[10],items[11],items[0]))
        mydb.commit()
        mycursor1.execute("SELECT MLSNumber,latitude,longitude,YearBuilt,SqFtTotal FROM rental_property.salesdata")

"""
SQL notes:
Select: all columns needed
    FROM: original data columns, plus distance column
        WHERE: filters based on coordinates, year, SqFt to reduce calculation
    WHERE: distance is less than a range

"""
def rentEstimate1(latitudeVariable,longitudeVariable, yearVariable,sqFtVariablePercent,mycursor,mycursor1,salesTable,mydb):
    mycursor.execute("Select *,AVG(distanceCalculate.ListPrice) as averageRent, MAX(distanceCalculate.ListPrice) as maxRent, \
                        MIN(distanceCalculate.ListPrice) as minRent, COUNT(distanceCalculate.ListPrice) as propertyCount, \
                        AVG(distanceCalculate.CDOM) as rentalCDOM\
                                FROM(SELECT TS.MLSNumber, TR.ListPrice, TR.CDOM,\
                                (select ST_Distance_Sphere(point(TR.longitude, TR.latitude), point(TS.longitude, \
                                TS.latitude))*0.000621371192) as distance\
                                    FROM rental_property.salesdata as TS, rental_property.rentaldata2 as TR\
                                    WHERE (TR.latitude between (TS.latitude-{}) and (TS.latitude+{})) \
                                        AND (TR.longitude between (TS.longitude-{}) and (TS.longitude+{})) \
                                        AND (TR.YearBuilt between (TS.YearBuilt-{}) and (TS.YearBuilt+{}))\
                                        AND (TR.SqFtTotal between TS.SqFtTotal*(1-{}) and TS.SqFtTotal*(1+{}))) as distanceCalculate\
                                WHERE distance < 1\
                                GROUP BY MLSNumber".format(latitudeVariable,latitudeVariable,longitudeVariable,longitudeVariable,\
                                                           yearVariable, yearVariable,sqFtVariablePercent,sqFtVariablePercent))
    for items in mycursor:
        print("UPDATE {} SET average={}, count={}, CDOM_Median={} WHERE MLSNumber={}\
        ;".format(salesTable,items[4],items[7],items[8],items[0]))

        mycursor1.execute("UPDATE {} SET average={}, count={}, CDOM_Median={} WHERE MLSNumber={}\
        ;".format(salesTable,items[4],items[7],items[8],items[0]))

        mydb.commit()

def updateRentEstimate(mycursor,mycursor1,mydb,salesTable="rental_property.salesdata",userInputTable="rental_property.user_input"):
    coordinateVariable = RDP.coordinatesVariables(mycursor,"rental_property.user_input")
    mycursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(userInputTable))
    inputList = list(mycursor)[0]
    latitudeVariable = coordinateVariable[0]
    longitudeVariable = coordinateVariable[1]
    yearVariable = inputList[5]
    sqFtVariablePercent = inputList[6]
    rentEstimate1(latitudeVariable,longitudeVariable,yearVariable,sqFtVariablePercent,mycursor,mycursor1,salesTable,mydb)


def results(mycursor,mydb,salesTable="rental_property.salesdata"):
    mycursor.execute("UPDATE {} SET annualCashFlow = 12 * (average - monthlyMortgage + monthlyInsurance + \
    monthlyPropertyTax + monthlyMaintenance+ monthlyHOA) WHERE average is not NULL".format(salesTable))
    mycursor.execute("UPDATE {} SET COC = annualCashFlow/downPayment".format(salesTable))
    mydb.commit()
