#!/usr/bin/env python

#__author__ == "Katy McKinney-Bock, katymck@gmail.com"

import pandas as pd
import geopandas
from shapely.geometry import Point
import numpy

CRIME = "crimereports/Open_Data_Sheet_data_CrimeData.csv"
RLIS_NEIGHBORHOODS = "../../Data_Raw/RLISNeighborhoods_HackOR/rlis_neighborhoods.geojson"

#imports/data prep
crime = pd.read_csv(CRIME)
crime = crime.dropna(subset = ['OpenDataLat', 'OpenDataLon'])

print(crime.head())

print(list(zip(crime.OpenDataLon, crime.OpenDataLat)))
print(type(crime.OpenDataLon[9]))
print(type(crime.OpenDataLat[9]))

crime['coordinates'] = list(zip(crime.OpenDataLon, crime.OpenDataLat))
crime['coordinates'] = crime['coordinates'].apply(Point)
geocrime = geopandas.GeoDataFrame(crime,geometry='coordinates')
geocrime.crs = {'init' :'epsg:4326'}

print(geocrime.head())

rlis = geopandas.read_file(RLIS_NEIGHBORHOODS)
print(rlis.head())
print(rlis.columns)

print("RLIS CRS: {}".format(rlis.crs))
print("Camps CRS: {}".format(geocrime.crs))

# geocrime.to_file("all_crime_v03.geojson", driver="GeoJSON")
# geocrime.to_file("all_crime_v03.csv", driver="CSV")

#join
crime_sub3 = geopandas.sjoin(geocrime, rlis, how="inner", op="intersects")


crime_sub3.rename(columns={'NAME':'NAME_RLIS', 'SUM_AREA':'SUM_AREA_RLIS', 'SUM_SqMile':'SUM_SqMile_RLIS',
                            'index_right':'index_right_RLIS'}, inplace=True)
print("Subset DF: {}".format(crime_sub3))

# crime_sub3.to_file("crime_neighborhoods_joined_v01.GeoJSON", driver="GeoJSON")
crime_sub3.to_file("crime_neighborhoods_joined_v01.csv", driver="CSV")


# #subset 3 neighborhoods

subset_names = ["HOSFORD-ABERNETHY", "BUCKMAN", "KERNS"]
subset_crime = crime_sub3.loc[crime_sub3['NAME'].isin(subset_names)]

subset_crime.to_file("crime_neighborhoods_joined_v01_subset.GeoJSON", driver="GeoJSON")
subset_crime.to_file("crime_neighborhoods_joined_v01_subset.csv", driver="CSV")


## after running first part of script, re-import and continue to get the second neighborhood
# manual column name change

CRIME2 = "crime_neighborhoods_joined_v01.csv"
CEID = "../../Data_Raw/VenturePortland/VenturePortland_Boundaries.json"

#imports/data prep
crime2 = pd.read_csv(CRIME2)

crime2['coordinates'] = list(zip(crime2.OpenDataLon, crime2.OpenDataLat))
crime2['coordinates'] = crime2['coordinates'].apply(Point)

geocrime2 = geopandas.GeoDataFrame(crime2,geometry='coordinates')
geocrime2.crs = {'init' :'epsg:4326'}

print(geocrime2.head())

ceid = geopandas.read_file(CEID)
print(ceid.head())
print(ceid.columns)

print("RLIS CRS: {}".format(ceid.crs))
print("Camps CRS: {}".format(geocrime2.crs))

#join
crime2_sub3 = geopandas.sjoin(geocrime2, ceid, how="inner", op="intersects")

print("Subset DF: {}".format(crime2_sub3))

crime2_sub3.to_file("crime_neighborhoods_joined_CEID_v01.GeoJSON", driver="GeoJSON")
crime2_sub3.to_file("crime_neighborhoods_joined_CEID_v01.csv", driver="CSV")
