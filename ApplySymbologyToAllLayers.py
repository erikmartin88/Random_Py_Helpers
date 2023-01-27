#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     25/10/2019
# Copyright:   (c) emartin 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

mxd = arcpy.mapping.MapDocument(r"K:\NRCS_CIG\GIS\WebMap\Aquatic_Prioritization\Aquatic_Prioritization.mxd")
workspace = r"K:\NRCS_CIG\GIS\WebMap\Aquatic_Prioritization\Aquatic_Prioritization.gdb\mapService"

arcpy.env.workspace = workspace

def main():
##    addSymbology()
    applySymbology()

def addSymbology():
    fcs = arcpy.ListFeatureClasses("Prioritized*")
    for fc in fcs:
        print("Adding symbology field to {}".format(fc))
        arcpy.AddField_management(fc, "Symbology3Class", "Text")
        fields = ("Type", "Tier", "Symbology3Class")
        with arcpy.da.UpdateCursor(fc, fields) as rows:
            for row in rows:
                if row[0] == "Crossing" and row[1] <=7 and row[1] is not None:
                    row[2] = "1 Crossing - Higher Priority"
                if row[0] == "Crossing" and row[1] >7 and row[1] <=14 and row[1] is not None:
                    row[2] = "2 Crossing - Medium Priority"
                if row[0] == "Crossing" and row[1] >14 and row[1] is not None:
                    row[2] = "3 Crossing - Lower Priority"
                if row[0] == "Crossing" and row[1] is  None:
                    row[2] = "4 Crossing - Not Prioritized"

                if row[0] == "Dam" and row[1] <=7 and row[1] is not None:
                    row[2] = "5 Dam - Higher Priority"
                if row[0] == "Dam" and row[1] >7 and row[1] <=14 and row[1] is not None:
                    row[2] = "6 Dam - Medium Priority"
                if row[0] == "Dam" and row[1] >14 and row[1] is not None:
                    row[2] = "7 Dam - Lower Priority"
                if row[0] == "Dam" and row[1] is  None:
                    row[2] = "8 Dam - Not Prioritized"
                rows.updateRow(row)

def applySymbology():
    lyrFile = r"K:\NRCS_CIG\GIS\WebMap\Aquatic_Prioritization\Aquatic_Prioritization_Scripts\ThreeTiers.lyr"
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        print("Symbolizing {}".format(lyr.name))
        arcpy.ApplySymbologyFromLayer_management(lyr, lyrFile)
    mxd.save()

if __name__ == '__main__':
    main()
