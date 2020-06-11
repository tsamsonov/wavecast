from netCDF4 import Dataset, num2date
import pandas
import math
import arcpy

filename = "ww2019.nc"
rootgrp = Dataset(filename, "r", format="NETCDF4")
for name in rootgrp.ncattrs():
   print("Global attr", name, "=", getattr(rootgrp,name))


keys = [key for key in rootgrp.variables.keys()][:]

print(rootgrp.variables)

df = pandas.DataFrame({'time': num2date(rootgrp.variables['time'][0],
                                        rootgrp.variables['time'].units),
                       'uwnd': rootgrp.variables['uwnd'][0],
                       'vwnd': rootgrp.variables['vwnd'][0],
                       'hs': rootgrp.variables['hs'][0],
                       'lm': rootgrp.variables['lm'][0],
                       't02': rootgrp.variables['t02'][0],
                       't0m1': rootgrp.variables['t0m1'][0],
                       't01': rootgrp.variables['t01'][0],
                       'fp': rootgrp.variables['fp'][0],
                       'dir': rootgrp.variables['dir'][0],
                       'cge': rootgrp.variables['cge'][0]})


for i in range(1, 25):
   df = df.append(
      pandas.DataFrame({'time': num2date(rootgrp.variables['time'][i],
                                         rootgrp.variables['time'].units),
                        'uwnd': rootgrp.variables['uwnd'][i],
                        'vwnd': rootgrp.variables['vwnd'][i],
                        'hs': rootgrp.variables['hs'][i],
                        'lm': rootgrp.variables['lm'][i],
                        't02': rootgrp.variables['t02'][i],
                        't0m1': rootgrp.variables['t0m1'][i],
                        't01': rootgrp.variables['t01'][i],
                        'fp': rootgrp.variables['fp'][i],
                        'dir': rootgrp.variables['dir'][i],
                        'cge': rootgrp.variables['cge'][i]})
   )

def f(x, y):
    return math.sqrt(x * x + y * y)

df['wnd'] = df[['uwnd','vwnd']].apply(lambda x: f(*x), axis=1)

df.to_csv(filename + '.csv')

arcpy.TableToTable_conversion(filename + '.csv', "Wavetin.gdb", "data")

# arcpy.da.NumPyArrayToTable(x, 'Y:/GitHub/wavecast/Wavetin.gdb/data')