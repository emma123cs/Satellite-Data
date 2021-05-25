import dataframe_image as dfi
import geopandas as gpd

def US_ports():
    ports_coordinates = gpd.read_file("../data/ports_us.geojson")
    dfi.export(ports_coordinates, "static/images/PortsCoordinates.png")