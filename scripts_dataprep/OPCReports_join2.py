#!/usr/bin/env python

#__author__ == "Katy McKinney-Bock, katymck@gmail.com"

import pandas as pd
import geopandas
from shapely.geometry import Point
import numpy


CSV_STEP3 = "onepointcontactreports/campsite_reports_processed_no_vehicles_deidentified_02.csv"
CSV_STEP2 = "onepointcontactreports/campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined.csv"

step3 = pd.read_csv(CSV_STEP3, encoding='UTF-8')
step2 = pd.read_csv(CSV_STEP2, encoding='UTF-8')

print(step2.head())
print(step3.head())

joined = pd.merge(step3, step2, how='left', on=['Item.ID'])

print(joined.columns)

joined = joined[['Unnamed: 0_x', 'Date.Created_x',
       'Date.Received', 'Item.ID', 'Status', 'Follow.Ups',
       'Where.is.the.campsite.concern.located..Please.provide.an.address.if.possible..If.no.address.is.available..please.provide.a.complete.description.of.the.site.s.location.',
       'If.having.difficulty.with.the.map..please.type.in.the.nearest.address.or.intersection..for.example..SW.Market.and.SW.14th..and.scroll.to.pinpoint.the.location...User.Specified.',
       'If.having.difficulty.with.the.map..please.type.in.the.nearest.address.or.intersection..for.example..SW.Market.and.SW.14th..and.scroll.to.pinpoint.the.location...System.Verified.',
       'Address.ID', 'Property.ID', 'State.ID', 'City',
       'How.long.has.the.site.been.there.', 'Is.the.site.occupied.',
       'How.many.campers.would.you.estimate.are.there.',
       'Are.children.present.', 'Are.dogs.present.',
       'Does.anyone.seem.to.be.medically.fragile.',
       'Are.there.tents.or.structures.there..If.so..how.many.',
       'Is.this.a.vehicle.',
       'Repeated.instances.of.overly.aggressive.behavior.from.campers',
       'Public.intoxication.and.or.conspicuous.drug.use..If.it.is.an.emergency..please.call.9.1.1..',
       'Campsite.obstructs.public.right.of.way', 'Misuse.of.public.spaces',
       'Structures.or.tents.present', 'Excessive.trash.and.or.biohazards',
       'Damage.to.the.environment', 'number_of_campers',
       'lon_y', 'lat_y', 'index_right',
       'NAME', 'SUM_AREA', 'SUM_SqMile']]

joined.columns = ['Unnamed: 0', 'Date.Created',
       'Date.Received', 'Item.ID', 'Status', 'Follow.Ups',
       'Where.is.the.campsite.concern.located..Please.provide.an.address.if.possible..If.no.address.is.available..please.provide.a.complete.description.of.the.site.s.location.',
       'If.having.difficulty.with.the.map..please.type.in.the.nearest.address.or.intersection..for.example..SW.Market.and.SW.14th..and.scroll.to.pinpoint.the.location...User.Specified.',
       'If.having.difficulty.with.the.map..please.type.in.the.nearest.address.or.intersection..for.example..SW.Market.and.SW.14th..and.scroll.to.pinpoint.the.location...System.Verified.',
       'Address.ID', 'Property.ID', 'State.ID', 'City',
       'How.long.has.the.site.been.there.', 'Is.the.site.occupied.',
       'How.many.campers.would.you.estimate.are.there.',
       'Are.children.present.', 'Are.dogs.present.',
       'Does.anyone.seem.to.be.medically.fragile.',
       'Are.there.tents.or.structures.there..If.so..how.many.',
       'Is.this.a.vehicle.',
       'Repeated.instances.of.overly.aggressive.behavior.from.campers',
       'Public.intoxication.and.or.conspicuous.drug.use..If.it.is.an.emergency..please.call.9.1.1..',
       'Campsite.obstructs.public.right.of.way', 'Misuse.of.public.spaces',
       'Structures.or.tents.present', 'Excessive.trash.and.or.biohazards',
       'Damage.to.the.environment', 'number_of_campers',
       'lon', 'lat', 'index_right',
       'NAME', 'SUM_AREA', 'SUM_SqMile']

print(joined.head())
print(joined.columns)

joined.to_csv("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined2_final.csv", index=False)

joined['coordinates'] = list(zip(joined.lon, joined.lat))
joined['coordinates'] = joined['coordinates'].apply(Point)
geosites = geopandas.GeoDataFrame(joined,geometry='coordinates')
geosites = geosites.drop(columns=['How.long.has.the.site.been.there.', 'Is.the.site.occupied.',
       'How.many.campers.would.you.estimate.are.there.',
       'Are.children.present.', 'Are.dogs.present.',
       'Does.anyone.seem.to.be.medically.fragile.',
       'Are.there.tents.or.structures.there..If.so..how.many.',
       'Is.this.a.vehicle.',
       'Repeated.instances.of.overly.aggressive.behavior.from.campers',
       'Public.intoxication.and.or.conspicuous.drug.use..If.it.is.an.emergency..please.call.9.1.1..',
       'Campsite.obstructs.public.right.of.way', 'Misuse.of.public.spaces',
       'Structures.or.tents.present', 'Excessive.trash.and.or.biohazards',
       'Damage.to.the.environment'])
#geosites.crs = {'init' :'epsg:3646'} #need to check with Lynn as to why this was the CRS for the inverse geocode.
geosites.crs = {'init' :'epsg:4326'}

geosites.to_file("campsite_reports_processed_no_vehicles_deidentified_neighborhoods_joined2_final.GeoJSON", driver="GeoJSON")
