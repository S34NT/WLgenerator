import pandas as pd
import re


def rankCars(allCars):

    numRows = allCars.shape[0]
    baseRank = 5.0
    theRankings = []

    #TODO: add different base ranks for different models


    for i in range(numRows):

        rank = baseRank
        singleCar = allCars.iloc[i]

        #Adjust the rank by the relative condition of the car
        odometer = singleCar[6]
        bMMR = re.sub("\D", "", singleCar[15])
        aMMR = re.sub("\D", "", singleCar[16])
        lowRange = re.sub("\D", "", singleCar[17])
        highRange = re.sub("\D", "", singleCar[18])
        avgOdom =  re.sub("\D", "", singleCar[19])
        year = singleCar[2]
        CR = singleCar[1]

        #If car has condition report, add the difference between the cars 
        #condition grade and the average condition grade for that model to the rank
        try:

            if(CR == 'Yes'):

                condition = singleCar[9]
                avgCondition = singleCar[20]

                conditionPoints = round((float(condition) - float(avgCondition)), 1)

                if(float(avgCondition) > 0.0):
                    rank += conditionPoints

        except: 
            pass

        try:

            #Add points if the odometer has less than 170,000 miles
            if int(odometer) < 170000:

                rank += .5
        except:
            pass


        #if the car has an average odometer value, add the difference between
        #odometer and the average odometer to the rank
        try:
            if int(avgOdom) != 0:

                odometerPoints = int(avgOdom)/int(odometer)

                rank += odometerPoints
        except:
            pass


        #if the cars adjusted MMR is less than baseMMR but higher than the 
        #low range MMR, increase the rank
        try:
            if(int(aMMR) < int(bMMR) & int(aMMR) > int(lowRange)):

                rank += .9
        except:
            pass


        try:
            #decrease the rank if the car is older than 2000
            if(int(year) < 2000):
                rank -= 1.6
        except:
            pass

        #Adjust the ranks according to the bMMR
        try:
            if(int(aMMR) <= 5000):
                rank += .6
            elif(int(aMMR) <= 6000):
                rank += .4
            elif(int(aMMR) <= 7000):
                rank += .3
            elif(int(aMMR) > 7000):
                rank = 0.0
        except:
            pass
        
        theRankings.append(round(rank, 1))


    return theRankings


            


