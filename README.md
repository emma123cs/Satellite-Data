# Satellite-Data

### The Rational behind the Group Project

Our shared passion for maritime sports and our interest in neural networks have led us to create this project. The back-end code was written in Python while the front-end application is enabled through HTML to elevate the level of coding and allow for interactions.



### Required Databases

The AIS Data can be downloaded from the [National Oceanic and Atmospheric Administration of the US.](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2018/index.html)

Additionally, to run the code, the following imports are necessary:

    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import sqlite3
    import seaborn as sns
    import folium
    from scipy.interpolate import CubicSpline
    import datetime
    import geopandas as gpd
    from shapely.geometry import Point




### Background Information on AIS Data

AIS (Automatic Identification System) tracks vessels across the globe by unique identifier numbers using GPS data. 

AIS data is available via Marine Traffic and allows for display of information about vessels worldwide. The information for each vessel is structured in this way:

- Vessel name, MMSI number and call sign
- Type of vessel (such as passenger, cargo, fishing) 
- Vessel’s position (current latitude and longitude) 
- Course over ground (COG) 
- Speed over ground (SOG) 
- Heading from your vessel
- Closest point of approach (CPA) (distance) 
- Time to closest point of approach (TCPA) 
- Vessels’ dimensions (length, beam and draught)





















### Structure of the Code

As previously mentioned, the code is structured into two parts: (1) the back-end code using Python and (2) the front-end, interactive application using HTML.

#### (1)	The back-end code in Python:

**Note:** The back-end code is integrated in the file _website.py_ and _portsCooridnates.py_ and only explained here seperately to provide a more comprehensive description of the code. 

(i)	We first create a data frame with the AIS Data for January 1st, 2018 (randomly selected day to serve as an example, any other day could also be used instead). To get a feeling for  the unique MMSIs in the AIS data, we also print them using df1.MMSI.unique(). This helps us to group the data for one illustrative MMSI in the AIS data and show the route on a map. 

(ii) To make the route more visual, we can also illustrate it on a world map, using folium.

(iii) The previously drawn route can also be split into coordinates for longitude and latitude. When plotting the coordinates in a scatter plot, it becomes clear that some coordinates are missing (can be seen by the dotted lines).

(iv) With a cubic spline function, we can then interpolate all missing latitude and longitude coordinates.

(v)	In a next step, we have marked the nine largest ports in a geojson file drawing ploygons around the ports. By using geopandas, we can outline the coordinates of the polygons around the ports.

(vi) We can now test how many ships from our AIS data frame fall within the port ploygons. For this, we first use a folium map again to display all polygons drawn around the nine ports on a world map.

(vii) Finally, we create a confusion matrix with the ships´ and ports´ data and match their coordinates to identify the ports with the most of our ships from the AIS data in it. This allows us to determine the ports in which most of our ships can be localized.




#### (2)	The front-end code with HTML:

We used Flask as a framework to create a simple website. The code of the Flask app can be found in the file “website.py”. 

(i)	The index.html file is the first HTML page that the user sees and is rendered by the app route (“/”) that is called instantly by running the code.  We used the HTML layout … which is linked in the sources down below. By starting the code also, the function for the Polygon-Map is called. 

(ii) The user has two options on what to do next. A) they can check out the data-analysis for a specific MMSI number or B) they can learn about maritime traffic in general. 

[![Whats-App-Image-2021-05-26-at-15-46-23-copy.jpg](https://i.postimg.cc/D0nbQMN0/Whats-App-Image-2021-05-26-at-15-46-23-copy.jpg)](https://postimg.cc/N9CMBpBv)

###### _Two options for the user to choose from_


(iii) In our dataset we include the coordinates of 12215 different MMSI. The user can enter one of these MMSI and get to app.route("/hello"), where they will find a menu with 6 options (five graphs and one map). By entering an MMSI number the functions for the different graphs and the folium map are called and create either PNG or, in the case of the map, an HTML file. By clicking on one of the options the associated app route renders an HTML which displays the earlier created PNG or map (v).

[![Whats-App-Image-2021-05-26-at-15-47-22.jpg](https://i.postimg.cc/vHfgcMSy/Whats-App-Image-2021-05-26-at-15-47-22.jpg)](https://postimg.cc/Tp2Ys86N)


_The user can search for an MMSI number in the database_

[![Whats-App-Image-2021-05-26-at-15-46-23.jpg](https://i.postimg.cc/FFM6vgLR/Whats-App-Image-2021-05-26-at-15-46-23.jpg)](https://postimg.cc/QVqmk7SG)

_The user is then directed to a page where he gets different information on its ship to choose from_


(iv) However, if the MMSI is not in our database, the site will display the error Message “That number is not in our database”. The form is created with the use of WTForms in the forms.py file. 

[![Whats-App-Image-2021-05-26-at-15-46-59.jpg](https://i.postimg.cc/Vs30f5g4/Whats-App-Image-2021-05-26-at-15-46-59.jpg)](https://postimg.cc/yWy8n1wS)

_The error message in case of invalid MMSI numbers_


(v)	When clicking on one of the six options the HTML page is rendered and saved in the templates folder. The HTML pages for the graphs follow a very simple layout:

(vi) The image URL displays the associated PNG from the images folder that have been created by calling the functions in the first app route to a specific MMSI. 

(vii) The user can now go back and forth within the app and type in any MMSI number they would like to see the data analysis to. The HTML pages for the graphs stay in the templates folder and are newly rendered with a new name and URL. Furthermore, the PNGs are also newly created. However, the HTML of the map always creates an additional HTML file with the MMSI number in the name. This leads to a smoother UI, as one had to restart the code to render a new map.
render_template('map' + str(MMSI) + '.html')

(viii) If the user decides they want to learn about maritime data in general, they can click on Polygon Coordinates on the index.html.  

(ix) The PortsCoordinates.png is created by running the portsCooridnates.py file. Because it doesn’t change by running the code and slowed down our side severely,  we excluded the file. However, if one would want to see different data from another day, they would need to rerun the portsCooridnates.py to create a new PNG. In order to do so, one would need to include the file into the website.py file and create a function and call it after the polymap() function.

(x)	The user can then choose to display the Polygon Map (which is explained in the Backend section No. vi)




### Future Applications

The idea behind the code is to use satellite imagery like it is done in Remote Sensing to train and test neural networks like the Yolo Algorithm for object detection. In a future application, satellite imagery could be downloaded for the nine identified ports and the ships in our database which entered these ports. This would allow for a precise download. Subsequently, bounding boxes could be drawn around the ships, ideally with the same ships appearing in different images. To ensure the download of the imagery with the most matches between ships and ports in our database, the confusion matrix could be used. The bounding boxes would then be labelled with the help of our database (e.g. MMSI numbers or vessel names) and used for training and testing of the algorithm. 




### Sources

https://appsilon.com/object-detection-yolo-algorithm/

https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2018/index.html

http://darribas.org/gds15/content/labs/lab_03.html

https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html

https://geopandas.org

https://geopandas.org/docs/user_guide/mapping.html

https://www.marinetraffic.com/en/ais/home/centerx:-12.0/centery:25.0/zoom:2

https://sentinelsat.readthedocs.io/en/stable/

https://towardsdatascience.com/creating-sea-routes-from-the-sea-of-ais-data-30bc68d8530e

https://www.youtube.com/watch?v=BvXMRo78XRA


