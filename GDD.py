#*********************************************************************************
#Calulate GDD from reclasses avg rasters

import arcpy
from arcpy.sa import *
from datetime import datetime


yearList = ['1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']

Workspace = r"K:\RegionalDatasets\Climate\NLDAS\tavg_shift_rc.gdb"
arcpy.env.workspace = Workspace	
avgRCRasterList = arcpy.ListRasters()

Workspace = r"K:\RegionalDatasets\Climate\GDD.gdb"
arcpy.env.workspace = Workspace	
gddRasterList = arcpy.ListRasters()

for year in yearList:
	gddList = []
	saveName = "GGD_" + year
	arcpy.AddMessage("Running year" + year)
	arcpy.AddMessage(datetime.now())
	for avgrc in avgRCRasterList:
		if year in avgrc and saveName not in gddRasterList:
			arcpy.AddMessage("Adding " + avgrc + " at " + str(datetime.now()) )
			gddList.append("K:\\RegionalDatasets\\Climate\\NLDAS\\tavg_shift_rc.gdb\\" + avgrc)
	arcpy.AddMessage("Calculating GDD for " + year)
	GDD = CellStatistics(gddList, "SUM", "NODATA")
	GDD.save("K:\\RegionalDatasets\\Climate\\GDD.gdb\\" + saveName)
#*********************************************************************************