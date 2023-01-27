#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     05/06/2015
# Copyright:   (c) emartin 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os

def main():

    dir= "K:\\EUSD\\ResilienceScoring\\webMap\\App\\ResilienceScore\\assets\\Finished\\"
    outputDir = "C:\\Users\\emartin\\Desktop\\test\\"
    for fn in os.listdir(dir):

        print (fn)
        newName = fn.upper()
        os.rename(dir+fn, outputDir+newName)




if __name__ == '__main__':
    main()