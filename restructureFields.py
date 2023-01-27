import time, arcpy
fc = "K:/SECOORA_WindTool/DataLayers/leases.gdb/temp"
fs = arcpy.ListFields(fc)
for f in fs:
    print((f.name))
    if f.type== "Integer":
        vals = {}
        fields = ("GRID_ID", f.name)
        with arcpy.da.SearchCursor(fc, fields) as rows:
            for row in rows:
                vals[row[0]] = row[1]
	
        arcpy.DeleteField_management(fc, f.name)
        arcpy.AddField_management(fc, f.name, "SHORT")
        with arcpy.da.UpdateCursor(fc, fields) as rows:
            for row in rows:
                row[1] = vals[row[0]]
                rows.updateRow(row)

    elif f.type == "String" and f.name != "GRID_ID":
        vals = {}
        fields = ("GRID_ID", f.name)
        with arcpy.da.SearchCursor(fc, fields) as rows:
            for row in rows:
                vals[row[0]] = row[1]
        arcpy.DeleteField_management(fc, f.name)
        arcpy.AddField_management(fc, f.name, "TEXT", field_length="20")
        with arcpy.da.UpdateCursor(fc, fields) as rows:
            for row in rows:
                row[1] = vals[row[0]]
                rows.updateRow(row)
    else:
        pass