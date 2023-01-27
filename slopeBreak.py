#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     27/12/2016
# Copyright:   (c) emartin 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import time
arcpy.env.overwriteOutput = True

def main():
    slopeBreaks("LINK", "C:\\Users\emartin\Google Drive\Congo\GISSync\AnalysisData.gdb\strline",  "FNODE_", "TNODE_", "GRAD_ABS")

def slopeBreaks(uniqueID, streams, FNodeField, TNodeField, percSlopeField):
    try:
        slopeStart = time.time()
        print("Calculating the number of slope breaks...")
        numSlopeBreaksField = "numSlopeBreaks"
        dsSlopeField = "DS_Slope"
        arcpy.AddField_management(streams, numSlopeBreaksField, "SHORT")
        arcpy.CalculateField_management(streams, numSlopeBreaksField, "0", "PYTHON")
        arcpy.AddField_management(streams, dsSlopeField, "DOUBLE")
        arcpy.CalculateField_management(streams, dsSlopeField, "0", "PYTHON")
        fields = (uniqueID, FNodeField, TNodeField, percSlopeField, numSlopeBreaksField, dsSlopeField)
        with arcpy.da.UpdateCursor(streams, fields) as uRows:
            for uRow in uRows:
                print(("Running slope breaks on ComID {}".format(uRow[0])))
                numSlopeBreaks = 0
                with arcpy.da.SearchCursor(streams, fields) as rows:
                    for row in rows:
                        #look upstream
                        if uRow[1] == row[2]:
                            if (abs(row[3] - uRow[3]) >=0.02):
                                numSlopeBreaks +=1
                    uRow[4] = numSlopeBreaks
                    uRows.updateRow(uRow)

        slopeEnd = time.time()
        slopeDuration = slopeEnd - slopeStart
        print(("Finsihed calculating slope breaks in {} seconds".format(slopeDuration)))


    except Exception as e:
        tb = sys.exc_info()[2]
        print(("Problem calculating number slope breaks. Failed on line {}".format(tb.tb_lineno)))
        print(e.message)
        sys.exit()

if __name__ == '__main__':
    main()