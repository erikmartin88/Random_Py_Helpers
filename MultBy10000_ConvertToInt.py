#*********************************************************************************
#Mulitply RC values by 1000 to convert to interger grids.  Should have done this earlier to speed things up.

import arcpy
from arcpy.sa import *
from datetime import datetime

Workspace = r"K:\RegionalDatasets\Climate\NLDAS\tavg_shift_rc.gdb"
arcpy.env.workspace = Workspace	
avgRCRasterList = arcpy.ListRasters()

Workspace = r"K:\RegionalDatasets\Climate\NLDAS\tavg_shift_rc_10000.gdb"
arcpy.env.workspace = Workspace	
thousandRCRasterList = arcpy.ListRasters()

for avgRCRaster in avgRCRasterList:
	saveName = avgRCRaster + "_1000"
	if saveName not in thousandRCRasterList:
		arcpy.AddMessage("Running " + avgRCRaster)
		arcpy.AddMessage(datetime.now())
		inRasName = "K:\\RegionalDatasets\\Climate\\NLDAS\\tavg_shift_rc.gdb\\" + avgRCRaster
		inRas = Raster(inRasName)
		thouRas = inRas * 10000
		intRas = Int(thouRas)
		intRas.save(saveName)