#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     05/04/2017
# Copyright:   (c) emartin 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, time, sys, os
import HR_DOR as hydroRout
import prepStreams as PS
from time import strftime
import myGlobals
import networkMetrics as NM
from collections import defaultdict
dateStamp= strftime("%Y%m%d_%I%M%S")
root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))

myWorkspace = arcpy.GetParameterAsText(0)
inStreams = arcpy.GetParameterAsText(1)
strUIDField = myGlobals.strUIDField 
segmentLengthField = "LengthKM"
inBarriers = arcpy.GetParameterAsText(2)
passabilityField = arcpy.GetParameterAsText(3)
snapDist = arcpy.GetParameterAsText(4)
singleGreatLakesFCN = arcpy.GetParameter(5)
singleOceanFCN = arcpy.GetParameter(6)
removeLargeRivers = arcpy.GetParameter(7)
outputFuncNet = os.path.join(myWorkspace, "FunctionalNetworks")
fNodeField = myGlobals.fNodeField
tNodeField = myGlobals.tNodeField
networkIDField = myGlobals.networkIDField
usNetID = myGlobals.usNetID
dsNetID =myGlobals.dsNetID
usStrID = myGlobals.usStrID
dsStrID = myGlobals.dsStrID
barrUIDField = myGlobals.barrUIDField
preppedNetwork = os.path.join(myWorkspace, "preppedNet")
preppedBarriers = os.path.join(myWorkspace, "preppedBarrs")
outHRTable = os.path.join(myWorkspace, "hr")
minStreamDASQKM = 0

arcpy.env.workspace = myWorkspace
arcpy.env.overwriteOutput = True



        
        
