from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
import itertools
from itertools import zip_longest
import csv
import io
import pandas as pd

def readData():
    xl = pd.ExcelFile('new working copy 1996-2017draft.xlsx') 
    df1 = xl.parse('new working copy 1996-2017draft')
    sitelat = df1.latitude
    sitelon = df1.longitude
    playerNames = df1.PlayerName
    birthPlaces = df1.BirthPlace

    cityName,popularity = [], []
    for i in range(0,len(birthPlaces)):
        m = 0
        cityToCheck =  birthPlaces[i]
        for x in range(0,len(birthPlaces)):
            if cityToCheck == birthPlaces[x]:
                m = m + 1
            else:
                pass
        popularity.append(m) 

    mergedList =list(zip(birthPlaces, popularity, sitelat, sitelon))
    birthPlaceSet = set(mergedList)
    birthPlacesCleaned = list(birthPlaceSet)

def printToCSV(birthPlacesCleaned):
    rows = (birthPlacesCleaned)
    #print(rows)
    #export_data = zip_longest(*rows, fillvalue = '')
    with io.open('popular citiesV13.csv', 'a', encoding="utf-8", newline='') as csv_file:
        wr = csv.writer(csv_file, lineterminator='\n')
        wr.writerow(['BirthPlaces', "Frequency", 'Latitude', 'Longitude'])
        wr.writerows(rows)

def main():
    cityName, popularity, mergedList, birthPlacesSet, birthPlacesCleaned = readData()
    printToCSV(birthPlacesCleaned)

if '__name__' == '__main__':
    main()