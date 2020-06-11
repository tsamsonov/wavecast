from netCDF4 import Dataset
import pandas
import geopandas


rootgrp = Dataset("ww2019.nc", "r", format="NETCDF4")
lons = rootgrp.variables['longitude'][:]
lats = rootgrp.variables['latitude'][:]
ids = [id for id in range(len(lats))]

df = pandas.DataFrame({'id': ids, 'lon': lons, 'lat': lats})
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lon, df.lat))

gdf.to_file('data/tin.shp')