def main():
    try:
        bigStart = time.time()
        
        #populate barrier UID
        arcpy.AddField_management(inBarriers, barrUIDField, "LONG")
        fields = (barrUIDField,)
        i = 1
        with arcpy.da.UpdateCursor(inBarriers, fields) as rows:
            for row in rows:
                row[0] = i
                rows.updateRow(row)
                i +=1
        
        if removeLargeRivers == True: #remove large rivers from the analysis so tribs are separate FCNs
            streamsNoLargeRivers = os.path.join(myWorkspace, "rivers_noLarge")
            exp = "DivDASqKM < 100000"
            arcpy.Select_analysis(inStreams, streamsNoLargeRivers, exp)
            streams = streamsNoLargeRivers
        else:
            streams = inStreams
        barriers, splitStreams = PS.prepRivers(myWorkspace, streams, inBarriers, strUIDField, barrUIDField, snapDist, tNodeField, fNodeField, segmentLengthField, minStreamDASQKM, preppedNetwork, preppedBarriers, outHRTable, usStrID, dsStrID)

        #assign an NDOID for river termini
        fields = ("NDOID")
        v = 999999
        with arcpy.da.UpdateCursor(splitStreams, fields) as rows:
            for row in rows:
                if row[0] == None:
                    row[0] = v
                    v += 1
                rows.updateRow(row)

        #run hydroRout for selected barriers
        numpyTable, arcHRTable = runHR(splitStreams, barriers, myWorkspace, strUIDField, "NDOID", "NUOID",  barrUIDField, 1, (strUIDField, "NDOID", "NUOID", fNodeField, tNodeField, "GNIS_Name"))
        finalFuncNet = functionalNetworks(arcHRTable, splitStreams, barriers, outputFuncNet)
        uniqueTouchingBay(finalFuncNet)
        getBarrUSDSNetsNear(finalFuncNet, strUIDField, networkIDField, barriers, usNetID, dsNetID, usStrID, dsStrID)


        outBarrs = os.path.join(myWorkspace, "outBarrs")
        arcpy.CopyFeatures_management(barriers, outBarrs)
        networkMetrics(finalFuncNet, outBarrs, passabilityField)
        bigEnd = time.time()
        bigD = bigEnd-bigStart
        arcpy.AddMessage("Finished functional river networks analysis in {} seconds".format(bigD))

        arcpy.SetParameter(8, outputFuncNet)


    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem on FN main line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def networkMetrics(finalFuncNet, barriers, passabilityField):
    try:
        arcpy.AddMessage("...calulcating cumulative discounted...")
        metricsDict, finalUSCumuDict, finalDSCumuDict, sumDict = NM.calcMetrics(finalFuncNet, dateStamp, barriers, passabilityField)

        nameRoots = []
        fields = arcpy.ListFields(barriers)
        for field in fields:
            if field.name.startswith("dsSum"):
                nameRoots.append(field.name.replace("dsSum_", ""))

        #initialize dicts
        finalDict = {}  # {fcn : totalCumuDisc}
        for rootName in nameRoots:
            finalDict[rootName] = {}
        networkDSBarr = {}
        networkUSBarrs = defaultdict(list)
        passabilities = {}
        fields = (barrUIDField, myGlobals.usNetID, myGlobals.dsNetID, passabilityField)
        with arcpy.da.SearchCursor(barriers, fields) as rows:
            for row in rows:
                networkDSBarr[row[1]] = row[0] # these are inverse so that we get the DS barrier for the FCN
                networkUSBarrs[row[2]].append(row[0]) #if the barrier has this FCN DS add it to the list of others that do too
                passabilities[row[0]] = row[3]

        #get a list of funcNetIDs
        funcNetIDs = []
        fields = (myGlobals.networkIDField)
        with arcpy.da.SearchCursor(finalFuncNet, fields) as rows:
            for row in rows:
                funcNetIDs.append(row[0])
        funcNetIDs = list(set(funcNetIDs))

        for funcNet in funcNetIDs:
            for rootName in nameRoots:
                 ## if there's a downstream barrier, the final value is the US cumulative of the DS barrier
                 ## plus the DS cumulative of the ds barrier * its passabiltiy
                if funcNet in networkDSBarr:
                    dsBarr = networkDSBarr[funcNet]
                    dsBarrPass = passabilities[dsBarr]
                    usCumu = finalUSCumuDict[rootName][dsBarr]
                    dsCumu = finalDSCumuDict[rootName][dsBarr]
                    finalVal = usCumu + (dsCumu * dsBarrPass)
                    finalDict[rootName][funcNet] = finalVal

                elif funcNet in networkUSBarrs:
                    ## get the us barriers
                    usBarrs = networkUSBarrs[funcNet]
                    valsToSum = []
                    for usBarr in usBarrs:
                        selfLength = sumDict[segmentLengthField][funcNet]#should eb the same, since all share the same net
                        #add the usCumuVal * their passabilty to a list to be summed
                        usBarrPass = passabilities[usBarr]
                        usCumu =  finalUSCumuDict[rootName][usBarr]
                        product = usBarrPass * usCumu
                        valsToSum.append(product)
                    valsToSum.append(selfLength)
                    finalVal = sum(valsToSum)
                    finalDict[rootName][funcNet] = finalVal
                else: # there's no barrier on the network
                    finalDict[rootName][funcNet] = sumDict[rootName][funcNet]

        outTableName = "fcnCumulativeDiscounted"
        arcpy.CreateTable_management(myWorkspace, "fcnCumulativeDiscounted")
        outTable = os.path.join(myWorkspace, outTableName)
        arcpy.AddField_management(outTable, myGlobals.networkIDField, "DOUBLE")
        fieldsToAdd = []
        for key in finalDict:
            fieldsToAdd.append("sum_{}".format(key))
            fieldsToAdd.append("cumuDisc_{}".format(key))
            arcpy.AddField_management(outTable, "sum_{}".format(key), "DOUBLE")
            arcpy.AddField_management(outTable, "cumuDisc_{}".format(key), "DOUBLE")

        fields = [myGlobals.networkIDField] + fieldsToAdd
        cursor = arcpy.da.InsertCursor(outTable, fields)

        for netID in funcNetIDs:
            row = [netID]
            for field in fields:
                root = field.split("_")[-1]
                if field.startswith("cumuDisc_"):
                    row.append(finalDict[root][netID])
                if field.startswith("sum_"):
                    row.append(sumDict[root][netID])
            cursor.insertRow(row)
        del cursor
        arcpy.SetParameter(9, outTable)
        
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calculating network metrics line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def uniqueTouchingBay(network):
    #HydroRout calculates all networks touching the ocean as networkID = 0.  This functional gives each topologically
    #unique network its own ID
    try:
        s= time.time()
        arcpy.AddMessage("...separating terminal FCNs")
        #get the highest batNetID, this will be the starting point for new IDs
        batNetIDs = []
        fields = networkIDField
        with arcpy.da.SearchCursor(network, fields) as rows:
            for row in rows:
                batNetIDs.append(row[0])
        highestBatNetID = max(batNetIDs)
        startingNewBatNetID = highestBatNetID + 1

        #buffer the networks by a small amount, dissolving on all.  Then explode them and assign each an ID
        networks0 = "{}/batNet0".format(arcpy.env.scratchGDB)
        buffDisso = "{}/buffDisso".format(arcpy.env.scratchGDB)
        exploded = "{}/exploded".format(arcpy.env.scratchGDB)
        joined = "{}/joined".format(arcpy.env.scratchGDB)
        if singleGreatLakesFCN == True and singleOceanFCN == False:
            exp = "{} = 0 and GreatLakesArcs = 0".format(networkIDField)
        elif singleGreatLakesFCN == False and singleOceanFCN == True:
            exp = "{} = 0 and OceanArcs =0".format(networkIDField)    
        elif singleGreatLakesFCN == True and singleOceanFCN == True:
            exp = "({} = 0 and OceanArcs =0 and GreatLakesArcs =0)".format(networkIDField)
        else:
            exp = "{} = 0".format(networkIDField)
        arcpy.Select_analysis(network, networks0, exp)
        arcpy.DeleteField_management(networks0, networkIDField)
        arcpy.Buffer_analysis(in_features = networks0, out_feature_class=buffDisso, buffer_distance_or_field="0.01 Meters", dissolve_option="ALL")
        arcpy.MultipartToSinglepart_management(buffDisso, exploded)
        arcpy.AddField_management(exploded, networkIDField, "LONG")
        fields = networkIDField
        with arcpy.da.UpdateCursor(exploded, fields) as rows:
            for row in rows:
                row[0] = startingNewBatNetID
                startingNewBatNetID +=1
                rows.updateRow(row)

        #join back to source
        arcpy.MakeFeatureLayer_management(networks0, "networkLyr")
        arcpy.MakeFeatureLayer_management(exploded, "polyLyr")
        arcpy.SpatialJoin_analysis("networkLyr", "polyLyr", joined)
        newNetIDDict = {}
        fields = (strUIDField, networkIDField)
        with arcpy.da.SearchCursor(joined, fields) as rows:
            for row in rows:
                newNetIDDict[row[0]] = row[1]

        with arcpy.da.UpdateCursor(network, fields) as rows:
            for row in rows:
                if row[0] in newNetIDDict:
                    row[1] = newNetIDDict[row[0]]
                    rows.updateRow(row)

        e= time.time()
        arcpy.AddMessage("...finished adding network IDs to networks that touch the ocean in {} seconds".format(e-s))

    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calculating networkIDs for networks touching the ocean on functionalNetworks line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()


