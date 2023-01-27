#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        makeNodes
# Purpose:		Make FNode and TNodes, then NDOID and NUOIDs for use in HydroRout
#
# Author:      emartin@tnc.org
#-------------------------------------------------------------------------------

import arcpy, sys, os, pandas as pd
from collections import defaultdict

def newNodes(input_lines,fNodeField, tNodeField):
    try:
        #Create new From and To nodes based on digitized line direction
        start = time.time()
        arcpy.AddField_management(input_lines, fNodeField, "LONG")
        arcpy.AddField_management(input_lines, tNodeField, "LONG")

        xy_dict = {}
        fields =('SHAPE@', fNodeField, tNodeField)
        with arcpy.da.UpdateCursor(input_lines, fields) as rows:
            for row in rows:
                # From Node
                from_key = '{},{}'.format(round(row[0].firstPoint.X, 7), round(row[0].firstPoint.Y, 7))
                #if xy_dict.has_key(from_key):
                if from_key in xy_dict:
                    row[1] = xy_dict[from_key]
                else:
                    row[1] = len(xy_dict) + 1
                    xy_dict[from_key] = len(xy_dict) + 1

                # To Node
                to_key = '{},{}'.format(round(row[0].lastPoint.X, 7), round(row[0].lastPoint.Y, 7))
                #if xy_dict.has_key(to_key):
                if to_key in xy_dict:
                    row[2] = xy_dict[to_key]
                else:
                    row[2] = len(xy_dict) + 1
                    xy_dict[to_key] = len(xy_dict) + 1
                rows.updateRow(row)
        end = time.time()
        duration = end-start
        print("...finished making new nodes in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calcing nodes on prepStreams line {}. {}".format(tb.tb_lineno, e)
        print(msg)
        sys.exit()

def upDownIDs(streams, strUIDField, fNodeField, tNodeField):
    try:
        #for each segemnt populate fields with the upstream and downstream segment IDs
        start = time.time()
        arcpy.AddField_management(streams, "NUOID", "TEXT")
        arcpy.AddField_management(streams, "NDOID", "LONG")
        makeIDs(streams, strUIDField, "NUOID", "NDOID", fNodeField, tNodeField)
        end = time.time()
        duration = end-start
        print("...finished getting stream us & ds IDs in {} seconds".format(duration))
    except Exception as e:
        tb = sys.exc_info()[2]
        msg ="Problem calcing up and down IDs on line {}. {}".format(tb.tb_lineno, e)
        print(msg)
        sys.exit()
		

def makeIDs(streamFC, segIDField, usSegIDField, dsSegIDField, fnodeField, tnodeField):
    try:
        fields = (segIDField, fnodeField, tnodeField)
        arr = arcpy.da.TableToNumPyArray(streamFC, fields)
        df = pd.DataFrame(arr)
        df2 = df
        #Join the dataframes -- analogous to a regular database join
        joinedDF = pd.merge(df, df2, left_on=fnodeField, right_on=tnodeField)
        usIDsDict = defaultdict(list)
        for index, row in joinedDF.iterrows():
            usIDsDict[int(row['{}_x'.format(segIDField)])].append(int(row['{}_y'.format(segIDField)]))

        joinedDF = pd.merge(df, df2, left_on=tnodeField, right_on=fnodeField)
        dsIDsDict = {}
        for index, row in joinedDF.iterrows():
            dsIDsDict[int(row['{}_x'.format(segIDField)])] = int(row['{}_y'.format(segIDField)])

        fields = (segIDField, usSegIDField, dsSegIDField)
        with arcpy.da.UpdateCursor(streamFC, fields) as rows:
            for row in rows:
                row[1] = str(usIDsDict[row[0]]).replace(",", "_").replace("[", "").replace("]", "").replace(" ", "")
                try:
                    row[2] = dsIDsDict[row[0]]
                except:
                    row[2] = None
                rows.updateRow(row)

    except Exception as e:
        tb = sys.exc_info()[2]
        print(" Failed on line {}. ".format(tb.tb_lineno) + str(e.message))
        sys.exit()