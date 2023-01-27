#-------------------------------------------------------------------------------
# Name:        flagSmallValueofDuplicatePair
# Purpose:     Identifies a smaller value of a duplicate pair.  Designed for
#
# Author:      emartin
#
# Created:     23/01/2015
# Copyright:   (c) emartin 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True
def main():
    table = r"C:\Users\emartin\Documents\ArcGIS\Default.gdb\NE_HUC12s_Intersect_Statisti_dupes"
    #for duplicate paris (where Index=1), marks "keep" as 0 for the smaller of "MAX_Shape_Area"
    fields = ["HUC12", "Index", "MAX_Shape_Area", "Keep"]

    with arcpy.da.SearchCursor(table, fields) as rows:
        for row in rows:
            if row[1] == 1:
                print(("Running HUC {}".format(row[0])))
                expression = '"HUC12" = \'{}\''.format(row[0])
                arcpy.MakeTableView_management(table, "tableView", expression)
                with arcpy.da.SearchCursor("tableView", fields) as sRows:
                    valList = []
                    for sRow in sRows:
                        valList.append(sRow[2])
                    maxVal = (max(valList))-1
                    print(maxVal)
                arcpy.MakeTableView_management(table, "tableView2", expression)

                with arcpy.da.UpdateCursor ("tableView2", fields) as uRows:
                    for uRow in uRows:
                        if (uRow[2] < maxVal):
                            print(("{} < {}".format(uRow[2], maxVal)))
                            uRow[3] = 0
                            uRows.updateRow(uRow)
                        elif (uRow[2] > maxVal):
                            print(("{} > {}".format(row[2], maxVal)))
                            uRow[3] = 1
                            uRows.updateRow(uRow)
                del valList


if __name__ == '__main__':
    main()
