# Split of data by year into new gdbs

import arcpy
from arcpy.sa import *

yearList = ['1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995']#, '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']

for year in yearList:
	gdbName = "tavg_shift_rc_10000_" + year + ".gdb"
	print gdbName
	arcpy.CreateFileGDB_management("H:\\TNC", gdbName)
	outGDBName = "H:\\TNC\\" + gdbName + "\\"
	print "Out GDB " + outGDBName + " made"
	arcpy.env.workspace = r"K:\RegionalDatasets\Climate\NLDAS\tavg_shift_rc_10000.gdb"
	thousandRCRasterList = arcpy.ListRasters("*%s*" %year) 
	
	for thousandRCRaster in thousandRCRasterList:
		inName = "K:\\RegionalDatasets\\Climate\\NLDAS\\tavg_shift_rc_10000.gdb\\" + thousandRCRaster
		saveName = outGDBName + thousandRCRaster
		print "Loading " + thousandRCRaster
		arcpy.CopyRaster_management(inName, saveName, "", "", "", "", "", "32_BIT_SIGNED")