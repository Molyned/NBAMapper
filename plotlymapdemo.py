import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import numpy as np
import pandas as pd
import random
import config

chart_studio.tools.set_credentials_file(config.username, config.api_key)
mapbox_access_token = config.map_key

def makeColours():
    colourList = []
    for x in range(22):
        colourOne = random.randint(1,256)
        colourTwo = random.randint(1,256)
        colourThree = random.randint(1,256)
        # 139,0,139 magenta
        # colourOne = 130+x
        # colourTwo = 0
        # colourThree = 130 + x
        colour = (colourOne, colourTwo, colourThree)
        goodcolour = str(colour)
        realcolour = 'rgb'+goodcolour
        colourList.append((realcolour))

def readData():
    draftClassData, draftYears, latitudeData, longitudeData = [], [], [], []
    xl = pd.ExcelFile('new working copy 1996-2017draft.xlsx') #, encoding = "ISO-8859-1")
    df1 = xl.parse('new working copy 1996-2017draft')
    sitelat = df1.latitude
    sitelon = df1.longitude
    playerNames = df1.PlayerName

    draftYears = []
    for i in range(0, 22):
        draftYear = 1996 + i
        draftYears.append(draftYear)

    n = 60
    for x in range(0,1320,n):
        draftClass = playerNames[x:(x+n)]
        latitude=sitelat[x:(x+n)]
        print(latitude)
        longitude=sitelon[x:(x+n)]
        draftClassData.append(draftClass)
        latitudeData.append(latitude)
        longitudeData.append(longitude)

def plotMap(latitudeData, longitudeData, draftYears, colourList, draftClassData):
    data = []
    for i in range(len(colourList)):
        roundNumber = str(i)
        trace = go.Scattermapbox(
                lat=latitudeData[i],
                lon=longitudeData[i],
                name = str(draftYears[i])+' Class',
                mode='markers',
                marker=dict(
                    size=(i+10)/2,
                    color= colourList[i],
                    opacity=0.7
                ),
                text=draftClassData[i],
                hoverinfo='text')
        data.append(trace)

    layout = go.Layout(
        title='1996 to 2017 NBA Draft',
        autosize=True,
        hovermode='closest',
        showlegend=True,
        #scope='usa',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
        legend = dict(
            traceorder = 'reversed'
        )
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='1996 to 2017 NBA Player Drafts')

def main():
    colourList = makeColours()
    draftClassData, draftYears, latitudeData, longitudeData = readData()
    data = plotMap(latitudeData, longitudeData, draftYears, colourList, draftClassData)

if '__name__' == '__main__':
    main()