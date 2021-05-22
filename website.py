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
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from forms import MMSI_Number
from flask_bootstrap import Bootstrap




#we create an instance of the Flask class
app = Flask(__name__)

app.config['SECRET_KEY']= 'Pxce1hxcfx9cxaax97xb7xedYx9b'

bootstrap = Bootstrap(app)


DATA_FRAME = pd.read_csv("../data/AIS_2018_01_01.csv")
grouped = DATA_FRAME.groupby("MMSI")


def simpleGraph(MMSI):
                plt.figure()
                x = grouped.get_group(MMSI).sort_values("BaseDateTime").LAT
                y = grouped.get_group(MMSI).sort_values("BaseDateTime").LON
                plt.plot(x,y)
                plt.xlabel("LAT")
                plt.ylabel("LON")
                plt.title("MMSI: " + str(MMSI))
                plt.savefig("static/images/simpleGraph_" + str(MMSI) + ".png")
  
def foliumMap(MMSI):
    actual_map = folium.Map(location=[grouped.get_group(MMSI).LAT.mean(),
                            grouped.get_group(MMSI).LON.mean()],
                zoom_start=13)

    f = folium.FeatureGroup("ship")
    l = folium.vector_layers.PolyLine(zip(grouped.get_group(MMSI).sort_values("BaseDateTime").LAT, 
                                        grouped.get_group(MMSI).sort_values("BaseDateTime").LON),
                                    popup="367651830", color="red").add_to(f)

    f.add_to(actual_map)
    actual_map.save("templates/map.html")

def scatteredGraphGreen(MMSI):
    grouped = DATA_FRAME.groupby("MMSI")
    #df2 = pd.to_datetime(grouped.get_group(367033570).BaseDateTime).sort_values()
    DATA_FRAME2 = grouped.get_group(int(MMSI))
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LAT
    plt.scatter(x,y,c="green")
    plt.savefig("static/images/greenGraph_"+ str(MMSI) + ".png")

def scatteredGraphRed(MMSI):
    grouped = DATA_FRAME.groupby("MMSI")
    #df2 = pd.to_datetime(grouped.get_group(367033570).BaseDateTime).sort_values()
    DATA_FRAME2 = grouped.get_group(int(MMSI))
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LON
    plt.scatter(x,y,c="red")
    plt.savefig("static/images/redGraph_"+ str(MMSI) + ".png")

def splineOne(MMSI):
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
    plt.savefig("static/images/Spline.png")

def splineTwo(MMSI):
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
    plt.savefig("static/images/Spline2.png")



@app.route("/", methods = ['GET', 'POST'])
def index():
    numbers = DATA_FRAME.MMSI.unique()
    message = ""
    form = MMSI_Number()
    #message = ""
    if form.validate_on_submit():
        number = form.MMSI_Number.data
        if number in numbers:
            # empty the form field
            global MMSI
            MMSI = number
            form.MMSI_Number.data = ""
            simpleGraph(MMSI)
            foliumMap(MMSI)
            scatteredGraphGreen(MMSI)
            scatteredGraphRed(MMSI)
            splineOne(MMSI)
            splineTwo(MMSI)

            return redirect(url_for('hello_world'))
        else:
            message = "That number is not in our database."
    return render_template('index.html', form=form, message=message)








@app.route("/hello")
def hello_world():
    return "<p>Find the analysis of the shiproute below<br><br><a href='/map'>map</a><br><a href='/simpleGraph'>Simple Graph</a><br><a href='/redGraph'>red Graph</a><br><a href='/greenGraph'>greenGraph</a><br><a href='/splineFunction'>splineFunction</a><br><a href='/splineFunction2'>splineFunction2</a></p>"

@app.route("/map")
def hello_map():
    return render_template('map.html')

@app.route("/simpleGraph")
def simpleGraph1():
    return render_template('simpleGraph.html', name = 'simpleGraph', url ="static/images/simpleGraph_" + str(MMSI) + ".png")

@app.route("/greenGraph")
def greenGraph():
    return render_template('greenGraph.html', name = 'greenGraph', url ="/static/images/greenGraph_"+ str(MMSI) + ".png")

@app.route("/redGraph")
def redGraph():
    return render_template('redGraph.html', name = 'redGraph', url ="/static/images/redGraph_"+ str(MMSI) + ".png")

@app.route("/splineFunction")
def Spline():
    return render_template('Spline.html', name = 'Spline', url ='/static/images/Spline.png')

@app.route("/splineFunction2")
def Spline2():
    return render_template('Spline2.html', name = 'Spline2', url ='/static/images/Spline2.png')

