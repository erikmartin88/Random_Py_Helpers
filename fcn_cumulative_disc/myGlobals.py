#-------------------------------------------------------------------------------
# Name:        Global variables for Maine statewide barrier prioritization
#
# Author:      emartin@tnc.org
#
# Created:     28/06/2018
#-------------------------------------------------------------------------------
import logging, datetime, os, sys, glob, arcpy
from time import strftime

dateStamp= strftime("%Y%m%d_%I%M%S")

#workspace variables
myWorkspace = "in_memory"
scriptPath = sys.path[0]
primeFolder = os.path.dirname(scriptPath)
GDBName = "Metrics.gdb"
metricsGDBFullPath = os.path.join(primeFolder, GDBName)
archiveFolder = "K:\\NRCS_CIG\\GIS\\Archive"


funcNetName ="FunctionalRiverNetwork"

strUIDField = "UNIQIDSZ2070"
barrUIDField = "barrUID"
barrNameField = "DamName"
snapDist ="100 Meters"
fNodeField = "From_Node"
tNodeField = "To_Node"
networkIDField = "batNetID"
segLengthField = "LengthKM"
usStrID = "usStrID" #name of US segmentID field given to barriers
dsStrID = "dsStrID" #name of DS segmentID field given to barriers
DA_kmField = "TotDASqKM"
preppedNetworkFullPath = "{}/preppedNetwork".format(metricsGDBFullPath)
preppedBarriers ="{}/preppedBarriers".format(metricsGDBFullPath)
artPathField = "lengexcl"


outHRTable = "{}/OutputHR_Networks".format(metricsGDBFullPath)
outputBarriers ="{}/Output_Barriers".format(metricsGDBFullPath)
minStreamDASQKM = 0
outputDict = {}
weightedValueFields =  ["LengthKM","LengthKMNoArts"] # these are fields that will be summarized in the cumulative US network
usNetID = "usNetID" #name of US functional network field given to barriers
dsNetID = "dsNetID" #name of DS functional network field given to barriers
usStrID = "usStrID" #name of US segmentID field given to barriers
dsStrID = "dsStrID" #name of DS segmentID field given to barriers



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
        print("Running dictionary Join  at {}...".format(stamp()))
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
        print("...Populating valueDict at {}...".format(stamp()))
        valueDict = dict([(r[0], (list(r[i] for i in fieldNums))) for r in arcpy.da.SearchCursor(sourceFC, sCursorFields)])

        print("...Updating values in join at {}...".format(stamp()))
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
                            print("Join type does not match the join type options of 'plainJoin', 'addJoin', or 'timesJoin'.  Enter one fo these options and try again...")
                            sys.exit()
                else:
                    pass
            del valueDict

    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem dictionary join on line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def stamp():
    myNow = str(datetime.datetime.now()).split('.')[0]
    return myNow