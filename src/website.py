#First we import all tools and the Flask class
from flask import Flask, render_template, url_for, redirect
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium
from scipy.interpolate import CubicSpline
import datetime
import io
import random
import geopandas as gpd
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from forms import MMSI_Number #imports the form MMSI_number from the file forms.py
from flask_bootstrap import Bootstrap
import dataframe_image as dfi #only needed if 'def US_ports():' function in website.py 





#we create an instance of the Flask class
app = Flask(__name__)

#the secret key is chosen randomly
app.config['SECRET_KEY']= 'Pxce1hxcfx9cxaax97xb7xedYx9b'

bootstrap = Bootstrap(app)

#we then create a dataframe with Pandas and sort it by MMSI no.
DATA_FRAME = pd.read_csv("../data/AIS_2018_01_01.csv")
grouped = DATA_FRAME.groupby("MMSI")


#by running the code the user first sees the index page
#we created function (functions if you choose to include the function from portsCoordinates.py) for the different buttons that are not specifically connected to the MMSI number of a single ship


def polymap():
  ports_coordinates = gpd.read_file("../data/ports_us.geojson")

  
  DATA_FRAME = ports_coordinates.to_crs(epsg=4326)

  map_of_ports = folium.Map(location=[37.09, -95.71], zoom_start=4)
  for _, r in DATA_FRAME.iterrows():
      sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
      geo_j = sim_geo.to_json()
      geo_j = folium.GeoJson(data=geo_j,
                            style_function=lambda x: {'fillColor': 'green'})
      folium.Popup(r['location']).add_to(geo_j)
      geo_j.add_to(map_of_ports)

    #instead of printing, we save the map as an HTML file
  map_of_ports.save("templates/Polymap.html")

#outcomment the following in order to reload the portsCoordinates.PNG
#def US_ports():
    #ports_coordinates = gpd.read_file("../data/ports_us.geojson")
    #dfi.export(ports_coordinates, "static/images/PortsCoordinates.png")


#we call the function(s):
    
polymap()


#outcomment the following in order to reload the portsCoordinates.PNG
#US_ports()


#then we create the fuctions that are linked to a specific MMSI number and call them later in the index app route
#every function below uses the 'savefig' command to create a PNG file except for the folium map which renders an HTML file
#the plotting of the routes and the different graphs follow the same logic:
#we create and sort the dataframe, enable a plot figure (matplotlib) and define the axis. Then we plot and save the file.
def shipRoute(MMSI):
                plt.figure()
                x = grouped.get_group(MMSI).sort_values("BaseDateTime").LAT
                y = grouped.get_group(MMSI).sort_values("BaseDateTime").LON
                plt.plot(x,y)
                plt.xlabel("LAT")
                plt.ylabel("LON")
                plt.title("MMSI: " + str(MMSI))
                plt.savefig("static/images/shipRoute.png")
  
def foliumMap(MMSI):
    actual_map = folium.Map(location=[grouped.get_group(MMSI).LAT.mean(),
                            grouped.get_group(MMSI).LON.mean()],
                zoom_start=13)

    f = folium.FeatureGroup("ship")
    l = folium.vector_layers.PolyLine(zip(grouped.get_group(MMSI).sort_values("BaseDateTime").LAT, 
                                        grouped.get_group(MMSI).sort_values("BaseDateTime").LON),
                                    popup="367651830", color="red").add_to(f)

    f.add_to(actual_map)
    #by rerunning the code, a new template is saved 
    actual_map.save("templates/map" + str(MMSI) + ".html")

def sLatitudeCoordinates(MMSI):
    grouped = DATA_FRAME.groupby("MMSI")
    DATA_FRAME2 = grouped.get_group(int(MMSI))
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LAT
    plt.scatter(x,y,c="green")
    plt.savefig("static/images/sLatitudeC.png")

def sLongitudeCoordinates(MMSI):
    grouped = DATA_FRAME.groupby("MMSI")
    DATA_FRAME2 = grouped.get_group(int(MMSI))
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LON
    plt.scatter(x,y,c="red")
    plt.savefig("static/images/scatteredLongitudeCoordinates.png")

