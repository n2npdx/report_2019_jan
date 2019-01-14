#!/usr/bin/env python

#__author__ == "Katy McKinney-Bock, katymck@gmail.com"

import pandas as pd
import geopandas
from shapely.geometry import Point
import numpy


SWEEPS = "onepointcontactreports/campsite_reports_processed_no_vehicles_deidentified_02.csv"
# TODO: change SWEEPS variable to a general DATA name
RLIS_NEIGHBORHOODS = "../../Data_Raw/RLISNeighborhoods_HackOR/rlis_neighborhoods.geojson"

#imports/data prep
sweeps = pd.read_csv(SWEEPS, encoding='UTF-8', skipinitialspace=True)
sweeps = sweeps.dropna(subset = ['lat', 'lon'])

#Use only if there is a leading space, and either lat or long imports only as string
#sweeps['long'] = sweeps['long'].str.strip()
#sweeps['long'] = sweeps['long'].apply(pd.to_numeric)

sweeps['coordinates'] = list(zip(sweeps.lon, sweeps.lat))
sweeps['coordinates'] = sweeps['coordinates'].apply(Point)
geosweeps = geopandas.GeoDataFrame(sweeps,geometry='coordinates')
geosweeps.crs = {'init' :'epsg:4326'}

# uncomment if subsetting columns out
# geosweeps = geosweeps[['Unnamed: 0'	,'Date.Created', 'Item.ID', 'lon', 'lat', 'coordinates']]

print(geosweeps.columns)
print(geosweeps.head())

rlis = geopandas.read_file(RLIS_NEIGHBORHOODS)
print(rlis.head())
print(rlis.columns)

print("RLIS CRS: {}".format(rlis.crs))
print("Camps original CRS: {}".format(geosweeps.crs))

print(geosweeps)
print(rlis.head())

# geosweeps.to_file("all_campsite_reports.geojson", driver="GeoJSON")
# geosweeps.to_file("all_campsite_reports.csv", driver="CSV")

#join
sweeps_sub3 = geopandas.sjoin(geosweeps, rlis, how="inner", op="intersects")

# bools = ["Repeated.instances.of.overly.aggressive.behavior.from.campers"]
# for bool_col in bools:
#     sweeps_sub3[bool_col] = sweeps_sub3[bool_col].astype('int')

# sweeps_sub4 = gdf_bool_to_int(sweeps_sub3)

print("Subset DF: {}".format(sweeps_sub3))

sweeps_sub3 = sweeps_sub3.drop(columns='number_of_campers')

# sweeps_sub3.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_02.GeoJSON", driver="GeoJSON")
# sweeps_sub3.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_02.csv", driver="CSV")
sweeps_sub3.to_csv("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_02.csv", index=False)

sweeps_sub4 = pd.read_csv("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_02.csv")
sweeps_sub4.to_json("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_02.json", orient='records')

#subset 3 neighborhoods

subset_names = ["HOSFORD-ABERNETHY", "BUCKMAN", "KERNS"]
subset_sweeps = sweeps_sub3.loc[sweeps_sub3['NAME'].isin(subset_names)]

subset_sweeps.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_subset.GeoJSON", driver="GeoJSON")
subset_sweeps.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined_subset.csv", driver="CSV")
