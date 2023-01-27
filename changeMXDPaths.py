#-------------------------------------------------------------------------------
# Name:        fix paths for all MXDs in a folder and nested subfolders.
# Purpose:      Can be used to universally chnage all "K:" to "L:"
#
# Author:      emartin
#
# Created:     11/09/2017
# Copyright:   (c) emartin 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os
import datetime

def main():
    try:
        rootdir = 'L:\\'
        subdirs = []
        mxds = []
        for subdir, dirs, files in os.walk(rootdir):
            subdirs.append(subdir[1:])
            for file in files:
                if file.endswith('.mxd'):
                    filepath =os.path.join(subdir, file)
                    mxds.append(filepath)
##        print subdirs
##        print mxds

        for mxd in mxds:
            print("Running {}".format(mxd))
            try:
                myMXD =arcpy.mapping.MapDocument(mxd)
                elements = []

                for lyr in arcpy.mapping.ListLayers(myMXD):
                    elements.append(lyr)
                for tab in arcpy.mapping.ListTableViews(myMXD):
                    elements.append(tab)
                for elem in elements:
                    try:
                        baseSpace =elem.workspacePath[1:]
                        if baseSpace in subdirs:
                            newSpace = elem.workspacePath.replace("K:", "L:")
                            print (elem.workspacePath + "==" + elem.name + " is now " + newSpace + "---" + elem.name)
                            try:
                                elem.findAndReplaceWorkspacePath(elem.workspacePath, newSpace)
                            except Exception as e:
                                print(str(e))
                    except:
                        print("Couldn't get path for layer {}".format(elem.name))


                myMXD.save()
            except:
                print("Problem opening {}.  Not updated.".format(mxd))


    except Exception as e:
        tb = sys.exc_info()[2]
        print ("Problem changing file paths on line {} at {}".format(tb.tb_lineno, stamp()))
        print(str(e))

def stamp():
    myNow = str(datetime.datetime.now()).split('.')[0]
    return myNow

if __name__ == '__main__':
    main()
