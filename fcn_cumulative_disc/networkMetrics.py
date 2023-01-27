#-------------------------------------------------------------------------------
# Name:        Network Metrics
# Purpose:     calculate basin-scale metrics for connectivity to the ocean
# Author:      emartin@tnc.org
#
# Created:     April 18, 2018
# Copyright:   (c) emartin 2018
#-------------------------------------------------------------------------------
import arcpy, time, myGlobals, sys, datetime, functools
from collections import defaultdict

networkIDField = myGlobals.networkIDField
segmentLengthField = myGlobals.segLengthField
weightedValueFields =myGlobals.weightedValueFields

usNetID = myGlobals.usNetID
dsNetID = myGlobals.dsNetID
barrUIDField = myGlobals.barrUIDField


outputDict = myGlobals.outputDict


def main():
    pass

def calcMetrics(funcNet, dateStamp, barriers, passabilityField):
    try:
        outputDict["1. Scenario"] = dateStamp

        # connectedToOcean(funcNet)
        sumDict = summarizeBarrierUSValues(barriers, funcNet, networkIDField, weightedValueFields)
        finalUSCumuDict, finalDSCumuDict = weightedFuncNet(barriers, weightedValueFields, passabilityField, sumDict)

        return outputDict, finalUSCumuDict, finalDSCumuDict, sumDict
    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem in calcMetrics line {} at {}. {}".format(tb.tb_lineno, stamp(), e))
        arcpy.AddError(str(e))
        sys.exit()
        
def summarizeBarrierUSValues(barriers, funcNetwork, networkIDField, weightedValueFields):
    try:
        sumDicts = {}
        for valueField in weightedValueFields:
            listDict = defaultdict(list)
            fields = (networkIDField, valueField)
            with arcpy.da.SearchCursor(funcNetwork, fields) as rows:
                for row in rows:
                    if row[1] != None:
                        listDict[row[0]].append(row[1])
                    else:
                        listDict[row[0]].append(0)
            sumDict = {}
            for k, v in listDict.iteritems():
                sumDict[k] = sum(v)

            #Join to barriers
            usAddField = "usSum_{}".format(valueField)
            arcpy.AddField_management(barriers, usAddField, "DOUBLE")
            dsAddField = "dsSum_{}".format(valueField)
            arcpy.AddField_management(barriers, dsAddField, "DOUBLE")
            fields = (usNetID, usAddField, dsNetID, dsAddField)
            with arcpy.da.UpdateCursor(barriers, fields) as rows:
                for row in rows:
                    if row[0] != None:
                        row[1] = sumDict[row[0]]
                    else:
                        row[1] = 0
                    if row[2] != None:
                        row[3] = sumDict[row[2]]
                    else:
                        row[3] = 0
                    rows.updateRow(row)

            #for each of the metrics being summed, add the results dictionary into a master dictionary
            sumDicts[valueField] = sumDict

        return sumDicts
    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem in summarize US values line {} at {}. {}".format(tb.tb_lineno, stamp(), e))
        arcpy.AddError(str(e))
        sys.exit()



def connectedToOcean(funcNetwork):
    #run closest to ocean metrics
    expression =  "{} = 0".format(networkIDField) #With HydroRout, 0 is connected to the ocean
    arcpy.MakeFeatureLayer_management(funcNetwork, "lowestNetwork", expression)
    fields=(segmentLengthField)
    longestTotalNet2Ocean = fieldSum("lowestNetwork", segmentLengthField)
    longestTotalNet2OceanMiles = longestTotalNet2Ocean * 0.621371
    outputDict["Unobstructed Ocean Access (miles)"] = longestTotalNet2OceanMiles


def fieldSum(netLayer, sumField):
    sumList = []
    fields=(sumField)
    with arcpy.da.SearchCursor(netLayer, fields) as rows:
        for row in rows:
            sumList.append(row[0])
    sumResult = sum(sumList)
    return sumResult


