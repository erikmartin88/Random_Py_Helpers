#-------------------------------------------------------------------------------
# Name:        find the barrier ID with the max hieght from a group with a common ID
# Purpose:
#
# Author:      emartin@tnc.org
#-------------------------------------------------------------------------------
import arcpy, sys, os
arcpy.env.overwriteOutputs = True

fc = r"K:\Ogooue\GIS_Data\DFP\LowerImpactDams\LowerImpactDams.gdb\all_projects_by_site"
uniqueIDField = "Project_Name"
valueField = "Installed_power__MW_"
groupIDField = "sName"
outTablePath = r"K:\Ogooue\GIS_Data\DFP\LowerImpactDams\LowerImpactDams.gdb"
outTableName = "largestDamBySite"

def main():
    #create the outputTable
    outTable = os.path.join(outTablePath, outTableName)
    if arcpy.Exists(outTable) == True:
        arcpy.Delete_management(outTable)
    arcpy.CreateTable_management(outTablePath, outTableName)
    arcpy.AddField_management(outTable, groupIDField, "TEXT") #change field type if text ID
    arcpy.AddField_management(outTable, uniqueIDField, "TEXT") #change field type if text ID


    #get a list of the group IDs
    groupIDs = []
    fields = (groupIDField)
    with arcpy.da.SearchCursor(fc, fields) as rows:
        for row in rows:
            groupIDs.append(row[0])
    groupIDs = set(groupIDs)

    #loop through each group and find the highest barrier
    #create an empty dictionary to hold the results
    results = {}
    for group in groupIDs:
        fields = (uniqueIDField, valueField, groupIDField)
        heights = []
        print(group)
        print(groupIDField)
        exp = "{} = '{}'".format(groupIDField, group) # if text groupID , need to wrap value in single quotes. where_clause = "{} = '{}'"
        with arcpy.da.SearchCursor(fc, fields, where_clause=exp) as rows:
            for row in rows:
                print((row[1]))
                heights.append(row[1])
        print(heights)
        maxHeight = max(heights)
        with arcpy.da.SearchCursor(fc, fields, where_clause=exp) as rows:
            for row in rows:
                if row[1] == maxHeight:
                    maxHeightID = row[0] #this will overwrite previous ones, so it will be the last dam with the max height
        results[group] = maxHeightID

    print(results)
    fields = (uniqueIDField, groupIDField)
    cursor =  arcpy.da.InsertCursor(outTable, fields)
    for group in results:
        row = [results[group], group]
        cursor.insertRow(row)



if __name__ == '__main__':
    main()