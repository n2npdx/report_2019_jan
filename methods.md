# Methods for data cleaning/prep (prior to R Notebook):

These steps were done to take the raw data files to a state that can either be sent to the front end for aggregation, or used in R for analysis.

## One Point of Contact Campsite Reports

1. Send campsite reports through `02OnePointContactReports/transforming_campsite_reports04.ipynb`:
  * File In: CSV of Campsite Reports (RAW)
  * This transforms X-Y coordinates into lat-long coordinates.
  * The CRS, according to the projection, is EPSG:3646. If EPSG:4326 is used, the conversion to lat-long is clearly wrong.
  * This also access the "How Many Campers are there?" question, and pulls integers from the strings. This is an estimate of number of campers, and is included in a column in the output.
  * File Out: CSV (with lat-long, num_campers column with integer estimate).

2. Send campsite reports through Deidentify_RepetitiveCols_Processing.Rmd.
  * File In: CSV with lat-long, num_campers column
  * Removes vehicle license plate number and description.
  * Removes "is there anything else we should know?" column with detailed description (possibly containing identifying info).
  * Removes blank rows.
  * File Out: CSV with no blank rows, removed repetitive columns and deidentified columns with vehicle information.

2.5. Take File Out, and convert all Boolean rows to TRUE or FALSE (sub yes/no, other boolean labels).
  * Manual find/replace, for now.

3. Send campsite reports through `spatialjoin_campsitereports.py`.
  * File In: CSV with no blank rows, removed deidentifying columns.
  * Joins lat-long coordinates to RLIS neighborhoods in geopandas.
  * ISSUE: Messes up Boolean values; it converts all booleans to integers, which then merges NA values and False values, as both are 0. Can't send through the entire campsite reports; needs to filter out all columns except for necessary ones.
  * File Out: CSV/GeoJSON with only neighborhood, lat-long, and report date and ID.

4. Join the spatial-joined data CSV (3) with the deidentified CSV in (2).
  * At the moment, this is manual.
  * Notes: Sort both files first by Item ID. THIS ISN'T WORKING, because the join loses some points that aren't found in PDX at all.
  * Join needs to be done in python.
  * WIP: `OPCReports_join2.py` - #STILL not working.

5. Convert the new CSV to GeoJSON.




## One Point of Contact/HUCIRP Campsite Sweeps

1. Download merged file from Google Drive (merging done manually); convert to CSV.
  * #TODO: Fix the Ê characters found (12) in Google sheets document.

2. Send sweeps data through `spatialjoin.py`.
  * File In: CSV with lat-long
  * Creates spatial column, and joins to RLIS neighborhoods in geopandas.
  * File Out: CSV and GeoJSON with neighborhood column and geometry column added.





## Crime reports

1. 





## Dispatched calls