def functionalNetworks(HRtable, riverNetwork, barriers, outputFuncNet):
    try:
        start = time.time()
        finalFuncNet = outputFuncNet
        arcpy.CopyFeatures_management(riverNetwork, finalFuncNet)
        dictJoin("plainJoin", True, HRtable, strUIDField, finalFuncNet, strUIDField, (networkIDField,))
        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished exporting functional river networks  in {} seconds".format(duration))
        return finalFuncNet
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calculating functional networks on functionalNetworks line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def getBarrUSDSNetsNear(streams, strIDField, networkIDField, barriers, usNetField, dsNetField, usSegField, dsSegField):
    try:
        start = time.time()
        field_names = [f.name for f in arcpy.ListFields(barriers)]
        for fld in (usNetField, dsNetField):#, usSegField, dsSegField):
            if fld in field_names:
                arcpy.DeleteField_management(barriers, fld)
            arcpy.AddField_management(barriers, fld, "LONG")

        #populate a dictionary with all the segments and their Network_IDs
        netDict = {}
        fields =(strIDField, networkIDField)
        with arcpy.da.SearchCursor(streams, fields) as rows:
            for row in rows:
                netDict[row[0]] = row[1]

        fields = (usSegField, dsSegField, usNetField, dsNetField)


        with arcpy.da.UpdateCursor(barriers, fields) as rows:
            for row in rows:
                usSegID = row[0]
                dsSegID = row[1]
                try:
                    row[2] = netDict[usSegID]
                except Exception as e:
                    row[2] = None
                try:
                    row[3] = netDict[dsSegID]
                except Exception as e:
                    row[3] = None
                rows.updateRow(row)

        #Remove barriers with Nulls with US/DS Seg or US/DS NEtwork.  These are not snapped
        #and cuase problme later on -- NO -- instead removed unsnapped barriers earlier
        ## arcpy.MakeFeatureLayer_management(barriers, "barrLyr")
        ## exp = "{} is null or {} is null".format(usSegField, dsSegField)
        ## arcpy.SelectLayerByAttribute_management("barrLyr", "NEW_SELECTION", exp)
        ## arcpy.DeleteFeatures_management("barrLyr")

        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished getting us & ds network IDs for barriers in {} seconds".format(duration))

    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="getting us & ds network IDs for barriers on functionalNetworks line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def runHR(streams, barriers, workspace, strUIDField, dnSegID, upSegID,  barrUIDField, export, keepFields):
    start = time.time()
    arcTable, numpyTable = hydroRout.run(streams, barriers, workspace, strUIDField, dnSegID, upSegID,  barrUIDField, export, keepFields, networkIDField)
    # arcpy.CopyRows_management(arcTable, outHRTable)
    end = time.time()
    duration = end-start
    arcpy.AddMessage("...finished HR in {} seconds".format(duration))


    start = time.time()
    dictJoin("plainJoin", True, arcTable, strUIDField, streams, strUIDField, (networkIDField,))
    end = time.time()
    duration = end-start
    arcpy.AddMessage("...finished dictionary join in {} seconds".format(duration))

    return numpyTable, arcTable


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
        valueDict = dict([(r[0], (list(r[i] for i in fieldNums))) for r in arcpy.da.SearchCursor(sourceFC, sCursorFields)])

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
                            arcpy.AddMessage("Join type does not match the join type options of 'plainJoin', 'addJoin', or 'timesJoin'.  Enter one fo these options and try again...")
                            sys.exit()
                else:
                    pass
            del valueDict

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddWarning("Problem dictionary join on line {}. {}".format(tb.tb_lineno, e))


if __name__ == '__main__':
    main()
