#-------------------------------------------------------------------------------
# Name:        resize JPEGs
# Purpose:
#
# Author:      emartin
#
# Created:     11/01/2018
# Copyright:   (c) emartin 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import PIL
from PIL import Image
import glob

inFolder = "K:\\DelawareRiver\\GIS\\Priority Dam Photos\\"
outFolder ="K:\\DelawareRiver\\GIS\\Priority Dam Photos\\resizedimages\\"
nameModifer = ""
extentions = ("PNG", "JPG") # will get saved as JPG


def main():
    for extention in extentions:
        images = glob.glob("{}*.{}".format(inFolder, extention))
        print(images)
        for image in images:
            resize(image)

def resize(image):
    nameWext =  image.split("\\")[-1].strip()
    name = nameWext.split(".")[0]
    ext =nameWext.split(".")[-1]
    print("Resizing {}".format(name))
    basewidth = 200
    img = Image.open(image)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    if ext == "JPG" or ext == "jpg":
        img.save(r'{}{}{}.JPG'.format(outFolder, name, nameModifer))
    if ext == "PNG" or ext == "png":
        imgRGB = img.convert('RGB')
        imgRGB.save(r'{}{}{}.JPG'.format(outFolder, name, nameModifer))

if __name__ == '__main__':
    main()
