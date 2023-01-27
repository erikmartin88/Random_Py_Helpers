#-------------------------------------------------------------------------------
# Name:        Select downstream barriers
# Purpose:      traverse batUSNetID and batDSNetID (or fromnode / tonode) and
#               populate a list with the downstream barrier IDs
#
# Author:      emartin
#
# Created:     01/08/2016
# Copyright:   (c) emartin 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
dams = r"K:\NAACC\MetricCalc\MetricCalcs.gdb\Insignificant\Use_Insignificant"
def main():
    myDict = {}
    fields = ("UNIQUE_ID", "batUSNetID","batDSNetID")
    print("Building dict")
    with arcpy.da.SearchCursor(dams, fields) as rows:
        for row in rows:
            myDict[row[0]] = (row[1], row[2])

    dsIDs = []
    getDSids("xy3664830182553503", myDict, dsIDs)
    print("dsIDs= {}".format(dsIDs))


def getDSids(startID, myDict, ids):
    """
    function to find all the downstream ids of a barrier by traversing the
    batUSNetID & batDSNetID
    startID: the barrier for which all downstream barriers are being found
    myDict: a dictionary of the barrier table where myDict["UNIQUE_ID"] = (batUSNetID, batDSNetID)
    ids = an empty list that will be populated with all of the downstream IDs
    """
    for key, value in myDict.iteritems():
        if value[0] == myDict[startID][1]:
            ids.append(key)
            return(getDSids(key, myDict, ids))


if __name__ == '__main__':
    main()
