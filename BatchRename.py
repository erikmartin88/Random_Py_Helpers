import arcpy
Workspace = "K:\\RegionalDatasets\\Climate\\GDD.gdb\\"
arcpy.env.workspace = Workspace

#datasets must not be in dataframe... either add warning message or loop through layers and remove actvie layer from current DF

#Rasters
rasterList = arcpy.ListRasters("GDD*", "All")
for raster in rasterList:
	newname = raster.replace("__", "_")
	print (raster)
	print (newname)
	arcpy.Rename_management(raster, newname)

#Feature Classes	
fcList = arcpy.ListFeatureClasses("Shift_GDD*", "All")
for fc in fcList:
	newname = fc.replace("Base10", "Base0")
	print (raster)
	print (newname)
	arcpy.Rename_management(fc, newname)