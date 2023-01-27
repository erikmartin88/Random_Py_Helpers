#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     04/08/2015
# Copyright:   (c) emartin 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
def main():
    root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))
    print root
    direct = os.path.dirname(__file__)
    print direct
    sourceFeats = os.path.join(direct, "NAACC_PrioritizeSurveys.gdb/HUC12_Input")
    print sourceFeats

if __name__ == '__main__':
    main()
