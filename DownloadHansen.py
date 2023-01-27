
import os, sys
import urllib

def main():
    lossyear = "K:/Global/Hansen/lossyear.txt"
    treecov ="K:/Global/Hansen/treecover2000.txt"

    lossyearObj = open(lossyear, 'r')
    lossyearURLS = lossyearObj.readlines()
    download(lossyearURLS)

    treecovObj = open(treecov, 'r')
    treecovURLS = treecovObj.readlines()
    download(treecovURLS)



def download(linestrings):
    for linestring in linestrings:
        url = linestring
        url_foldername = url[81:-4]
##        path = "K:/Global/Hansen/" + url_foldername
##        os.makedirs(path)
        path = "K:/Global/Hansen/" + url_foldername
        print "downloading url {}".format(url)
        fileName = path + url_foldername + ".tif"
        urllib.urlretrieve(url, fileName)


if __name__ == '__main__':
    main()