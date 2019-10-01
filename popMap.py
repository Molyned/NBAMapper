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

def readData():
    xl = pd.ExcelFile('popular citiesV13.xlsx') 
    df1 = xl.parse('popular citiesV13.xlsx')
    sitelat = df1.Latitude
    sitelon = df1.Longitude
    playerNames = df1.BirthPlaces
    popular = df1.Frequency
    draftClassData, latitudeData, longitudeData, colourList = [], [], [], []

    for x in range(len(playerNames)):
        latitude=sitelat[x]
        longitude=sitelon[x]
        draftClass = popular[x]
        draftClassData.append(draftClass)
        latitudeData.append(latitude)
        longitudeData.append(longitude)

def plotMap(draftClassData, latitudeData, longitudeData, colourList):
    data = []
    for i in range(len(playerNames)):
        trace = go.Scattermapbox(
                lat=[sitelat[i]],
                lon=[sitelon[i]],
                name = playerNames[i],
                mode='markers',
                marker=dict(
                    size=draftClassData[i],
                    color= 'red',
                    opacity=0.7
                ),
                text=playerNames[i],
                hoverinfo='text')
        data.append(trace)
        
    layout = go.Layout(
        title='Popular Cities',
        autosize=True,
        hovermode='closest',
        showlegend=False,
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
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='Popular Cities')

def main():
    data, draftClassData, latitudeData, longitudeData, colourList = readData()
    data = plotMap( draftClassData, latitudeData, longitudeData, colourList)

if '__name__' == '__main__':
    main()