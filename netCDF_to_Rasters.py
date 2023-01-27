import arcpy
from arcpy.sa import *
from dateutil import rrule
from datetime import datetime

arcpy.env.overwriteOutput = True
Workspace = "K:\\RegionalDatasets\\Climate\\NLDAS\\"
arcpy.env.workspace = Workspace
outpath = "K:\\RegionalDatasets\\Climate\\NLDAS\\NLDAS.gdb\\"
yearList = [1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010] 

baseNameMax = "K:\\RegionalDatasets\\Climate\\NLDAS\\nldas_met_update.obs.daily.tasmax.YEAR.nc"
baseNameMin = "K:\\RegionalDatasets\\Climate\\NLDAS\\nldas_met_update.obs.daily.tasmin.YEAR.nc"
for year in yearList:
	fileNameMax = baseNameMax.replace("YEAR", str(year))
	fileNameMin = baseNameMin.replace("YEAR", str(year))
	print fileNameMax
	print fileNameMin
	
	#Get all of the days in each of the years
	a = '1/1/%s' %year
	b = '12/31/%s' %year	
	for dt in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(a, '%m/%d/%Y'),until=datetime.strptime(b, '%m/%d/%Y')):
		day = dt.strftime('%m/%d/%Y') #formatted for use in the SelectByDimension tool
		dayName = day.replace("/", "_")	#formatted for use in file saving
		
		#copy the Max temperature rasters of each of the days in the year
		arcpy.MakeNetCDFRasterLayer_md(fileNameMax, "tasmax", "longitude", "latitude", "tasmax_Layer", "#", "time #" ,"BY_VALUE")
		arcpy.SelectByDimension_md("tasmax_Layer","time %s" %day,"BY_VALUE") 
		outfileMax = outpath + "tasmax_" + dayName
		print "Saving file " + outfileMax
		arcpy.AddMessage("Saving file " + outfileMax)
		arcpy.CopyRaster_management("tasmax_Layer",outfileMax ,"#","#","-999","NONE","NONE","#","NONE","NONE")
		
		#copy the Min temperature rasters of each of the days in the year
		arcpy.MakeNetCDFRasterLayer_md(fileNameMin, "tasmin", "longitude", "latitude", "tasmin_Layer", "#", "time #" ,"BY_VALUE")
		arcpy.SelectByDimension_md("tasmin_Layer","time %s" %day,"BY_VALUE") 
		outfileMin = outpath + "tasmin_" + dayName
		print "Saving file " + outfileMin
		arcpy.AddMessage("Saving file " + outfileMin)
		arcpy.CopyRaster_management("tasmin_Layer",outfileMin ,"#","#","-999","NONE","NONE","#","NONE","NONE")