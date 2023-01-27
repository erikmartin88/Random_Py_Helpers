#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     28/05/2019
# Copyright:   (c) emartin 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys, glob, arcpy
workspace = "K:\\RegionalDatasets\\StreamCat\\"
gdb = os.path.join(workspace, "StreamCAT_Region0102.gdb")
arcpy.env.workspace = gdb
def main():

    CSVs = glob.glob("{}\\*.csv".format(workspace))
    roots = []
    for csv in CSVs:
        root = csv.replace("_Region01.csv", "").replace("_Region02.csv", "").replace(workspace, "")
        roots.append(root)
    roots = list(set(roots))

    existingTables = arcpy.ListTables()
    for root in roots:
        if root not in existingTables:
            tables = glob.glob("{}\\{}_Region*.csv".format(workspace, root))
            print(("merging {}".format(tables)))
            arcpy.Merge_management(tables, root)
        else:
            print(("{} already in GDB".format(root)))

if __name__ == '__main__':
    main()
