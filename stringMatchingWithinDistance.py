#-------------------------------------------------------------------------------
# Name:        Distance name matches
# Purpose:      Find potential matches between points based on a search
#               distance and string comparison
#
# Author:      Erik Martin, The Nature COnservancy, emartin@tnc.org
#
# Created:     Sept 5, 2013
#-------------------------------------------------------------------------------

import arcpy
import sys
from collections import defaultdict
def main():
    try:
        arcpy.env.overwriteOutput=True
        # User Variables -------------------------------------------------------
        #feature class with duplicate records
        fc = r"C:\Users\emartin\Desktop\To_Erik_9_22\Erikscriptrun.gdb\SEPT_19_DATABASE_ALL_DUPLICATES_REMOVED1"
        nameField = "Dam_name"
        matchField = "PotenMatch"
        reasonField = "DupeReason"

        #distance with which to search for duplicates.  In map units
        searchDist = "500"

        # Word pairs to not mark as duplicates.  e.g. "upper" & "lower"
        # use lower case
        keyPairs= {
        "1" : "2",
        "upper" : "lower",
        "3" : "4",
        "2" : "3",
        "4" : "5",
        "5" : "6",
        "6" : "7",
        "7" : "8",
        }
##        keyWordPairs = [("1", "2"), ("1","3"), ("1", "4"), ("2", "3"), ("2", "4"), ("2", "5"), ("3", "4"), ("3", "5"), ("3", "6"), ("4", "5"), ("4","6"), ("4", "7"), ("5", "6"), ("5", "7"), ("5", "8"), ("6", "7"), ("6",  "8"), ("6", "9"), ("7", "8"), ("7", "9") , ("8", "9"), ("upper", "lower"), ("upper", "middle"), ("middle", "lower")]


        #-----------------------------------------------------------------------

        workspace = "in_memory"
        arcpy.env.workspace = workspace
        arcpy.MakeFeatureLayer_management(fc, "fc_lyr")
        fc_lyr = "fc_lyr"

        fields = ("OBJECTID", nameField, matchField, reasonField)
        with arcpy.da.UpdateCursor(fc_lyr, fields) as rows:
            for row in rows:
                objID = row[0]
                print(("running OBJECTID # " + str(objID)))
                if row[2] == 1:
                    print ("already flagged")
                if row[2] == 0:
                    arcpy.MakeFeatureLayer_management(fc, "selector", '"OBJECTID" = {}'.format(objID))
                    origInName = row[1]
                    inName = origInName.lower()
                    inName = inName.replace("dam" , "")
                    inName = inName.replace("lake" , "")
                    inName = inName.replace("pond" , "")
                    inName = inName.replace("." , "")
                    inName = inName.replace("#" , "")
                    inName = inName.replace("," , "")


                    arcpy.SelectLayerByLocation_management(fc_lyr, "WITHIN_A_DISTANCE", "selector", searchDist)
                    arcpy.SelectLayerByLocation_management(fc_lyr, "INTERSECT", "selector", "", "REMOVE_FROM_SELECTION")
                    arcpy.CopyFeatures_management(fc_lyr, "nearFeats")

                    with arcpy.da.SearchCursor("nearFeats", fields) as nearRows:
                        nearNameList = []

                        for nearRow in nearRows:
                            nearPotMatch = nearRow[2]
                            origNearName = nearRow[1]
                            nearObjID = nearRow[0]
                            nearName = origNearName.lower()
                            nearNameList.append(nearName)

                            if (len(nearNameList) >= 1 and (row[2] == 0) and nearRow[2] == 0):

                                print(("    in name = " + origInName + "  near name = " + origNearName))
                                match = set(inName.split()).intersection(set(nearName.split()))
                                lenMatch = (len(match))
                                match = str(match)
                                matchPretty = match.replace("set([", "")
                                matchPretty = matchPretty.replace("u'", "'")
                                matchPretty = matchPretty.replace("])", "")

                                keyWordMatch = 0
                                for key, value in keyPairs.items():
                                    #identify potential dupes that have both pairs of key words
                                    if ((inName.find(key)!=-1) and (nearName.find(value)!=-1)):
                                        keyWordMatch = 1
                                        print("    dam names include key words to ignore")
                                        row[2] = 2
                                        row[3]= "Match with objid {} but includes keywords to ignore. inName='{}'.  nearName='{}'".format(nearObjID, origInName, origNearName)
                                    if ((inName.find(value)!=-1) and (nearName.find(key)!=-1)):
                                        keyWordMatch = 1
                                        print("    dam names include key words to ignore")
                                        row[2] = 2
                                        row[3]= "Match with objid {} but includes keywords to ignore. inName='{}'.  nearName='{}'".format(nearObjID, origInName, origNearName)


                                if((lenMatch>0) and (nearPotMatch == 0) and (keyWordMatch == 0)):

                                    print(("    match on '{}' Adding flag".format(matchPretty)))
                                    row[2] = 1
                                    row[3] = "Dupe with objID {}. inName ='{}'.  nearName='{}'. Match words = '{}'".format(nearObjID, origInName, origNearName, matchPretty)

                                else:
                                    print("    no match")
                                    row[2] = 0
                                rows.updateRow(row)

    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem finding matched records...")
        print("Line {}".format(tb.tb_lineno))
        print(e.message)
        sys.exit()
if __name__ == '__main__':
    main()