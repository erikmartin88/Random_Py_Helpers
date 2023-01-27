import arcpy
	
arcpy.env.workspace = r"K:\RegionalDatasets\Climate\NLDAS\NLDAS.gdb"
rasterList = arcpy.ListRasters("*max*")
print(rasterList)
for raster in rasterList:
	arcpy.AddMessage("Moving raster " + raster)
	arcpy.Copy_management(raster, r"K:\RegionalDatasets\Climate\NLDAS\tmax.gdb\%s" %raster)
	arcpy.Delete_management(raster)
	
arcpy.env.workspace = r"K:\RegionalDatasets\Climate\NLDAS\NLDAS.gdb"
rasterList = arcpy.ListRasters("*min*")
print(rasterList)
for raster in rasterList:
	arcpy.AddMessage("Moving raster " + raster)
	arcpy.Copy_management(raster, r"K:\RegionalDatasets\Climate\NLDAS\tmin.gdb\%s" %raster)
	arcpy.Delete_management(raster)