def weightedFuncNet(barriers, valueFields, passabilityField, sumDict):
    try:
        finalUSDict = {}
        finalDSDict = {}
        for valueField in valueFields:
            usBarrierValueField = "usSum_{}".format(valueField)
            dsBarrierValueField = "dsSum_{}".format(valueField)

            fields = (barrUIDField, usNetID, dsNetID, usBarrierValueField, dsBarrierValueField, passabilityField)
            #get a list of barriers with 0 passability that will define the upper extent of a functional network
            stops = []
            with arcpy.da.SearchCursor(barriers, fields) as rows:
                for row in rows:
                    thisPass = row[5]
                    if thisPass == 0:
                        stops.append(str(row[0]))

            netDict = {}
            uIDs =[]
            #Build a dictionary with the key values
            with arcpy.da.SearchCursor(barriers, fields) as rows:
                for row in rows:
                    bUIDval = row[0]
                    usNetIDval = row[1]
                    dsNetIDval = row[2]
                    usBarrierValueFieldVal = row[3]
                    dsBarrierValueFieldVal = row[4]
                    thisPass = row[5]
                    netDict[bUIDval] = (usNetIDval, dsNetIDval, usBarrierValueFieldVal, dsBarrierValueFieldVal, thisPass)
                    uIDs.append(bUIDval)


            finalUSDict[valueField] = {}
            finalDSDict[valueField] = {}
            usNetPassDict = {}

            for uID in uIDs: #process each barrier

                #get the us cumulative discounted value
                calcUSCumuDiscVal(uID, netDict, stops, usNetPassDict, finalUSDict[valueField])

                dsVal = getDSCumulative(uID, netDict, stops)
                finalDSDict[valueField][uID] = dsVal


            finalUSCumuDiscField = "usCumuDisc_{}".format(valueField)
            arcpy.AddField_management(barriers, finalUSCumuDiscField, "DOUBLE")
            finalDSCumuDiscField = "dsCumuDisc_{}".format(valueField)
            arcpy.AddField_management(barriers, finalDSCumuDiscField, "DOUBLE")
            fields = (barrUIDField, finalUSCumuDiscField, usBarrierValueField, finalDSCumuDiscField, dsBarrierValueField)
            with arcpy.da.UpdateCursor(barriers, fields) as rows:
                for row in rows:
                    row[1] = finalUSDict[valueField][row[0]]
                    try:
                        row[3] = finalDSDict[valueField][row[0]]
                    except:
                        row[3] = -999
                    rows.updateRow(row)

        return finalUSDict, finalDSDict

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem calculating weighted us functional network on networkMetrics line {} at {}. {}".format(tb.tb_lineno, stamp(), e))
        arcpy.AddError(str(e))
        sys.exit()


