#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     03/06/2014
# Copyright:   (c) emartin 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
workspace =arcpy.GetParameterAsText(0)
inputPolys = arcpy.GetParameterAsText(1)
output =arcpy.GetParameterAsText(2)
algorithm =arcpy.GetParameterAsText(3)
tolerance =arcpy.GetParameterAsText(4)
minArea =arcpy.GetParameterAsText(5)
topoErrors =arcpy.GetParameterAsText(6)
keepPoints =arcpy.GetParameterAsText(7)

arcpy.env.workspace = workspace
def main():
    try:
        result = arcpy.SimplifyPolygon_cartography(inputPolys,output,algorithm,tolerance,minArea,topoErrors, keepPoints)
        arcpy.SetParameterAsText(8, result)

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage("Problem simplifying polygon...")
        arcpy.AddMessage ("Line {}".format(tb.tb_lineno))
        arcpy.AddMessage( e.message)
        sys.exit()
if __name__ == '__main__':
    main()
