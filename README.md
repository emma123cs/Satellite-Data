# Satellite-Data

### The Rational behind the Group Project

Our shared passion for maritime sports and our interest in neural networks have led us to create this project. The back-end code was written in Python while the front-end application is enabled through HTML to elevate the level of coding and allow for interactions.



### Required Databases

The AIS Data can be downloaded from the [National Oceanic and Atmospheric Administration of the US.](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2018/index.html)
In order to run the code, one has to download the dataset and store it in the DATA folder and run the flask app from _website.py_ in the SRC folder.

### Running the code 

After installing Python on your computer follow the Terminal Commands:
    
    git clone https://github.com/emma123cs/Satellite-Data.git
    cd Satellite-Data
    python3 -m venv env
    source env/bin/activate
    cd src
    pip3 install -r requirements.txt

**Note:** Store the AIS.cvs file inside the data folder (_AIS_2018_01_01.cvs_)

    export FLASK_APP=website
    flask run


### Imports in website.py

The following imports are necessary:

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
    from flask_wtf import FlaskForm
    from wtforms import IntegerField
    from wtforms.validators import DataRequired, Length





### Background Information on AIS Data

AIS (Automatic Identification System) tracks vessels across the globe by unique identifier numbers using GPS data. 

AIS data is available via [Marine Traffic](https://www.marinetraffic.com/en/ais/home/centerx:-12.0/centery:25.0/zoom:2) and allows for display of information about vessels worldwide. The information for each vessel is structured in this way:

- Vessel name, MMSI number and call sign
- Type of vessel (such as passenger, cargo, fishing) 
- Vessel???s position (current latitude and longitude) 
- Course over ground (COG) 
- Speed over ground (SOG) 
- Heading from your vessel
- Closest point of approach (CPA) (distance) 
- Time to closest point of approach (TCPA) 
- Vessels??? dimensions (length, beam and draught)





















### Structure of the Code

As previously mentioned, the code is structured into two parts: (1) the back-end code using Python and (2) the front-end, interactive application using HTML.

#### (1)	The back-end code in Python:

**Note:** The back-end code is integrated in the file _website.py_ and _portsCooridnates.py_ and only explained here seperately to provide a more comprehensive description of the code. 

(i)	We first created a data frame with the AIS Data for January 1st, 2018 (randomly selected day to serve as an example, any other day could also be used instead. One would just have to adjust the URL inside _website.py_. To get a feeling for  the unique MMSIs in the AIS data, we also printed them using df1.MMSI.unique(). This helped us to group the data for one illustrative MMSI in the AIS data and show the route on a map. 

(ii) To make the route more visual, we can also illustrate it on a world map, using folium.

---------
[![Whats-App-Image-2021-05-26-at-16-49-49.jpg](https://i.postimg.cc/3JKGb1jp/Whats-App-Image-2021-05-26-at-16-49-49.jpg)](https://postimg.cc/qg5gN85M)
##### _Route of ship with the MMSI 366950020_
---------

(iii) The previously drawn route can also be split into coordinates for longitude and latitude. When plotting the coordinates in a scatter plot, it becomes clear that some coordinates are missing (can be seen by the dotted lines).

(iv) With a cubic spline function, we can then interpolate all missing latitude and longitude coordinates.

(v)	In a next step, we have marked the nine largest ports in a geojson file (stored in DATA, _ports_us.geojson_), drawing ploygons around the ports. By using geopandas, we can outline the coordinates of the polygons around the ports.

(vi) We can also visualize all polygons drawn around the nine ports on a world map, using folium again.

---------
[![Whats-App-Image-2021-05-26-at-16-51-38.jpg](https://i.postimg.cc/sX7Wb00P/Whats-App-Image-2021-05-26-at-16-51-38.jpg)](https://postimg.cc/JD7tkK8t)
##### _One of the polygons around the Port of Newark_
---------


#### (2)	The front-end code with HTML:

We used Flask as a framework to create a simple website. The code of the Flask app can be found in the file _website.py_. 

(i)	The _index.html_ file is the first HTML page that the user sees and is rendered by the app route (???/???) that is called instantly by running the code.  We used the simple HTML layout from John Sobanski, which is linked in the sources down below. By starting the code, the function _polymap()_ for the Polygon-Map is called simultaneously. 

(ii) The user has two options on what to do next. A) they can check out the data analysis for a specific MMSI number, or B) they can learn about maritime traffic in general. 

---------
[![Whats-App-Image-2021-05-26-at-15-46-23-copy.jpg](https://i.postimg.cc/D0nbQMN0/Whats-App-Image-2021-05-26-at-15-46-23-copy.jpg)](https://postimg.cc/N9CMBpBv)
##### _Two options for the user to choose from_
---------

(iii) In our dataset, we included the coordinates of 12215 different MMSI numbers. The user can enter one of these MMSI and get to _app.route("/hello")_, where they will find a menu with 6 options (five graphs and one map). By entering an MMSI number, the functions for the different graphs and the folium map are called and create either PNG or an HTML file in the case of the map. By clicking on one option, the associated app route renders an HTML that displays the earlier created PNG or map (v).

(iv) However, if the MMSI is not in our database, the site will display the error message ???That number is not in our database???. The form is created with the use of WTForms in the _forms.py_ file and allows only for integers to be typed into the field. The user will be reminded of that restriction with another error message.

---------
[![Whats-App-Image-2021-05-26-at-15-47-22.jpg](https://i.postimg.cc/vHfgcMSy/Whats-App-Image-2021-05-26-at-15-47-22.jpg)](https://postimg.cc/Tp2Ys86N)
##### _The user can search for an MMSI number in the database_
---------
[![Whats-App-Image-2021-05-26-at-15-46-23.jpg](https://i.postimg.cc/FFM6vgLR/Whats-App-Image-2021-05-26-at-15-46-23.jpg)](https://postimg.cc/QVqmk7SG)
##### _The user is then directed to a page where he gets different information on its ship to choose from_
---------
[![Whats-App-Image-2021-05-26-at-15-46-59.jpg](https://i.postimg.cc/Vs30f5g4/Whats-App-Image-2021-05-26-at-15-46-59.jpg)](https://postimg.cc/yWy8n1wS)
##### _The error message in case the user writes string instead of integers_
---------

(v)	When clicking on one of the six options, the HTML page is rendered and saved in the templates folder. The HTML pages for the graphs follow a simple layout:
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <p>{{ name }}</p>

        <img src={{ url }} alt="Chart" > 
    </body>
    </html>


(vi) The image URL displays the associated PNG from the images folder that has been created by calling the functions in the first app route to a specific MMSI. 

(vii) The user can now go back and forth within the app and type in any MMSI number for which they would like to see the data analysis. The HTML pages for the graphs stay in the templates folder and are newly rendered with a new name and URL. Furthermore, the PNGs are also newly created. However, the HTML of the map always establishes an additional HTML file with the MMSI number in the name. This leads to a smoother UI, as one had to restart the code to render a new map.

    render_template('map' + str(MMSI) + '.html')

(viii) If the user decides that he wants to learn about maritime data in general, he can click on "Polygon Coordinates" on the _index.html_. It will show him the coordinates of a few ports in the United States as examples. 

(ix) The _PortsCoordinates.png_ is created by running the _portsCooridnates.py_ file. Because it doesn???t change by running the code and slowed down our side severely,  we excluded the file from the website code. However, we can reload it every time by deleting the '#' in front of the 'US-ports()' function in _website.py_ and call it.

(x)	The user can then choose to display the Polygon Map (which is explained above).





### Future Applications

The idea behind the code is to use satellite imagery like it is done in Remote Sensing to train and test neural networks like the Yolo Algorithm for object detection. In a future application, satellite imagery could be downloaded for the nine identified ports and the ships in our database which entered these ports. This would allow for a precise download. Subsequently, bounding boxes could be drawn around the ships, ideally with the same ships appearing in different images. To ensure the download of the imagery with the most matches between ships and ports in our database, the confusion matrix could be used. The bounding boxes would then be labelled with the help of our database (e.g. MMSI numbers or vessel names) and used for training and testing of the algorithm. 




### Sources

https://appsilon.com/object-detection-yolo-algorithm/

https://betterprogramming.pub/how-to-use-flask-wtforms-faab71d5a034

https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2018/index.html

http://darribas.org/gds15/content/labs/lab_03.html

https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask-de

https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html

https://flask.palletsprojects.com/en/2.0.x/

https://geopandas.org

https://geopandas.org/docs/user_guide/mapping.html

https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/02-Templates/templates

https://john.soban.ski/pass-bootstrap-html-attributes-to-flask-wtforms.html

https://www.marinetraffic.com/en/ais/home/centerx:-12.0/centery:25.0/zoom:2

https://www.oreilly.com/library/view/flask-web-development/9781491991725/ch04.html#:~:text=The%20validate_on_submit()%20method%20of,by%20all%20the%20field%20validators.&text=When%20a%20user%20navigates%20to,validate_on_submit()%20will%20return%20False%20

https://pythonhosted.org/Flask-Bootstrap/

https://sentinelsat.readthedocs.io/en/stable/

https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages

https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask

https://towardsdatascience.com/creating-sea-routes-from-the-sea-of-ais-data-30bc68d8530e

https://www.youtube.com/watch?v=BvXMRo78XRA

