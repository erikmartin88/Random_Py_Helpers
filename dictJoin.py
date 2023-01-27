#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     08/04/2021
# Copyright:   (c) emartin 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, sys, os, datetime
def main():
    sourceFC = r"K:\OffshoreWindMap\Data\FinalData.gdb\ALL_WHALES_HIGHBIO_WITHPRESENCE_V3"
    updateFC = r"K:\OffshoreWindMap\Data\FinalData.gdb\MONTHLY_WHALES_HIGHBIO_V2"
    sourceJoinField = "GRID_ID"
    updateJoinField = "GRID_ID"
    fields = "M001,M002,M004,M005,M006,M007,M008,M009,M010,M011,M012,M013,M015,M016,M017,M018,M019,M020,M021,M022,M023,M024,M025,M026,M028,M029,M030,M031,M032"
    dictJoin("plainJoin", False, sourceFC, sourceJoinField, updateFC, updateJoinField, fields)


def dictJoin(joinType, addField, sourceFC,  sourceJoinField, updateFC, updateJoinField, fields):
    """
        joinType: 'plainJoin', 'addJoin' or 'timesJoin' to either join in the updated field, or add or multiple join value by existing value
        addField: boolean whether field has to be added to update table -- faster if False
        sourceFC: the feature class that has the fields to be joined
        sourceJoinField: the field from the source FC that will be used ot make the join
        updateFC: the feature class that will have values added to it
        updateJoinField: the field from the updateFC that is used to make the join
        fields: fields to be joined-- as a list - must add a trailing comma if only one field
    """
    try:
        print("......running dictionary Join...")
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
        print("...Populating valueDict...")

        valueDict = dict([(r[0], (list(r[i] for i in fieldNums))) for r in arcpy.da.SearchCursor(sourceFC, sCursorFields)])
        print (valueDict)

        print("...Updating values in join...")
        uCursorFields = [updateJoinField] + list(fields)
        with arcpy.da.UpdateCursor(updateFC, uCursorFields) as updateRows:
            for updateRow in updateRows:
                joinFieldValue = updateRow[0]
                if joinFieldValue in valueDict and joinFieldValue != None:
                    i = 1
                    while i <= numJoinFields:
                        if joinType == "plainJoin":
                            updateRow[i] = valueDict[joinFieldValue][i-1]
                            updateRows.updateRow(updateRow)
                            i +=1
                        elif joinType == "addJoin":
                            updateRow[i] = updateRow[i] + valueDict[joinFieldValue][i-1]
                            updateRows.updateRow(updateRow)
                            i +=1
                        elif joinType == "timesJoin":
                            updateRow[i] = updateRow[i] * valueDict[joinFieldValue][i-1]
                            updateRows.updateRow(updateRow)
                            i +=1
                        elif joinType == "custom":
                            pass
                        else:
                            arcpy.AddError("Join type does not match the join type options of 'plainJoin', 'addJoin', or 'timesJoin'.  Enter one fo these options and try again...")
                            sys.exit()
                else:
                    pass
            del valueDict

    except Exception as e:
        tb = sys.exc_info()[2]
        msg = "Problem with dictionary join on functionalNetworks line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()



def stamp():
    myNow = str(datetime.datetime.now()).split('.')[0]
    return myNow

if __name__ == '__main__':
    main()
