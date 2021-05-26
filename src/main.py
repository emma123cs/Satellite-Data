import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from scipy.interpolate import CubicSpline
import datetime
import geopandas as gpd
from shapely.geometry import Point
import seaborn as sns
import sqlite3



shipMMSI = 367689010
DATA_FRAME = pd.read_csv("../data/AIS_2018_01_01.csv")
grouped = DATA_FRAME.groupby("MMSI")
DATA_FRAME2 = grouped.get_group(int(shipMMSI))
DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])
df_2019 = pd.read_csv("../data/AIS_2019_01_01.csv")
MMSI = shipMMSI


def simpleGraph(MMSI):
  plt.figure()
  x = grouped.get_group(MMSI).sort_values("BaseDateTime").LAT
  y = grouped.get_group(MMSI).sort_values("BaseDateTime").LON
  plt.plot(x,y)
  plt.xlabel("LAT")
  plt.ylabel("LON")
  plt.title("MMSI: " + str(MMSI))
  return plt


def greenGraph(MMSI):
  DATA_FRAME2 = grouped.get_group(MMSI)
  DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])

  plt.figure()
  x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
  y = DATA_FRAME2.LAT
  plt.scatter(x,y,c="green")
  plt.show()

  plt.figure()
  x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
  y = DATA_FRAME2.LON
  plt.scatter(x,y,c="green")
  plt.show()


def foliumMap(MMSI):
    actual_map = folium.Map(location=[grouped.get_group(MMSI).LAT.mean(),
                            grouped.get_group(MMSI).LON.mean()],
                zoom_start=13)

    f = folium.FeatureGroup("ship")
    l = folium.vector_layers.PolyLine(zip(grouped.get_group(MMSI).sort_values("BaseDateTime").LAT, 
                                        grouped.get_group(MMSI).sort_values("BaseDateTime").LON),
                                    popup="367651830", color="red").add_to(f)

    f.add_to(actual_map)
    actual_map.save("index.html")


    #return actual_map._repr_html_()


def scatteredGraph(MMSI):
    grouped = DATA_FRAME.groupby("MMSI")
    #df2 = pd.to_datetime(grouped.get_group(367033570).BaseDateTime).sort_values()
    DATA_FRAME2 = grouped.get_group(int(shipMMSI))
    DATA_FRAME2 = DATA_FRAME2.sort_values(by = ["BaseDateTime"])

    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LAT
    plt.scatter(x,y,c="red")
    plt.show()

    plt.figure()
    x = pd.to_datetime(DATA_FRAME2.BaseDateTime)
    y = DATA_FRAME2.LON
    plt.scatter(x,y,c="red")
    plt.show()


def splineFunction(MMSI):
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
    plt.show()

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
    plt.show()


def polyMap(MMSI):
  ports_coordinates = gpd.read_file("../data/ports_us.geojson")

  #print(ports_coordinates.crs)
  DATA_FRAME = ports_coordinates.to_crs(epsg=4326)

  map_of_ports = folium.Map(location=[37.09, -95.71], zoom_start=4)
  for _, r in DATA_FRAME.iterrows():
      sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
      geo_j = sim_geo.to_json()
      geo_j = folium.GeoJson(data=geo_j,
                            style_function=lambda x: {'fillColor': 'green'})
      folium.Popup(r['location']).add_to(geo_j)
      geo_j.add_to(map_of_ports)

  map_of_ports.save("Polymap.html")

#simpleGraph(shipMMSI)
#greenGraph(shipMMSI)
#foliumMap(shipMMSI)
#scatteredGraph(shipMMSI)
#splineFunction(shipMMSI)
#polyMap(shipMMSI)