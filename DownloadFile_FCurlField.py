#-------------------------------------------------------------------------------
# Name:        download files from http using urls in a feature class field
# Purpose:
#
# Author:      emartin
#
# Created:     22/08/2013
# Copyright:   (c) emartin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib
import arcpy
import os

def main():
    fc = r"K:\ChesapeakeMarine\GIS\LiDAR\VAElevenCo\toDownload.shp"
    urlField = "DEM_URL"
    saveDir = r"K:\ChesapeakeMarine\GIS\LiDAR\VAElevenCo"

    #get the current directory and change to the save directory
    curDir = os.getcwd()
    os.chdir (saveDir)

    with arcpy.da.SearchCursor(fc, urlField) as rows:
        for row in rows:
            #main URL path from FC field
            urlPath = row[0]
            fileName = urlPath.split("/")[-1].strip()

            #aux & xml paths built from urlPath
            auxPath = urlPath + ".aux.xml"
            xmlPath = urlPath + ".xml"

            #aux & xml file names built from urlName
            auxName = fileName + ".aux.xml"
            xmlName = fileName + ".xml"

            #get list of existing files and don't download if already have it
            fileList = os.listdir(saveDir)
            if fileName not in fileList:
                print("Downloading " + fileName + " from " + urlPath)
                urllib.urlretrieve (urlPath, fileName)
            if auxName not in fileList:
                urllib.urlretrieve (auxPath, auxName)
            if xmlName not in fileList:
                urllib.urlretrieve (xmlPath, xmlName)

    #switch back to original directory
    os.chdir(curDir)



##DeleteBelow
    fc = r"K:\ChesapeakeMarine\GIS\LiDAR\VACoNorth\toDownload.shp"
    urlField = "DEM_URL"
    saveDir = r"K:\ChesapeakeMarine\GIS\LiDAR\VACoNorth"

    #get the current directory and change to the save directory
    curDir = os.getcwd()
    os.chdir (saveDir)

    with arcpy.da.SearchCursor(fc, urlField) as rows:
        for row in rows:
            #main URL path from FC field
            urlPath = row[0]
            fileName = urlPath.split("/")[-1].strip()

            #aux & xml paths built from urlPath
            auxPath = urlPath + ".aux.xml"
            xmlPath = urlPath + ".xml"

            #aux & xml file names built from urlName
            auxName = fileName + ".aux.xml"
            xmlName = fileName + ".xml"

            #get list of existing files and don't download if already have it
            fileList = os.listdir(saveDir)
            if fileName not in fileList:
                print("Downloading " + fileName + " from " + urlPath)
                urllib.urlretrieve (urlPath, fileName)
            if auxName not in fileList:
                urllib.urlretrieve (auxPath, auxName)
            if xmlName not in fileList:
                urllib.urlretrieve (xmlPath, xmlName)

    #switch back to original directory
    os.chdir(curDir)
if __name__ == '__main__':
    main()
