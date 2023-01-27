#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     04/05/2016
# Copyright:   (c) emartin 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

def main():
    fc = r"K:\PenobscotBlueprint\GIS\WebMap\MapServices\PenobscotBlueprint.gdb\Penobscot_Barriers"
    field = "HUC12_Name"
    results = unique_values(fc, field)
    print(results)


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


if __name__ == '__main__':
    main()
