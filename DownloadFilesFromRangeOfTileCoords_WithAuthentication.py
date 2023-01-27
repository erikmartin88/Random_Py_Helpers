#!/usr/bin/python
from http.cookiejar import CookieJar
from urllib.parse import urlencode
import os
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import itertools
import mySecrets

def main():
    saveDir = r"K:\Global\SRTM30\VoidFilled\Africa"
    africaEastings = list(range(10, 18))
    africaNorthings = list(range(10, 38))
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

    #see https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
    username = mySecrets.earthDataUser
    password = mySecrets.earthDataPass
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
    cookie_jar = CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPBasicAuthHandler(password_manager),
        urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)

    for zipFile in urls:
        fileName = zipFile.split("/")[-1].strip()
        urlPath = zipFile.replace(fileName, "")

        fileList = os.listdir(saveDir)
        if fileName not in fileList:
            try:
                print(("Downloading " + fileName + " from " + urlPath))
                u = urllib.request.Request(zipFile)
                response = urllib.request.urlopen(u)
                f = open('{}\\{}'.format(saveDir, fileName), 'wb+')
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = response.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                f.close()
            except Exception as e:
                print(("Download {} unavailable".format(zipFile)))
                tb = sys.exc_info()[2]
                print((str(e)))


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
        url ="{}N{}W{}.SRTMGL1.hgt.zip".format(urlRoot, pair[0], pair[1])
        urlList.append(url)
##    print(urlList)
    return urlList

if __name__ == '__main__':
    main()
