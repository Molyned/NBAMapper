from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import csv
import io
import webbrowser
from itertools import zip_longest
from geopy.geocoders import Nominatim

def getPlayerNames():
    draftPage = 'https://en.wikipedia.org/wiki/'
    endString = '_NBA_draft'
    playerNamesData = []
    for i in range(1996, 2017):
        year = str(i)
        draftYearPage = [draftPage+year+endString]
        for pg in draftYearPage:
            page = urlopen(pg)
            soup = BeautifulSoup(page, 'html.parser')
            for i in range(0, 60):   
                for d1 in soup.find_all('span', {"class":"fn"})[i].find_all('a')[0:1]:
                    playerName = d1.get_text(strip=True)
                    playerNamesData.append((playerName))

def scrapePlayerPage(playerNamesData):     
    wikiPage = 'https://en.wikipedia.org/wiki/'
    excelData, urlData = [], []
    for i in range(0, 540):
        playerURL = wikiPage + playerNamesData[i]
        # Change Spaces to underscores
        new = ""
        for c in playerURL:
            d = c
            if c == " ":
                d = "_"
            new = new + d
        playerURL = new
        urlData.append(playerURL)
        try:
            page = urlopen(playerURL)
            soup = BeautifulSoup(page, 'html.parser')
            nameC = "BAD"
            for j in range(10):
                tmp = soup.find_all("tr")[j].text
                if "Born" in tmp:
                    nameC = tmp
                    break
        except:
            try:
                playerURL = wikiPage + playerNamesData[i] + " (basketball)"
                # Change Spaces to underscores
                new = ""
                for c in playerURL:
                    d = c
                    if c == " ":
                        d = "_"
                    new = new + d
                playerURL = new
                page = urlopen(playerURL)
                soup = BeautifulSoup(page, 'html.parser')
                nameC = "BADD"
                for j in range(10):
                    tmp = soup.find_all("tr")[j].text
                    if "Born" in tmp:
                        nameC = tmp
                        break
            except:
                nameC = "n/a"
        excelData.append((nameC))
        
def cleanPlayerData(excelData):
    cleanedData = []
    for i in range(0, 540):
        try: 
            playerBirthPlace = excelData[i]
            indexAge = playerBirthPlace.index("age")
            nameCountry =  playerBirthPlace[indexAge+7:]
        except: 
            nameCountry = 'n/a'
        cleanedData.append((nameCountry))

def getLatLon(cleanedData):
    latData, lonData = [], []
    for i in range(0, 540):
        try:
            playerLoc = cleanedData[i]
            geolocator = Nominatim()
            loc = geolocator.geocode(playerLoc)
            lon = (loc.longitude)
        except:
            lon =  'n/a'
        lonData.append((lon))

    for i in range(0, 540):
        try:
            playerLoc = cleanedData[i]
            geolocator = Nominatim()
            loc = geolocator.geocode(playerLoc)
            lat = (loc.latitude)
        except:
            lat =  'n/a'
        latData.append((lat))

def createCSV(playerNamesData, cleanedData, latData, lonData):
    rows = (playerNamesData,cleanedData, latData, lonData)
    export_data = zip_longest(*rows, fillvalue = '')
    with io.open('1996-2017DraftV2.csv', 'a', encoding="utf-8", newline='') as csv_file:
        wr = csv.writer(csv_file, lineterminator='\n')
        wr.writerow(("PlayerName", "BirthPlace", "latitude", 'longitude'))
        wr.writerows(export_data)

def main():
    playerNamesData = getPlayerNames()
    excelData, urlData = scrapePlayerPage(playerNamesData)
    cleanedData = cleanPlayerData(excelData)
    lonData, latData = getLatLon(cleanedData)
    createCSV()

if '__name__' == '__main__':
    main()