import arcpy
from arcpy.sa import *
sourceWorkspace = "K:\\LakeTanganyika\\WebMap\\MapService\\AfricanGreatLakes_WM.gdb\\"
outputWorksapce ="K:\\LakeTanganyika\\WebMap\\MapService\\AfricanGreatLakes_WM_clip.gdb\\"
arcpy.env.workspace = sourceWorkspace
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True

failList = []
try:
    rasterList = arcpy.ListRasters()
    for raster in rasterList:
        print(("Extracting {}".format(raster)))
        outRaster = outputWorksapce + raster

        try:
            arcpy.gp.ExtractByMask_sa(raster, "K:/LakeTanganyika/WebMap/MapService/AfricanGreatLakes_WM_clip.gdb/AreaInterest", outRaster)
        except:
            failList.append(raster)
    print(failList)
    arcpy.CheckInExtension('Spatial')

except Exception as e:
    tb = sys.exc_info()[2]
    print(("Problem calculating geology metrics on line {}".format(tb.tb_lineno)))
    print((e.message))
    sys.exit()
    arcpy.CheckInExtension('Spatial')