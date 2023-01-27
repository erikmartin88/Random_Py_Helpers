#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     21/06/2016
# Copyright:   (c) emartin 2016import glob, os



# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, glob


def main():

    rename(r'C:\Users\emartin\Desktop\PicturesEdit4WebTool', r'*.jpg', r'%s')

def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title.upper() + ".JPG"))

if __name__ == '__main__':
    main()
