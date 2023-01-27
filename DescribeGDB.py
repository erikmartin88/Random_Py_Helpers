#-------------------------------------------------------------------------------
# Name:        Describe geodatabase
#
# Purpose:     Writes simple metadata to text file for all feature classes and
#              rasters in a geodatabase using arcpy.Describe.  Also takes the
#              "Description" field from the metadata.
#
# Author:      Erik Martin, The Nature Conservancy, emartin@tnc.org
#
# Created:     09/09/2013
#-------------------------------------------------------------------------------


def main():
    import arcpy
    import sys
    from xml.etree.ElementTree import ElementTree
    from xml.etree.ElementTree import Element, SubElement

    arcpy.env.overwriteOutput = True
    try:
        #-----------------------User variables----------------------------------
        #geodatabase within which all FCs and rasters will be described
        gdb ="K:\\Ogooue\\GIS_Data\\OgooueFWBlueprint.gdb\\"

        #tamporary location where FGDC xmls will be written
        xmlFilePath = "K:\\Ogooue\\GIS_Data\\temp\\"

        # empty text files that will be written to.  These can then be opened in
        # Excel as "pipe" (|) delimted text files.  Set up to write raster and
        # vector data to separate files, but setting these variabels to the
        # same text file would write them all together.
        vectorDescFile = "K:\\Ogooue\\GIS_Data\\temp\\vector.txt"
        rasterDescFile = "K:\\Ogooue\\GIS_Data\\temp\\raster.txt"

        #location of the ArcGIS tranlator.  Used to export metadata to FGDC xml
        translatorpath = r"C:\Program Files (x86)\ArcGIS\Desktop10.1\Metadata\Translator\ARCGIS2FGDC.xml"

        #-----------------------------------------------------------------------

        desc = arcpy.Describe(gdb)

        # Print GDB path & name
        print ("Geodatabase: " + desc.catalogPath)

        for child in desc.children:
            if child.dataType == "FeatureClass":
                fields = []
                fc = child.name
                fcPath = gdb + "\\" + fc
                xmlfile = "{}\{}.xml".format(xmlFilePath, fc)
                arcpy.ExportMetadata_conversion(fcPath, translatorpath, xmlfile)
                tree = ElementTree() # make an ElementTree object
                tree.parse(xmlfile) # read the xml into the ElementTree
                spot = tree.find("idinfo/descript/abstract") # find whatever tag you want

                #get list of field names
                for field in child.fields:
                    fields.append(field.name)

                #final describe string
                print("Not in Feature Dataset" + " | " + fc + " | " + spot.text + " | " + str(fields) + "\r\n")
                stringtowrite = ("Not in Feature Dataset" + " | " + fc + " | " + spot.text + " | " + str(fields) + "\r\n")
                uStringtowrite = stringtowrite.encode('utf-8')

                f = open(vectorDescFile, "a")
                f.write(uStringtowrite)
                f.close

            if child.dataType == "FeatureDataset":
                for secondChild in child.children:
                    fields = []
                    fd = child.name
                    fc = secondChild.name
                    fcPath = gdb + fd + "\\" + fc
                    xmlfile = "{}\{}.xml".format(xmlFilePath, fc)
                    arcpy.ExportMetadata_conversion(fcPath, translatorpath, xmlfile)
                    tree = ElementTree() # make an ElementTree object
                    tree.parse(xmlfile) # read the xml into the ElementTree
                    spot = tree.find("idinfo/descript/abstract") # find whatever tag you want

                    #get list of field names
                    for field in secondChild.fields:
                        fields.append(field.name)

                    #final describe string
                    print(fd + " | " + fc + " | " + spot.text + " | " + str(fields) + "\r\n")
                    stringtowrite = (fd + " | " + fc + " | " + spot.text + " | " + str(fields) + "\r\n")
                    uStringtowrite = stringtowrite.encode('utf-8')

                    f = open(vectorDescFile, "a")
                    f.write(uStringtowrite)
                    f.close

            if child.dataType == "RasterDataset":
                raster = child.name
                rasterPath = gdb + "\\" + raster
                xmlfile = r"K:\Ogooue\GIS_Data\temp\{}.xml".format(raster)
                arcpy.ExportMetadata_conversion(rasterPath, translatorpath, xmlfile)
                tree = ElementTree() # make an ElementTree object
                tree.parse(xmlfile) # read the xml into the ElementTree
                spot = tree.find("idinfo/descript/abstract") # find whatever tag you want

                #get raster band properties
                band = arcpy.Describe("{}/Band_1".format(rasterPath))
                if band.isInteger == True:
                    integer = "Integer"
                else:
                    integer = "Float"
                cellSize =band.meanCellWidth

                #final describe string
                print(raster + " | " + str(cellSize) + " | " + integer + " | "+ spot.text + "\r\n")
                stringtowrite = (raster + " | " + str(cellSize) + " | " + integer + " | "+ spot.text + "\r\n")
                uStringtowrite = stringtowrite.encode('utf-8')

                f = open(rasterDescFile, "a")
                f.write(uStringtowrite)
                f.close

    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem describing data...")
        print ("Line {}".format(tb.tb_lineno))
        print (e.message)
        sys.exit()

if __name__ == '__main__':
    main()
