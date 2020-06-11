import arcpy
import os, sys, traceback

def create_scratch(path):
    def_workspace = arcpy.env.workspace

    workspace = os.path.dirname(path)

    print(workspace)

    n = len(workspace)
    if n > 4:
        end = workspace[n - 4: n]  # extract last 4 letters
        if end == ".gdb":  # geodatabase
            workspace = os.path.dirname(workspace)
            print(workspace)
        end = workspace[n - 5: n]  # extract last 5 letters
        if end == ".gpkg":  # geodatabase
            workspace = os.path.dirname(workspace)
            print(workspace)

    arcpy.env.workspace = workspace
    workspaces = arcpy.ListWorkspaces("*", "Folder")
    names = [os.path.basename(w) for w in workspaces]
    i = 0
    name = 'scratch'
    while name in names:
        name = 'scratch' + str(i)
        i += 1
    arcpy.CreateFolder_management(workspace, name)

    workspace += '/' + name

    arcpy.CreateFileGDB_management(workspace, 'Scratch.gdb')

    arcpy.env.workspace = def_workspace

    return(workspace)


def tin_contours(in_points, in_field, contour_interval, base_contour, index_step, clip_features, out_contours, out_bands):

    try:
        arcpy.CheckOutExtension("3D")
        arcpy.CheckOutExtension("Spatial")

        arcpy.env.overwriteOutput = True

        # ORGANIZE WORKSPACE
        workspace = create_scratch(out_contours)

        tin = '{0}/{1}_tin'.format(workspace, in_field)

        if (clip_features != None):
            arcpy.CreateTin_3d(tin,
                               arcpy.Describe(in_points).spatialReference,
                               ';'.join([
                                   "{0} {1} masspoints".format(in_points, in_field),
                                   "'{0}' <None> hardclip".format(clip_features)
                               ])
                               )
        else:
            arcpy.CreateTin_3d(tin,
                               arcpy.Describe(in_points).spatialReference,
                               "{0} {1} masspoints".format(in_points, in_field))

        arcpy.SurfaceContour_3d(tin, out_contours, contour_interval, base_contour, 'Z', 1, contour_interval * index_step, 'index')

        if (out_bands != None):

            ext = clip_features

            if (ext == None):
                ext = 'in_memory/{0}_ext'.format(in_field)
                arcpy.MinimumBoundingGeometry_management(in_points, ext, 'CONVEX_HULL')

            arcpy.FeatureToPolygon_management([out_contours, ext], out_bands)

            arcpy.ddd.AddSurfaceInformation(out_bands, tin, "Z_MEAN")

        arcpy.Delete_management(workspace)


    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
        arcpy.AddError(pymsg)

    return

if __name__ == '__main__':

    in_points = arcpy.GetParameterAsText(0)
    in_field = arcpy.GetParameterAsText(1)
    contour_interval = float(arcpy.GetParameterAsText(2))
    base_contour = float(arcpy.GetParameterAsText(3))
    index_step = int(arcpy.GetParameterAsText(4))
    clip_features = arcpy.GetParameterAsText(5)
    out_contours = arcpy.GetParameterAsText(6)
    out_bands = arcpy.GetParameterAsText(7)

    tin_contours(in_points, in_field, contour_interval, base_contour, clip_features, out_contours, out_bands)