def getDSCumulative(uID, netDict, stops):
    try:
        # netDict[bUIDval] = (usNetIDval, dsNetIDval, usBarrierValueFieldVal, dsBarrierValueFieldVal, thisPass)
        finalValsToSum = [] # create a list that will hold all the values to be summed in the end

        # get DS barrID
        firstDownID = None
        for key, value in netDict.iteritems():
            if value[0] == netDict[uID][1]:
                firstDownID = key  # this is the first barrier downstream.
                # arcpy.AddMessage("first down ID = {}".format(firstDownID))
                break

        if firstDownID != None:
            if netDict[firstDownID][4] == 0:  # if the next dam down is a full barrier, just return the DS value that's already calcd
                return netDict[uID][3]
            stops.append(str(uID)) #the current barrier should be a stop -- when tracing back up from DS barrs, don't want to go through this barr
            passScores = [1] #this will be a list to hold all ds passabiltiy scores. Start out with 1, since the ds net get full credit
            upTribs(firstDownID, netDict, stops, finalValsToSum, passScores) #this is where the action ahppens
        else: #if there's no other barrier downstream, just take the ds func net length
            return netDict[uID][3]

        finalVal = sum(finalValsToSum)
        return finalVal

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError(
            "Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        arcpy.AddError(str(e))

def upTribs(thisID, netDict, stops, finalValsToSum, passScores):
    try:
        # arcpy.AddMessage("Processing dsID {} up to {}".format(thisID, previousID))
        # traceupstream from dsID
        usNetPassDict = {} #don't actrually use this, but create since it's used in US tracing
        finalUSDict = {} #final dictionary to hold the ds cumulative discounted values for each barrier
        downID = None #initialize to none
        # arcpy.AddMessage("stops used = {}".format(stops))
        nextDownSum = calcUSCumuDiscVal(thisID, netDict, stops, usNetPassDict, finalUSDict) #get the cumulative discounted US value for the barrier downstream when this barrier is considered to be a full barrier
        # arcpy.AddMessage("nextDownSum = {}".format(nextDownSum))
        # arcpy.AddMessage("Pass scores = {}".format(passScores))
        passScoreProd = functools.reduce((lambda x, y: x * y), passScores) #get the product of all current passability scores
        # arcpy.AddMessage("Formula = {} * {}".format(nextDownSum, passScoreProd))
        nextDownVal = nextDownSum * passScoreProd # get the product pf the cum values and the passability scores
        # arcpy.AddMessage("mod us cumulative for {} = {}".format(thisID, nextDownVal))
        finalValsToSum.append(nextDownVal) #add the final value to the list to be summed
        # arcpy.AddMessage("finalValsToSum = {}".format(finalValsToSum))
        stops.pop() #remove the current barrier from the list of stops

        #get the next barrier downstream
        for key, value in netDict.iteritems():
            if value[0] == netDict[thisID][1]:
                downID = key  # this is the next barrier downstream.
                break
        if downID != None:
            nextDownMultiplier = netDict[thisID][4] #the passabiltiy of the current barrier will be the multiplier for the downstream barriers US discounted network
            # arcpy.AddMessage("nextDownPass = {}".format(nextDownMultiplier))
            if nextDownMultiplier != 0: #if the next downstream barrier is not a full barrier
                passScores.append(nextDownMultiplier) #add this barrier's passability score to the list
                stops.append(str(thisID)) #make this barrier a stop now
                return (upTribs(downID,  netDict, stops, finalValsToSum, passScores)) #and repeat the process

        else:
            nextDownMultiplier = netDict[thisID][4]  # the passabiltiy of the current barrier will be the multiplier for the downstream barriers US discounted network
            passScores.append(nextDownMultiplier)
            passScoreProd = functools.reduce((lambda x, y: x * y), passScores)  # get the product of all current passability scores
            val = netDict[thisID][3] * passScoreProd  #if there's no more downstream barriers, take the DS value for this barrier * its passabiltiy
            finalValsToSum.append(val)

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        arcpy.AddError(str(e))

def calcDSCumuDiscVal(uID, netDict, stops, netPassDict, finalDict):
    try:
        # process upstream cumulative discounted
        dsTribIDs = []
        getDSTribIDs([uID, ], netDict, dsTribIDs, stops)  # get the upstream barriers


        usVals = []
        for dsTribID in dsTribIDs:  # process the upstream barriers
            dsIDs = []
            getDSids(dsTribID, netDict, dsIDs)  # get a list of the barriers downstream of each upstream barrier
            dsIDs = dsIDs[:dsIDs.index(uID)]  # remove the uID barrier and all further downstream barriers from the list
            dsPassScores = []
            if dsIDs == []:  # if there are no downstream barriers in the list, we know that this is the next barrier upstream
                usVal = netDict[dsTribID][2] * netDict[dsTribID][4]  # multiple the funcUS * passability
                dsPassScores.append(netDict[dsTribID][4])  # do this separately for the ds passability scores that will be assigned ot the networks
            else:  # otherwise, this barrier is several barriers upstream of the target barrier
                passabilityScores = []  # initialize a list that will hold the passability scores
                for myid in dsIDs:
                    passabilityScores.append(netDict[myid][4])  # for each of the barriers between the US barrier and the target barrier, add their passability score to a list
                    dsPassScores.append(netDict[myid][4])
                passabilityScores.append(netDict[dsTribID][4])  # also add the passability score of the US barrier
                dsPassScores.append(netDict[dsTribID][4])  # also add the passability score of the US barrier
                passabilityMultiplier = functools.reduce(lambda x, y: x * y, passabilityScores)  # multiply all the passability scores together
                usVal = netDict[dsTribID][2] * passabilityMultiplier  # multiply the passability multiplier by the batFuncUS of the US barrier to get the cumulative (depreciated) upstream network of the US barrier
            netPassDict[dsTribID] = functools.reduce(lambda x, y: x * y, dsPassScores)  # multiply all the passability scores together
            usVals.append(usVal)  # sum up all the values of the upstream barriers
            finalDict[uID] = sum(usVals)  # write the final value to a dictionary tied to teh target barrier ID

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError(
            "Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        arcpy.AddError(str(e))
        finalDict[uID] = -999  # add a flag for those that throw an error.  This will happen if there are duplicate points


def calcUSCumuDiscVal(uID, netDict, stops, netPassDict, finalDict):
    try:
        # process upstream cumulative discounted
        usIDs = []
        getUSids([uID, ], netDict, usIDs, stops)  # get the upstream barriers
        usVals = []
        for usID in usIDs:  # process the upstream barriers
            dsIDs = []
            getDSids(usID, netDict, dsIDs)  # get a list of the barriers downstream of each upstream barrier
            try:
                dsIDs = dsIDs[:dsIDs.index(uID)]  # remove the uID barrier and all further downstream barriers from the list
            except:
                arcpy.AddWarning("{} not in dsID list".format(uID))
            dsPassScores = []
            if dsIDs == []:  # if there are no downstream barriers in the list, we know that this is the next barrier upstream
                usVal = netDict[usID][2] * netDict[usID][4]  # multiple the funcUS * passability
                dsPassScores.append(netDict[usID][4])  # do this separately for the ds passability scores that will be assigned ot the networks
            else:  # otherwise, this barrier is several barriers upstream of the target barrier
                passabilityScores = []  # initialize a list that will hold the passability scores
                for myid in dsIDs:
                    passabilityScores.append(netDict[myid][4])  # for each of the barriers between the US barrier and the target barrier, add their passability score to a list
                    dsPassScores.append(netDict[myid][4])
                passabilityScores.append(netDict[usID][4])  # also add the passability score of the US barrier
                dsPassScores.append(netDict[usID][4])  # also add the passability score of the US barrier
                passabilityMultiplier = functools.reduce(lambda x, y: x * y, passabilityScores)  # multiply all the passability scores together
                usVal = netDict[usID][2] * passabilityMultiplier  # multiply the passability multiplier by the batFuncUS of the US barrier to get the cumulative (depreciated) upstream network of the US barrier
            netPassDict[usID] = functools.reduce(lambda x, y: x * y, dsPassScores)  # multiply all the passability scores together
            usVals.append(usVal)  # sum up all the values of the upstream barriers
        usVals.append(netDict[uID][2])
        finalVal = sum(usVals)
        finalDict[uID] = finalVal  # write the final value to a dictionary tied to teh target barrier ID
        return finalVal

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        arcpy.AddError(str(e))
        finalDict[uID] = -999  # add a flag for those that throw an error.  This will happen if there are duplicate points

def getDSStop(startID, myDict, stops):
    """
    function to find all the downstream ids of a barrier by traversing the
    batUSNetID & batDSNetID
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict["UNIQUE_ID"] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the downstream IDs
    """
    #netDict[bUIDval] = (usNetIDval, dsNetIDval, usBarrierValueFieldVal, dsBarrierValueFieldVal, thisPass)
    try:
        for key, value in myDict.iteritems():
            if value[0] == myDict[startID][1]:
                if str(key) not in stops:
                    return(getDSStop(key, myDict, stops))
                else:
                    return key



    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def getDSidsToStop(startID, myDict, ids, stops):
    """
    function to find all the downstream ids of a barrier by traversing the
    batUSNetID & batDSNetID
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict["UNIQUE_ID"] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the downstream IDs
    """
    #netDict[bUIDval] = (usNetIDval, dsNetIDval, usBarrierValueFieldVal, dsBarrierValueFieldVal, thisPass)
    try:
        for key, value in myDict.iteritems():
            if value[0] == myDict[startID][1]:
                ids.append(key)
                if str(key) not in stops:
                    return(getDSidsToStop(key, myDict, ids, stops))
            if str(key) in stops:
                break
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def getDSids(startID, myDict, ids, stop=None):
    """
    function to find all the downstream ids of a barrier by traversing the
    batUSNetID & batDSNetID
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict["UNIQUE_ID"] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the downstream IDs
    """
    try:

        for key, value in myDict.iteritems():
            if value[0] == myDict[startID][1] and str(key) != stop:
                ids.append(key)
                return(getDSids(key, myDict, ids))
            if str(key) == stop:
                break
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def getDSTribIDs(startIDs, myDict, ids, stops):
    """
    function to find all the upstream ids of a barrier by traversing the
    fNode and tNode
    startID: the barrier for which all upstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segID] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the upstream IDs
    """
    try:
        curIDs = []
        for startID in startIDs:
            for key, value in myDict.iteritems():
                if value[0] == myDict[startID][1] and str(key) not in stops:
                    ids.append(key)
                    curIDs.append(key)
        if curIDs !=[]:
            getDSTribIDs(curIDs, myDict, ids, stops)
        return ids
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting upstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def getUSids(startIDs, myDict, ids, stops):
    """
    function to find all the upstream ids of a barrier by traversing the
    fNode and tNode
    startID: the barrier for which all upstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segID] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the upstream IDs
    """
    try:
        curIDs = []
        for startID in startIDs:
            for key, value in myDict.iteritems():
                if value[1] == myDict[startID][0] and str(key) not in stops:
                    ids.append(key)
                    curIDs.append(key)
        if curIDs !=[]:
            getUSids(curIDs, myDict, ids, stops)
        return ids
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting upstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def stamp():
    myNow = str(datetime.datetime.now()).split('.')[0]
    return myNow

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
##        print("Running dictionary Join  at {}...".format(stamp()))
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
##        print("...Populating valueDict at {}...".format(stamp()))
        valueDict = dict([(r[0], (list(r[i] for i in fieldNums))) for r in arcpy.da.SearchCursor(sourceFC, sCursorFields)])

##        print("...Updating values in join at {}...".format(stamp()))
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

if __name__ == '__main__':
    main()
