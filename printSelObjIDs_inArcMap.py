objIDs = []
fields = ("OBJECTID")
with arcpy.da.SearchCursor("Indigenous lands", fields) as rows:
     for row in rows:
         objIDs.append(row[0])
		 
print objIDs
