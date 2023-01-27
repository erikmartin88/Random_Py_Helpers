#-------------------------------------------------------------------------------
# Name:        NestedWatersheds
# Purpose:      Develop nested watershed
#
# Author:      Erik Martin, emartin@tnc.org
#               adapted from "ESRI ARCINFO AML for Nested Watershed Development
#               (Fitzhugh, 2005)"
#               FitzHugh, Thomas W. 2005. GIS Tools for Freshwater Biodiversity
#               Conservation Planning. Transactions in GIS, Vol: 9, No: 2,
#               Pages: 247-263. The Nature Conservancy, Olympia, Washington
#               http://dx.doi.org/10.1111/j.1467-9671.2005.00215.x
#
# Created:     October 2013
#-------------------------------------------------------------------------------
"""
Conversions to develop watersheds at thresholds of 100, 1000, 10000, 100000,
1000000 and 10000000 square kilometers from data stored in geographic
(unprojected) coordinates.

3 arc-seconds grid resolution = 90m
1 dd = 3600 seconds * (90m/3s) = 108000 m
1m = 1.08 e-5 = 0.0000108 dd
3s grid cell = (90)^2 m2 = 8100 m2/grid cell = 123 grid cells/km2
"""
import arcpy
import sys
import time
from time import strftime
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

def main():
    start = time.time()
    arcpy.AddMessage("Starting nested watershed script at {}.".format(strftime("%H:%M:%S")))
    print("Starting nested watershed script at {}.".format(strftime("%H:%M:%S")))

    #Set analysis-wide variables
    workspace = arcpy.GetParameterAsText(0)
    flowacc =  arcpy.GetParameterAsText(1)
    flowdir =  arcpy.GetParameterAsText(2)

    lo1 = float(arcpy.GetParameterAsText(3))
    up1 = float(arcpy.GetParameterAsText(4))
    lo2 = float(arcpy.GetParameterAsText(5))
    up2 = float(arcpy.GetParameterAsText(6))
    lo3 = float(arcpy.GetParameterAsText(7))
    up3 = float(arcpy.GetParameterAsText(8))
    lo4 = float(arcpy.GetParameterAsText(9))
    up4 = float(arcpy.GetParameterAsText(10))
    lo5 = float(arcpy.GetParameterAsText(11))
    up5 = float(arcpy.GetParameterAsText(12))


    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    #Set threshold values for defining watersheds.  Each iteration takes the
    #size class, lower threshold, upper thresold, and flow accum & flow dir as inputs
    #Pass each of these to the generateSheds function
    sheds1 = generateSheds(1, lo1, up1, flowacc, flowdir)
    sheds2 = generateSheds(2, lo2, up2, flowacc, flowdir)
    sheds3 = generateSheds(3, lo3, up3, flowacc, flowdir)
    sheds4 = generateSheds(4, lo4, up4, flowacc, flowdir)
    sheds5 = generateSheds(5, lo5, up5, flowacc, flowdir)


    #Union results and calculate primary watershed code
    arcpy.AddMessage("Unioning watersheds at {}.".format(strftime("%H:%M:%S")))
    print("Unioning watersheds at {}.".format(strftime("%H:%M:%S")))
    arcpy.Union_analysis([sheds1, sheds2, sheds3, sheds4, sheds5], "basin_parts", "NO_FID")
    arcpy.AddField_management("basin_parts", "WSCODE", "LONG")
    fields = ("WS1CODE", "WS2CODE","WS3CODE","WS4CODE","WS5CODE","WSCODE")
    with arcpy.da.UpdateCursor("basin_parts", fields) as updateRows:
        for updateRow in updateRows:
            if updateRow[4] != 0:
                updateRow[5] = updateRow[4]
            if updateRow[3] != 0:
                updateRow[5] = updateRow[3]
            if updateRow[2] != 0:
                updateRow[5] = updateRow[2]
            if updateRow[1] != 0:
                updateRow[5] = updateRow[1]
            if updateRow[0] != 0:
                updateRow[5] = updateRow[0]
            updateRows.updateRow(updateRow)

    #Clean up fields in unioned table
    fieldList = arcpy.ListFields("basin_parts")
    for field in fieldList:
        if "gridcode" in field.name:
            arcpy.DeleteField_management("basin_parts", field.name)
        if "Id" in field.name:
            arcpy.DeleteField_management("basin_parts", field.name)

    end = time.time()
    seconds = end-start
    minutes = seconds/60
    arcpy.AddMessage("Finished generating nested watersheds.  Total run time = {} minutes".format(minutes))

