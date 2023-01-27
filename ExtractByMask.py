import arcpy
from arcpy.sa import *


Workspace = r"K:\RegionalDatasets\Climate\PRISM\PRISM.gdb"
arcpy.env.workspace = Workspace

rasterList = arcpy.ListRasters("*tm*", "All")
for raster in rasterList:
	mask = r"K:\CT_River_Basin\GIS_Data\CT_River_Basin.shp"
	outExtractByMask = ExtractByMask(raster, mask)
	outExtractByMask.save("K:\\CT_River_Basin\\GIS_Data\\ClimateData.gdb\\" + raster)
	
	

