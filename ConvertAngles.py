#-------------------------------------------------------------------------------
# Name:        Convert Angles
# Purpose:      Convert ArcGIS Near tool output "NEAR_ANGLE" to Azimuth angles
#
# Author:      emartin
#
# Created:     29/09/2016
# Copyright:   (c) emartin 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
def main():

    #DOUBLE CHECK BEFORE USING -- THIS IS COPIED FROM AN OLD SCRIPT AND I THINK IS WRONG
    nearOutput = r"K:\HbD\GIS\Apes\Apes.gdb\barriers"
    convertAngles(nearOutput)


def convertAngles(fc):
    try:
        print("starting conversion")
        arcpy.AddField_management(fc, "NEAR_ANGLE_AZIMUTH", "DOUBLE")
        with arcpy.da.UpdateCursor(fc, ["NEAR_ANGLE", "NEAR_ANGLE_AZIMUTH", "NEAR_DIST"]) as rows:
            for row in rows:
                angle = row[0]
                if angle <= 180 and angle > 90:
                    azAng = (360.0 - (angle - 90))
                else:
                    azAng =(abs(angle - 90))
                if row[2] !=0:
                    row[1] = azAng
                else:
                    row[1] = 0
                rows.updateRow(row)


    except Exception as e:
        tb = sys.exc_info()[2]
        print(("There was a problem converting angles on line {} ".format(tb.tb_lineno)))
        print((str(e)))

if __name__ == '__main__':
    main()