def generateSheds(sizecl, lo, up, flowacc, flowdir):
    try:
        #Set environment variables
        arcpy.env.mask = flowacc
        arcpy.env.cellSize = flowacc
        arcpy.env.snapRaster = flowacc
        arcpy.env.extent = flowacc

        #Set variables which change on each iteration
        streamnetSave = "streamnet{}".format(sizecl)
        streamlink = "streamlink{}".format(sizecl)
        streamFC = "streamFC{}".format(sizecl)
        inStream = "inStream{}".format(sizecl)
        inStreamGrid = "inStreamGrid{}".format(sizecl)
        watershedsGr = "Watersheds_Size{}".format(sizecl)
        watershedsPoly = "WatershedsPoly_Size{}".format(sizecl)
        maskSave = "mask{}".format(sizecl)

        arcpy.AddMessage("Defining flow accumulation cutoff for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Defining flow accumulation cutoff for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        streamnet = Con(Raster(flowacc)> lo, 1)
        streamnet.save(streamnetSave)

        arcpy.AddMessage("Generating raster stream network for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Generating raster stream network for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        streaml = StreamLink(streamnet, flowdir)
        streaml.save(streamlink)

        mask = Con(Raster(flowacc) < up, 1)
        mask.save(maskSave)
        arcpy.env.mask = maskSave

        #Convert to vectors
        StreamToFeature(streaml, flowdir, streamFC)

        #This whole FREQUENCY piece is to eliminate adjacent segments of the same size, which would subdivide the watershed
        arcpy.AddMessage("Generating frequency tables & joining to streams for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Generating frequency tables & joining to streams for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        arcpy.Frequency_analysis(streamFC,"tnodefreq", "to_node")
        arcpy.Frequency_analysis(streamFC,"fnodefreq", "from_node")

        #joining frequency back to streamFC
        arcpy.AddField_management(streamFC, "freqt", "LONG")
        arcpy.AddField_management(streamFC, "freqf", "LONG")
        arcpy.MakeFeatureLayer_management(streamFC, "fc_lyr")
        arcpy.AddJoin_management("fc_lyr","to_node", "tnodefreq", "to_node")
        arcpy.CalculateField_management("fc_lyr", "freqt", "!tnodefreq.FREQUENCY!", "PYTHON")
        arcpy.RemoveJoin_management("fc_lyr")
        arcpy.AddJoin_management("fc_lyr","from_node", "fnodefreq", "from_node")
        arcpy.CalculateField_management("fc_lyr", "freqf", "!fnodefreq.FREQUENCY!", "PYTHON")
        arcpy.RemoveJoin_management("fc_lyr")
        expression = '"freqt" = 1 AND "freqf" = 1'
        arcpy.Select_analysis(streamFC, inStream, expression)

        #Convert input stream lines back to rasters to use as input to the watershed tool
        arcpy.AddMessage("Generating the input stream line grid for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Generating the input stream line grid for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        arcpy.PolylineToRaster_conversion(inStream, "grid_code", inStreamGrid)

        arcpy.AddMessage("Generating watersheds raster for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Generating watersheds raster for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        outWatersheds = Watershed(flowdir, inStreamGrid, "VALUE")
        outWatersheds.save(watershedsGr)

        arcpy.AddMessage("Generating watersheds polygons for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        print("Generating watersheds polygons for size {} at {}...".format(sizecl, strftime("%H:%M:%S")))
        arcpy.RasterToPolygon_conversion(watershedsGr, watershedsPoly, "NO_SIMPLIFY", "VALUE")

        arcpy.AddField_management(watershedsPoly, "WS{}CODE".format(sizecl), "LONG")
        expression = "({}*100000) + !gridcode!".format(sizecl)
        arcpy.CalculateField_management(watershedsPoly, "WS{}CODE".format(sizecl), expression, "PYTHON" )

        return watershedsPoly

    except Exception, e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Failed on line {}.".format( tb.tb_lineno))
        arcpy.AddMessage(e.message)
        print("Failed on line {}.".format( tb.tb_lineno))
        print(e.message)


if __name__ == '__main__':
    main()