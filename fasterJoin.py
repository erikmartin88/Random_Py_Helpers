#-------------------------------------------------------------------------------
# Name:        Faster Join
# Purpose:      A faster way to join fields from one ArcGIS Feature Class to another
#
# Author:      Erik Martin, emartin@tnc.org
#
# Created:     26/07/2016
# Copyright:   (c) emartin 2016
#-------------------------------------------------------------------------------
import arcpy
import sys

source = r"K:\RegionalDatasets\EastDivision\NEAquaticHabitatClassification\flowlines_nahcs.shp"
update = r"K:\NAACC\CurrentData.gdb\ProjectDendrite"

def main():
    #Only need to open an edit session if working on a Geometric Network or some such thing
##    with arcpy.da.Editor("K:/NAACC/CurrentData.gdb") as edit:
##        dictJoin(False, source, "COMID", update, "COMID", "DA_Area", "DA_Forest", "DA_Ag", "DA_Natural", "DA_ImprvCount", "DA_ImprvSum")
    dictJoin(True, source, "COMID", update, "COMID", "NESLPCL", "D_NESLPCL", "NEGEOCL", "D_NEGEOCL", "NETEMPCL", "D_NETEMPCL")


def dictJoin(addField, sourceFC,  sourceJoinField, updateFC, updateJoinField, fields):
    """
        addField: boolean whether field has to be added to update table -- faster if False
        sourceFC: the feature class that has the fields to be joined
        sourceJoinField: the field from the source FC that will be used ot make the join
        updateFC: the feature class that will have values added to it
        updateJoinField: the field from the updateFC that is used to make the join
        fields: fields to be joined-- as a list - must add a trailing comma if only one field
    """

    try:
        #add new empty fields
        if addField == True:
            fieldsToAdd = arcpy.ListFields(sourceFC)
            for fieldToAdd in fieldsToAdd:
                if fieldToAdd.name in fields:
                    arcpy.AddField_management(updateFC, fieldToAdd.name, fieldToAdd.type)

        #get the number of join fields and add on the source join ID
        numJoinFields = len(fields)
        sCursorFields = [sourceJoinField] + list(fields)
        fieldNums = list(range(1, numJoinFields + 1))

        #populate the dict with the source join ID and fields to Join
        print("Populating valueDict...")
        valueDict = dict([(r[0], (list(r[i] for i in fieldNums))) for r in arcpy.da.SearchCursor(sourceFC, sCursorFields)])

        print("Updating fields...")
        uCursorFields = [updateJoinField] + list(fields)
        with arcpy.da.UpdateCursor(updateFC, uCursorFields) as updateRows:
            for updateRow in updateRows:
                joinFieldValue = updateRow[0]
                if joinFieldValue in valueDict and joinFieldValue != None:
                    i = 1
                    while i <= numJoinFields:
                        updateRow[i] = valueDict[joinFieldValue][i-1]
                        updateRows.updateRow(updateRow)
                        i +=1
                else:
                    pass
            del valueDict

    except Exception as e:
        tb = sys.exc_info()[2]
        print(("Problem dictionary join on line {}".format(tb.tb_lineno)))
        print((e.message))
        sys.exit()

if __name__ == '__main__':
    main()
