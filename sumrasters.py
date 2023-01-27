import os,sys
import arcpy
from arcpy.sa import *

sPath = sys.path[0]
dataPath = 'C:/temp/data' # ADD your workspace path here
outPath = 'C:/temp/output'

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('Spatial')
arcpy.env.scratchWorkspace = outPath
arcpy.env.workspace = dataPath
#create a list of rasters in the workspace
rasters = arcpy.ListRasters('','')

i = 0
#loop through rasters in list
for raster in rasters:
    print("processing raster: %s" %os.path.join(dataPath,raster))

    #convert nodata to zero
    out1 = Con(IsNull(raster), 0, raster)

    #sum rasters together
    if i == 0:
        out2 = arcpy.Raster(out1)
        i += 1
    else:
        out2 = out2 + out1
        i += 1

#save final output
out.save(os.path.join(outPath,'sumRas'))
