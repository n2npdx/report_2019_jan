#!/usr/bin/env python

#__author__ == "Katy McKinney-Bock, katymck@gmail.com"

import pandas as pd
import geopandas
from shapely.geometry import Point
import numpy


REPORTS = "onepointcontactreports/campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined2_final.csv"

#imports/data prep
sweeps = pd.read_csv(REPORTS, encoding='UTF-8')

sweeps['coordinates'] = list(zip(sweeps.lon, sweeps.lat))
sweeps['coordinates'] = sweeps['coordinates'].apply(Point)
geosweeps = geopandas.GeoDataFrame(sweeps,geometry='coordinates')
geosweeps.crs = {'init' :'epsg:4326'}

print(geosweeps.columns)
print(geosweeps.head())

print("Camps original CRS: {}".format(geosweeps.crs))


geosweeps.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined2_final.geojson", driver="GeoJSON")
