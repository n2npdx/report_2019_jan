#!/usr/bin/env python

#__author__ == "Katy McKinney-Bock, katymck@gmail.com"

import pandas as pd
import geopandas
from shapely.geometry import Point
import numpy

SWEEPS = "sweeps/SweepsData_master01_v04.csv"
RLIS_NEIGHBORHOODS = "../../Data_Raw/RLISNeighborhoods_HackOR/rlis_neighborhoods.geojson"

#imports/data prep
sweeps = pd.read_csv(SWEEPS, encoding='UTF-8', skipinitialspace=True)
sweeps = sweeps.dropna(subset = ['lat', 'long'])

print(list(zip(sweeps.long, sweeps.lat)))
print(type(sweeps.long[9]))
print(type(sweeps.lat[9]))
#Use only if there is a leading space, and either lat or long imports only as string
# sweeps['long'] = sweeps['long'].str.strip()
# sweeps['long'] = sweeps['long'].apply(pd.to_numeric)

sweeps['coordinates'] = list(zip(sweeps.long, sweeps.lat))
sweeps['coordinates'] = sweeps['coordinates'].apply(Point)
geosweeps = geopandas.GeoDataFrame(sweeps,geometry='coordinates')
geosweeps.crs = {'init' :'epsg:4326'}

print(geosweeps.head())

rlis = geopandas.read_file(RLIS_NEIGHBORHOODS)
print(rlis.head())
print(rlis.columns)

print("RLIS CRS: {}".format(rlis.crs))
print("Camps CRS: {}".format(geosweeps.crs))

geosweeps.to_file("all_sweeps_v03.geojson", driver="GeoJSON")
geosweeps.to_file("all_sweeps_v03.csv", driver="CSV")

#join
sweeps_sub3 = geopandas.sjoin(geosweeps, rlis, how="inner", op="intersects")

print("Subset DF: {}".format(sweeps_sub3))

sweeps_sub3.to_file("sweeps_neighborhoods_joined_v04.GeoJSON", driver="GeoJSON")
sweeps_sub3.to_file("sweeps_neighborhoods_joined_v04.csv", driver="CSV")



#subset 3 neighborhoods

subset_names = ["HOSFORD-ABERNETHY", "BUCKMAN", "KERNS"]
subset_sweeps = sweeps_sub3.loc[sweeps_sub3['NAME'].isin(subset_names)]

subset_sweeps.to_file("sweeps_neighborhoods_joined_v04_subset.GeoJSON", driver="GeoJSON")
subset_sweeps.to_file("sweeps_neighborhoods_joined_v04_subset.csv", driver="CSV")
