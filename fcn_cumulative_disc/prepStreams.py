#-------------------------------------------------------------------------------
# Name:        Prep streams
# Purpose:     Steps to prepare rivers and barriers from the NHDPlus (preprocessed to a dendrite)
#               & a combined barrier dataset for the Kennebec DST - BART.
#
# Author:      emartin@tnc.org
#
# Created:     April 18, 2018
# Copyright:   (c) emartin 2018
#-------------------------------------------------------------------------------
import arcpy
import time
import sys, os
import UpstreamIDs_PandasForLargeLayers as usIDs
from collections import defaultdict
import myGlobals



arcpy.env.overwriteOutput = True

def main():
    pass



def prepRivers(myWorkspace, inStreams, inBarriers, strUIDField, barrUIDField, snapDist, tNodeField, fNodeField, segmentLengthField, minStreamDASQKM, preppedNetwork, preppedBarriers, outHRTable, usStrID, dsStrID):
    arcpy.env.workspace = myWorkspace
    
    #make a copy of barriers, snap them, and delete unsnapped barriers 
    barriers = snap(inBarriers, inStreams, myWorkspace, snapDist)
       
    splitStreams = fracture(inStreams, barriers, myWorkspace, segmentLengthField,)
    newID(splitStreams, strUIDField)
    newNodes(splitStreams, fNodeField, tNodeField)
    upDownIDs(splitStreams, strUIDField, fNodeField, tNodeField)
    getBarrUSDSIdsNear(splitStreams, strUIDField, barriers, usStrID, dsStrID, myWorkspace, fNodeField, tNodeField, barrUIDField)
    setBarrierStreamSegID(barriers, strUIDField, usStrID)

    # export(splitStreams, preppedNetwork, barriers, preppedBarriers)
    return barriers, splitStreams


def snap(sourceBarriers, streams, myWorkspace, snapDist):
    try:
        #Make a working copy of the barriers and snap them to streams
        start = time.time()
        barriers = os.path.join(myWorkspace, "snappedBarriers")
        arcpy.CopyFeatures_management(sourceBarriers, barriers)
        arcpy.Snap_edit(barriers, [[streams, "EDGE", snapDist]])
        barrLyr = "barrLyr"
        arcpy.MakeFeatureLayer_management(barriers, barrLyr)
        arcpy.SelectLayerByLocation_management(barrLyr, "INTERSECT", streams)
        arcpy.SelectLayerByAttribute_management(barrLyr, "SWITCH_SELECTION")
        arcpy.DeleteFeatures_management(barrLyr)
        
        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished snapping barriers in {} seconds".format(duration))
        return barriers
    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddError("Problem snapping on line {}. {}".format(tb.tb_lineno,e))
 

        
