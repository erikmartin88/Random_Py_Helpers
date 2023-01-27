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
import os
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import itertools
import base64
import requests
def main():
    saveDir = r"K:\Global\SRTM30\VoidFilled\Africa"
    africaEastings = list(range(0, 47))
    africaNorthings = list(range(10, 80))
    africa = makeURLList(africaEastings, africaNorthings)
    downloadURLs(saveDir, africa)

##    seAsiaEastings =range(54, 60)
##    seAsiaNorthings =range(6, 10)
##    seAsia =makeURLList(seAsiaEastings, seAsiaNorthings)
##    downloadURLs(saveDir, seAsia)





def downloadURLs(saveDir, urls):
    #get the current directory and change to the save directory
    curDir = os.getcwd()
    os.chdir (saveDir)

    for zipFile in urls:
        fileName = zipFile.split("/")[-1].strip()
        urlPath = zipFile.replace(fileName, "")

        fileList = os.listdir(saveDir)
        if fileName not in fileList:
            try:
                print(("Downloading " + fileName + " from " + urlPath))

                request = urllib.request.Request(zipFile)
                base64string = base64.b64encode('%s:%s' % ("erikmartin88", "ZU0tXWsbREZ1VNyoAYW9"))
                request.add_header("Authorization", "Basic %s" % base64string)

                u = urllib.request.urlopen(request)
                f = open('{}\\{}'.format(saveDir, fileName), 'wb+')

                meta = u.info()

                file_size = int(meta.getheaders("Content-Length")[0])
                print(("Downloading: %s Bytes: %s" % (fileName, file_size)))

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
##                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
##                    status = status + chr(8)*(len(status)+1)
##                    print status,
                f.close()
            except:
                print(("Download {} unavailable".format(zipFile)))
    os.chdir(curDir)


def makeURLList(eastRange, northRange):
    urlRoot ="https://e4ftl01.cr.usgs.gov/SRTM/SRTMGL1.003/2000.02.11/"
    urlList = []
    pairs = []

    for east in eastRange:
        for north in northRange:
            #next 2 lines pad with leading 0s
            e = str(east).zfill(2)
            n = str(north).zfill(3)
            pairs.append([e, n])
##            pairs.append([east, north])
    for pair in pairs:
        url ="{}N{}E{}.SRTMGL1.hgt.zip".format(urlRoot, pair[0], pair[1])
        urlList.append(url)
    print(urlList)
    return urlList

if __name__ == '__main__':
    main()
