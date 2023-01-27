#-------------------/-----------------------------------------------------------
# Name:        Export Map book by fields
# Purpose:      Exports a series of PDFs using a series of fields to display
#               different species
# Author:      Erik Martin, The Nature Conservancy, emartin@tnc.org
#
# Created:     Sept 12, 2013
#-------------------------------------------------------------------------------
import arcpy
import sys

def main():
    try:
        saveDir = r"C:\Users\emartin\Desktop\SpeciesMaps"
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        speciesLayer = arcpy.mapping.ListLayers(mxd, "Species")[0]

#--------------------Get Common Name from lookup table
        lookupDict = {}
        lookupTab = r"K:\CT_River_Basin\GIS_Data\General.gdb\tblSpecies"
        fields = ("Species_code", "Common_name")
        with arcpy.da.SearchCursor(lookupTab, fields) as rows:
            for row in rows:
                sppCode = row[0]
                lookupDict[sppCode] = row[1]

#---------------Export maps based on fields  each field is a different spp
        fields = arcpy.ListFields(speciesLayer, "MEAN*")
        for field in fields:
            fieldName = field.name
            rootName = fieldName.replace("MEAN_", "")
            commonName = lookupDict[rootName]
            speciesLayer.name = commonName
            speciesLayer.symbology.valueField = fieldName
            speciesLayer.symbology.numClasses = 6

            #-----This section formats the labels to have 2 decimal places.  Not very Pythonic
            breaks = speciesLayer.symbology.classBreakValues
            roundedBreaks = [round(elem, 2) for elem in breaks]
            roundedBreaks.pop(0)
            breakLength = len(roundedBreaks)
            if breakLength ==2:
                labels = ["0", "{}- {}".format(roundedBreaks[0], roundedBreaks[1])]
            if breakLength ==3:
                labels = ["0", "{}- {}".format(roundedBreaks[0], roundedBreaks[1]), "{}- {}".format(roundedBreaks[1], roundedBreaks[2])]
            if breakLength ==4:
                labels = ["0", "{}- {}".format(roundedBreaks[0], roundedBreaks[1]), "{}- {}".format(roundedBreaks[1], roundedBreaks[2]), "{}- {}".format(roundedBreaks[2], roundedBreaks[3])]
            if breakLength ==5:
                labels = ["0", "{}- {}".format(roundedBreaks[0], roundedBreaks[1]), "{}- {}".format(roundedBreaks[1], roundedBreaks[2]), "{}- {}".format(roundedBreaks[2], roundedBreaks[3]), "{}- {}".format(roundedBreaks[3], roundedBreaks[4])]
            if breakLength ==6:
                labels = ["0", "{}- {}".format(roundedBreaks[0], roundedBreaks[1]), "{}- {}".format(roundedBreaks[1], roundedBreaks[2]), "{}- {}".format(roundedBreaks[2], roundedBreaks[3]), "{}- {}".format(roundedBreaks[3], roundedBreaks[4]), "{}- {}".format(roundedBreaks[4], roundedBreaks[5])]
            speciesLayer.symbology.classBreakLabels = labels

#--------------Export to PDF
            arcpy.RefreshActiveView()
            arcpy.mapping.ExportToPDF(mxd, r"{}\{}.pdf".format(saveDir, fieldName))
            speciesLayer.name = "Species"

    except Exception, e:
        tb = sys.exc_info()[2]
        print ("Problem with the mapping module...")
        print "Line {}".format(tb.tb_lineno)
        print e.message
        sys.exit()
if __name__ == '__main__':
    main()
