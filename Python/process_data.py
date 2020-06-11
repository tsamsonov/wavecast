import arcpy
import numpy

from TINcontours import tin_contours

def unique_values_np(table, field):  ## http://geospatialtraining.com/get-a-list-of-unique-attribute-values-using-arcpy/
    data = arcpy.da.TableToNumPyArray(table, [field])
    return numpy.unique(data[field])

def unique_values(table, field):  ## http://geospatialtraining.com/get-a-list-of-unique-attribute-values-using-arcpy/
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

arcpy.env.overwriteOutput=True

arcpy.CheckOutExtension("3D")

arcpy.env.workspace = "Y:/GitHub/wavecast"
datatab = 'Wavetin.gdb/data'
tindata = 'data/tin.shp'

sea = 'data/seab.shp'
ext = 'data/sea.shp'

tinpts = 'in_memory/tinpts'
tinlyr = 'tinlyr'

arcpy.CopyFeatures_management(tindata, tinpts)
arcpy.MakeFeatureLayer_management(tinpts, tinlyr)

nrows = 37826

vars = ['wnd', 'hs', 'lm', 'fp', 'cge', 't02', 't0m1', 't01']
intervals = [1, 0.5, 5, 0.1, 0.5, 0.5, 0.5, 0.5]

dates = unique_values(datatab, 'time')
print(dates)

for i in range(len(dates)):

        datalyr = 'datalyr' + str(i)
        query = "time = timestamp '{0}'".format(dates[i])

        arcpy.MakeTableView_management(datatab, datalyr, query)
        arcpy.AddJoin_management(tinlyr, 'FID', datalyr, 'id')


        # print(arcpy.GetCount_management(tinlyr).getOutput(0))

        for j in range(len(vars)):
            tin_contours(tinlyr, vars[j], intervals[j], 0, ext,
                         'data/Output.gdb/{0}_cont_{1}'.format(vars[j], i),
                         'data/Output.gdb/{0}_band_{1}'.format(vars[j], i))
            print('Finished {0} {1}'.format(vars[j], dates[i]))

        arcpy.RemoveJoin_management(tinlyr)