def sLatitude(MMSI):
    fig = plt.Figure()
    DATA_FRAME2 = grouped.get_group(MMSI)
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LAT
    cs = CubicSpline(x, y)

    base = datetime.datetime(2018, 1, 1, 0, 0, 0)
    xs = np.array([base + datetime.timedelta(minutes=i) for i in range(1440)])
    xs = pd.to_datetime(xs)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(x.to_numpy(), y, 'o', label='data')
    ax.plot(xs, cs(xs), label="S")
    ax.legend(loc='lower left', ncol=2)
    plt.savefig("static/images/splineLatitude.png")

def sLongitude(MMSI):
    fig = plt.Figure()
    DATA_FRAME2 = grouped.get_group(MMSI)
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LON
    cs = CubicSpline(x, y)

    base = datetime.datetime(2018, 1, 1, 0, 0, 0)
    xs = np.array([base + datetime.timedelta(minutes=i) for i in range(1440)])
    xs = pd.to_datetime(xs)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(x.to_numpy(), y, 'o', label='data')
    ax.plot(xs, cs(xs), label="S")
    ax.legend(loc='lower left', ncol=2)
    plt.savefig("static/images/splineLongitude.png")


#below we have all the different app routes that render HTML files that display the PNGs of the graphs 
@app.route("/", methods = ['GET', 'POST']) 
def index():
    #we create an array of all unique MMSI numbers in the dataset
    numbers = DATA_FRAME.MMSI.unique()
    message = ""
    #we imported the form from forms.py with the help of WTForms
    form = MMSI_Number()
    #the logic of the if statement: if the MMSI no is available in our dataset go to next page, else error message.
    if form.validate_on_submit():
        number = form.MMSI_Number.data
        if number in numbers:
            global MMSI
            MMSI = number
            #empty the form field
            form.MMSI_Number.data = ""
            #we call the functions with the specific MMSI which leads to the PNGs and the folium map being created
            shipRoute(MMSI)
            foliumMap(MMSI)
            sLatitudeCoordinates(MMSI)
            sLongitudeCoordinates(MMSI)
            sLatitude(MMSI)
            sLongitude(MMSI)
            return redirect(url_for('hello_world'))
        else:
            message = "That number is not in our database."
    return render_template('index.html', form=form, message=message)

@app.route("/hello")
def hello_world():
    return "<p>Find the analysis of the shiproute below<br><br><a href='/map'>map</a><br><a href='/shipRoute'>Ship Route</a><br><a href='/scatteredLongitudeCoordinates'>Scattered Longitude Coordinates</a><br><a href='/scatteredLatitudeCoordinates'>Scattered Latitude Coordinates</a><br><a href='/splineLatitude'>Spline Latitude</a><br><a href='/splineLongitude'>Spline Longitude</a></p>"

@app.route("/shipRoute")
def shipRoute1():
    return render_template('shipRoute.html', name = 'Ship Route', url ="Satellite-Data/src/static/images/shipRoute.png")

@app.route("/scatteredLatitudeCoordinates")
def scatteredLatitudeCoordinates():
    return render_template('scatteredLatitudeCoordinates.html', name = 'Scattered Latitude Coordinates', url ="Satellite-Data/src/static/images/sLatitudeC.png")

@app.route("/scatteredLongitudeCoordinates")
def scatteredLongitudeCoordinates():
    return render_template('scatteredLongitudeCoordinates.html', name = 'Scattered Longitude Coordinates', url ="Satellite-Data/src/static/images/scatteredLongitudeCoordinates.png")

@app.route("/splineLatitude")
def splineLatitude():
    return render_template('splineLatitude.html', name = 'Spline Latitude', url ='Satellite-Data/src/static/images/splineLatitude.png')

@app.route("/splineLongitude")
def splineLongitude():
    return render_template('splineLongitude.html', name = 'Spline Longitude', url ='Satellite-Data/src/static/images/splineLongitude.png')

#and the routes that display the general map and the specific map with the ship route
@app.route("/map")
def hello_map():
    return render_template('map' + str(MMSI) + '.html')

@app.route("/polymap")
def poly_map():
    return render_template('Polymap.html')

# and the route for the poorts coordinates 
@app.route("/PortsPolys")
def poly_ports():
    return render_template('poly_ports.html', name = 'Polygon Coordinates', url ='/static/PortsCoordinates.png')
