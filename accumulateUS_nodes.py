#-------------------------------------------------------------------------------
# Name:        Accumulate US values using nodes
# Purpose:      traverse network using fromnode / tonode and sums upstream
#               values.  Add result to an accumulation field
#
# Author:      emartin
#
# Created:     July 25, 2017
# Copyright:   (c) emartin 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import time

streams = r"C:\Users\emartin\Desktop\accumulate.gdb\Rivieres_total"
sourceField = "ctch_sqkm"
accumField = "da_sqkm"
segIDField = "NOID"
fNodeField = "From_Node"
tNodeField = "To_Node"


def main():
    start = time.time()
    myDict = {}
    fields = (segIDField, fNodeField, tNodeField)
    print("Building dict")
    with arcpy.da.SearchCursor(streams, fields) as rows:
        for row in rows:
            myDict[row[0]] = (row[1], row[2])

##    dsIDs = []
##    getDSids(3, myDict, dsIDs)
##    print("dsIDs= {}".format(dsIDs))


    #get a list of all segment IDs
    allIDs = []
    with arcpy.da.SearchCursor(streams, segIDField) as rows:
        for row in rows:
            allIDs.append(row[0])

    #init a dict to hold accumulated values
    accumDict = {}
    #for each segment
    for segID in allIDs:
        segStart = time.time()
        usIDs = []
        #find its upstream IDs
        idstart = time.time()
        resIDs = getUSids([segID], myDict, usIDs)
        resIDs.append(segID) #include the original segemnt in the accumulation
        idend=time.time()
        idur= idstart - idend
        print(("Got id for segemnt {} in {} sec".format(segID, idur)))

        #sum the values
        accstart = time.time()
        accumVal = sumValues(streams, segIDField, sourceField, resIDs)
        #write the accumulated value to a dictionary
        accumDict[segID] = accumVal
        accend = time.time()
        accdur = accstart-accend
        print(("...Accumumalated segemnt {} in {} sec".format(segID, accdur)))
        segEnd = time.time()
        segDuration = segEnd - segStart
        print(("...Finished segemnt {} in {} sec".format(segID, segDuration)))

    #write accumulated value back to streams
    fields = (segIDField, accumField)
    with arcpy.da.UpdateCursor(streams, fields) as rows:
        for row in rows:
            row[1] = accumDict[row[0]]
            rows.updateRow(row)

    end = time.time()
    duration = end-start
    print(("finished accumulation in {} seconds".format(duration)))


def getDSids(startID, myDict, ids):
    """
    function to find all the downstream ids of a barrier by traversing the
    fNode and tNode
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segID] = (fNode, tNode)
    ids = an empty list that will be populated with all of the downstream IDs
    """
    for key, value in myDict.items():
        if value[0] == myDict[startID][1]:
            ids.append(key)
            return(getDSids(key, myDict, ids))

def getUSids(startIDs, myDict, ids):
    """
    function to find all the upstream ids of a barrier by traversing the
    fNode and tNode
    startID: the barrier for which all upstream barriers are being found
    myDict: a dictionary of the barrier table where myDict[segID] = (fNode, tNode)
    ids = an empty list that will be populated with all of the upstream IDs
    """
    curIDs = []
    for startID in startIDs:
        for key, value in myDict.items():
            if value[1] == myDict[startID][0]:
                ids.append(key)
                curIDs.append(key)
    if curIDs !=[]:
        getUSids(curIDs, myDict, ids)
    return ids

def sumValues(streams, segIDField, sourceField, ids):
    """Sum a attribute values based on a list of feature IDs
    streams: stream network
    segIDField: field with unique IDs
    sourceField: field with values to be summed
    ids: a list of IDs to be summed
    """
    vals=[]
    ids = tuple(ids)
    fields = (segIDField, sourceField)
    idsStr = str(ids).rstrip(')')
    idsStr = idsStr.rstrip(',')
    idsStr = idsStr +")"
    exp = "{} in {}".format(segIDField, idsStr)
    with arcpy.da.SearchCursor(streams, fields, exp) as rows:
        for row in rows:
            vals.append(row[1])
    accumVal = sum(vals)
    return accumVal





if __name__ == '__main__':
    main()
