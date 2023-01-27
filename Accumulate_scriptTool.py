#-------------------------------------------------------------------------------
# Erik Martin, The Nature Conservancy, emartin@tnc.org, July 2013
#
# Accumulate upstream attributes tool.  Utilizes Geometric Network tools & requires
# ArcGIS 10.1 or greater.
#
# Script provided as-is.
#-------------------------------------------------------------------------------

import arcpy
import sys
Workspace = "in_memory"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = Workspace
import time

def accumulate():
    try:
        #variables
        network = arcpy.GetParameterAsText(0)
        netHydroFC_path = arcpy.GetParameterAsText(1)
        nonNetHydroFC = arcpy.GetParameterAsText(2)
        accumSourceField1 = arcpy.GetParameterAsText(3)
        accumTargetField1 = arcpy.GetParameterAsText(4)
        fields = ("OBJECTID", accumSourceField1, accumTargetField1)
        numFields = 1
        if arcpy.GetParameterAsText(5)!= "":
            accumSourceField2 = arcpy.GetParameterAsText(5)
            accumTargetField2 = arcpy.GetParameterAsText(6)
            fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2)
            numFields = 2
        if arcpy.GetParameterAsText(7) != "":
            accumSourceField3 = arcpy.GetParameterAsText(7)
            accumTargetField3 = arcpy.GetParameterAsText(8)
            fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2, accumSourceField3, accumTargetField3)
            numFields = 3
        if arcpy.GetParameterAsText(9) != "":
            accumSourceField4 = arcpy.GetParameterAsText(9)
            accumTargetField4 = arcpy.GetParameterAsText(10)
            fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2, accumSourceField3, accumTargetField3, accumSourceField4, accumTargetField4)
            numFields = 4
        if arcpy.GetParameterAsText(11) != "":
            accumSourceField5 = arcpy.GetParameterAsText(11)
            accumTargetField5 = arcpy.GetParameterAsText(12)
            fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2, accumSourceField3, accumTargetField3, accumSourceField4, accumTargetField4, accumSourceField5, accumTargetField5)
            numFields = 5
        if arcpy.GetParameterAsText(13) != "":
            accumSourceField6 = arcpy.GetParameterAsText(13)
            accumTargetField6 = arcpy.GetParameterAsText(14)
            fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2, accumSourceField3, accumTargetField3, accumSourceField4, accumTargetField4, accumSourceField5, accumTargetField5, accumSourceField6, accumTargetField6)
            numFields = 6
        calculateMe = arcpy.GetParameterAsText(15)

        #get the text name of the network FC without the full path by taking what's after the last "\"
        netHydroFC = netHydroFC_path.split("\\")[-1].strip()

        #list fields to include in cursor
        ##fields = ("OBJECTID", accumSourceField1, accumTargetField1, accumSourceField2, accumTargetField2, accumSourceField3, accumTargetField3)
        arcpy.AddMessage("Running...")
        #open arcpy.da cursor
        with arcpy.da.UpdateCursor(nonNetHydroFC, fields) as rows:
            arcpy.AddMessage(fields)
            print(fields)
            for row in rows:
                #get values for each row
                rowObjID = row[0]

                #if there are Nulls in the source field, treat them as 0s, otherwise use value
                if row[1] is None:
                    rowCtchVal1 = 0
                else:
                    rowCtchVal1 = float(row[1])
                DAval1 = float(row[2])
                if numFields >1:
                    if row[3] is None:
                        rowCtchVal2 = 0
                    else:
                        rowCtchVal2 = float(row[3])
                if numFields >2:
                    if row[5] is None:
                        rowCtchVal3 = 0
                    else:
                        rowCtchVal3 = float(row[5])
                if numFields >3:
                    if row[7] is None:
                        rowCtchVal4 = 0
                    else:
                        rowCtchVal4 = float(row[7])
                if numFields >4:
                    if row[9] is None:
                        rowCtchVal5 = 0
                    else:
                        rowCtchVal5 = float(row[9])
                if numFields >5:
                    if row[11] is None:
                        rowCtchVal6 = 0
                    else:
                        rowCtchVal6 = float(row[11])

                #If there's already an accumulated value skip that record
                if DAval1 != int(calculateMe):
                    arcpy.AddMessage("ObjectID " + str(rowObjID) + " is already calculated")

                #If the value is equal to the "calculate me" flag run the operation
                if DAval1 == int(calculateMe):

                    start = time.time()
                    #make a feature layer in memory and select the record that is active in the cursor
                    arcpy.MakeFeatureLayer_management(nonNetHydroFC, "sel_lyr")
                    selection = '"OBJECTID" = {}'.format(rowObjID)
                    arcpy.SelectLayerByAttribute_management("sel_lyr", "NEW_SELECTION", selection)

                    #create a point at the start vertex of the selected record
                    arcpy.FeatureVerticesToPoints_management("sel_lyr", "flag", "START")

                    #select the upstream network & take the line layer from the returned layer group (network + junctions)
                    flag = "flag"
                    arcpy.TraceGeometricNetwork_management(network, "netLayer", flag, "TRACE_UPSTREAM")
                    usSelection = arcpy.SelectData_management("netLayer", netHydroFC)

                    #sum first field
                    field = accumSourceField1
                    usVals1 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                    sumUSVals1 = float(sum(usVals1))
                    newDAVal1 = float(sumUSVals1 + rowCtchVal1)
                    row[2] = newDAVal1

                    #if selected, sum 2nd field
                    if numFields >= 2:
                        field = accumSourceField2
                        usVals2 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                        sumUSVals2 = float(sum(usVals2))
                        newDAVal2 = float(sumUSVals2 + rowCtchVal2)
                        row[4] = newDAVal2

                    #if selected, sum 3rd field
                    if numFields >= 3:
                        field = accumSourceField3
                        usVals3 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                        sumUSVals3 = float(sum(usVals3))
                        newDAVal3 = float(sumUSVals3 + rowCtchVal3)
                        row[6] = newDAVal3

                    #if selected, sum 4th field
                    if numFields >= 4:
                        field = accumSourceField4
                        usVals4 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                        sumUSVals4 = float(sum(usVals4))
                        newDAVal4 = float(sumUSVals4 + rowCtchVal4)
                        row[8] = newDAVal4

                    #if selected, sum 5th field
                    if numFields >= 5:
                        field = accumSourceField5
                        usVals5 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                        sumUSVals5 = float(sum(usVals5))
                        newDAVal5 = float(sumUSVals5 + rowCtchVal5)
                        row[10] = newDAVal5

                    #if selected, sum 6th field
                    if numFields == 6:
                        field = accumSourceField6
                        usVals6 = [r[0] for r in arcpy.da.SearchCursor(usSelection, (field))]
                        sumUSVals6 = float(sum(usVals6))
                        newDAVal6 = float(sumUSVals6 + rowCtchVal6)
                        row[12] = newDAVal6

                    end = time.time()
                    duration = end-start
                    duration = round(duration, 2)
                    arcpy.AddMessage("Finished ObjectID# {} in {} seconds.".format(rowObjID, duration))
                    print(("Finished ObjectID# {} in {} seconds.".format(rowObjID, duration)))

                rows.updateRow(row)

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError("Problem accumulating values...")
        arcpy.AddError("Line {}".format(tb.tb_lineno))
        arcpy.AddError(e.message)
        sys.exit()

if __name__ == '__main__':
    accumulate()