def fracture(streams, barriers, myWorkspace, segmentLengthField,):
    try:
        #Split the streams at the barrier locations
        start = time.time()
        splitStreams ="{}/Fracture".format(myWorkspace)
        filteredStreams ="{}/filteredStreams".format(myWorkspace)

        exp = "1=1"
        arcpy.Select_analysis(streams, filteredStreams, exp)
        arcpy.SplitLineAtPoint_management(filteredStreams, barriers, splitStreams, "1 Meters")

        #get length of new segments
        arcpy.AddField_management(splitStreams, segmentLengthField, "DOUBLE")
        segLengthNoArtPaths = "{}NoArts".format(segmentLengthField)
        arcpy.AddField_management(splitStreams, segLengthNoArtPaths, "DOUBLE")
        fields = ("SHAPE@LENGTH", segmentLengthField, segLengthNoArtPaths, myGlobals.artPathField)
        with arcpy.da.UpdateCursor(splitStreams, fields) as rows:
            for row in rows:
                row[1] = row[0]/1000
                if row[3] == 1: #this is a lake/pond artificial path
                    row[2] = 0
                else:
                    row[2] = row[0]/1000
                rows.updateRow(row)

        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished fracture in {} seconds".format(duration))
        return splitStreams

    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem running fracture on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def newID(streams, strUIDField):
    try:
        #Add a new Segment ID for each segment of the newly split streams, based on OBJECTID
        start = time.time()
        fields = (strUIDField)
        i = 1
        with arcpy.da.UpdateCursor(streams, fields) as rows:
            for row in rows:
                row[0] = i
                rows.updateRow(row)
                i +=1
        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished new stream IDs in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem adding new IDs on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def newNodes(input_lines, fNodeField, tNodeField):
    try:
        #Create new From and To nodes for the newly split streams
        start = time.time()
        arcpy.AddField_management(input_lines, fNodeField, "LONG")
        arcpy.AddField_management(input_lines, tNodeField, "LONG")

        xy_dict = {}
        fields =('SHAPE@', fNodeField, tNodeField)
        with arcpy.da.UpdateCursor(input_lines, fields) as rows:
            for row in rows:
                # From Node
                from_key = '{},{}'.format(round(row[0].firstPoint.X, 7), round(row[0].firstPoint.Y, 7))
                if from_key in xy_dict:
                    row[1] = xy_dict[from_key]
                else:
                    row[1] = len(xy_dict) + 1
                    xy_dict[from_key] = len(xy_dict) + 1

                # To Node
                to_key = '{},{}'.format(round(row[0].lastPoint.X, 7), round(row[0].lastPoint.Y, 7))
                if to_key in xy_dict:
                    row[2] = xy_dict[to_key]
                else:
                    row[2] = len(xy_dict) + 1
                    xy_dict[to_key] = len(xy_dict) + 1
                rows.updateRow(row)
        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished making new nodes in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calcing nodes on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def upDownIDs(streams, strUIDField, fNodeField, tNodeField):
    try:
        #for each segemnt populate fields with the upstream and downstream segment IDs
        start = time.time()
        arcpy.AddField_management(streams, "NUOID", "TEXT")
        arcpy.AddField_management(streams, "NDOID", "LONG")
        usIDs.makeIDs(streams, strUIDField, "NUOID", "NDOID", fNodeField, tNodeField)
        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished getting stream us & ds IDs in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calcing up and down IDs on line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def getBarrUSDSIdsNear(streams, strIDField, barriers, usSegField, dsSegField, myWorkspace, fNodeField, tNodeField, barrUIDField):
    try:
        #For each barrier get the segment IDs of the upstream and downstream segments
        start = time.time()
        field_names = [f.name for f in arcpy.ListFields(barriers)]
        for fld in (dsSegField, usSegField):
            if fld not in field_names:
                arcpy.AddField_management(barriers, fld, "LONG")

        nearTable ="{}/barrierSegs".format(myWorkspace)
        #new IDs are the same as OBJECTID, so can just use the Near Table tool, which returns the nearest OBJECTID
        arcpy.GenerateNearTable_analysis(barriers, [streams], nearTable, "10 Meters", "NO_LOCATION", "NO_ANGLE", "ALL")

        #Populate a dict with the stream segments & their From_Node and To_Node
        strSegNodeDict = defaultdict(list)
        fields =(strIDField, fNodeField, tNodeField)
        with arcpy.da.SearchCursor(streams, fields) as rows:
            for row in rows:
                strSegNodeDict[row[0]]= [row[1], row[2]]
    
        #Populate a dict with the US & DS segment IDs for each barrier. Don't know which is which at this point
        barrierSegDict = defaultdict(list)
        fields =("IN_FID", "NEAR_FID")
        with arcpy.da.SearchCursor(nearTable, fields) as rows:
            for row in rows:
                barrierSegDict[row[0]].append(row[1])

        OIDs = arcpy.ListFields(barriers, None, "OID")
        OIDfield = OIDs[0].name

       
        fields = (barrUIDField, dsSegField, usSegField, OIDfield)
        with arcpy.da.UpdateCursor(barriers, fields) as rows:
            for row in rows:
                barrID = row[0]
                usdsList = []
                for i, seg in enumerate(barrierSegDict[row[3]]):
                    #segment IDs and Fnode and TNode
                    segID =barrierSegDict[row[3]][i]
                    fNode =strSegNodeDict[segID][0]
                    tNode =strSegNodeDict[segID][1]
                    usdsList.append([segID, fNode, tNode])

                #if first segement's from node == 2nd segement's to node, then
                #first segemnt is DS and second segment is US
                try:
                    if usdsList[0][1] == usdsList[1][2]:
                        row[1]=usdsList[0][0]
                        row[2]=usdsList[1][0]
                    else:
                        row[1]=usdsList[1][0]
                        row[2]=usdsList[0][0]
                    rows.updateRow(row)
                except:
                    pass



        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished barrier us & ds IDs in {} seconds".format(duration))

    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem getting US & DS barrier IDs on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def setBarrierStreamSegID(barriers, strUIDField, usStrID):
    try:
        #For each barrier get the stream segemnt ID it is assocaited with.  This should be the upstream one
        start = time.time()
        field_names = [f.name for f in arcpy.ListFields(barriers)]
        if strUIDField in field_names:
            pass

        else:
            arcpy.AddField_management(barriers, strUIDField, "LONG")

        fields =(strUIDField, usStrID)
        with arcpy.da.UpdateCursor(barriers, fields) as rows:
            for row in rows:
                row[0] = row[1]
                rows.updateRow(row)

        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished setting barrier stream segment IDs in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem setting stream barrier segment on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()

def export(instreams, outstreams, inbarriers, outbarriers):
    try:
        #Export the prepped data
        start = time.time()
        arcpy.CopyFeatures_management(instreams, outstreams)
        arcpy.CopyFeatures_management(inbarriers, outbarriers)

        end = time.time()
        duration = end-start
        arcpy.AddMessage("...finished exporting in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem exporting on prepStreams line {}. {}".format(tb.tb_lineno, e)
        arcpy.AddError(msg)
        sys.exit()


if __name__ == '__main__':
    main()

