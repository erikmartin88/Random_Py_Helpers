#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     12/09/2013
# Copyright:   (c) emartin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import os
    import sys
    import urllib
    import urllib2
    import itertools
    makeURLList()

    saveDir = "K:\\Chesapeake_v3\\GIS\\SourceData\\LandCover\\ChesHighRes"

    #get the current directory and change to the save directory
    curDir = os.getcwd()
    os.chdir (saveDir)

    zipList = []

    for zipFile in zipList:
        fileName = zipFile.split("/")[-1].strip()
        urlPath = zipFile.replace(fileName, "")

        fileList = os.listdir(saveDir)
        if fileName not in fileList:
            print("Downloading " + fileName + " from " + urlPath)
            u = urllib2.urlopen(zipFile)
            f = open('{}\\{}'.format(saveDir, fileName), 'wb+')

            meta = u.info()

            file_size = int(meta.getheaders("Content-Length")[0])
            print("Downloading: %s Bytes: %s" % (fileName, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print(status)

            f.close()

    os.chdir(curDir)

def makeURLList(eastRange, northRange):
    urlRoot ="http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff"
    urlList = []
    pairs = []
    eastRange = range(33, 47)
    northRange = range(5, 19)
    for east in eastRange:
        for north in northRange:
            pairs.append([east, north])
    for pair in pairs:
        url ="{}/srtm_{}_{}.zip".format(urlRoot, pair[0], pair[1])
        urlList.append(url)
    print(urlList)
    return urlList

if __name__ == '__main__':
    main()
