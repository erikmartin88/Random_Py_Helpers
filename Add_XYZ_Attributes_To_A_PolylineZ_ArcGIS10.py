try:

    print ("Add the start node, end node geometry and line slope to the attribute table...")
    print ("A Two-Bit Algorithms, L.O.L. product (gerry@gabrisch.us)")
    print ("Copyright 2013 Gerry Gabrisch")
    print
    import arcpy, math, os, sys, traceback
    print ("go")
    infc = arcpy.GetParameterAsText(0)
    #infc = r"C:\gtemp\WDFWStreamCatalogWork\StreamCatalog.gdb\testData_SplitLine"
    fieldList = arcpy.ListFields(infc)
    fieldList2 = []
    for field in fieldList:
        fieldList2.append(field.name)


    if " FROM_X" not in fieldList2:
        arcpy.AddField_management(infc, "FROM_X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    if "FROM_Y" not in fieldList2:
        arcpy.AddField_management(infc, "FROM_Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED","")
    if "FROM_Z" not in fieldList2:
        arcpy.AddField_management(infc, "FROM_Z", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED","")
    if  "TO_X" not in fieldList2:
        arcpy.AddField_management(infc, "TO_X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED","")
    if "TO_Y" not in fieldList2:
        arcpy.AddField_management(infc, "TO_Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED","")
    if "TO_Z" not in fieldList2:
        arcpy.AddField_management(infc, "TO_Z", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED","")
    if "PERC_SLOPE" not in fieldList2:
        arcpy.AddField_management(infc, "PERC_SLOPE","DOUBLE","", "", "", "", "NULLABLE", "NON_REQUIRED","")

    Alltheparts = []

    g = arcpy.Geometry()
    geometryList = arcpy.CopyFeatures_management(infc, g)
    
    for geometry in geometryList:
        firstPoint = geometry.firstPoint
        lastPoint =  geometry.lastPoint
        lineLength = geometry.length
        therun = geometry.length
        if firstPoint.Z:
            therise = firstPoint.Z- lastPoint.Z
            percentSlope = (therise/therun *100)
        else:
            firstPoint.Z = -999
            lastPoint.Z = -999
            percentSlope = -999
        partGeometry = [firstPoint.X,firstPoint.Y,firstPoint.Z,lastPoint.X, lastPoint.Y, lastPoint.Z, percentSlope]
        Alltheparts.append(partGeometry)
    counter = 0
    rows = arcpy.UpdateCursor(infc)
    for row in rows:
        row.setValue("FROM_X",Alltheparts[counter][0])
        row.setValue("FROM_Y",Alltheparts[counter][1])
        row.setValue("FROM_Z",Alltheparts[counter][2])
        row.setValue("TO_X",Alltheparts[counter][3])
        row.setValue("TO_Y",Alltheparts[counter][4])
        row.setValue("TO_Z",Alltheparts[counter][5])
        row.setValue("PERC_SLOPE",Alltheparts[counter][6])
        counter += 1
        rows.updateRow(row)

    print ("Done")

except arcpy.ExecuteError: 
    msgs = arcpy.GetMessages(2) 
    arcpy.AddError(msgs) 
    print (msgs)
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    print (pymsg + "\n")
    print (msgs)