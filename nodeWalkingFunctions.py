#-------------------------------------------------------------------------------
# Name:        various functions to walk networks
# Purpose:
#
# Author:      emartin
#
# Created:     02/07/2021
# Copyright:   (c) emartin 2021
#-------------------------------------------------------------------------------
import sys, arcpy, datetime

def main():
    pass


def walkUp(startIDs, myDict, ids):
    """
    function to find all the upstream ids of a segment by traversing the
    fNode and tNode
    startID: the segment for which all upstream segments are being found
    myDict: a dictionary of the river table where myDict[segID] = (fNode, tNode)
    ids = an empty list that will be populated with all of the upstream IDs
    """
    try:
        curIDs = []
        for startID in startIDs:
            for key, value in myDict.iteritems():
                if value[1] == myDict[startID][0]:
                    ids.append(key)
                    curIDs.append(key)
        if curIDs !=[]:
            walkUp(curIDs, myDict, ids)
        return ids
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting upstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def walkDown(startIDs, myDict, ids):
    """
    function to find all the downstream segment ids of a segment by traversing the
    fNode and tNode.  Walks downstream (straightline path) AND up a final tributary
    if there is one
    startID: the segment for which all downstream segments are being found
    myDict: a dictionary of the river table where myDict[segID] = (fNode, tNode)
    ids = an empty list that will be populated with all of the downstream IDs
    """

    try:
        curIDs = []
        for startID in startIDs:
            for key, value in myDict.iteritems():
                if value[0] == myDict[startID][1]:
                    ids.append(key)
                    curIDs.append(key)

        if curIDs !=[]:
            return(walkDown(curIDs, myDict, ids))

        #try walking up from the last to see if there's a trib to go up
        #find if there's a trib coming in
        if len(ids) >0:
            lastDSSeg = ids[-1]
            lastToNode = myDict[lastDSSeg][1]

            for key, value in myDict.iteritems():
                if value[1] == lastToNode and key != lastDSSeg:
                    ids.append(key)
                    walkUp([key], myDict, ids)
        return ids
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))


def buildNetworkDict(fc, segID, NDOID, NUOID):
    """
    function to build dictionaries with the downstream segment ID and upstream
    segment IDs.  Using the HydroRout NDOID and NUOID format
    """
    try:
        fields = (segID, NDOID, NUOID)
        dsSegDict = {}
        usSegDict = {}
        with arcpy.da.SearchCursor(fc, fields) as rows:
            for row in rows:
                dsSegDict[row[0]] =  row[1]
                if row[2] != "":
                    usSegDict[row[0]] =  [int(i) for i in row[2].split("_")]
                else:
                    usSegDict[row[0]] =  []

        return dsSegDict, usSegDict

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem building network dict on line {} at {}. {}".format(tb.tb_lineno, stamp(), e))
        arcpy.AddError(str(e))
        sys.exit()

def buildNodeDict(fc, segID, fNodeField, tNodeField):
    """
    function to build a dictionary of from_nodes and to_nodes from a river FC
    """
    try:
        fields = (segID, fNodeField, tNodeField)
        nodeDict = {}
        with arcpy.da.SearchCursor(fc, fields) as rows:
            for row in rows:
                nodeDict[row[0]] = [row[1], row[2]]

        return nodeDict

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem building node dict on line {} at {}. {}".format(tb.tb_lineno, stamp(), e))
        arcpy.AddError(str(e))
        sys.exit()

def getUSsegs(startIDs, myDict, usIDs):
    """
    function to find all the downstream ids of a barrier by traversing the
    NUOIDs (HydroRout format)
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segmentID] = NDOID
    usIDs an empty list to append to
    """
    try:
        curIDs = []
        if startIDs != [-999]:
            for startID in startIDs:
                usIDs.append(startID)
                for usVal in myDict[startID]:
                    usIDs.append(usVal)
                    curIDs.append(usVal)
        if curIDs !=[]:
            getUSsegs(curIDs, myDict, usIDs)
        return list(set(usIDs))

    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting upstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))


def getDSsegs(startID, myDict, dsIDs):
    """
    function to find all the downstream ids of a barrier by traversing the
    NDOID (HydroRout format)
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segmentID] = NDOID
    dsIDs an empty list to append to
    """
    try:
        for key in myDict:
            if key == startID:
                dsVal = myDict[key]
                dsIDs.append(dsVal)
                return (getDSsegs(myDict[key], myDict, dsIDs))
        return dsIDs
    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem getting downstream IDs on networkMetrics line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def stamp():
    myNow = str(datetime.datetime.now()).split('.')[0]
    return myNow

if __name__ == '__main__':
    main()
